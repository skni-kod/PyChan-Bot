import nextcord
from nextcord.ext import commands
from Core.Decorators.decorators import Decorator

try:
    from config import riot_token
except ImportError:
    raise ImportError("Riot token not found!")

import requests


class SummonerInfo(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    @commands.command(
        pass_context=True,
        name="lolkonto",
        category="League of Legends",
        help_={
            "title": "lolkonto",
            "description": "Funkcja do pokazywania informacji o przywoływaczu.",
            "fields": [
                {
                    "name": "sposób użycia",
                    "value": "lolkonto `[nazwa Gracza]` ",
                }
            ],
        },
    )
    @Decorator.pychan_decorator
    async def summoner_info(self, ctx, name):
        headers = {"X-Riot-Token": riot_token}

        url = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
        data = requests.get(f"{url}{name}", headers=headers)
        data = data.json()

        urlRanks = "https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/"
        dataRanks = requests.get(f'{urlRanks}{data["id"]}', headers=headers)
        dataRanks = dataRanks.json()

        rangaPlayer = ""
        for x in range(0, len(dataRanks)):
            dataHelp = dict(dataRanks[x])
            if str(dataHelp["queueType"]) == "RANKED_SOLO_5x5":
                rangaPlayer += (
                    "Ranga Solo/Duo"
                    + " : "
                    + str(dataHelp["tier"])
                    + " "
                    + str(dataHelp["rank"])
                    + "\n"
                )
            if str(dataHelp["queueType"]) == "RANKED_FLEX_SR":
                rangaPlayer += (
                    "Ranga Flex"
                    + " : "
                    + str(dataHelp["tier"])
                    + " "
                    + str(dataHelp["rank"])
                    + "\n"
                )

        urlChampionMastery = "https://eun1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"
        dataChampionMastery = requests.get(
            f'{urlChampionMastery}{data["id"]}', headers=headers
        )
        dataChampionMastery = dataChampionMastery.json()

        nameChampion = {
            "266": " Aatrox",
            "103": " Ahri",
            "84": " Akali",
            "166": " Akshan",
            "12": " Alistar",
            "32": " Amumu",
            "34": " Anivia",
            "1": " Annie",
            "523": " Aphelios",
            "22": " Ashe",
            "136": " Aurelion Sol",
            "268": " Azir",
            "432": " Bard",
            "53": " Blitzcrank",
            "63": " Brand",
            "201": " Braum",
            "51": " Caitlyn",
            "164": " Camille",
            "69": " Cassiopeia",
            "31": " Cho'Gath",
            "42": " Corki",
            "122": " Darius",
            "131": " Diana",
            "119": " Draven",
            "36": " Dr. Mundo",
            "245": " Ekko",
            "60": " Elise",
            "28": " Evelynn",
            "81": " Ezreal",
            "9": " Fiddlesticks",
            "114": " Fiora",
            "105": " Fizz",
            "3": " Galio",
            "41": " Gangplank",
            "86": " Garen",
            "150": " Gnar",
            "79": " Gragas",
            "104": " Graves",
            "887": " Gwen",
            "120": " Hecarim",
            "74": " Heimerdinger",
            "420": " Illaoi",
            "39": " Irelia",
            "427": " Ivern",
            "40": " Janna",
            "59": " Jarvan IV",
            "24": " Jax",
            "126": " Jayce",
            "202": " Jhin",
            "222": " Jinx",
            "145": " Kai'Sa",
            "429": " Kalista",
            "43": " Karma",
            "30": " Karthus",
            "38": " Kassadin",
            "55": " Katarina",
            "10": " Kayle",
            "141": " Kayn",
            "85": " Kennen",
            "121": " Kha'Zix",
            "203": " Kindred",
            "240": " Kled",
            "96": " Kog'Maw",
            "7": " LeBlanc",
            "64": " Lee Sin",
            "89": " Leona",
            "876": " Lillia",
            "127": " Lissandra",
            "236": " Lucian",
            "117": " Lulu",
            "99": " Lux",
            "54": " Malphite",
            "90": " Malzahar",
            "57": " Maokai",
            "11": " Master Yi",
            "21": " Miss Fortune",
            "62": " Wukong",
            "82": " Mordekaiser",
            "25": " Morgana",
            "267": " Nami",
            "75": " Nasus",
            "111": " Nautilus",
            "518": " Neeko",
            "76": " Nidalee",
            "56": " Nocturne",
            "20": " Nunu & Willump",
            "2": " Olaf",
            "61": " Orianna",
            "516": " Ornn",
            "80": " Pantheon",
            "78": " Poppy",
            "555": " Pyke",
            "246": " Qiyana",
            "133": " Quinn",
            "497": " Rakan",
            "33": " Rammus",
            "421": " Rek'Sai",
            "526": " Rell",
            "888": " Renata Glasc",
            "58": " Renekton",
            "107": " Rengar",
            "92": " Riven",
            "68": " Rumble",
            "13": " Ryze",
            "360": " Samira",
            "113": " Sejuani",
            "235": " Senna",
            "147": " Seraphine",
            "875": " Sett",
            "35": " Shaco",
            "98": " Shen",
            "102": " Shyvana",
            "27": " Singed",
            "14": " Sion",
            "15": " Sivir",
            "72": " Skarner",
            "37": " Sona",
            "16": " Soraka",
            "50": " Swain",
            "517": " Sylas",
            "134": " Syndra",
            "223": " Tahm Kench",
            "163": " Taliyah",
            "91": " Talon",
            "44": " Taric",
            "17": " Teemo",
            "412": " Thresh",
            "18": " Tristana",
            "48": " Trundle",
            "23": " Tryndamere",
            "4": " Twisted Fate",
            "29": " Twitch",
            "77": " Udyr",
            "6": " Urgot",
            "110": " Varus",
            "67": " Vayne",
            "45": " Veigar",
            "161": " Vel'Koz",
            "711": " Vex",
            "254": " Vi",
            "234": " Viego",
            "112": " Viktor",
            "8": " Vladimir",
            "106": " Volibear",
            "19": " Warwick",
            "498": " Xayah",
            "101": " Xerath",
            "5": " Xin Zhao",
            "157": " Yasuo",
            "777": " Yone",
            "83": " Yorick",
            "350": " Yuumi",
            "154": " Zac",
            "238": " Zed",
            "221": " Zeri",
            "115": " Ziggs",
            "26": " Zilean",
            "142": " Zoe",
            "143": " Zyra",
        }
        championMastery = ""
        for x in range(0, 3):
            dataHelp = dict(dataChampionMastery[x])
            championMastery += (
                str(x + 1) + " : " + nameChampion[str(dataHelp["championId"])]
            )
            championMastery += (
                "\nLVL Mastery : "
                + str(dataHelp["championLevel"])
                + "\nPunkty Masteri : "
                + str(dataHelp["championPoints"])
                + "\n\n"
            )

        embed = nextcord.Embed(title=f'{data["name"]}', color=nextcord.Color.dark_blue())
        embed.add_field(
            name="Poziom konta : ", value=f'{data["summonerLevel"]}', inline=False
        )
        embed.add_field(name="Ranga : ", value=f"{rangaPlayer}", inline=False)
        embed.add_field(
            name="Champion top 3 Mastery : ", value=f"{championMastery}", inline=False
        )
        await ctx.send(embed=embed)
