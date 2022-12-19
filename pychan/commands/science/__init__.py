from nextcord.ext import commands
from maths import Maths


class Science(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Maths(bot))
