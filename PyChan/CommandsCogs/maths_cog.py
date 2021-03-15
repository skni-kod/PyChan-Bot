import discord
from discord.ext import commands

from Functions.maths_functions import *


class Maths(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def zamiana(self, ctx, from_param: int, to_param: int, number):
        if (from_param < 2 or from_param > 16) or (to_param < 2 or to_param > 16):
            raise commands.errors.BadArgument

        converted_number = ''

        if from_param == 10:
            converted_number = dec_float_to_another(
                to_param, number)['converted']['number']
        elif to_param == 10:
            converted_number = another_float_to_dec(from_param, number)['dec']
        else:
            converted_number = another_float_to_dec(from_param, number)['dec']
            converted_number = dec_float_to_another(to_param, converted_number)[
                'converted']['number']

        await ctx.send(f'{number} ({from_param}) = {converted_number} ({to_param})')

    @commands.command(pass_context=True, name='zamiana+')
    async def zamiana_z_rozpisaniem(self, ctx, from_param: int, to_param: int, number):
        if (from_param < 2 or from_param > 16) or (to_param < 2 or to_param > 16):
            raise commands.errors.BadArgument

        message = ''

        def convert_from_dec(number_param):
            number_param = float(number_param)
            numbers_dict = dec_float_to_another(to_param, float(number_param))
            message = ''
            if int(number_param) != 0:
                message = message + f'{int(number_param)} / {to_param}\n'
                for dict in numbers_dict['integer']:
                    for x, y in dict.items():
                        message = message + f'{x} r {y}\n'
                message = message + \
                    str(numbers_dict['converted']['integer']) + '\n\n'
            if float(number_param) - int(number_param) != 0:
                message = message + \
                    f'{float(number_param) - int(number_param)} * {to_param}\n'
                for dict in numbers_dict['fraction']:
                    for x, y in dict.items():
                        message = message + f'{x} | {y}\n'
                message = message + \
                    str(numbers_dict['converted']['fraction']) + '\n\n'

            message = message + \
                f'{number_param} (10) = ' + \
                f"{numbers_dict['converted']['number']} ({to_param})\n"
            return message

        def convert_to_dec(number_param):
            message = ''
            message = message + f'{number_param}({from_param}) = '
            numbers_dict = another_float_to_dec(from_param, number_param)

            if numbers_dict['integer'][0] == 0 and len(numbers_dict['integer']) == 1:
                pass
            else:
                for i, (x, y) in enumerate(numbers_dict['integer'].items(), start=1):
                    message = message + f'{y} * {from_param}^{x}'
                    if i < len(numbers_dict['integer']):
                        message = message + ' + '
            print(numbers_dict)
            if len(numbers_dict['fraction']) == 0:
                pass
            else:
                if len(numbers_dict['integer']) > 1:
                    message = message + ' + '
                for i, (x, y) in enumerate(numbers_dict['fraction'].items(), start=1):
                    message = message + f'{y} * {from_param}^{x}'
                    if i < len(numbers_dict['fraction']):
                        message = message + ' + '

            if numbers_dict['integer'][0] == 0 and len(numbers_dict['integer']) == 1 and len(numbers_dict['fraction']) == 0:
                pass
            else:
                message = message + ' = '

            message = message + f'{numbers_dict["dec"]} ({10})\n\n'
            return [message, numbers_dict["dec"]]

        if from_param == 10:
            message = convert_from_dec(number)
        elif to_param == 10:
            message = convert_to_dec(number)[0]
        else:
            list_h = convert_to_dec(number)
            message = list_h[0]
            message = message + convert_from_dec(list_h[1])

        await ctx.send(message)

    @commands.command(pass_context=True)
    async def ieee754_32(self, ctx, number: float):
        data = ieee754_32(str(number))
        embed = discord.Embed(title='IEEE 754/32BIT',
                              description='',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Sign',
                        value=data[0],
                        inline=False)
        embed.add_field(name='Exponent',
                        value=data[1],
                        inline=False)
        embed.add_field(name='Significand',
                        value=data[2],
                        inline=False)
        embed.add_field(name='"IEEE 754/32BIT',
                        value=data[3],
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def ieee754_64(self, ctx, number: float):
        data = ieee754_64(str(number))
        embed = discord.Embed(title='IEEE 754/64BIT',
                              description='',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Sign',
                        value=data[0],
                        inline=False)
        embed.add_field(name='Exponent',
                        value=data[1],
                        inline=False)
        embed.add_field(name='Significand',
                        value=data[2],
                        inline=False)
        embed.add_field(name='"IEEE 754/64BIT',
                        value=data[3],
                        inline=False)

        await ctx.send(embed=embed)
