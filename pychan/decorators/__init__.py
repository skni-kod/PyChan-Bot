import functools
import random

from rate_me import RateMe
from sleep_time import SleepTime

def pychan_decorator(func):
    @functools.wraps(func)
    async def wrapper(bot, ctx, *args, **kwargs):
        # 1% chance that it will happen
        if random.randint(1, 100) < 2:
            await SleepTime.sleep_time(ctx)
        else:
            await func(bot, ctx, *args, **kwargs)
        # ask about Bot rate
        await RateMe.rate_me(ctx)

    return wrapper
