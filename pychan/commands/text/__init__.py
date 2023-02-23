from nextcord.ext import commands
from .bored import BoredAPI
from .fun_fact import FunFact
from .covid import Covid
from .west import KanyeWestQuote
from .converter import Currency


class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(KanyeWestQuote(bot))
        self.bot.add_cog(FunFact(bot))
        self.bot.add_cog(BoredAPI(bot))
        self.bot.add_cog(Covid(bot))
        self.bot.add_cog(Currency(bot))

