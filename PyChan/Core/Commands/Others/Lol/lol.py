import discord
from discord.ext import commands
from riotwatcher._apis.league_of_legends.ChampionApiV3 import ChampionApiV3

from Core.Commands.Others.Lol.Function.summoner_info import SummonerInfo
from Core.Commands.Others.Lol.Function.champion import Champion

class Lol(commands.Cog):
    """Class contains science categories
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(SummonerInfo(bot))
        self.bot.add_cog(Champion(bot))