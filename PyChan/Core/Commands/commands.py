import discord
from discord.ext import commands

from Core.Commands.Help.help import Help
from Core.Commands.Images.images import Images
from Core.Commands.Others.others import Others
from Core.Commands.Science.science import Science
from Core.Commands.Settings.settings import Settings
from Core.Commands.SKNIKOD.skni_kod import SKNIKOD
from Core.Commands.Text.text import Text
from Core.Commands.Utilities.utilities import Utilities
from Core.Commands.Games.games import Games


class Commands(commands.Cog):
    """Class contains commands
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(Help(bot))
        self.bot.add_cog(Images(bot))
        self.bot.add_cog(Others(bot))
        self.bot.add_cog(Science(bot))
        self.bot.add_cog(SKNIKOD(bot))
        self.bot.add_cog(Settings(bot))
        self.bot.add_cog(Text(bot))
        self.bot.add_cog(Utilities(bot))
        self.bot.add_cog(Games(bot))
