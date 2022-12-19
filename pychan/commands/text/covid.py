from nextcord.ext import commands
import requests


class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        name="covid",
        category="Tekst",
        usage=" ",
        help="""
               Liczba zachorowań na COVID-19 w Polsce z wczorajszego dnia.
               """
    )
    async def covid_zakazenia(self, ctx):

        url = "https://api.covid19api.com/live/country/poland/status/confirmed"
        response = requests.get(url, verify=False)
        api_data = response.json()

        liczba_zachorowan = api_data[::-1][0]['Confirmed'] - \
            api_data[::-1][1]['Confirmed']
        dzien = api_data[::-1][1]["Date"]
        dzien_zamiana = dzien.replace("T00:00:00Z", "")

        await ctx.channel.send("W dniu {} było {} zachorowań ".format(dzien_zamiana, liczba_zachorowan))
