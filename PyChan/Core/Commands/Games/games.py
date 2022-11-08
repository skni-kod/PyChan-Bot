from nextcord.ext import commands

from Core.Commands.Games.Functions.osu import Osu
from Core.Commands.Games.Functions.summoner_info import SummonerInfo
from Core.Commands.Games.Functions.lastMatch import LastMatch

class Games(commands.Cog):
    """Class contains gaming methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(Osu(bot))
        self.bot.add_cog(SummonerInfo(bot))
        self.bot.add_cog(LastMatch(bot))
