import functools
import random
import nextcord

def pychan_decorator(func):
    @functools.wraps(func)
    async def wrapper(bot, ctx, *args, **kwargs):
        # 1% chance that it will happen
        if random.randint(1, 100) < 2:
            await sleep_time(ctx)
        else:
            await func(bot, ctx, *args, **kwargs)

    return wrapper

async def sleep_time(ctx):
    """Bot complains that it is tired """
    embed = nextcord.Embed(title='',
                           description='',
                           color=nextcord.Color.dark_purple())
    embed.set_image(
        url='https://cdn.discordapp.com/attachments/763164789458337802/831593468656222268/anime_sleepy.png')
    await ctx.send('Zmęczona jestem, napisz później :sleeping:')
    await ctx.send(embed=embed)
