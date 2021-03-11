import discord
from discord.ext import commands

from CommandsCogs.commands_cog import Commands
from CommandsCogs.help_cog import Help
from CommandsCogs.maths_cog import Maths

# utworzenie instancji bota
bot = commands.Bot(command_prefix='^')

# usunięcie domyślnej komendy 'help'
bot.remove_command('help')

# dodanie funkcji z innych plikówa
bot.add_cog(Commands(bot))
bot.add_cog(Help(bot))
bot.add_cog(Maths(bot))


# informacja o uruchomieniu się bota
@bot.event
async def on_ready():
    print('Bot is ready')


from token_key import token

bot.run(token)
