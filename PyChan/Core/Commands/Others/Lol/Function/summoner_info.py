import discord
from discord.ext import commands

try:
    from riot_token import token
except ImportError:
    raise ImportError('Riot token not found!')

import requests


class SummonerInfo(commands.Cog):

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    @commands.command(pass_context=True, name='lolkonto')
    async def summoner_info(self, ctx, name):
        headers = {"X-Riot-Token": token}

        url = 'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
        data = requests.get(f'{url}{name}', headers=headers)

        data = data.json()

        embed = discord.Embed(title=f'{data["name"]}',
                              color=discord.Color.dark_purple())
        embed.add_field(name='ID',
                        value=f'`{data["id"]}`',
                        inline=False)
        embed.add_field(name='Poziom konta',
                        value=f'{data["summonerLevel"]}',
                        inline=False)

        await ctx.send(embed=embed)
