import discord
from discord.ext import commands

from PyChan.Core.Commands.Maths.Functions.convert_numbers import Convert_numbers
from PyChan.Core.Commands.Maths.Functions.convert_numbers_plus import Convert_numbers_plus
from PyChan.Core.Commands.Maths.Functions.ieee754_32 import Ieee754_32
from PyChan.Core.Commands.Maths.Functions.ieee754_64 import Ieee754_64


class Maths(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Convert_numbers(bot))
        self.bot.add_cog(Convert_numbers_plus(bot))
        self.bot.add_cog(Ieee754_32(bot))
        self.bot.add_cog(Ieee754_64(bot))
