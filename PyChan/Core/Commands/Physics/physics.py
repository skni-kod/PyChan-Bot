import discord
from discord.ext import commands


class Physics(commands.Cog):
    """Class contains physics commands
    """
    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
