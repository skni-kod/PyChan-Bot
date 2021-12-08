import json
import discord
from discord.embeds import Embed
from discord.ext import commands, tasks
from datetime import datetime
import requests
import datetime
from operator import itemgetter

SESION_ID = "53616c7465645f5f9cbbb1a00de4996a946bbe9bfc3dc7508ef03f4522d0298cc9b39de12d441612e9a79e3df9ac8771"


class AoC(commands.Cog):
    """Class contains QR generator method
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    @commands.command(pass_context=True, name='AoC')
    async def AoC(self, ctx, leaderb: int, div: int):

        tab_mess = []
        for x in range(int(div)):
            tab_mess.append(await ctx.send("-"))
        AoC_loop.start(tab_mess, leaderb)


@tasks.loop(minutes=15)
async def AoC_loop(tab_mess, lb_id):

    data = AoC_data(lb_id)
    extracted_data = extrac_data(data)
    embed_tab = embed_data(extracted_data)
    for i, x in enumerate(embed_tab):
        await tab_mess[i].edit(embed=x)


def get_delta_time() -> str:
    dt = datetime.datetime.now()
    output = ((24 - dt.hour - 1) * 60 * 60) + \
        ((60 - dt.minute - 1) * 60) + (60 - dt.second) + 18000 + 3600
    return str(datetime.timedelta(seconds=output))


def AoC_data(lb_id) -> json:
    leaderboard_id = int(lb_id)
    api_url = "https://adventofcode.com/{}/leaderboard/private/view/{}".format(
        datetime.datetime.today().year,
        leaderboard_id)
    r = requests.get(
        "{}.json".format(api_url),
        cookies={"session": SESION_ID})
    return r.json()


def extrac_data(data) -> list[str]:
    tab = []
    for key in data['members'].keys():
        tab.append([data['members'][key]['name'],
                   int(data['members'][key]['stars']),
                   data['members'][key]['completion_day_level'],
                   int(data['members'][key]['local_score'])])
    tab = sorted(tab, key=itemgetter(3), reverse=True)
    return tab


def embed_data(extracted_data) -> list[Embed]:
    counter = 0
    counter_2 = 0
    embed_tab = []
    embed_tab.append(discord.Embed(title=f"Advent of Code\nCzas do następnego zadania: {get_delta_time()}\n",
                                   color=discord.Color.dark_purple()))
    for i, l in enumerate(extracted_data):
        days = str(list(l[2].keys())).replace(
            '[', '').replace(']', '').replace("'", '')
        days_sorted = days.split(',')
        days_sorted = [int(num) for num in days_sorted]
        days_sorted.sort(reverse=True)
        if l[1]:
            if counter < 9:
                embed_tab[counter_2].add_field(name=l[0],
                                               value=f"```<Punkty>: {l[3]}\n<Gwiazdki>: {l[1]}\n<Ukończone dni> {str(days_sorted).replace(']','').replace('[','')}```", inline=False)
                counter += 1
            else:
                embed_tab.append(discord.Embed(title=f"Advent of Code\nCzas do następnego zadania: {get_delta_time()}",
                                               color=discord.Color.dark_purple()))
                embed_tab[counter_2].add_field(name=l[0],
                                               value=f"```<Punkty>: {l[3]}\n<Gwiazdki>: {l[1]}\n<Ukończone dni> {days}```", inline=False)
                counter = 0
                counter_2 += 1
    return embed_tab
