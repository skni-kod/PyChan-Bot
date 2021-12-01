import discord
from discord.ext import commands

from Core.Commands.Text.Functions.fun_fact import FunFact


class Text(commands.Cog):
    """Class contains commands with text commands
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(FunFact(bot))