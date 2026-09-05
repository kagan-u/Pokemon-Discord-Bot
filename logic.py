import aiohttp
import random


class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = random.randint(200, 400)
        self.power = random.randint(30, 60)
        self.level = 1
        self.xp = 0
        self.ability = None
        self.image_url = None

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self

    def get_level_up_xp(self):
        return self.level * 50

    def gain_xp(self, amount):
        self.xp += amount
        leveled = False
        while self.xp >= self.get_level_up_xp():
            self.xp -= self.get_level_up_xp()
            self.level += 1
            self.power += random.randint(3, 8)
            self.hp += random.randint(10, 25)
            leveled = True
        return leveled

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def fetch_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.name = data['forms'][0]['name']
                    self.ability = data['abilities'][0]['ability']['name']
                    self.image_url = data['sprites']['front_default']
                    return True
                return False

    async def info(self):
        if not self.name:
            await self.fetch_data()
        return (
            f"Pokémonunuzun ismi: {self.name}\n"
            f"Sağlık: {self.hp} | Güç: {self.power}\n"
            f"Seviye: {self.level} | XP: {self.xp}/{self.get_level_up_xp()}\n"
            f"Yetenek: {self.ability}"
        )

    async def show_img(self):
        if not self.image_url:
            await self.fetch_data()
        return self.image_url

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullanıldı!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"


class Wizard(Pokemon):
    pass


class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_power}"
