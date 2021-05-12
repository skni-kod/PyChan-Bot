import discord
from discord.ext import commands, tasks

from Core.Commands.Utilities.Functions.ssh import Ssh
from Database.database import Database

class Utilities(commands.Cog):
    """Class contains commands with utilities
    """
    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(Ssh(bot))
        self.check_connect_with_db.start()