import nextcord
import datetime
import requests
from nextcord.ext import commands

from Core.Decorators.decorators import Decorator

try:
    from config import riot_token_TFT
except ImportError:
    raise ImportError("Riot TFT token not found!")



class TfT(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


    @commands.group(
        name = "tft",
        category = "Gry"
    )

    async def tft(self, ctx: commands.Context):
        pass

    @tft.command(
        pass_context = True,
        name = 'konto',
        usage = '<nick>',
        help = """Funkcja do pokazywania informacji o przywoływaczu 
               """
    )


    @Decorator.pychan_decorator
    async def konto(self, ctx, name):
        headers = {"X-Riot-Token": riot_token_TFT}
        url = "https://eun1.api.riotgames.com/tft/summoner/v1/summoners/by-name/"
        data = requests.get(f"{url}{name}", headers=headers)
        data = data.json()



        urlRanks = "https://eun1.api.riotgames.com/tft/league/v1/entries/by-summoner/"
        dataRanks = requests.get(f'{urlRanks}{data["id"]}', headers=headers)
        dataRanks = dataRanks.json()

        dataRanks=dataRanks[0]
        
        rangaPlayer = ""

        rangaPlayer += ("RANKED_TFT : " 
                    + str(dataRanks["tier"])
                    + " "
                    + str(dataRanks["rank"])
                    + "\n"
                    + "leaguePoints : "
                    + str(dataRanks["leaguePoints"])
                    + "\n"
                    + "wins : "
                    + str(dataRanks["wins"])
                    + "\n"
                    + "losses : "
                    + str(dataRanks["losses"])
                    )





        embed = nextcord.Embed(title=f'{data["name"]}', color=nextcord.Color.dark_blue())
        embed.add_field(
            name="Poziom konta : ", value=f'{data["summonerLevel"]}', inline=False )

        embed.add_field(name="Ranga : ", value=f"{rangaPlayer}", inline=False)


        await ctx.send(embed=embed)

 