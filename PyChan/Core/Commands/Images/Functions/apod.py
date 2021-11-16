import requests
import discord
from discord.ext import commands
from apod_token import apod_token

class ApodImage(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='apod')
    async def apod(self, ctx):
        data = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={apod_token}")
        imgurl = data.json()['hdurl']

        embed = discord.Embed(title='Astronomy picture of the day',
                            description= data.json()['explanation'],
                            color=discord.Color.dark_purple())

        if("youtube.com" in imgurl):
            await ctx.send(imgurl)
        else:
            embed.set_image(url = imgurl)

        await ctx.send(embed = embed)



        