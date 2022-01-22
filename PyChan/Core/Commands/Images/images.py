import discord
from discord.ext import commands

from Core.Commands.Images.Functions.ocr import OCR
from Core.Commands.Images.Functions.apod import ApodImage


class Images(commands.Cog):
    """Class contains images methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(OCR(bot))
        self.bot.add_cog(ApodImage(bot))
