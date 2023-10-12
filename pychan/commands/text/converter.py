import nextcord
import requests
from nextcord.ext import commands
import datetime

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(

        name="currency",
        category="Tekst"
    )

    async def currency(self, ctx: commands.Context):
        '''Funkcja pozwalajaca realizować różne działania na walutach'''
        pass

    @currency.command(
        pass_context=True,
        name='convert',
        aliases = ['change'],
        usage='<waluta1> <waluta2> <ilość> ',
        help="Funkcja przeliczająca wybrane waluty."
    )

    async def convert(self, ctx, currency1, currency2, amount):
        
        if currency1== 'PLN':
            value1 = 1
        else:
            embed = nextcord.Embed
            url = f'http://api.nbp.pl/api/exchangerates/rates/a/{currency1}'
            w1 = requests.get(url, verify=False)
            w1_res = w1.json()
            value1 = 1
            value1 = w1_res["rates"][0]['mid']
        if currency2 == 'PLN':
            value2 = 1
        else: 
            url = f'http://api.nbp.pl/api/exchangerates/rates/a/{currency2}'
            w2 = requests.get(url, verify=False)
            w2_res = w2.json()
            value2 = w2_res["rates"][0]['mid']
        div =  (value1/value2)
        result = div * float(amount)
        result  = round(result,2)
        embed = nextcord.Embed(title = f"Konwersja {currency1} -> {currency2}", description=f"{amount} {currency1} = {result} {currency2}  ", color = nextcord.Color.blue())
        await ctx.channel.send(embed=embed)

    @currency.command(
        pass_context=True,
        name='exchange',
        usage='<waluta>',
        aliases = ['rate'],
        help="Funkcja sprawdzająca kurs wybranej waluty w dniu dzisiejszym. "
    )
    
   
    async def exchange(self, ctx, c1):


        embed = nextcord.Embed
        url = f'http://api.nbp.pl/api/exchangerates/rates/a/{c1}/today/'
        rate = requests.get(url, verify=False)
        rate_res = rate.json()
        rate1 = rate_res["rates"][0]['mid']
        embed = nextcord.Embed(title = f"Kurs {c1} w dniu dzisiejszym", description=rate1, color = nextcord.Color.blue())
        await ctx.channel.send(embed=embed)

    
    
    @currency.command(
        pass_context=True,
        name='info',
        usage='',
        help='''Wyświetla dostepne waluty i ich oznaczenia'''
    )

    async def info(self,ctx):
        embed = nextcord.Embed(title = "Możliwe waluty do działania na nich:", description=
                              '''PLN: Polski złoty\nUSD: Dolar Amerykański\n EUR: Euro\n HUF: Forint
                                 CZK: Korona czeska\nGBP: Funt Brytyjski\nCHF: Frank Szwajcarski
                                 DKK: Korona Duńska\nNOK: Korona Norweska\nSEK: Korona Szwedzka
                                 CNY: Juan Chiński\nINR: Rupia Indyjska\nMXN: Peso Meksykańskie
                                 BGN: Lew Bułgarski\nRON: Lej Rumuński\nJPY: Jen Japoński     
                                 ''',                                         
                                color = nextcord.Color.blue())
        await ctx.channel.send(embed=embed)

