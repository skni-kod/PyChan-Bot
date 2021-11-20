import discord
from discord.ext import commands

from Core.Commands.Others.Lol.Function.summoner_info import SummonerInfo


class Lol(commands.Cog):
    """Class contains science categories
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(SummonerInfo(bot))
