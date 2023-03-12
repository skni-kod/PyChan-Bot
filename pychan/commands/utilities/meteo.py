import nextcord
from nextcord.ext import commands
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


plt.rcParams['figure.facecolor'] = '#313338'
plt.rcParams['axes.facecolor'] = '#313338'
plt.rcParams['text.color'] = '#ffffff'
plt.rcParams['axes.labelcolor'] = '#ffffff'
plt.rcParams['xtick.color'] = '#ffffff'
plt.rcParams['ytick.color'] = '#ffffff'
plt.rc('axes',edgecolor='#ffffff')

weather_codes = {
    0: 'clear-sky.png',
    1: 'mainly-clear.png',
    2: 'partialy-cloudy.png',
    3: 'overcast.png',
    45: 'fog.png',
    48: 'fog.png',
    51: 'drizzle.png',
    53: 'drizzle.png',
    55: 'drizzle.png',
    56: 'drizzle-snow.png',
    57: 'drizzle-snow.png',
    61: 'rain.png',
    63: 'rain.png',
    65: 'rain.png',
    66: 'rain-snow.png',
    67: 'rain-snow.png',
    71: 'snow.png',
    73: 'snow.png',
    75: 'snow.png',
    77: 'snow.png',
    80: 'rain.png',
    81: 'rain.png',
    82: 'rain.png',
    85: 'rain-snow.png',
    86: 'rain-snow.png',
    96: 'thunderstorm.png',
    96: 'thunderstorm-rain.png',
    99: 'thunderstorm-rain.png'
}


def get_location(location):
    url = "https://nominatim.openstreetmap.org/search?q=" + location + '&format=jsonv2&limit=1&accept-language=pl'
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

    url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lot + '&hourly=rain&current_weather=true&timezone=auto'      
    r = requests.get(url)
    weather = r.json()
    weather = weather['current_weather']

    return weather


def send_daily_request(location):
    lat = location['latitude']
    lot = location['longitude']

    url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lot + '&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,rain_sum,showers_sum,snowfall_sum,precipitation_probability_max&current_weather=true&timezone=auto'

    r = requests.get(url)
    weather = r.json()
    daily = weather['daily']
    now = weather['current_weather']

    return daily, now


def send_hourly_request(location, type):
    lat = location['latitude']
    lot = location['longitude']

    if type == 'temperature':
        url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lot + '&hourly=temperature_2m&current_weather=true&timezone=auto'
        unit = 'temperature_2m'
    elif type == 'pressure':
        url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lot + '&hourly=surface_pressure&current_weather=true&timezone=auto'
        unit = 'surface_pressure'
    elif type == 'precipitation':
        url = 'https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lot + '&hourly=precipitation_probability,rain,showers,snowfall&current_weather=true&timezone=auto'

    r = requests.get(url)
    weather = r.json()

    if type == 'precipitation':
        settings = {
            'unit': {
                    'unit_rain': weather['hourly_units']['rain'],
                    'unit_showers': weather['hourly_units']['showers'],
                    'unit_snowfall': weather['hourly_units']['snowfall'],
                    'unit_probability': weather['hourly_units']['precipitation_probability']
            },
            'now': weather['current_weather']['time']
        }
    else:
        settings = {
            'unit': weather['hourly_units'][unit],
            'now': weather['current_weather']['time']
        }

    weather = weather['hourly']
  
    return weather, settings


def prepare_daily(weather):

    data = {}

    for i in range(len(weather['time'])):
        day = {
            'time': weather['time'][i],
            'code': weather['weathercode'][i],
            'temperature_max': weather['temperature_2m_max'][i],
            'temperature_min': weather['temperature_2m_min'][i],
            'sunrise': weather['sunrise'][i],
            'sunset': weather['sunset'][i],
            'rain': weather['rain_sum'][i],
            'shower': weather['showers_sum'][i],
            'snow': weather['snowfall_sum'][i],
            'precipitation_probability': weather['precipitation_probability_max'][i]
        }

        data[i] = day

    return data


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
        'state': weather_codes[weather['weathercode']]  
    }
    
    return data


def prepare_hourly(location, weather, type, settings):
    tmp = weather['time']
    time = []
    y = []    
    current_time = settings['now']
    stop = 0

    for i in range(len(tmp)):
        if stop != 24:
            if str(tmp[i]) >= current_time:
                stop += 1
                time.append(tmp[i][5:10] + ' ' + tmp[i][-5:])
                y.append(weather[type][i])
    
    data = {
    'name': location['name'],
    'time': time,
    'y': y,
    }

    return data


def create_graph(weather, unit):


    x_set = weather['time']
    y_set = weather['y']
    
    fig = plt.figure()

    fig.set_figwidth(14)
    plt.plot(x_set,y_set, marker='o')


    for x,y in zip(x_set,y_set):
        label = str(y) + unit
        plt.annotate(label,
                     (x,y),
                     textcoords='offset points', xytext=(0,-10), color='white', ha='center')

    plt.axvline(x=x_set[0], color='g', linestyle='-')
    plt.gcf().autofmt_xdate()
    plt.grid()

    plt.title(weather['name'])

    return fig


def create_image(location, daily, now):

    week = {
        0: "Poniedziałek",
        1: "Wtorek",
        2: "Środa",
        3: "Czwartek",
        4: "Piątek",
        5: "Sobota",
        6: "Niedziela"
    }
    
    background = Image.open('pychan/commands/utilities/meteo_assets/template.png')

    
    minutes = str(datetime.now().minute)

    if len(minutes) == 1:
        minutes = '0' + minutes

    local_hour = now['time'][-5:-3] + ':' + minutes

    img = background.copy()
    background.close()

    meteo_font = ImageFont.truetype('pychan/commands/utilities/meteo_assets/NotoSans-Medium.ttf', 40)
    
    tmp = location['name'].split(', ')
    title = tmp[0] + ', ' + tmp [-2] + ', ' + tmp[-1]

    d = ImageDraw.Draw(img)
    d.multiline_text((30,20), title, font = meteo_font, fill = (255,255,255))

    d.text((1085,20), "Czas Lokalny", font = meteo_font, fill = (255,255,255))
    
    meteo_font = ImageFont.truetype('pychan/commands/utilities/meteo_assets/NotoSans-Medium.ttf', 30)
    d.text((30,70), str(now['temperature'])+ "°C", font=meteo_font, fill=(255,255,255))
    d.text((1085,70), local_hour, font = meteo_font, fill = (255,255,255))

    x_tmp = 150
   
    meteo_font = ImageFont.truetype('pychan/commands/utilities/meteo_assets/NotoSans-Medium.ttf', 30)
    for i in range(7):
        y_tmp = 160

        week_day = datetime.strptime(daily[i]['time'], '%Y-%m-%d')
        d.text((x_tmp - 55,y_tmp), week[week_day.weekday()], font=meteo_font, fill=(255,255,255))
        d.text((x_tmp - 55,y_tmp + 70), str(daily[i]['time'][-5:]), font=meteo_font, fill=(255,255,255))

        #Weather Icon
        icon_path = 'pychan/commands/utilities/meteo_assets/weather-icons/' + weather_codes[daily[i]['code']]
        icon = Image.open(icon_path)
        img.paste(icon, (x_tmp - 55, y_tmp + 140), icon)
        icon.close()
        
        y_tmp = 495

        #Temperature Max
        d.text((x_tmp - 10 ,y_tmp + 5), str(daily[i]['temperature_max']) + "°C", font=meteo_font, fill=(255,255,255))

        #Temperature Min
        d.text((x_tmp - 10 ,y_tmp + 75), str(daily[i]['temperature_min']) + "°C", font=meteo_font, fill=(255,255,255))

        #Percipitation % 
        d.text((x_tmp - 10,y_tmp + 150), str(daily[i]['precipitation_probability']) + "%", font=meteo_font, fill=(255,255,255))

        #Sunrise
        sunrise = datetime.strptime(daily[i]['sunrise'], '%Y-%m-%dT%H:%M')
        d.text((x_tmp - 10,y_tmp + 220), str(sunrise)[11:16], font=meteo_font, fill=(255,255,255))

        #Sunset
        sunset = datetime.strptime(daily[i]['sunset'], '%Y-%m-%dT%H:%M')
        d.text((x_tmp - 10,y_tmp + 295), str(sunset)[11:16], font=meteo_font, fill=(255,255,255))
        
        x_tmp += 200


    return img


class Meteo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def __init__(self, bot):
        """
        Constructor method
        """
        self.bot = bot

    @commands.group(
        name='meteo',
        category='Narzędzia',
    )

    async def meteo(self, ctx: commands.Context):
        '''Komendy Związane z pogodą'''
        pass

    @meteo.command(
        pass_context=True,
        name='teraz',
        usage='TODO',
        help=   """
                TODO
                """
        )

    async def teraz(self, ctx, *, search):

        if len(search) != 0:
            location = get_location(search)
            if location == 0:
                await ctx.send("Nie znaleziono lokalizacji, spróbuj ponownie")
            else:
                weather = send_weather_request(location)
                weather = prepare_weather(location, weather)

                file_name = 'pychan/commands/utilities/meteo_assets/weather-icons/' + weather['state']
                file = nextcord.File(file_name, filename=weather['state'])

                embed = nextcord.Embed(title="Meteo \u2602")
                embed.set_thumbnail(url='attachment://' + weather['state'])
                embed.add_field(name="Lokalizacja", value=weather['name'], inline=False)
                embed.add_field(name="Temperatura", value=weather['temperature'], inline=False)
                embed.add_field(name="Prędkość Wiatru", value=weather['wind_speed'], inline=False)
                embed.add_field(name="Kierunek Wiatru", value=weather['wind_direction'], inline=False)

                await ctx.send(embed=embed, file=file)
            
        else:
            await ctx.send("Proszę podać lokalizację")
    

    @meteo.command(
        pass_context=True,
        name='temperatura',
        usage='TODO',
        help=   """
                TODO
                """
    )


    async def temperatura(self, ctx, *, search):
        if len(search) != 0:
            location = get_location(search)
            if location == 0:
                await ctx.send("Nie znaleziono lokalizacji, spróbuj ponownie")
            else:
                weather, settings = send_hourly_request(location, 'temperature')
                weather = prepare_hourly(location, weather, 'temperature_2m', settings)
                f = create_graph(weather, settings['unit'])
                bytes = BytesIO()
                f.savefig(bytes, format='PNG')
                bytes.seek(0)
                await ctx.send("***Meteo Temperatura \U0001F321***")
                await ctx.send(file=nextcord.File(fp=bytes, filename='image.png'))
                
                bytes.close()

        else:
            await ctx.send("Proszę podać lokalizację")


    @meteo.command(
        pass_context=True,
        name='ciśnienie',
        usage='TODO',
        help=   """
                TODO
                """
    )


    async def ciśnienie(self, ctx, *, search):
        if len(search) != 0:
            location = get_location(search)
            if location == 0:
                await ctx.send("Nie znaleziono lokalizacji, spróbuj ponownie")
            else:
                weather, settings = send_hourly_request(location, 'pressure')
                weather = prepare_hourly(location, weather, 'surface_pressure', settings)
                f = create_graph(weather, settings['unit'])
                bytes = BytesIO()
                f.savefig(bytes, format='PNG')
                bytes.seek(0)
                await ctx.send("***Meteo Ciśnienie***")
                await ctx.send(file=nextcord.File(fp=bytes, filename='image.png'))
                
                bytes.close()

        else:
            await ctx.send("Proszę podać lokalizację")

    
    @meteo.command(
        pass_context=True,
        name='opady',
        usage='TODO',
        help=   """
                TODO
                """
    )


    async def opady(self, ctx, *, search):
        if len(search) != 0:
            location = get_location(search)
            if location == 0:
                await ctx.send("Nie znaleziono lokalizacji, spróbuj ponownie")
            else:
                weather, settings = send_hourly_request(location, 'precipitation')

                await ctx.send("***Meteo Opady\n***")

                await ctx.send("***Prawdopodobieństwo Opadów***")
                weather_probability = prepare_hourly(location, weather, 'precipitation_probability', settings)
                f = create_graph(weather_probability, settings['unit']['unit_probability'])
                bytes = BytesIO()
                f.savefig(bytes, format='PNG')
                bytes.seek(0)
                await ctx.send(file=nextcord.File(fp=bytes, filename='image.png'))
                bytes.close()

                await ctx.send("***Suma Przelotnych Opadów***")
                weather_probability = prepare_hourly(location, weather, 'showers', settings)
                f = create_graph(weather_probability, settings['unit']['unit_showers'])
                bytes = BytesIO()
                f.savefig(bytes, format='PNG')
                bytes.seek(0)
                await ctx.send(file=nextcord.File(fp=bytes, filename='image.png'))
                bytes.close()

                await ctx.send("***Suma Opadów Deszczu***")
                weather_probability = prepare_hourly(location, weather, 'rain', settings)
                f = create_graph(weather_probability, settings['unit']['unit_rain'])
                bytes = BytesIO()
                f.savefig(bytes, format='PNG')
                bytes.seek(0)
                await ctx.send(file=nextcord.File(fp=bytes, filename='image.png'))
                bytes.close()

                
                await ctx.send("***Suma Opadów Śniegu***")
                weather_probability = prepare_hourly(location, weather, 'snowfall', settings)
                f = create_graph(weather_probability, settings['unit']['unit_snowfall'])
                bytes = BytesIO()
                f.savefig(bytes, format='PNG')
                bytes.seek(0)
                await ctx.send(file=nextcord.File(fp=bytes, filename='image.png'))
                bytes.close()

        else:
            await ctx.send("Proszę podać lokalizację")



    @meteo.command(
            pass_context=True,
            name='week',
            usage='TODO',
            help=   """
                    TODO
                    """
        )


    async def week(self, ctx, *, search):
        if len(search) != 0:
            location = get_location(search)
            if location == 0:
                await ctx.send("Nie znaleziono lokalizacji, spróbuj ponownie")
            else:
                daily, now = send_daily_request(location)
                daily = prepare_daily(daily)
                image = create_image(location, daily, now)

                bytes = BytesIO()
                image.save(bytes, format='PNG')
                bytes.seek(0)

                await ctx.send("***Meteo Week \U0001F321***")
                await ctx.send(file=nextcord.File(fp=bytes, filename=(location['name'] + '.png')))

                image.close()
                bytes.close()
                
        else:
            await ctx.send("Proszę podać lokalizację")