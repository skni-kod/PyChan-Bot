from nextcord.ext import commands

from booth import BoothAlgorithm
from convert_numbers import ConvertNumbers
from convert_numbers_plus import ConvertNumbersPlus
from graphs import Graphs
from ieee754_32 import Ieee754x32
from ieee754_64 import Ieee754x64
from permutations import Permutations


class Maths(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(BoothAlgorithm(bot))
        self.bot.add_cog(ConvertNumbers(bot))
        self.bot.add_cog(ConvertNumbersPlus(bot))
        self.bot.add_cog(Graphs(bot))
        self.bot.add_cog(Ieee754x32(bot))
        self.bot.add_cog(Ieee754x64(bot))
        self.bot.add_cog(Permutations(bot))
