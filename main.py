import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='^')

# informacja o uruchomieniu się bota
@bot.event
async def on_ready():
    print('Bot is ready')

from token_key import token

bot.run(token)