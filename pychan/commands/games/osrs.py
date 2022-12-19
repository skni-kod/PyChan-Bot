import nextcord
from nextcord.ext import commands
from osrs_api import GrandExchange, Hiscores, Item

skillsPerms = {'attack': '<:osrs_attack:1041097852648161360>',  'hitpoints': '<:osrs_hitpoints:1041122749294329876>', 'mining': '<:osrs_mining:1041123033177399306>',
               'strength': '<:osrs_strength:1041123003720810557>', 'agility': '<:osrs_agility:1041123509629362297>', 'smithing': '<:osrs_smithing:1041123398731972638>',
               'defence': '<:osrs_defence:1041123882180022282>', 'herblore': '<:osrs_herblore:1041123956733779968>', 'fishing': '<:osrs_fishing:1041124029899219076>',
               'ranged': '<:osrs_ranged:1041124096114688091>', 'thieving': '<:osrs_thieving:1041124182924202055>', 'cooking': '<:osrs_cooking:1041124263182213232>',
               'prayer': '<:osrs_prayer:1041124321285914694>', 'crafting': '<:osrs_crafting:1041124418220478464>', 'firemaking': '<:osrs_firemaking:1041124535778426960>',
               'magic': '<:osrs_magic:1041127032978944130>', 'fletching': '<:osrs_fletching:1041127143687594034>', 'woodcutting': '<:osrs_woodcutting:1041127210733535302>',
               'runecrafting': '<:osrs_runecraft:1041124609841434644>', 'slayer': '<:osrs_slayer:1041124679601094676>', 'farming': '<:osrs_farming:1041124747225878609>',
               'construction': '<:osrs_construction:1041124815764996146>', 'hunter': '<:osrs_hunter:1041124880982229022>', 'total': '🏆'
               }

skillsNoPerms = {'attack': '⚔️',  'hitpoints': '❤️', 'mining': '⛏️',
                 'strength': '✊', 'agility': '🏃', 'smithing': '🔨',
                 'defence': '🛡️', 'herblore': '🌿', 'fishing': '🐟',
                 'ranged': '🏹', 'thieving': '🏃', 'cooking': '🍲',
                 'prayer': '✨', 'crafting': '🛠️', 'firemaking': '🔥',
                 'magic': '🧙', 'fletching': '🔪', 'woodcutting': '🌳',
                 'runecrafting': '🍪', 'slayer': '💀', 'farming': '🌽',
                 'construction': '🏡', 'hunter': '🐾', 'total': '🏆'
                 }


class Osrs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="osrs",
        category="Gry"
    )
    async def osrs(self, ctx: commands.Context):
        '''Komendy związane z grą Old School Runescape'''
        pass

    @osrs.command(
        pass_context=True,
        name='user',
        usage='<nick>',
        help="""Wyświetla statystyki danego gracza
    
                **Oznaczenia**
                ⚔️ `- Attack       `| ❤️ `- Hitpoints `| ⛏️ `- Mining`
                ✊ `- Strength     `| 🏃 `- Agility   `| 🔨 `- Smithing`
                🛡️ `- Defence      `| 🌿 `- Herblore  `| 🐟 `- Fishing`
                🏹 `- Ranged       `| 💰 `- Thieving  `| 🍲 `- Cooking`
                ✨ `- Prayer       `| 🛠️ `- Crafting  `| 🔥 `- Firemaking`
                🧙 `- Magic        `| 🔪 `- Fletching `| 🌳 `- Woodcutting`
                🍪 `- Runecraft    `| 💀 `- Slayer    `| 🌽 `- Farming`
                🏡 `- Construction `| 🐾 `- Hunter    `| 🏆 `- Total`
               """
    )
    async def user(self, ctx, *, accountName: str):
        if nextcord.abc.GuildChannel.permissions_for(ctx.channel, ctx.me).external_emojis:
            skills = skillsPerms
        else:
            skills = skillsNoPerms
        accountExists = True
        try:
            accountData = Hiscores(accountName)
        except Exception:
            accountExists = False
            embed = nextcord.Embed(
                title=f"Nie znaleziono informacji o koncie {accountName}",
                color=nextcord.Color.yellow(),
                description="Może to oznaczać, że nie jest w top 2,000,000 graczy lub takie konto nie istnieje"
            )
        if accountExists:
            accountStats = accountData.skills
            embed = nextcord.Embed(
                title=f"Statystyki gracza {accountName}",
                color=nextcord.Color.yellow(),
            )
            skillsTotal = 0
            counter = 0
            reset = 0
            result = ""
            xpTotal = 0
            for skill in skills:
                if skill != 'total':
                    skillsTotal += accountStats[f'{skill}'].level
                    xpTotal += accountStats[f'{skill}'].xp
                if skill != 'total' and counter == 2:
                    result += f"{skills[skill]} {accountStats[skill].level}\n\n"
                    xpTotal += accountStats[f'{skill}'].xp
                    counter = 0
                    reset = 1
                if skill != 'total' and counter != 2 and not reset == 1:
                    result += f"{skills[skill]} {accountStats[skill].level} | "
                    xpTotal += accountStats[f'{skill}'].xp
                    counter += 1
                if skill == 'total':
                    result += f"{skills[skill]} {skillsTotal}"
                reset = 0
            result += f"\n\n**{accountData.rank} miejsce na globalnej liście**"
            result += f"\n\n**{xpTotal} XP**"
            embed.description = result
            await ctx.send(embed=embed)

    @osrs.command(
        pass_context=True,
        name='price',
        usage='<przedmiot>',
        help="""Wyświetla cenę danego przedmiotu.
        
                  Jesli przedmiot przedmiot ma więcej niż jeden wynik, \
                  lub została wprowadzona niepełna nazwa, zostaną wyświetlone wszystkie przedmioty z pasującą nazwą.
                  Wszystkie wyniki zostaną wyświetlone z trendem z ostatnich 30 dni.
               """
    )
    async def price(self, ctx, *, itemName: str):
        '''Wyświetla cenę danego przedmiotu'''
        itemId = Item.get_ids(itemName)
        if not itemId:
            embed = nextcord.Embed(
                title=f"Nie znaleziono przedmiotu \"{itemName}\"",
                color=nextcord.Color.yellow(),
            )
        else:
            if (type(itemId) == list):
                [Item.id_to_name(id) for id in itemId]
            embed = nextcord.Embed(
                title=f"Przedmioty pasujące do \"{itemName}\"",
                color=nextcord.Color.yellow(),
            )
            if type(itemId) == list:
                for id in itemId:
                    item = GrandExchange.item(id)
                    itemTrend = item.price_info.trend_30
                    if (itemTrend.trend == 'negative'):
                        trendEmoji = '📉'
                    elif (itemTrend.change == 0):
                        trendEmoji = '📊'
                    else:
                        trendEmoji = '📈'
                    embed.add_field(
                        name=f"{item.name}",
                        value=f"Cena: {item.price()} gp \n Trend: {trendEmoji} | {round(itemTrend.change, 0)}% (ostatnie 30 dni)"
                    )
                embed.set_thumbnail(
                    url=f"https://oldschool.runescape.wiki/images/{Item.id_to_name(itemId[0]).replace(' ', '_')}_detail.png")
            else:
                item = GrandExchange.item(itemId)
                itemTrend = item.price_info.trend_30
                if (itemTrend.trend == 'negative'):
                    trendEmoji = '📉'
                elif (itemTrend.change == 0):
                    trendEmoji = '📊'
                else:
                    trendEmoji = '📈'
                embed.add_field(
                    name=f"{item.name}",
                    value=f"Cena: {item.price()} gp \n Trend: {trendEmoji} | {round(itemTrend.change, 0)}% (ostatnie 30 dni)"
                )
                embed.set_thumbnail(
                    url=f"https://oldschool.runescape.wiki/images/{Item.id_to_name(itemId).replace(' ', '_')}_detail.png")
        await ctx.send(embed=embed)
