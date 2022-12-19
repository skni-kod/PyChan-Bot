from nextcord.ext import commands

from Core.Commands.Music.Functions.playingmusic import PlayingMusic


class Music(commands.Cog):
    """Class contains music methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(PlayingMusic(bot))
