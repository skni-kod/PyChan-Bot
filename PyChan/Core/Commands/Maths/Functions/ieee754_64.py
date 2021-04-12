import discord
from discord.ext import commands
from Core.Commands.Maths.Functions.maths_functions import *


class Ieee754_64(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='ieee754_64')
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
        embed.add_field(name='IEEE 754/64BIT',
                        value=data[3],
                        inline=False)

        await ctx.send(embed=embed)