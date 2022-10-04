import nextcord
from nextcord.ext import commands, tasks
from itertools import cycle

class ChangeStatus(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.status = cycle([nextcord.Activity(type=nextcord.ActivityType.watching, name='^help and eaten snake'),
                        nextcord.Game('Snake in Snake')])

  @tasks.loop(minutes=30)
  async def change_status(self):
      game = nextcord.Game("with the API")
      await self.bot.change_presence(activity=next(self.status))


