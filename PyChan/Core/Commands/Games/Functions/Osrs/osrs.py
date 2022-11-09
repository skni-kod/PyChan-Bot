import nextcord
from osrs_api import Hiscores
from osrs_api import GrandExchange
from osrs_api import Item
from nextcord.ext import commands

class Osrs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        pass_context=True,
        name='osrs',
        category='Gry',
        help_={
            "title": "Oldschool Runescape",
            "description": "Komenda wyświetla informacje o danym graczu. Może być również wykorzystana do sprawdzenia ceny danego przedmiotu na Grand Exchange",
            "fields": [
                {
                    "name": "Statystyki:",
                    "value": "osrs user:h3ryin - wyświetli statystyki gracza h3ryin",
                },
                {
                    "name": "Cena przedmiotu:",
                    "value": "osrs price:Abyssal Whip - wyświetli obecną cenę przedmiotu Abyssal Whip"  
                },
                {
                    "name": "Oznaczenia:",
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
    
    async def osrs(self, ctx, *args):
        """
        Gets HiScore data of a user or a price of an item, depending on
        whether the "user:" or "price:" argument was used.
        """
        
        
        if ' '.join((args)).split(":")[0] == "user":
            
            skills = {'attack': '⚔️',  'hitpoints': '❤️', 'mining': '⛏️', 
                  'strength': '✊', 'agility': '🏃', 'smithing': '🔨', 
                  'defence': '🛡️', 'herblore': '🌿', 'fishing': '🐟', 
                  'ranged': '🏹', 'thieving': '🏃', 'cooking': '🍲', 
                  'prayer': '✨', 'crafting': '🛠️', 'firemaking': '🔥', 
                  'magic': '🧙', 'fletching': '🔪', 'woodcutting': '🌳', 
                  'runecrafting': '🍪', 'slayer': '💀', 'farming': '🌽',
                  'construction': '🏡', 'hunter': '🐾', 'total': '🏆'
            }
            
            accountName = ' '.join(args).split(":")[1]
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
        
        if ' '.join((args)).split(":")[0] == "price":
            itemName = ' '.join(args).split(":")[1].lower()
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
                    elif(itemTrend.trend == 'positive'):
                        trendEmoji = '📈'
                    else:
                        trendEmoji = '📊'
                    embed.add_field(
                        name = f"{item.name}",
                        value = f"Cena: {item.price()} gp \n Trend: {trendEmoji} | {round(itemTrend.change, 0)}% (ostatnie 7 dni)"
                    )
                    embed.set_thumbnail(url = f"https://oldschool.runescape.wiki/images/{Item.id_to_name(itemId).replace(' ', '_')}_detail.png")
        await ctx.send(embed=embed)