import discord
from discord.ext import commands

from Database.database import Database
from Core.Commands.Settings.Functions.get_server_prefix import GetServerPrefix


class Listeners(commands.Cog):
    """Class contains Bot event methods"""

    def __init__(self, bot):
        """Constructor method"""
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Function is called when messege is sent

        :param message: contains information about message
        :type message: discord.Message
        """

        if message.author.bot:
            return

        if str(message.content).lower() == "pychan!":
            await message.channel.send(
                "Wołałeś mnie?\n"
                f"Napisz `{GetServerPrefix.get_server_prefix(self, message)}help`, aby dowiedzieć się jakie mam komendy"
            )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Function is called when Bot joins to server

        :param guild: contains information about server
        :type guild: discord.Guild
        """

        Database.add_guild(guild.id)
        for member in guild.members:
            Database.add_member(member.guild_id, guild.id)

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        Database.add_member(member.guild_id, ctx.guild.guild_id)
