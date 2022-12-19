from nextcord.ext import commands
from .commands import Commands
from .errors import Errors
from .listeners import Listeners


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Commands(bot))
        self.bot.add_cog(Errors(bot))
        self.bot.add_cog(Listeners(bot))
