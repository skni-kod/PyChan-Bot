from nextcord.ext import commands
from .get_members_projects import GetMembersProjects
from .reactionstomessage import ReactionsToMessage


class SKNIKOD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(GetMembersProjects(bot))
        self.bot.add_cog(ReactionsToMessage(bot))