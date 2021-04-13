import discord
from discord.ext import commands

from Core.core import Core
from token_key import token


def main():
    # utworzenie instancji bota
    bot = commands.Bot(command_prefix='^')

    # usunięcie domyślnej komendy 'help'
    bot.remove_command('help')

    # dodanie funkcji z innych plikówa
    bot.add_cog(Core(bot))

    # informacja o uruchomieniu się bota
    @bot.event
    async def on_ready():
        print('Bot is ready')

    bot.run(token)


if __name__ == '__main__':
    main()
