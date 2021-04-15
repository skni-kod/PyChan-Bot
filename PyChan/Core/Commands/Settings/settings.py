import discord
from discord.ext import commands

from Core.Commands.Settings.Functions.change_prefix import Change_prefix


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Change_prefix(bot))

