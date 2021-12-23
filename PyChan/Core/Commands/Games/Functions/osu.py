import os

import discord
from discord.ext import commands
from ossapi import Ossapi, GameMode
from config import osu_token


class Osu(commands.Cog):
    """
    Class contains osu methods
    """

    def __init__(self, bot):
        """
        Constructor method
        """
        self.bot = bot
        self.osu = Ossapi(osu_token)

    @commands.command(pass_context=True, name='osu')
    async def osu(self, ctx: discord.ext.commands.Context, *username):
        """
        Gets image from attachment and extracts text from it

        :param ctx: The context in which a command is called
        :type ctx: discord.ext.commands.Context
        """
        username = ' '.join(username)
        user = rank = self.osu.get_user(username, GameMode.STD)
        if not user:
            return await ctx.reply('Taki gracz nie istnieje!')

        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.set_author(name=f"Profil {user.username}",
                         url=f'https://osu.ppy.sh/u/{user.user_id}',
                         icon_url=f'https://osu.ppy.sh/images/flags/{user.country}.png')

        embed.description = f"""
        **Ranga globanla:** #{user.rank} (#{user.country_rank} {user.country})
        **PP:** {user.pp_raw}
        **Celność:** {round(user.accuracy, 2)}%
        **Liczba zagrań:** {user.playcount}
        **Poziom:** {user.level}
        """

        embed.set_footer(text=f'Dołączył {str(user.join_date)}')
        embed.set_thumbnail(url=f'https://a.ppy.sh/{user.user_id}?.jpeg')

        await ctx.send(embed=embed)
