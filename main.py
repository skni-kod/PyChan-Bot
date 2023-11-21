#!/usr/bin/env python3

import nextcord
from nextcord.ext import commands
from config import discord_token
from pychan.commands.text.reddit import Reddit
from pychan import database, status
from pychan.core import Core
from pychan.help import PyChanHelp


def main():
    database.create_database()

    intents = nextcord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(
        command_prefix=database.get_guild_prefix, intents=intents,
        help_command=PyChanHelp()
    )

    bot.add_cog(Core(bot))

    @bot.event
    async def on_ready():
        change_status = status.ChangeStatus(bot)
        change_status.change_status.start()

        print("Bot is ready")

    bot.run(discord_token)

def cleanup():
    database.close_database()
    Reddit.reddit.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
