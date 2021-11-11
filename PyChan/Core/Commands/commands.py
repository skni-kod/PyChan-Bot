import discord
from discord.ext import commands

from Core.Commands.Help.help import Help
from Core.Commands.Images.images import Images
from Core.Commands.Science.science import Science
from Core.Commands.Settings.settings import Settings
from Core.Commands.SKNIKOD.skni_kod import SKNIKOD
from Core.Commands.Utilities.utilities import Utilities


class Commands(commands.Cog):
    """Class contains commands
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(Help(bot))
        self.bot.add_cog(Images(bot))
        self.bot.add_cog(Science(bot))
        self.bot.add_cog(SKNIKOD(bot))
        self.bot.add_cog(Settings(bot))
        self.bot.add_cog(Utilities(bot))
