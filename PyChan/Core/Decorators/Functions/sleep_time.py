import discord
from discord.ext import commands
import random

class SleepTime:
    """Class which contains sleep_time method
    """

    @classmethod
    async def sleep_time(cls, ctx):
        """Bot complains that it is tired

        :param ctx: the context in which a command is called
        """
        embed = discord.Embed(title='',
                              description='',
                              color=discord.Color.dark_purple())
        embed.set_image(url='https://cdn.discordapp.com/attachments/763164789458337802/831593468656222268/anime_sleepy.png')
        await ctx.send('Zmęczona jestem, napisz później :sleeping:')
        await ctx.send(embed=embed)