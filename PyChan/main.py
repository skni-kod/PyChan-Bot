import discord
from discord.ext import commands

from Core.core import Core
from token_key import token

from Core.Commands.Settings.Functions.get_server_prefix import GetServerPrefix
from Database.database import Database


def main():
    """Main function where the bot instance is created
    Default command 'help' is removed and is added cog file 'Core'
    Function 'get_server_prefix' is assigned 'command_prefix' and gets the prefix depending on the server on which the function is called
    """
    intents = discord.Intents(
        messages=True, guilds=True, members=True, reactions=True)
    bot = commands.Bot(
        command_prefix=GetServerPrefix.get_server_prefix, intents=intents)
    bot.remove_command('help')
    bot.add_cog(Core(bot))

    @bot.event
    async def on_ready():
        """is called when Bot is ready
        """
        Database.create_database()
        Database.update_database(bot)

        print('Bot is ready')

    bot.run(token)


if __name__ == '__main__':
    main()
