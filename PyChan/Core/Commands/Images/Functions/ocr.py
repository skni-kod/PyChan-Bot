import discord
from discord.ext import commands
import requests
import json
from config import ocr_token
import os


def send_ocr_request(url):
    """
    Function that sends request to OCR Space via API
    :param url: URL to png/jpg file
    :type url: string

    :return: Returns JSON response
    :rtype: string
    """
    data = {'url': url, 'isOverlayRequired': False, 'apikey': ocr_token, 'language': 'pol'}
    r = requests.post('https://api.ocr.space/parse/image', data=data, timeout=10)
    return r.content.decode()


class OCR(commands.Cog):
    """
    Class contains ocr methods
    """

    def __init__(self, bot):
        """
        Constructor method
        """
        self.bot = bot

    @commands.command(pass_context=True, name='ocr', category='Obraz')
    async def ocr(self, ctx):
        """
        Gets image from attachment and extracts text from it

        :param ctx: The context in which a command is called
        :type ctx: discord.ext.commands.Context
        """
        if len(ctx.message.attachments) != 0:
            if ctx.message.attachments[0].filename.lower().endswith((".png", ".jpg")):
                try:
                    output = json.loads(send_ocr_request(ctx.message.attachments[0].url))
                    if output["OCRExitCode"] == 1 and output["IsErroredOnProcessing"] is False:
                        if len(output['ParsedResults'][0]['ParsedText'])>2000:
                            with open('ocr.txt', 'w', encoding="UTF-8") as file:
                                file.write(output['ParsedResults'][0]['ParsedText'])

                            file = discord.File("ocr.txt")
                            await ctx.send(file=file)
                            os.remove("ocr.txt")
                        else:
                            await ctx.send(f"```{output['ParsedResults'][0]['ParsedText']}```")
                    else:
                        await ctx.send("Wystąpił błąd. Spróbuj ponownie za chwilę.")
                except Exception as e:
                    print(e)
                    await ctx.send("Wystąpił błąd. Spróbuj ponownie za chwilę.")
            else:
                await ctx.send("Wymagany format pliku to: .png lub .jpg")
        else:
            await ctx.send("Brak załacznika w wiadomości.")
