import discord
from discord.ext import commands


from Core.Commands.Others.Lol.Function.summoner_info import SummonerInfo
from Core.Commands.Others.Lol.Function.champion import Champion
from Core.Commands.Others.Lol.Function.lastMatch import LastMatch

class Lol(commands.Cog):
    """Class contains science categories
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(SummonerInfo(bot))
        self.bot.add_cog(Champion(bot))
        self.bot.add_cog(LastMatch(bot))