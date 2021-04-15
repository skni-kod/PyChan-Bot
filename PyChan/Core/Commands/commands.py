import discord
from discord.ext import commands

from PyChan.Core.Commands.Help.help import Help
from PyChan.Core.Commands.Maths.maths import Maths
from PyChan.Core.Commands.Physics.physics import Physics
from PyChan.Core.Commands.Settings.settings import Settings
from PyChan.Core.Commands.Utilities.utilities import Utilities

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Help(bot))
        self.bot.add_cog(Maths(bot))
        self.bot.add_cog(Physics(bot))
        self.bot.add_cog(Settings(bot))
        self.bot.add_cog(Utilities(bot))
