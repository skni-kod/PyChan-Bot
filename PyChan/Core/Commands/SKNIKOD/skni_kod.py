import nextcord
from nextcord.ext import commands

from Core.Commands.SKNIKOD.Functions.get_members_projects import GetMembersProjects


class SKNIKOD(commands.Cog):
    """Class contains SKNI KOD methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(GetMembersProjects(bot))
