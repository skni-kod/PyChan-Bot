import discord
from discord.ext import commands

from Functions.maths_functions import *


class Maths(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def zamiana(self, ctx, from_param: int, to_param: int, number):
        try:
            decimal = int(number, from_param)
        except:
            raise

        if to_param == 2:
            converted = bin(decimal)
        elif to_param == 8:
            converted = oct(decimal)
        elif to_param == 10:
            converted = decimal
        elif to_param == 16:
            converted = hex(decimal)
        await ctx.send(f'{number} ({from_param}) = {converted} ({to_param})')

    @commands.command(pass_context=True, name='zamiana+')
    async def zamiana_z_rozpisaniem(self, ctx, from_param: int, to_param: int, number):
        dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12,
                'D': 13, 'E': 14, 'F': 15}

        message = ''

        if from_param == 10:
            number = float(number)
            numbers_dict = dec_float_to_another(to_param, float(number))

            if int(number) != 0:
                message = message + f'{int(number)} / {to_param}\n'
                for dict in numbers_dict['integer']:
                    for x, y in dict.items():
                        message = message + f'{x} r {y}\n'
                message = message + numbers_dict['converted']['integer'] + '\n\n'

            if float(number) - int(number) != 0:
                message = message + f'{float(number) - int(number)} * {to_param}\n'
                for dict in numbers_dict['fraction']:
                    for x, y in dict.items():
                        message = message + f'{x} | {y}\n'
                message = message + numbers_dict['converted']['fraction'] + '\n\n'

            message = message + numbers_dict['converted']['number']
        else:
            raise Exception

        await ctx.send(message)
