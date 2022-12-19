from nextcord.ext import commands
from .change_prefix import ChangePrefix


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(ChangePrefix(bot))
