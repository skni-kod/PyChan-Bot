from nextcord.ext.commands import Cog, command, guild_only
from nextcord.ext.commands import Context
import random

from pychan import database

class Gamble(Cog):
    @guild_only()
    @command(name='gamba', category='Ekonomia')
    async def gamble(self, ctx: Context, coins: int):
        '''Zrzuć monetą i wygraj majątek!'''
        with database.Session() as session:
            member = database.get_guild_member(session, ctx.author.id, ctx.guild.id)
            if random.getrandbits(1) == 1:
                member.coins -= coins 
                session.commit()
                await ctx.reply(f'Tracisz wszystko i masz teraz {member.coins} monet.')
            else:
                member.coins += coins
                session.commit()
                await ctx.reply(f'Podwajasz swój majątek i masz teraz {member.coins} monet.')

