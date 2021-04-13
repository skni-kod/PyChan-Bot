import discord
from discord.ext import commands

from Core.Commands.Utilities.Functions.ssh import Ssh

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Ssh(bot))
