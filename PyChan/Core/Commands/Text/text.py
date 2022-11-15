import nextcord
from nextcord.ext import commands
from Core.Commands.Text.Functions.bored import BoredAPI

from Core.Commands.Text.Functions.fun_fact import FunFact
from Core.Commands.Text.Functions.covid import Covid
from Core.Commands.Text.Functions.west import KanyeWestQuote


class Text(commands.Cog):
    """Class contains commands with text commands
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(KanyeWestQuote(bot))
        self.bot.add_cog(FunFact(bot))
        self.bot.add_cog(BoredAPI(bot))
        self.bot.add_cog(Covid(bot))