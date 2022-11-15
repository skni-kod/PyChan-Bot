import nextcord
from nextcord.ext import commands

from Core.Commands.Utilities.Functions.ssh import SSH
from Core.Commands.Utilities.Functions.AoC import AoC
from Core.Commands.Utilities.Functions.west import KanyeWestQuete

class Utilities(commands.Cog):
    """Class contains commands with utilities
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(SSH(bot))
        self.bot.add_cog(AoC(bot))
        self.bot.add_cog(KanyeWestQuete(bot))