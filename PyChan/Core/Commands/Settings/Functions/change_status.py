import discord
from discord.ext import commands, tasks
from itertools import cycle

class ChangeStatus(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.status = cycle([discord.Activity(type=discord.ActivityType.watching, name='^help'),
                        discord.Game('Snake')]) 
    
  @tasks.loop(minutes=30)
  async def change_status(self):
      game = discord.Game("with the API")
      await self.bot.change_presence(activity=next(self.status))

    
    