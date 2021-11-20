import discord
from discord.ext import commands
import requests

class Facts(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True, name='ciekawostka')
  async def fact(self, ctx):
    r = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
    r = r.json()
    await ctx.send(r['text'])