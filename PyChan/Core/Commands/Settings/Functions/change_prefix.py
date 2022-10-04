import nextcord
from nextcord.ext import commands
from Core.Decorators.decorators import Decorator

from Database.database import Database


class ChangePrefix(commands.Cog):
    """Class contains command used to change Bot's prefix
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    class CheckLength:
        """Class contains `check_length` method
        """

        @staticmethod
        def check_length(arg):
            """Checks if input string length is 1, else raise BadArgument error

            :param arg: Input string
            :type arg: str
            :raises commands.errors.BadArgument: string is longer than 1
            :return: Return the same string
            :rtype: str
            """
            if len(arg) != 1:
                raise commands.errors.BadArgument
            return arg

    @commands.command(pass_context=True, name='zmienprefix')
    @Decorator.pychan_decorator
    async def change_prefix(self, ctx, prefix: CheckLength.check_length):
        """Changes server's command prefix

        :param ctx: the context in which a command is called
        :type ctx: nextcord.ext.commands.Context
        :param prefix: new prefix which invokes commands
        :type prefix: str
        """
        old_prefix = \
            Database.get_one(Database.db_servers, {'_id': ctx.guild.id}, selection={'settings.prefix': 1, '_id': 0})[
                'settings']['prefix']
        # Zapytanie w MongoDB, aby wejsc glebiej do slownika po kluczach uzywamy '.'
        if Database.update_one(Database.db_servers, {'_id': ctx.guild.id}, {'settings.prefix': prefix}):
            await ctx.send(f'Pomyślnie zmienio prefix z {old_prefix} na {prefix}')
