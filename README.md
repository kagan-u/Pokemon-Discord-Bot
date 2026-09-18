# Pokemon Discord Bot
**Powered By Vi3ecode.com**
Discord sunucunuzda çalıştırabileceğiniz basit bir Pokemon botu. Rastgele Pokemon oluşturup geliştime, eğit ve diğer kullanıcılarla savaş.

## Komutlar

| Komut | Aciklama |
|-------|----------|
| `!go` | Rastgele bir Pokemon olusturur. Turu (Pokemon/Wizard/Fighter) sansla belirlenir |
| `!info` | Mevcut Pokemonunun bilgilerini gosterir (isim, hp, guc, seviye, xp) |
| `!list` | Pokemonunun kisa ozetini gosterir |
| `!attack @kullanici` | Belirttigin kisiye saldirirsin |
| `!train` | Pokemonunu egitirsin, XP kazanirsin |
| `!hunt` | Vahsi Pokemon avlarsin, XP kazanirsin ama hasar da alabilirsin |
| `!evolve` | Pokemonunu guclendirirsin, seviye atlatirsin |

## Pokemon Turleri

- **Pokemon**: Standart tur. Dengeli HP ve gucu var.
- **Wizard**: Sihirbaz Pokemon. Dusuk HP ama yuksek gucu var. Dusmanlara karsi %20 sansla kalkan kullanabilir.
- **Fighter**: Savasci Pokemon. Yuksek HP ama dusuk gucu var. Saldirdiginda ekstra guc ekler.

## Nasil Calistirilir

1. Repoyu klonla
2. `pip install -r requirements.txt` ile bagimliliklari yukle
3. `config.py` dosyasina Discord bot tokenini yaz
4. `python main.py` ile calistir

## Gereksinimler

- Python 3.8+
- discord.py
- aiohttp
