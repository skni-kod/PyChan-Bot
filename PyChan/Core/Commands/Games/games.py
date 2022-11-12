from nextcord.ext import commands

from Core.Commands.Games.Functions.Osrs.osrs import Osrs
from Core.Commands.Games.Functions.osu import Osu
from Core.Commands.Games.Functions.summoner_info import SummonerInfo
from Core.Commands.Games.Functions.last_match import LastMatch
import config

class Games(commands.Cog):
    """Class contains gaming methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        
        if len(config.osu_token):
            self.bot.add_cog(Osu(bot))
        else:
            print("Osu! API token not found. Related commands will not be loaded")

        if len(config.riot_token):
            self.bot.add_cog(SummonerInfo(bot))
            self.bot.add_cog(LastMatch(bot))
        else:
            print("Riot API token not found. Related commands will not be loaded")

        self.bot.add_cog(Osrs(bot))
