import requests
import nextcord
from nextcord.ext import commands

class KanyeWestQuote(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True, 
        name='kanyequote',
        aliases=['kanye', 'kanyequote', 'west'],
        usage = " ",
        help = """
               Wysyła losowy cytat Kanye Westa
               """
    )
    async def kanyeQuote(self, ctx):
        data = requests.get('https://api.kanye.rest/')
        quote = data.json()['quote']

        embed = nextcord.Embed(title='Kanye West Quote',
                            description=quote,
                            color=nextcord.Color.dark_purple())
        await ctx.send(embed = embed)