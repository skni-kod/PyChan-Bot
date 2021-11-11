import discord
from discord.ext import commands

from Core.Commands.Science.Maths.maths import Maths


class Science(commands.Cog):
    """Class contains science categories
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(Maths(bot))
