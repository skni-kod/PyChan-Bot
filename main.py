from discord.ext.commands import Bot, when_mentioned_or
from forecastiopy import *
from opencage.geocoder import OpenCageGeocode
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

from keys import *

BOT_PREFIX = ("^",)
client = Bot(command_prefix=when_mentioned_or("^"))
geocoder = OpenCageGeocode(GEOCODER_KEY)


@client.command(name='calka',
                description="Liczy całke",
                pass_context=True)
async def bot_integral(context, expression):
    await context.trigger_typing()
    try:
        print(expression)
        x = Symbol('x')
        xpr = parse_expr(expression)
        result = integrate(xpr, x)
        p = pretty(Eq(Integral(xpr, x), Add(result, Symbol('C'))), use_unicode=False)
        print(p)
        await context.channel.send("```" + str(p) + "```" + ", " + context.message.author.mention)
    except:
        await context.channel.send("Coś poszło nie tak :/, pamiętaj potęga to '**'")


@client.command(name='pochodna',
                description="Liczy pochodną",
                pass_context=True)
async def bot_diff(context, expression):
    try:
        await context.trigger_typing()
        print(expression)
        x = Symbol('x')
        xpr = parse_expr(expression)
        result = diff(xpr, x)
        p = pretty(Eq(Derivative(xpr, x), result), use_unicode=False)
        print(p)
        await context.channel.send("```" + str(p) + "```" + ", " + context.message.author.mention)
    except:
        await context.channel.send("Coś poszło nie tak :/, pamiętaj potęga to '**'")


@client.command(name='granica',
                description="Liczy granicę",
                pass_context=True)
async def bot_limit(context, expression):
    try:
        await context.trigger_typing()
        print(expression)
        x = Symbol('x')
        xpr = parse_expr(expression)
        result = limit(xpr, x, oo)
        p = pretty(Eq(Limit(xpr, x, oo), result), use_unicode=False)
        print(p)
        await context.channel.send("```" + str(p) + "```" + ", " + context.message.author.mention)
    except:
        await context.channel.send("Coś poszło nie tak :/, pamiętaj potęga to '**'")


@client.command(pass_context=True)
async def ping(ctx):
    await ctx.channel.send('{}ms'.format(client.latency * 1000))


@client.command(name='square',
                description="Kwadrat",
                brief="Answers from the beyond.",
                pass_context=True)
async def square(context, number):
    await context.trigger_typing()
    squared_value = int(number) * int(number)
    await context.channel.send(str(number) + " squared is " + str(squared_value))


@client.command(name='aboutme',
                description="Info about me",
                brief="Important Thing",
                pass_context=True)
async def aboutme(context):
    await context.trigger_typing()
    await context.channel.send("https://chomado.com/wp-content/uploads/2018/09/189828_python.png")


@client.command(name='pogoda',
                description="Wheather",
                brief="Answers from the beyond.",
                pass_context=True)
async def bot_weather(context, placeName):
    await context.trigger_typing()
    try:
        geocode = geocoder.geocode(placeName, no_annotations=1, language="pl")[0]['geometry']
        print("DUPA")
        print(geocode['lat'])
        print(geocode['lng'])
        fio = ForecastIO.ForecastIO(FORECAST_KEY, latitude=geocode['lat'],
                                    longitude=geocode['lng'],
                                    units=ForecastIO.ForecastIO.UNITS_SI)
        print("DUPA2")
        current = FIOCurrently.FIOCurrently(fio)
        minutely = FIOMinutely.FIOMinutely(fio)
        hourly = FIOHourly.FIOHourly(fio)
        daily = FIODaily.FIODaily(fio)
        currentString = f"""
    
    Temperature: {current.temperature:g} C
    Apparent Temperature: {current.apparentTemperature:g} C
    Precipitation Type: {current.precipType if hasattr(current, "precipType") else "None"}
    Precipitation Probability: {current.precipProbability:g}
    Precipitation Intensity: {current.precipIntensity:g}
    Wind Speed: {current.windSpeed:g} mps
    Wind Gust: {current.windGust:g} mps
    Visibility: {current.visibility:g} km
    Humidity: {current.humidity:g}
    Pressure: {current.pressure:g} hPa
    Dew Point: {current.dewPoint:g} C
    """

        summary = f"""Input place: {placeName}
    GeoCode: {geocode['lat']}, {geocode['lng']} (Lat, Lng)
    
    """
        if hasattr(current, 'summary'):
            summary += current.summary + "\n"
        if hasattr(minutely, 'summary'):
            summary += minutely.summary + "\n"
        if hasattr(hourly, 'summary'):
            summary += hourly.summary + "\n"
        if hasattr(daily, 'summary'):
            summary += daily.summary + "\n"

        for item in current.get().keys():
            print(item + ' : ' + str(current.get()[item]))

        await context.channel.send("```" + summary + currentString + "```")
    except:
        await context.channel.send("Pewnie znowu api key nieautoryzowany")


client.run(TOKEN)
