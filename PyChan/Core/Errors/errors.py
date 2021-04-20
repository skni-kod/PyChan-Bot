import discord
from discord.ext import commands


class Errors(commands.Cog):
    """Class which handles errors raised by other methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Function is called when error is raised

        :param ctx: the context in which a command is called
        :type ctx: discord.ext.commands.Context
        :param error: contains information about error
        :type error: discord.ext.commands.CommandError
        """
        if isinstance(error, commands.errors.CommandNotFound):
            embed = discord.Embed(color=discord.Color.dark_purple())
            embed.add_field(name='Błąd',
                            value='Podana komenda nie istnieje',
                            inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send('Niepoprawny parametr')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('Brakuje wymaganego parametru')
        elif isinstance(error, Exception):
            await ctx.send('Coś poszło nie tak')
            print(error)
        else:
            print(error)
