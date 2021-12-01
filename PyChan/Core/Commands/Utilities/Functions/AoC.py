import discord
from discord.ext import commands, tasks
from datetime import datetime
import requests
import datetime
from operator import itemgetter


SESION_ID = "53616c7465645f5f9cbbb1a00de4996a946bbe9bfc3dc7508ef03f4522d0298cc9b39de12d441612e9a79e3df9ac8771"


def get_delta_time():
    dt = datetime.datetime.now()
    output = ((24 - dt.hour - 1) * 60 * 60) + \
        ((60 - dt.minute - 1) * 60) + (60 - dt.second) + 18000 + 3600
    return str(datetime.timedelta(seconds=output))


@tasks.loop(seconds=5)
async def AoC_loop(message, arg):
    embed = discord.Embed(title=f"Advent of Code\nCzas do następnego zadania: {get_delta_time()}",
                          color=discord.Color.dark_purple())
    leaderboard_id = int(arg)
    api_url = "https://adventofcode.com/{}/leaderboard/private/view/{}".format(
        datetime.datetime.today().year,
        leaderboard_id)
    r = requests.get(
        "{}.json".format(api_url),
        cookies={"session": SESION_ID})
    data = r.json()
    tab = []
    for key in data['members'].keys():
        tab.append([data['members'][key]['name'],
                   int(data['members'][key]['stars']),
                   data['members'][key]['completion_day_level']])
    tab = sorted(tab, key=itemgetter(1), reverse=True)
    for l in tab:
        days = str(list(l[2].keys())).replace(
            '[', '').replace(']', '').replace("'", '')
        if l[1]:
            embed.add_field(name=l[0],
                            value=f"```<Gwiazdki>: {l[1]}\n<Ukończone dni> {days}```", inline=False)
    await message.edit(embed=embed)


class AoC(commands.Cog):
    """Class contains QR generator method
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    @ commands.command(pass_context=True, name='AoC')
    async def AoC(self, ctx, arg):

        message = await ctx.send("-")
        AoC_loop.start(message, arg)
