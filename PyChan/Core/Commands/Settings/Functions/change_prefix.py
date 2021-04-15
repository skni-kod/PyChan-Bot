import discord
from discord.ext import commands
from Core.Decorators.decorators import Decorator

from Database.database import Database


class Change_prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class Check_length():
        @staticmethod
        def check_length(arg):
            if len(arg) != 1:
                raise commands.errors.BadArgument
            return arg

    @commands.command(pass_context=True, name='zmienprefix')
    @Decorator.pychan_decorator
    async def change_prefix(self, ctx, prefix: Check_length.check_length):
        old_prefix = \
            Database.get_one(Database.db_servers, {'_id': ctx.guild.id}, selection={'settings.prefix': 1, '_id': 0})[
                'settings']['prefix']
        # Zapytanie w MongoDB, aby wejsc glebiej do slownika po kluczach uzywamy '.'
        if Database.update_one(Database.db_servers, {'_id': ctx.guild.id}, {'settings.prefix': prefix}):
            await ctx.send(f'Pomyślnie zmienio prefix z {old_prefix} na {prefix}')
