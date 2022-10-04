import nextcord
from nextcord.ext import commands

from Core.core import Core
from config import nextcord_token

from Core.Commands.Settings.Functions.get_server_prefix import GetServerPrefix
from Core.Commands.Settings.Functions.change_status import ChangeStatus
from Database.database import Database


def main():
    """Main function where the bot instance is created
    Default command 'help' is removed and is added cog file 'Core'
    Function 'get_server_prefix' is assigned 'command_prefix' and gets the prefix depending on the server on which the function is called
    """
    intents = nextcord.Intents.default()
    intents.message_content = True


    bot = commands.Bot(
        command_prefix=GetServerPrefix.get_server_prefix, intents=intents
    )
    
    bot.remove_command("help")
    bot.add_cog(Core(bot))

    @bot.event
    async def on_ready():
        """is called when Bot is ready"""
        Database.create_database()
        Database.update_database(bot)
        change_status = ChangeStatus(bot)
        change_status.change_status.start()

        print("Bot is ready")

    bot.run(nextcord_token)


if __name__ == "__main__":
    main()
