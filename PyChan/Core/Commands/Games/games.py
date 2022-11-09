import nextcord
from nextcord.ext import commands
from Core.Commands.Games.Functions.osu import Osu
from Core.Commands.Games.Functions.Osrs.osrs import Osrs


class Games(commands.Cog):
    """Class contains gaming methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(Osu(bot))
        self.bot.add_cog(Osrs(bot))