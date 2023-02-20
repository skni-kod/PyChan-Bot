import nextcord
from nextcord.ext import commands
import requests
import json
from config import waifu2x_token


def send_waifu2x_request(url):
    """
    Functions sends request to Waifu2x API
    :param url: URL to png/jpg file
    :type url: string

    :return: Returns JSON response
    :rtype: string
    """
    r = requests.post(
        "https://api.deepai.org/api/waifu2x",
        data={'image': url, },
        headers={'api-key': waifu2x_token}
    )
    return r.content.decode()


class Waifu2x(commands.Cog):
    """
    Class containing Waifu2x method
    """

    def __init__(self, bot):
        """
        Constructor
        """
        self.bot = bot

    @commands.command(
        pass_context=True,
        name='waifu2x',
        category='Media',
        usage="<link do obrazu w formacie .png lub .jpg>",
        help="""
               Przeskalowuje podany obraz w formacie .png lub .jpg
               używając funkcji waifu2x aplikacji deepai.org
               """
    )
    async def waifu2x(self, ctx):
        """
        Gets image from attachement and upscales it

        :param ctx: The context in which a command is called
        :type ctx: nextcord.ext.commands.Context
        """
        if len(ctx.message.attachments) != 0:
            if ctx.message.attachments[0].filename.lower().endswith((".png", ".jpg")):
                output = json.loads(send_waifu2x_request(
                    ctx.message.attachments[0].url))
                await ctx.send(output["output_url"])
            else:
                await ctx.send("Błędny format pliku")
        else:
            await ctx.send("Brak załącznika")
