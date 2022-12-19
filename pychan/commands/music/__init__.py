from nextcord.ext import commands

from playingmusic import PlayingMusic


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(PlayingMusic(bot))
