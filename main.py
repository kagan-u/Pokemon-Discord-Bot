import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents, proxy="http://127.0.0.1:8080")


@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')


@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        chance = random.randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Wizard(author)
        elif chance == 3:
            pokemon = Fighter(author)
        await pokemon.fetch_data()
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémon görüntüsü yüklenemedi.")
    else:
        await ctx.send("Zaten bir Pokémon oluşturmuşsun.")


@bot.command()
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Önce `!go` ile bir Pokémon oluşturun!")


@bot.command()
async def list(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        await ctx.send(
            f"**{pokemon.name.upper()}** | HP: {pokemon.hp} | Güç: {pokemon.power} | Seviye: {pokemon.level}"
        )
    else:
        await ctx.send("Henüz bir Pokémonunuz yok! `!go` ile başlayın.")


@bot.command()
async def evolve(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        await ctx.send("Önce `!go` ile bir Pokémon oluşturun!")
        return

    pokemon = Pokemon.pokemons[author]
    cost = pokemon.level * 30

    if pokemon.xp < cost:
        await ctx.send(f"Evolv etmek için yeterli XP yok! Gereken: {cost} XP (Mevcut: {pokemon.xp} XP)")
        return

    pokemon.xp -= cost
    pokemon.level += 1
    pokemon.power += random.randint(5, 15)
    pokemon.hp += random.randint(20, 50)
    await ctx.send(
        f"**{pokemon.name.upper()}** evolved! Yeni seviye: {pokemon.level}\n"
        f"Yeni HP: {pokemon.hp} | Yeni Güç: {pokemon.power}"
    )


@bot.command()
async def train(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        await ctx.send("Önce `!go` ile bir Pokémon oluşturun!")
        return

    pokemon = Pokemon.pokemons[author]

    events = [
        ("yabani bir Pokémon ile çalıştı", 15, 25),
        ("ağaçlara saldırdı", 10, 20),
        ("nehirde yüzdü", 12, 22),
        ("dağa tırmandı", 18, 30),
        ("kaya parçaladı", 14, 24),
        ("hız koşusu yaptı", 11, 19),
        ("gölge boksü yaptı", 16, 26),
    ]

    event = random.choice(events)
    xp_gain = random.randint(event[1], event[2])

    leveled = pokemon.gain_xp(xp_gain)

    msg = f"**{pokemon.name.upper()}** {event[0]}!\n+{xp_gain} XP"
    if leveled:
        msg += f"\n**Seviye atladı!** Yeni seviye: {pokemon.level}\nHP: {pokemon.hp} | Güç: {pokemon.power}"

    await ctx.send(msg)


@bot.command()
async def hunt(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        await ctx.send("Önce `!go` ile bir Pokémon oluşturun!")
        return

    pokemon = Pokemon.pokemons[author]
    result = random.random()

    if result < 0.3:
        wild_power = random.randint(10, pokemon.power + 20)
        damage = wild_power // 2
        pokemon.hp -= damage
        xp_gain = random.randint(20, 40)

        if pokemon.hp <= 0:
            pokemon.hp = 1
            await ctx.send(
                f"**{pokemon.name.upper()}** vahşi bir Pokémon ile savaştı!\n"
                f"Kötü yaralandı! HP: {pokemon.hp}\n"
                f"+{xp_gain} XP"
            )
        else:
            leveled = pokemon.gain_xp(xp_gain)
            msg = (
                f"**{pokemon.name.upper()}** vahşi bir Pokémon ile savaştı!\n"
                f"Hasar aldı: -{damage} HP | Kalan HP: {pokemon.hp}\n"
                f"+{xp_gain} XP"
            )
            if leveled:
                msg += f"\n**Seviye atladı!** Yeni seviye: {pokemon.level}"
            await ctx.send(msg)

    elif result < 0.7:
        xp_gain = random.randint(25, 50)
        leveled = pokemon.gain_xp(xp_gain)
        msg = f"**{pokemon.name.upper()}** vahşi bir Pokémon yakaladı!\n+{xp_gain} XP"
        if leveled:
            msg += f"\n**Seviye atladı!** Yeni seviye: {pokemon.level}\nHP: {pokemon.hp} | Güç: {pokemon.power}"
        await ctx.send(msg)

    else:
        xp_gain = random.randint(30, 60)
        leveled = pokemon.gain_xp(xp_gain)
        msg = f"**{pokemon.name.upper()}** nadir bir Pokémon buldu!\n+{xp_gain} XP"
        if leveled:
            msg += f"\n**Seviye atladı!** Yeni seviye: {pokemon.level}\nHP: {pokemon.hp} | Güç: {pokemon.power}"
        await ctx.send(msg)


@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Savaş için her iki tarafın da Pokémon sahibi olması gerekir!")
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")


bot.run(token)
