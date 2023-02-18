import nextcord
from nextcord.ext import commands
import requests
import json

weather_codes = {
    '0': 'Nie występują żadne znaczące zjawiska pogodowe',
    '1': 'Chmury na ogół zanikają lub stają się cieńsze (podczas ostatniej godziny)',
    '2': 'Stan nieba na ogól bez zmian (podczas ostatniej godziny)',
    '3': 'Chmury w stadium tworzenia się lub rozwoju (podczas ostatniej godziny)',
    '4': 'Dym, zmętnienie lub pył w powietrzu, widzialność równa lub większa od 1 km',
    '5': 'Dym, zmętnienie lub pył w powietrzu, widzialność mniejsza niż 1 km',
    '10': 'Zamglenie',
    '11': 'Pył diamentowy',
    '12': 'Błyskawica odległa',
    '18': 'Nawałnica',
    '20': 'Mgła, w miejscu obserwacji w ciągu ostatniej godziny, lecz nie w czasie dokonywania obserwacji',
    '21': 'Opad, w miejscu obserwacji w ciągu ostatniej godziny, lecz nie w czasie dokonywania obserwacji',
    '22': 'Mżawka lub Śnieg ziarnisty, w miejscu obserwacji w ciągu ostatniej godziny, lecz nie w czasie dokonywania obserwacji',
    '23': 'Deszcz (niemarznący), w miejscu obserwacji w ciągu ostatniej godziny, lecz nie w czasie dokonywania obserwacji',
    '24': 'Śnieg, w miejscu obserwacji w ciągu ostatniej godziny, lecz nie w czasie dokonywania obserwacji',
    '25': 'Marznący Deszcz lub Mżawka, w miejscu obserwacji w ciągu ostatniej godziny, lecz nie w czasie dokonywania obserwacji',
    '26': 'Burza (z lub bez Opadu), w miejscu obserwacji w ciągu ostatniej godziny, lecz nie w czasie dokonywania obserwacji',
    '27': 'Niska zamieć śnieżna lub wichura piaskowa',
    '28': 'Niska zamieć śnieżna lub wichura piaskowa, widzialność 1 km lub więcej',
    '29': 'Niska zamieć śnieżna lub wichura piaskowa, widzialność poniżej 1 km',
    '30': 'Mgła',
    '31': 'Mgła lub Mgła lodowa w płatach',
    '32': 'Mgła lub Mgła lodowa, rzedniejąca w ciągu ostatniej godziny',
    '33': 'Mgła lub Mgła lodowa, bez dostrzegalnych zmian w ciągu ostatniej godziny',
    '34': 'Mgła lub Mgła lodowa, gęstniejąca w ciągu ostatniej godziny',
    '35': 'Mgła osadzająca szadź',
    '40': 'Opad',
    '41': 'Opad, słaby lub umiarkowany',
    '42': 'Opad, silny',
    '43': 'Opad ciekły, słaby lub umiarkowany',
    '44': 'Opad ciekły, silny',
    '45': 'Opad w postaci stałej, słaby lub umiarkowany',
    '46': 'Opad w postaci stałej, silny',
    '47': 'Opad marznący, słaby lub umiarkowany',
    '48': 'Opad marznący, silny',
    '50': 'Mżawka',
    '51': 'Mżawka nie marznąca, słaba',
    '52': 'Mżawka nie marznąca, umiarkowana',
    '53': 'Mżawka nie marznąca, silna',
    '54': 'Mżawka marznąca, słaba',
    '55': 'Mżawka marznąca, umiarkowana',
    '56': 'Mżawka marznąca, silna',
    '57': 'Mżawka z Deszczem, słaba',
    '58': 'Mżawka z Deszczem, umiarkowana lub silna',
    '60': 'Deszcz',
    '61': 'Deszcz nie marznący, słaby',
    '62': 'Deszcz nie marznący, umiarkowany',
    '63': 'Deszcz nie marznący, silny',
    '64': 'Deszcz marznący, słaby',
    '65': 'Deszcz marznący, umiarkowany',
    '66': 'Deszcz marznący, silny',
    '67': 'Deszcz (lub Mżawka) ze Śniegiem, słaby',
    '68': 'Deszcz (lub Mżawka) ze Śniegiem, umiarkowany lub silny',
    '70': 'Śnieg',
    '71': 'Śnieg, słaby',
    '72': 'Śnieg, umiarkowany',
    '73': 'Śnieg silny',
    '74': 'Ziarna lodowe, słabe',
    '75': 'Ziarna lodowe, umiarkowane',
    '76': 'Ziarna lodowe, silne',
    '77': 'Śnieg ziarnisty',
    '78': 'Kryształki lodowe',
    '80': 'Przelotny Deszcz lub Deszcz z przerwami',
    '81': 'Przelotny Deszcz lub Deszcz z przerwami, słaby',
    '82': 'Przelotny Deszcz lub Deszcz z przerwami, umiarkowany',
    '83': 'Przelotny Deszcz lub Deszcz z przerwami, silny',
    '84': 'Przelotny Deszcz lub Deszcz z przerwami, gwałtowny',
    '85': 'Przelotny Śnieg lub Śnieg z przerwami, słaby',
    '86': 'Przelotny Śnieg lub Śnieg z przerwami, umiarkowany',
    '87': 'Przelotny Śnieg lub Śnieg z przerwami, silny',
    '89': 'Grad',
    '90': 'Burza',
    '91': 'Burza słaba lub umiarkowana, bez Opadu',
    '92': 'Burza słaba lub umiarkowana, z Przelotnym Deszczem lub Śniegiem',
    '93': 'Burza słaba lub umiarkowana, z Gradem',
    '94': 'Burza silna, bez Opadu',
    '95': 'Burza silna, z Przelotnym Deszczem i/lub Śniegiem',
    '96': 'Burza silna, z Gradem',
    '99': 'Trąba (tornado)',
}


def get_location(location):
    url = "https://nominatim.openstreetmap.org/search?q=" + location + '&format=jsonv2&limit=1'
    r = requests.get(url)
    r = r.json()
    
    if r:
        r = r[0]
    else:
        return 0

    data = {
        'name': r['display_name'],
        'latitude': r['lat'],
        'longitude': r['lon']
    }

    return data


def send_weather_request(location):
    lat = location['latitude']
    lot = location['longitude']

    url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lot + '&hourly=rain&current_weather=true'      
    r = requests.get(url)
    weather = r.json()
    weather = weather['current_weather']

    return weather


def prepare_weather(location, weather):

    wind_degree = float(weather['winddirection'])
    wind_direction = 'Północny'
    if wind_degree >= 337.5 and wind_degree < 22.5:
        wind_direction = 'Północny'
    elif wind_degree >= 22.5 and wind_degree < 67.5:
        wind_direction = 'Północno-Wschodni'
    elif wind_degree >= 67.5 and wind_degree < 112.5:
        wind_direction = 'Wschodni'
    elif wind_degree >= 112.5 and wind_degree < 157.5:
        wind_direction = 'Południowo-Wschodni'
    elif wind_degree >= 157.5 and wind_degree < 202.5:
        wind_direction = 'Południowy'
    elif wind_degree >= 202.5 and wind_degree < 247.5:
        wind_direction = 'Południowo-Zachodni'
    elif wind_degree >= 247.5 and wind_degree < 292.5:
        wind_direction = 'Zachodni'
    elif wind_degree >= 292.5 and wind_degree < 337.5:
        wind_direction = 'Północno-Zachodni'

    data = {
        'name': location['name'],
        'temperature': str(weather['temperature']) + ' °C',
        'wind_speed': str(weather['windspeed']) + ' km/h',
        'wind_direction': wind_direction,
        'state': weather_codes[str(weather['weathercode'])]  
    }
    
    return data


class Meteo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def __init__(self, bot):
        """
        Constructor method
        """
        self.bot = bot

    @commands.command(
        pass_context=True,
        name='meteo',
        category='Narzędzia',
        usage='placeholder',
        help="""
              aaaa
              """
    )

    async def meteo(self, ctx, *, search):

        if len(search) != 0:
            location = get_location(search)
            if location == 0:
                await ctx.send("Nie znaleziono lokalizacji, spróbuj ponownie")
            else:
                weather = send_weather_request(location)
                weather = prepare_weather(location, weather)
                embed = nextcord.Embed(title="Meteo \u2602")
                embed.add_field(name="Lokalizacja", value=weather['name'], inline=False)
                embed.add_field(name="Temperatura", value=weather['temperature'], inline=False)
                embed.add_field(name="Prędkość Wiatru", value=weather['wind_speed'], inline=False)
                embed.add_field(name="Kierunek Wiatru", value=weather['wind_direction'], inline=False)
                embed.add_field(name="Stan", value=weather['state'], inline=False)

                await ctx.send(embed=embed)
            
        else:
            await ctx.send("Proszę podać lokalizację")