# Work with Python 3.6
import datetime
import os
import random
import asyncio
import time

import aiohttp
import json
import requests
from bs4 import BeautifulSoup
from discord import Game, File
from discord.ext.commands import Bot, when_mentioned_or
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from unit_converter.converter import convert, converts

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

from forecastiopy import *

from opencage.geocoder import OpenCageGeocode

import this
import codecs

import oblicz_30
import oblicz_22

import keys

EMOTIONS = (
    'normal',
    'very happy',
    'happy',
    'sad',
    'very sad',
    'agreeable',
    'alert',
    'amused',
    'angry',
    'apologetic',
    'argumentative',
    'assertive',
    'bored',
    'calm',
    'concerned',
    'contemplative',
    'cool',
    'curious',
    'dancing',
    'determined',
    'devious',
    'didactic',
    'distracted',
    'doubting',
    'excited',
    'flirty',
    'forceful',
    'forgetful',
    'furious',
    'gentle',
    'grumpy',
    'guilty',
    'hatred',
    'joking',
    'jumpy',
    'lazy',
    'love',
    'mean',
    'mocking',
    'modest',
    'naughty',
    'negative',
    'nice',
    'nosey',
    'positive',
    'proud',
    'questioning',
    'relaxed',
    'reluctant',
    'righteous',
    'robotic',
    'rude',
    'sarcastic',
    'serious',
    'shouting',
    'shy',
    'silly',
    'singing',
    'sleepy',
    'smug',
    'stubborn',
    'supportive',
    'sure',
    'sweetness',
    'sympathy',
    'thoughtful',
    'tired',
    'tongue out',
    'unsure',
    'victorious',
    'winking',
    'worried ',
)

BOT_PREFIX = ("^", )

client = Bot(command_prefix=when_mentioned_or("^"))

PATH_TO_DRIVERS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers")
FIREFOX_EXE_NAME = "geckodriver.exe" if os.name == 'nt' else "geckodriver"


print(os.path.join(PATH_TO_DRIVERS_DIR, FIREFOX_EXE_NAME))

driver = webdriver.Firefox(
   executable_path=os.path.join(PATH_TO_DRIVERS_DIR, FIREFOX_EXE_NAME))
driver.get("https://www.cleverbot.com/")

geocoder = OpenCageGeocode(GEOCODER_KEY)

beer_bottles_number = 99

session = requests.Session()
resp = session.get("http://www.jabberwacky.com/")

@client.command(name='calka',
                description="Counts an intergral",
                brief="Answers from the beyond.",
                pass_context=True)
async def bot_integral(context, expression):
    await context.trigger_typing()
    print(expression)
    x = Symbol('x')
    xpr = parse_expr(expression)
    result = integrate(xpr, x)
    p = pretty(Eq(Integral(xpr, x), Add(result, Symbol('C'))), use_unicode=False)
    print(p)
    await context.send("```" + str(p) + "```" + ", " + context.message.author.mention)


@client.command(name='pochodna',
                description="Counts an deriative",
                brief="Answers from the beyond.",
                pass_context=True)
async def bot_diff(context, expression):
    await context.trigger_typing()
    print(expression)
    x = Symbol('x')
    xpr = parse_expr(expression)
    result = diff(xpr, x)
    p = pretty(Eq(Derivative(xpr, x), result), use_unicode=False)
    print(p)
    await context.send("```" + str(p) + "```" + ", " + context.message.author.mention)


@client.command(name='granica',
                description="Counts an limit",
                brief="Answers from the beyond.",
                pass_context=True)
async def bot_limit(context, expression):
    await context.trigger_typing()
    print(expression)
    x = Symbol('x')
    xpr = parse_expr(expression)
    result = limit(xpr, x, oo)
    p = pretty(Eq(Limit(xpr, x, oo), result), use_unicode=False)
    print(p)
    await context.send("```" + str(p) + "```" + ", " + context.message.author.mention)


@client.command(name='konwertuj',
                description="Counts an limit",
                brief="Answers from the beyond.",
                pass_context=True)
async def bot_convert(context, expression, desires_unit):
    await context.trigger_typing()
    print(expression)
    p = convert(expression, desires_unit)
    await context.send("```" + str(p) + "```" + ", " + context.message.author.mention)


@client.command(name='tell',
                description="Talk with bot",
                brief="Answers from the beyond.",
                pass_context=True)
async def bot_tell(context, message, mood="normal"):
    global resp
    await context.trigger_typing()
    if mood not in EMOTIONS:
        await context.channel.send(
            "Invalid Emotion!. Available: " + EMOTIONS.__str__())
        return

    bs = BeautifulSoup(resp.text, 'html.parser')
    inputs = bs.find_all('input')
    params = {inp['name']: inp['value'] for inp in inputs}
    params['reaction'] = ''
    params['emotion'] = ''
    del params['sub']
    # pprint.pprint(params)
    print(params['vText2'])
    params['vText1uni'] = message
    params['vText1'] = ''.join(
        ["|" + hex(ord(x)).replace("x", "").upper() if ord(x) > 127 else x for
         x in list(params['vText1uni'])])
    params['emotion'] = mood if mood != "normal" else ''

    resp = session.post("http://www.jabberwacky.com/", data=params)
    bs = BeautifulSoup(resp.text, 'html.parser')
    txt = bs.find('input', {
        'name': 'vText2'
    })['value']
    await context.channel.send(txt)


@client.command(name='resettell',
                description="Talk with bot",
                brief="Answers from the beyond.",
                pass_context=True)
async def reset_tell(ctx):
    global resp
    resp = session.get("http://www.jabberwacky.com/")
    await ctx.channel.send("Tell zresetowany")


@client.command(pass_context=True)
async def ping(ctx):
    now = datetime.datetime.utcnow()
    delta = now-ctx.message.created_at
    await ctx.channel.send('{}ms'.format(client.latency * 1000))


@client.command(name='dupa',
                description="Talk with bot",
                brief="Answers from the beyond.",
                pass_context=True)
async def bot_dupa(context, code):
    await context.trigger_typing()
    result = oblicz_30.oblicz30(code.replace("```", ''))
    await context.channel.send("```" + result + "```", file=File('foo.png'))
    

@client.command(name='dupa2',
                description="Talk with bot",
                brief="Answers from the beyond.",
                pass_context=True)
async def bot_dupa2(context, code):
    await context.trigger_typing()
    result = oblicz_22.oblicz22(code.replace("```", ''))
    await context.channel.send("```" + result + "```", file=File('foo.png'))

@client.command(name='tellfajniejszy',
                description="Talk with bot",
                brief="Answers from the beyond.",
                pass_context=True)
async def bot_tell(context, message):
    await context.trigger_typing()
    input = driver.find_element_by_name("stimulus")
    input.send_keys(message)
    button = driver.find_element_by_name("thinkaboutitbutton")
    button.click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, 'thinkaboutitbutton')))
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'snipTextIcon')))
    time.sleep(0.5)
    text = driver.find_element_by_id('line1') \
        .find_element_by_class_name('bot').text
    await context.channel.send(text)


@client.command(name='square',
                description="Square a number",
                brief="Answers from the beyond.",
                pass_context=True)
async def square(context, number):
    await context.trigger_typing()
    squared_value = int(number) * int(number)
    await context.channel.send(str(number) + " squared is " + str(squared_value))


@client.command(name='pogoda',
                description="Wheather",
                brief="Answers from the beyond.",
                pass_context=True)
async def bot_weather(context, placeName):
    await context.trigger_typing()
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

    await context.channel.send("```" + summary  + currentString + "```")


@client.event
async def on_ready():
    await client.change_presence(activity=Game("with humans"))
    #await client.status(Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.command(name='bitcoin',
                description="Get an bitcoin course",
                brief="Answers from the beyond.",
                pass_context=True)
async def bitcoin(context):
    await context.trigger_typing()
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await context.send("Bitcoin price is: $" + response['bpi']['USD']['rate'])


@client.command(name='pep8',
                description="Info about pep8",
                brief="Important Thing",
                pass_context=True)
async def pep_eight(context):
    await context.trigger_typing()
    await context.send("Informations about PEP8 - https://www.python.org/dev/peps/pep-0008/")


@client.command(name='zen',
                description="Zen of Python",
                brief="Important Thing",
                pass_context=True)
async def zen(context):
    await context.trigger_typing()
    await context.send("```" + codecs.encode(this.s, 'rot13') + "```")


@client.command(name='aboutme',
                description="Info about me",
                brief="Important Thing",
                pass_context=True)
async def aboutme(context):
    await context.trigger_typing()
    await context.send("https://chomado.com/wp-content/uploads/2018/09/189828_python.png")


@client.command(name='beer',
                description="Beer!",
                brief="Important Thing",
                pass_context=True)
async def beer(context):
    global beer_bottles_number
    await context.trigger_typing()
    response = ""
    if beer_bottles_number == 1:
        response = '1 bottle of beer on the wall, 1 bottle of beer!\nSo take ' \
                   'it down, pass it around, no more bottles of beer on the ' \
                   'wall! '
        beer_bottles_number -= 1
    elif beer_bottles_number == 2:
        response = '2 more bottles of beer on the wall, 2 more bottles of ' \
                   'beer!\n So take one down, pass it around, 1 more bottle ' \
                   'of beer on the wall! '
        beer_bottles_number -= 1
    elif beer_bottles_number == 0:
        response = "No more bottles of beer on the wall, no more bottles of " \
                   "beer.\n Go to the store and buy some more, 99 bottles of " \
                   "beer on the wall. "
        beer_bottles_number = 99
    else:
        response = f"{beer_bottles_number} bottles of beer on the wall, " \
                   f"{beer_bottles_number} bottles of beer!\n So take it " \
                   f"down, pass it around, {beer_bottles_number - 1} more " \
                   f"bottles of beer on the wall! "
        beer_bottles_number -= 1
    await context.send(response)


async def list_servers():
    """await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)"""


client.loop.create_task(list_servers())
client.run(TOKEN)
