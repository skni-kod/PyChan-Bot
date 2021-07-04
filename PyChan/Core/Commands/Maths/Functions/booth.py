import discord
from discord.ext import commands
from Core.Commands.Maths.Functions.maths_functions import *
from Core.Decorators.decorators import Decorator
from tabulate import tabulate

class BoothAlgorithm(commands.Cog):
    """
    The class contains Booth Algorithm method
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='booth')
    async def booth(self, ctx, liczba1: int, liczba2: int):
        convert = twos_complement_equal_length(liczba1, liczba2)
        booth_result = booth(liczba1, liczba2)
        header = f"""Algorytm Bootha | Zadane parametry:
        P  = {liczba1} (DEC) = {convert[0]} (U2)
        -P = {-liczba1}(DEC) = {convert[1]} (U2)
        Q  = {liczba2} (DEC) = {convert[2]} (U2)
        Wynik operacji = {liczba1*liczba2} (DEC) = {booth_result[1]} (U2)"""

        steps = tabulate(booth_result[0], headers="firstrow")
        await ctx.send(f"```{header}```\n"
                       f"```{steps}```")
