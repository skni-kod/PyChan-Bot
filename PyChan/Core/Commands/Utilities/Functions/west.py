import requests
import discord
from discord.ext import commands

class KanyeWestQuete(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='KanyeQuote')
    async def kanyeQuote(self, ctx):
        data = requests.get('https://api.kanye.rest/')
        quote = data.json()['quote']

        embed = discord.Embed(title='Kanye West Quote',
                            description=quote,
                            color=discord.Color.dark_purple())
        await ctx.send(embed = embed)