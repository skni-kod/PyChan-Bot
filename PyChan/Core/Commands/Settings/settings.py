import discord
from discord.ext import commands

from Core.Commands.Settings.Functions.change_prefix import ChangePrefix
from Core.Commands.Settings.Functions.change_status import ChangeStatus


class Settings(commands.Cog):
    """Class contains commands with settings
    """
    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(ChangePrefix(bot))
        self.bot.add_cog(ChangeStatus(bot))

