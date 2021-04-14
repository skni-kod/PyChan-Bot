import discord
from discord.ext import commands

from PyChan.Core.Commands.commands import Commands
from PyChan.Core.Errors.errors import Errors
from PyChan.Core.Listeners.listeners import Listeners


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Commands(bot))
        self.bot.add_cog(Errors(bot))
        self.bot.add_cog(Listeners(bot))