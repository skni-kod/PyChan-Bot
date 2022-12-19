from nextcord.ext import commands
from get_members_projects import GetMembersProjects


class SKNIKOD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(GetMembersProjects(bot))
