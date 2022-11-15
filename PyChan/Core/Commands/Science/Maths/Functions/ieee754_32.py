import nextcord
from nextcord.ext import commands
from Core.Commands.Science.Maths.Functions.maths_functions import *
from Core.Decorators.decorators import Decorator


class Ieee754x32(commands.Cog):
    """
    The class contains ieee754_32 method
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context = True,
        name = "ieee754_32",
        category = "Nauka",
        usage = "<liczba>",
        help = """
                Zamienia dowolną liczbę w systemie dziesiętnym w liczbę binarną przy użyciu zapisu liczby zmiennoprzecinkowej w standarcie IEEE754 32bit
                """
    )
    @Decorator.pychan_decorator
    async def ieee754_32(self, ctx, number: float):
        """
        Sends the reply message to the user

        :param ctx: The context in which a command is called
        :type ctx: nextcord.ext.commands.Context

        :param number: Number to change
        :type number: float
        """
        data = ieee754_32(str(number))
        embed = nextcord.Embed(
            title="IEEE 754/32BIT", description="", color=nextcord.Color.dark_purple()
        )
        embed.add_field(name="Sign", value=data[0], inline=False)
        embed.add_field(name="Exponent", value=data[1], inline=False)
        embed.add_field(name="Significand", value=data[2], inline=False)
        embed.add_field(name='"IEEE 754/32BIT', value=data[3], inline=False)

        await ctx.send(embed=embed)
