#!/usr/bin/env python3

import nextcord
from nextcord.ext import commands
from Core.core import Core
from Core.help import PyChanHelp
from config import discord_token
from Core.Commands.Settings.Functions.change_status import ChangeStatus
import Database

def main():
    """Main function where the bot instance is created
    Function 'get_server_prefix' is assigned 'command_prefix' and gets the prefix depending on the server on which the function is called
    """
    Database.create_database()

    intents = nextcord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(
        command_prefix=Database.get_guild_prefix, intents=intents,
        help_command=PyChanHelp()
    )
    
    bot.add_cog(Core(bot))

    @bot.event
    async def on_ready():
        """is called when Bot is ready"""
        change_status = ChangeStatus(bot)
        change_status.change_status.start()

        print("Bot is ready")

    bot.run(discord_token)


if __name__ == "__main__":
    main()
