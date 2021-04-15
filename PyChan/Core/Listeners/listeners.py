import discord
from discord.ext import commands

from PyChan.Database.database import Database
from PyChan.Core.Commands.Settings.Functions.get_server_prefix import get_server_prefix


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # zdarzenia na wpisane słowa
    @commands.Cog.listener()
    async def on_message(self, message):
        # Kończy funkcje, jeśli wiadomość napisał bot
        if message.author.bot:
            return

        if str(message.content).lower() == 'pychan!':
            await message.channel.send('Wołałeś mnie Onii-chan?\n'
                                       f'Napisz `{get_server_prefix(self, message)}help`, aby dowiedzieć się jakie mam komendy')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        settings = {'prefix': '^'}
        Database.insert_one(Database.db_servers, {'_id': guild.id, 'settings': settings})
