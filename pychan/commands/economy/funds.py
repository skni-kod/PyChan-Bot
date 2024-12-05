from nextcord.ext import commands
from nextcord.ext.commands import Cog, guild_only
from nextcord.ext.commands import Context
from nextcord.ext.commands import group
from nextcord.user import User

from pychan import database

debug = True

def admin_only_or_debug(f):
    if debug:
        return f
    else:
        return commands.has_permissions(administrator=True)(f)
    
class Funds(Cog):
    @guild_only()
    @group(name='hajs', category='Ekonomia')
    async def funds(self, ctx: Context):
        '''Komendy administracyjne do zarządzania ekonomią serwera'''
        if not ctx.subcommand_passed:
            with database.Session() as session:
                member = database.get_guild_member(session, ctx.author.id, ctx.guild.id)
                await ctx.reply(f'Posiadasz {member.coins} monet.')

    @guild_only()
    @admin_only_or_debug
    @funds.command(name='dodaj')
    async def add(self, ctx: Context, user: User, coins: int):
        with database.Session() as session:
            member = database.get_guild_member(session, user.id, ctx.guild.id)
            member.coins += coins
            session.commit()
            await ctx.reply(f'{user.display_name} ma teraz {member.coins} monet.')

    @guild_only()
    @admin_only_or_debug
    @funds.command(name='ustaw')
    async def set_(self, ctx: Context, user: User, coins: int):
        with database.Session() as session:
            member = database.get_guild_member(session, user.id, ctx.guild.id)
            member.coins = coins
            session.commit()
            await ctx.reply(f'{user.display_name} ma teraz {member.coins} monet.')

    @guild_only()
    @admin_only_or_debug
    @funds.command(name='zabierz')
    async def tax(self, ctx: Context, user: User, coins: int):
        with database.Session() as session:
            member = database.get_guild_member(session, user.id, ctx.guild.id)
            member.coins -= coins
            session.commit()
            await ctx.reply(f'{user.display_name} ma teraz {member.coins} monet.')

