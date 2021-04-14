import discord
from discord.ext import commands
from PyChan.Core.Commands.Maths.Functions.maths_functions import *
from PyChan.Core.Decorators.decorators import Decorator


class Convert_numbers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='zamiana')
    @Decorator.pychan_decorator
    async def convert_numbers(self, ctx, from_param: int, to_param: int, number):
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
