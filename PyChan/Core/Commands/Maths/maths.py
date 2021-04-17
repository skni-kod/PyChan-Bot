import discord
from discord.ext import commands

from Core.Commands.Maths.Functions.convert_numbers import Convert_numbers
from Core.Commands.Maths.Functions.convert_numbers_plus import Convert_numbers_plus
from Core.Commands.Maths.Functions.ieee754_32 import Ieee754_32
from Core.Commands.Maths.Functions.ieee754_64 import Ieee754_64
from Core.Commands.Maths.Functions.permutations import Permutations


class Maths(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Convert_numbers(bot))
        self.bot.add_cog(Convert_numbers_plus(bot))
        self.bot.add_cog(Ieee754_32(bot))
        self.bot.add_cog(Ieee754_64(bot))
        self.bot.add_cog(Permutations(bot))
