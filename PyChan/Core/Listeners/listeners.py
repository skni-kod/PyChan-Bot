from nextcord.ext import commands
from nextcord.message import Message

from Database.database import Database


class Listeners(commands.Cog):
    """Class contains Bot event methods"""

    def __init__(self, bot):
        """Constructor method"""
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        if message.content.lower() == "pychan!":
            await message.channel.send(
                "Wołałeś mnie?\n"
                f"Napisz `{Database.get_guild_prefix(self.bot, message)}help`, aby dowiedzieć się jakie mam komendy"
            )

