import discord
from discord.ext import commands


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
                                       'Napisz `^help`, aby dowiedzieć się jakie mam komendy')
