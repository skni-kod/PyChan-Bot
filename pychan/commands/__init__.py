from nextcord.ext import commands

from .images import Images
from .music import Music
from .science import Science
from .settings import Settings
from .sknikod import SKNIKOD
from .text import Text
from .utilities import Utilities
from .games import Games


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Images(bot))
        self.bot.add_cog(Music(bot))
        self.bot.add_cog(Science(bot))
        self.bot.add_cog(SKNIKOD(bot))
        self.bot.add_cog(Settings(bot))
        self.bot.add_cog(Text(bot))
        self.bot.add_cog(Utilities(bot))
        self.bot.add_cog(Games(bot))
