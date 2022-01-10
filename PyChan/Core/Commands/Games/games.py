import discord
from discord.ext import commands
from Core.Commands.Games.Functions.osu import Osu


class Games(commands.Cog):
    """Class contains gaming methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(Osu(bot))
