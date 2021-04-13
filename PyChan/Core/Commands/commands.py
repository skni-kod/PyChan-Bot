import discord
from discord.ext import commands

from Core.Commands.Errors.errors import Errors
from Core.Commands.Help.help import Help
from Core.Commands.Listeners.listeners import Listeners
from Core.Commands.Maths.maths import Maths
from Core.Commands.Physics.physics import Physics
from Core.Commands.Utilities.utilities import Utilities

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Errors(bot))
        self.bot.add_cog(Help(bot))
        self.bot.add_cog(Listeners(bot))
        self.bot.add_cog(Maths(bot))
        self.bot.add_cog(Physics(bot))
        self.bot.add_cog(Utilities(bot))
