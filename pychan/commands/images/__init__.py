from nextcord.ext import commands

from ocr import OCR
from qr_generator import QR
from apod import ApodImage
from waifu2x import Waifu2x
from ascii import ASCII


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(OCR(bot))
        self.bot.add_cog(QR(bot))
        self.bot.add_cog(ApodImage(bot))
        self.bot.add_cog(Waifu2x(bot))
        self.bot.add_cog(ASCII(bot))
