import discord
from discord.ext import commands

from Core.Commands.Help.help import Help
from Core.Commands.Maths.maths import Maths
from Core.Commands.Physics.physics import Physics


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Help(bot))
        self.bot.add_cog(Maths(bot))
        self.bot.add_cog(Physics(bot))
