from nextcord.ext import commands

from pychan.commands.economy.funds import Funds
from pychan.commands.economy.gamble import Gamble


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.add_cog(Funds())
        bot.add_cog(Gamble())
