from nextcord.ext import commands
from .maths import Maths
from .chomsky import Chomsky
from .greybach import Greybach


class Science(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Maths(bot))
        self.bot.add_cog(Chomsky(bot))
        self.bot.add_cog(Greybach(bot))
