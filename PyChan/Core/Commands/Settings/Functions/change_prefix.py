from typing import Optional
from nextcord.ext import commands
import Database

class ChangePrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def check_length(arg):
        if len(arg) != 1:
            raise commands.errors.BadArgument
        return arg

    @commands.command(category='Ustawienia')
    async def prefix(self, ctx: commands.Context, *, prefix: Optional[str]):
        '''Ustawia prefix dla tego serwera'''
        if not ctx.guild:
            await ctx.send('Tutaj nie możesz zmienić prefixu')
            return 

        if not prefix:
            await ctx.send(f'Aktualny prefix to `{ctx.prefix}`')
        else:
            Database.set_guild_prefix(ctx.guild, prefix)
            await ctx.send(f'Pomyślnie zmienio prefix z `{ctx.prefix}` na `{prefix}`')
