import nextcord
from nextcord.ext import commands
import functools
import random

from Core.Decorators.Functions.rate_me import RateMe
from Core.Decorators.Functions.sleep_time import SleepTime


class Decorator():
    """Class contains own PyChan decorator
    """

    @staticmethod
    def pychan_decorator(func):
        """PyChan decorator processes given function

        :param func: Input function
        :return: Function return the same function as given
        """

        @functools.wraps(func)
        async def wrapper(bot, ctx, *args, **kwargs):
            """Calls function before/after given function

            :param bot: instance of Bot
            :param ctx: the context in which a command is called
            :param args: list of arguments
            :param kwargs: list of keyword arguments
            """

            # 1% chance that it will happen
            if random.randint(1, 100) < 2:
                await SleepTime.sleep_time(ctx)
            else:
                await func(bot, ctx, *args, **kwargs)
            # ask about Bot rate
            await RateMe.rate_me(ctx)

        return wrapper
