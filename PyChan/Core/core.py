import discord
from discord.ext import commands

from Core.Commands.commands import Commands
from Core.Errors.errors import Errors
from Core.Listeners.listeners import Listeners


class Core(commands.Cog):
    """Class which loads all Cogs and passes it to main
    """
    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(Commands(bot))
        self.bot.add_cog(Errors(bot))
        self.bot.add_cog(Listeners(bot))