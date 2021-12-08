import os

import discord
from discord.ext import commands
from ossapi import Ossapi, GameMode


class Osu(commands.Cog):
    """
    Class contains osu methods
    """

    def __init__(self, bot):
        """
        Constructor method
        """
        self.bot = bot
        self.osu = Ossapi(os.getenv("OSU_API_KEY"))

    @commands.command(pass_context=True, name='osu')
    async def osu(self, ctx: discord.ext.commands.Context, *username):
        """
        Gets image from attachment and extracts text from it

        :param ctx: The context in which a command is called
        :type ctx: discord.ext.commands.Context
        """
        username = ' '.join(username)
        rank = self.osu.get_user(username, GameMode.STD).rank
        await ctx.reply("dfzvfgd: " + str(rank))


