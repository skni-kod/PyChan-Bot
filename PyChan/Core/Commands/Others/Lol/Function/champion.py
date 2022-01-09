import discord
from discord.ext import commands

from riotwatcher import LolWatcher, ApiError

try:
    from Riot_token import token
except ImportError:
    raise ImportError('Riot token not found!')

import requests


class Champion(commands.Cog):

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    @commands.command(pass_context=True, name='champion')
    async def summoner_info(self, ctx, name):


        my_region = 'eun1'
        lol_watcher = LolWatcher(token)
        me = lol_watcher.summoner.by_name(my_region, name)


        versions = lol_watcher.data_dragon.versions_for_region(my_region)
        champions_version = versions['n']['champion']

        current_champ_list = lol_watcher.data_dragon.champions(champions_version, name)

        await ctx.send(current_champ_list)

        embed = discord.Embed(title=f'{"Champion List"}',
                              color=discord.Color.dark_blue())
        embed.add_field(name='Champion',
                        value=f'`{champions_version}`',
                        inline=False)
        embed.add_field(name='Champion',
                        value=f'`{current_champ_list}`',
                        inline=False)



        await ctx.send(embed=embed)

        try:
            response = lol_watcher.summoner.by_name(my_region, 'this_is_probably_not_anyones_summoner_name')
        except ApiError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
                print('this retry-after is handled by default by the RiotWatcher library')
                print('future requests wait until the retry-after time passes')
            elif err.response.status_code == 404:
                 print('Summoner with that ridiculous name not found.')
            else:
                raise