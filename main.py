import discord
from discord.ext import commands

from commands import Commands
from help import Help
from maths import Maths

# utworzenie instancji bota
bot = commands.Bot(command_prefix='^')

# usunięcie domyślnej komendy 'help'
bot.remove_command('help')

# dodanie funkcji z innych plików
bot.add_cog(Commands(bot))
bot.add_cog(Help(bot))
bot.add_cog(Maths(bot))


# informacja o uruchomieniu się bota
@bot.event
async def on_ready():
    print('Bot is ready')


from token_key import token

bot.run(token)
