import discord
from discord.ext import commands, tasks
from itertools import cycle

class ChangeStatus(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    status = cycle([discord.Activity(type=discord.ActivityType.watching, name='^help'),
                    discord.Game('Snake')])

    @tasks.loop(seconds=10)
    async def change_status():
        await self.bot.change_presence(activity=next(status))
    
    change_status.start()