import datetime
import discord
from discord.ext import commands, tasks
from discord.utils import get

SKNIKOD_ID = 381092165729910786

category_ids = [
    974250414910345286,  # sekcja game-dev
    435872812373114880,  # sekcja aplikacji webowych
    974250580862205952,  # sekcja elektroniki i retro
]


class InactiveProjects(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="inactive_projects")
    async def check_inactive_projects(self, ctx):
        ### skni_kod https://discordpy.readthedocs.io/en/stable/api.html?highlight=get_guild#guild
        skni_kod = self.bot.get_guild(SKNIKOD_ID)
        for category_id in category_ids:
            ### category https://discordpy.readthedocs.io/en/stable/api.html?highlight=get_guild#categorychannel
            category = get(skni_kod.categories, id=category_id)
            ### channel https://discordpy.readthedocs.io/en/stable/api.html?highlight=get_guild#textchannel
            for channel in category.text_channels:
                if "projekt" in channel.name:
                    ### message https://discordpy.readthedocs.io/en/latest/api.html#discord.Message
                    message = await channel.fetch_message(channel.last_message_id)
                    ### time_delta https://docs.python.org/3/library/datetime.html#datetime.timedelta
                    time_delta = datetime.datetime.now() - message.created_at

                    if time_delta.days >= 1:
                        await ctx.send(
                            f"{channel.name} is inactive for {time_delta.days} days"
                        )
