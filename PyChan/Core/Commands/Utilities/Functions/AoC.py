import discord
from discord.ext import commands, tasks
from datetime import datetime
import requests
import datetime
from operator import itemgetter


SESION_ID = "53616c7465645f5f9cbbb1a00de4996a946bbe9bfc3dc7508ef03f4522d0298cc9b39de12d441612e9a79e3df9ac8771"


@tasks.loop(minutes=15)
async def AoC_loop(message, arg):
    leaderboard_id = int(arg)
    api_url = "https://adventofcode.com/{}/leaderboard/private/view/{}".format(
        datetime.datetime.today().year - 1,
        leaderboard_id)
    r = requests.get(
        "{}.json".format(api_url),
        cookies={"session": SESION_ID})
    tab = []
    for key in r.json()['members'].keys():
        tab.append([r.json()['members'][key]['name'],
                   int(r.json()['members'][key]['stars'])])
    tab = sorted(tab, key=itemgetter(1), reverse=True)
    data = ''
    for l in tab:
        data += (f'{l[0]} <Gwiazdki>:{l[1]}\n')
    await message.edit(content=data)


class AoC(commands.Cog):
    """Class contains QR generator method
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    @ commands.command(pass_context=True, name='AoC')
    async def AoC(self, ctx, arg):

        message = await ctx.send("Starting...")
        AoC_loop.start(message, arg)
