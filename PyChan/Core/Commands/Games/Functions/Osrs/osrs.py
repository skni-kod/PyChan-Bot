import nextcord
from osrs_api import Hiscores
from osrs_api import GrandExchange
from osrs_api import Item
from nextcord.ext import commands

class Osrs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(
        name = "osrs",
        category = "Gry",
        help_ = {
            "title": "osrs",
            "description": f"Komendy związane z grą Old School Runescape\nUżyj `help osrs <podkomenda>` aby uzyskać więcej informacji na temat danej podkomendy",
            "fields": [
                {
                    "name": "user",
                    "value": "Wyświetla statystyki danego gracza",
                },
                {
                    "name": "price",
                    "value": "Wyświetla cenę danego przedmiotu",
                }
            ]
        }
    )
    async def osrs(self, _: commands.Context):
        pass
    
    @osrs.command(
        pass_context=True,
        name='user',
        help_={
            "title": "osrs user",
            "description": "wyświetla statystyki danego graczu.",
            "fields": [
                {
                    "name": "Przykład użycia",
                    "value": f"`osrs user Lynx Titan` - wyświetli statystyki gracza Lynx Titan",
                },
                {
                    "name": "Oznaczenia",
                    "value": """
```
⚔️ - Attack       | ❤️ - Hitpoints | ⛏️ - Mining
✊ - Strength     | 🏃 - Agility   | 🔨 - Smithing
🛡️ - Defence      | 🌿 - Herblore  | 🐟 - Fishing
🏹 - Ranged       | 💰 - Thieving  | 🍲 - Cooking
✨ - Prayer       | 🛠️ - Crafting  | 🔥 - Firemaking
🧙 - Magic        | 🔪 - Fletching | 🌳 - Woodcutting
🍪 - Runecraft    | 💀 - Slayer    | 🌽 - Farming
🏡 - Construction | 🐾 - Hunter    | 🏆 - Total
```
"""
#If it's not indented this way, the code block keeps the space before the actual content
                }
            ],
        }
    )
    async def user(self, ctx, *, accountName: str):
        skills = {'attack': '⚔️',  'hitpoints': '❤️', 'mining': '⛏️', 
                'strength': '✊', 'agility': '🏃', 'smithing': '🔨', 
                'defence': '🛡️', 'herblore': '🌿', 'fishing': '🐟', 
                'ranged': '🏹', 'thieving': '🏃', 'cooking': '🍲', 
                'prayer': '✨', 'crafting': '🛠️', 'firemaking': '🔥', 
                'magic': '🧙', 'fletching': '🔪', 'woodcutting': '🌳', 
                'runecrafting': '🍪', 'slayer': '💀', 'farming': '🌽',
                'construction': '🏡', 'hunter': '🐾', 'total': '🏆'
        }
        accountExists = True
        try:
            accountData = Hiscores(accountName)
        except Exception:
            accountExists = False
            embed = nextcord.Embed(
                title = f"Nie znaleziono informacji o koncie {accountName}",
                color = nextcord.Color.yellow(),
                description = "Może to oznaczać, że nie jest w top 2,000,000 graczy lub takie konto nie istnieje"
            )
        if accountExists:
            accountStats = accountData.skills
            embed = nextcord.Embed(
                title = f"Statystyki gracza {accountName}",
                color = nextcord.Color.yellow(),
            )
            skillsTotal = 0
            counter = 0
            reset = 0
            result = ""
            for skill in skills:
                if skill != 'total':
                    skillsTotal += accountStats[f'{skill}'].level
                if skill != 'total' and counter == 2:
                    result += f"{skills[skill]} {accountStats[skill].level}\n\n"
                    counter = 0
                    reset = 1
                if skill != 'total' and counter != 2 and not reset == 1:
                    result += f"{skills[skill]} {accountStats[skill].level} | "
                    counter += 1
                if skill == 'total':
                    result += f"{skills[skill]} {skillsTotal}"
                reset = 0
            embed.description = result
            await ctx.send(embed=embed)
    
    @osrs.command(
        pass_context=True,
        name='price',
        help_ = {
            "name": "osrs price",
            "description": "Wyświetla cenę danego przedmiotu. Jesli przedmiot przedmiot ma więcej niż jeden wynik,\
                            wszystkie wyniki zostaną wyświetlone z trendem z ostatnich 7 dni.",
            "fields": [
                {
                    "name": "Przykład użycia",
                    "value": "`osrs price rune platebody` - wyświetli cenę rune platebody\n\
                              `osrs price dragon dag` - wyświetli ceny wszystkich przedmiotów zaczynających się od dragon dag"
                }
            ]
        }
    )
    async def price(self, ctx, *, itemName: str):
            itemId = Item.get_ids(itemName)
            if not itemId:
                embed = nextcord.Embed(
                    title = f"Nie znaleziono przedmiotu \"{itemName}\"",
                    color = nextcord.Color.yellow(),
                )
            else:
                if(type(itemId) == list):
                    [Item.id_to_name(id) for id in itemId]
                embed = nextcord.Embed(
                    title = f"Przedmioty pasujące do \"{itemName}\"",
                    color = nextcord.Color.yellow(),
                )
                result = ""
                if type(itemId) == list:
                    for id in itemId:
                        item = GrandExchange.item(id)
                        itemTrend = item.price_info.trend_30
                        if(itemTrend.trend == 'negative'):
                            trendEmoji = '📉'
                        elif(itemTrend.trend == 'positive'):
                            trendEmoji = '📈'
                        else:
                            trendEmoji = '📊'
                        embed.add_field(
                            name = f"{item.name}",
                            value = f"Cena: {item.price()} gp \n Trend: {trendEmoji} | {round(itemTrend.change, 0)}% (ostatnie 7 dni)"   
                        )
                    embed.set_thumbnail(url = f"https://oldschool.runescape.wiki/images/{Item.id_to_name(itemId[0]).replace(' ', '_')}_detail.png")
                else:
                    item = GrandExchange.item(itemId)
                    itemTrend = item.price_info.trend_30
                    if(itemTrend.trend == 'negative'):
                        trendEmoji = '📉'
                    elif(itemTrend.change == 0):
                        trendEmoji = '📊'
                    else:
                        trendEmoji = '📈'
                    embed.add_field(
                        name = f"{item.name}",
                        value = f"Cena: {item.price()} gp \n Trend: {trendEmoji} | {round(itemTrend.change, 0)}% (ostatnie 7 dni)"
                    )
                    embed.set_thumbnail(url = f"https://oldschool.runescape.wiki/images/{Item.id_to_name(itemId).replace(' ', '_')}_detail.png")
            await ctx.send(embed=embed)