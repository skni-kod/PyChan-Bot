import discord
from discord.ext import commands

from requests import get

class BoredAPI(commands.Cog):

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    @commands.command(pass_context=True, name='nudzesie')
    async def bored(self, ctx):

        url = "https://www.boredapi.com/api/activity/"  # from api to json
        response = get(url)
        dic = response.json()

        await ctx.send("Weź sobie " + dic["activity"])
