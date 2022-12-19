import nextcord
from nextcord.ext import commands

from Core.Commands.Images.Functions.ocr import OCR
from Core.Commands.Images.Functions.qr_generator import QR
from Core.Commands.Images.Functions.apod import ApodImage
from Core.Commands.Images.Functions.waifu2x import Waifu2x
from Core.Commands.Images.Functions.ASCII import ASCII


class Images(commands.Cog):
    """Class contains images methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        self.bot.add_cog(OCR(bot))
        self.bot.add_cog(QR(bot))
        self.bot.add_cog(ApodImage(bot))
        self.bot.add_cog(Waifu2x(bot))
        self.bot.add_cog(ASCII(bot))
