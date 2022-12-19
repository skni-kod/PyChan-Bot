from nextcord.ext import commands
from tabulate import tabulate
from .maths_functions import *


class BoothAlgorithm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        name='booth',
        category='Nauka',
        usage = "<P> <Q>` - gdzie P i Q to liczby całkowite",
        help = """
                Mnoży dwie liczby całkowite z użyciem algorytmu Booth\'a i wyświetla kroki.
                """
    )
    async def booth(self, ctx: commands.Context, liczba1: int, liczba2: int):
        """
        Sends the reply message to the user with step by step solution of multiplication of two integers with the booth algorithm

        :param ctx: The context in which a command is called
        :type ctx: nextcord.ext.commands.Context

        :param liczba1: First number
        :type liczba1: int

        :param liczba2: Second number
        :type liczba2: int
        """
        # conversion and performing calculations
        convert = twos_complement_equal_length(liczba1, liczba2)
        booth_result = booth(liczba1, liczba2)

        # Check if result is correct
        multiply = liczba1 * liczba2
        multiply_u2 = twos_complement(multiply)
        if len(multiply_u2) < len(booth_result[1]):
            multiply_u2 = bin_extend_in_U2(
                multiply_u2, len(booth_result[1]) - len(multiply_u2))
        if multiply_u2 != booth_result[1]:
            await ctx.send("Błąd podczas obliczeń")
            return

        # create response
        header = f"""Algorytm Bootha | Zadane parametry:
        P  = {liczba1} (DEC) = {convert[0]} (U2)
        -P = {-liczba1}(DEC) = {convert[1]} (U2)
        Q  = {liczba2} (DEC) = {convert[2]} (U2)
        Wynik operacji = {liczba1 * liczba2} (DEC) = {booth_result[1]} (U2)"""
        await ctx.send(f"```{header}```\n")

        steps = tabulate(booth_result[0], headers="firstrow")
        lines = steps.split('\n')
        steps_msg = ""
        for i in range(len(lines)):
            steps_msg = steps_msg + '\n' + lines[i]
            if (i + 1) % 30 == 0:
                await ctx.send(f"```{steps_msg}```\n")
                print(steps_msg)
                steps_msg = ""
        await ctx.send(f"```{steps_msg}```\n")
