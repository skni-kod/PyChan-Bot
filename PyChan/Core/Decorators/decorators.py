import discord
from discord.ext import commands
import functools
import random

from Core.Decorators.Functions.rate_me import Rate_me
from Core.Decorators.Functions.sleep_time import Sleep_time

class Decorator():
    @staticmethod
    def pychan_decorator(func):
        @functools.wraps(func)
        async def wrapper(bot, ctx, *args, **kwargs):
            # 1% szans że funkcja się nie wykona
            if random.randint(1,100) < 2:
                await Sleep_time.sleep_time(ctx)
            else:
                await func(bot, ctx, *args, **kwargs)
            # zapytanie o ocene pracy bota
            await Rate_me.rate_me(ctx)
        return wrapper