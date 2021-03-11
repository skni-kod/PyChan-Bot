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

    @zamiana.error
    async def zamiana_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Podany system nie jest liczbą')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Brakuje wymaganego parametru')
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send('Podana liczba jest niepoprawna')
        elif isinstance(error, Exception):
            await ctx.send('Coś poszło nie tak')
        else:
            await ctx.send('Coś poszło nie tak')

        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.add_field(name='Zamiana',
                        value='Poprawna składnia:\n'
                              '`^zamiana <system liczbowy, z którego zamieniamy> <system liczbowy, do którego zamieniamy> <liczba>`',
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, name='zamiana+')
    async def zamiana_z_rozpisaniem(self, ctx, from_param: int, to_param: int, number):
        dict = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12,
                'D': 13, 'E': 14, 'F': 15}

        print(dec_to_another(16, 232))

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

    @zamiana_z_rozpisaniem.error
    async def zamiana_z_rozpisaniem_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Podany system nie jest liczbą')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Brakuje wymaganego parametru')
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send('Podana liczba jest niepoprawna')
        elif isinstance(error, Exception):
            await ctx.send('Coś poszło nie tak')
        else:
            await ctx.send('Coś poszło nie tak')

        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.add_field(name='Zamiana',
                        value='Poprawna składnia:\n'
                              '`^zamiana <system liczbowy, z którego zamieniamy> <system liczbowy, do którego zamieniamy> <liczba>`',
                        inline=False)
        await ctx.send(embed=embed)
