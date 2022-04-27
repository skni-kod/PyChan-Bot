import requests
import discord
from discord.ext import commands
from config import apod_token

class ApodImage(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot
    """
    Sends a request to NASA's Astronomy picture of the day via API
    and gets an image (or video) along with a description
    """

    @commands.command(pass_context=True, name='apod', category='Obraz')
    async def apod(self, ctx):
        data = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={apod_token}")
        imgurl = data.json()['hdurl']

        embed = discord.Embed(title='Astronomy picture of the day',
                            description= data.json()['explanation'],
                            color=discord.Color.dark_purple())

        """
        If it gets an image, it is embedded with the description
        If it's a video, it's sent separately from description
        """

        if("youtube.com" in imgurl):
            await ctx.send(imgurl)
        else:
            embed.set_image(url = imgurl)

        await ctx.send(embed = embed)
