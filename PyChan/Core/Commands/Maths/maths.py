import discord
from discord.ext import commands

from Core.Commands.Maths.Functions.convert_numbers import ConvertNumbers
from Core.Commands.Maths.Functions.convert_numbers_plus import ConvertNumbersPlus
from Core.Commands.Maths.Functions.ieee754_32 import Ieee754x32
from Core.Commands.Maths.Functions.ieee754_64 import Ieee754x64
from Core.Commands.Maths.Functions.permutations import Permutations


class Maths(commands.Cog):
    """Class which contains maths methods
    """
    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(ConvertNumbers(bot))
        self.bot.add_cog(ConvertNumbersPlus(bot))
        self.bot.add_cog(Ieee754x32(bot))
        self.bot.add_cog(Ieee754x64(bot))
        self.bot.add_cog(Permutations(bot))
