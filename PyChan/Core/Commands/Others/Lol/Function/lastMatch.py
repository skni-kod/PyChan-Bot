from msilib.schema import Error
import discord
from discord.ext import commands


try:
    from Riot_token import token
except ImportError:
    raise ImportError('Riot token not found!')

import requests


class LastMatch(commands.Cog):

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    @commands.command(pass_context=True, name='lolmecze')
    async def lastMatch(self, ctx, name , numberMatch):
        headers = {"X-Riot-Token": token}

        url = 'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
        data = requests.get(f'{url}{name}', headers=headers)
        data = data.json()

        urlMatch = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"
        dataMatch = requests.get(f'{urlMatch}{data["puuid"]}{"/ids?start=0&count="}{str(numberMatch)}{"&"}',headers=headers)
        dataMatch=dataMatch.json()


        matchChampionInfoList=[]
        matchChampionStatsWhoWinList=[]

        urlStatsMatch = "https://europe.api.riotgames.com/lol/match/v5/matches/"
        for x in dataMatch:
            dataHelp=str(x)
            dataStatsMatchAll = requests.get(f'{urlStatsMatch}{dataHelp}',headers=headers)
            dataStatsMatchAll=dataStatsMatchAll.json()
            dataStats=dataStatsMatchAll["info"]

            matchChampionInfo=""
            matchChampionStatsWhoWin=""
            matchChampionInfo += "Tryp Gry : " + str(dataStats["gameMode"])
            matchChampionInfo += " Czas w unix : " + str(dataStats["gameStartTimestamp"])

            dataStatsMatchAllPlayer=dataStats["participants"]

            for a in dataStatsMatchAllPlayer:
                dataStatsMatch = a
                if str(dataStatsMatch["summonerName"]) == name:
                    if dataStatsMatch["win"]:
                        matchChampionInfo += "  Wygrana" + "\n"
                    else:
                        matchChampionInfo += "  Przegrana" + "\n"

                    matchChampionStatsWhoWin += str(dataStatsMatch["championName"])
                    matchChampionStatsWhoWin += "\t" + str(dataStatsMatch["kills"]) + " / " + str(dataStatsMatch["deaths"]) + " / " + str(dataStatsMatch["assists"])
                    matchChampionStatsWhoWin += "\t cs : " + str(dataStatsMatch["totalMinionsKilled"]+dataStatsMatch["neutralMinionsKilled"]) + "\t gold : " + str(dataStatsMatch["goldEarned"])
               
            matchChampionInfoList.append(matchChampionInfo)
            matchChampionStatsWhoWinList.append(matchChampionStatsWhoWin)


        embed = discord.Embed(title=f'{"Mecze Gracza : " + data["name"]}',
                              color=discord.Color.dark_orange())
        for x in range(0,len(matchChampionInfoList)):         
            embed.add_field(name=matchChampionInfoList[x],
                            value=f'{matchChampionStatsWhoWinList[x]}',
                            inline=False)
        await ctx.send(embed=embed)
