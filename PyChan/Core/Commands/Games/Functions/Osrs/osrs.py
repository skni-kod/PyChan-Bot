import nextcord
from osrs_api import Hiscores
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
            
            skills = ['attack',  'hitpoints', 'mining', 
                  'strength', 'agility', 'smithing', 
                  'defence', 'herblore', 'fishing', 
                  'ranged', 'thieving', 'cooking', 
                  'prayer', 'crafting', 'firemaking', 
                  'magic', 'fletching', 'woodcutting', 
                  'runecrafting', 'slayer', 'farming',
                  'construction', 'hunter', 'total'
            ]
            skillsNames = ['⚔️',  '❤️', '⛏️', 
                           '✊', '🏃', '🔨', 
                           '🛡️', '🌿', '🐟', 
                           '🏹', '💰', '🍲', 
                           '✨', '🛠', '🔥', 
                           '🧙', '🔪', '🌳', 
                           '🍪', '💀', '🌽',
                           '🏡', '🐾', "🏆"
            ]
            
            accountName = ' '.join(args).split(":")[1]
            accountData = Hiscores(accountName)
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
                    result += f"{skillsNames[skills.index(skill)]} {accountStats[skill].level}\n\n"
                    counter = 0
                    reset = 1
                if skill != 'total' and counter != 2 and not reset == 1:
                    result += f"{skillsNames[skills.index(skill)]} {accountStats[skill].level} | "
                    counter += 1
                if skill == 'total':
                    result += f"{skillsNames[skills.index(skill)]} {skillsTotal}"
                reset = 0
            embed.description = result
        await ctx.send(embed=embed)