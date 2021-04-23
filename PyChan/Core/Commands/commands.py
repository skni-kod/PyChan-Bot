import discord
from discord.ext import commands

from Core.Commands.Help.help import Help
from Core.Commands.Maths.maths import Maths
from Core.Commands.Physics.physics import Physics
from Core.Commands.Settings.settings import Settings
from Core.Commands.Utilities.utilities import Utilities

class Commands(commands.Cog):
    """Class contains commands
    """
    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(Help(bot))
        self.bot.add_cog(Maths(bot))
        self.bot.add_cog(Physics(bot))
        self.bot.add_cog(Settings(bot))
        self.bot.add_cog(Utilities(bot))
