import discord
from discord.ext import commands

from Core.Commands.Science.Maths.Functions.booth import BoothAlgorithm
from Core.Commands.Science.Maths.Functions.convert_numbers import ConvertNumbers
from Core.Commands.Science.Maths.Functions.convert_numbers_plus import ConvertNumbersPlus
from Core.Commands.Science.Maths.Functions.ieee754_32 import Ieee754x32
from Core.Commands.Science.Maths.Functions.ieee754_64 import Ieee754x64
from Core.Commands.Science.Maths.Functions.permutations import Permutations


class Maths(commands.Cog):
    """Class contains maths methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(BoothAlgorithm(bot))
        self.bot.add_cog(ConvertNumbers(bot))
        self.bot.add_cog(ConvertNumbersPlus(bot))
        self.bot.add_cog(Ieee754x32(bot))
        self.bot.add_cog(Ieee754x64(bot))
        self.bot.add_cog(Permutations(bot))
