from nextcord.ext import commands
from .aoc import AoC
from .prefix import ChangePrefix
from .meteo import Meteo


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(AoC(bot))
        self.bot.add_cog(ChangePrefix(bot))
        self.bot.add_cog(Meteo(bot))
