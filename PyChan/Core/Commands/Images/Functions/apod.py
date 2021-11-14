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

        embed = discord.Embed(title='Astronomy picture of the day',
                            description= data.json()['explanation'],
                            color=discord.Color.dark_purple())

        embed.set_image(url = data.json()['hdurl'])
        await ctx.send(embed = embed)