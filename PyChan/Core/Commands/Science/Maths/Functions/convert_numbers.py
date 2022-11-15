import nextcord
from nextcord.ext import commands
from Core.Commands.Science.Maths.Functions.maths_functions import *
from Core.Decorators.decorators import Decorator


class ConvertNumbers(commands.Cog):
    """
    The class contains convert_numbers method
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context= True,
        name = "zamiana",
        category = "Nauka",
        usage = "zamiana <system z którego zamienamy> <system do którego zamieniamy> <liczba>",
        help = {"""
               Zamienia liczbę z dowolnego systemu liczbowego na inny z przedziału <2,16>
               """
        }
    )
    @Decorator.pychan_decorator
    async def convert_numbers(self, ctx, from_param: int, to_param: int, number):
        """
        Sends the reply message to the user

        :param ctx: The context in which a command is called
        :type ctx: nextcord.ext.commands.Context

        :param from_param: Base number system
        :type from_param: int

        :param to_param: Target number system
        :type to_param: int

        :param number: Number to change
        :type number: str

        :raises commands.errors.BadArgument: User entered wrong arguments
        """
        if (from_param < 2 or from_param > 16) or (to_param < 2 or to_param > 16):
            raise commands.errors.BadArgument

        converted_number = ""

        if from_param == 10:
            converted_number = dec_float_to_another(to_param, number)["converted"][
                "number"
            ]
        elif to_param == 10:
            converted_number = another_float_to_dec(from_param, number)["dec"]
        else:
            converted_number = another_float_to_dec(from_param, number)["dec"]
            converted_number = dec_float_to_another(to_param, converted_number)[
                "converted"
            ]["number"]

        await ctx.send(f"{number} ({from_param}) = {converted_number} ({to_param})")
