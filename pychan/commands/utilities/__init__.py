from nextcord.ext import commands
from .ssh import SSH
from .aoc import AoC

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(SSH(bot))
        self.bot.add_cog(AoC(bot))
