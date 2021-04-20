import discord
from discord.ext import commands

from Core.Commands.Settings.Functions.change_prefix import ChangePrefix


class Settings(commands.Cog):
    """Class which contains commands with settings
    """
    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(ChangePrefix(bot))

