import os

import discord
import ossapi
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
        user = self.osu.get_user(username, GameMode.STD)
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

    @commands.command(pass_context=True, name='osutop')
    async def osutop(self, ctx: discord.ext.commands.Context, *username):
        """
        Gets image from attachment and extracts text from it

        :param ctx: The context in which a command is called
        :type ctx: discord.ext.commands.Context
        """
        username = ' '.join(username)

        user = self.osu.get_user(username, GameMode.STD)
        if not user:
            return await ctx.reply('Taki gracz nie istnieje!')

        plays = self.osu.get_user_best(user.user_id, limit=5, user_type=ossapi.UserLookupKey.ID)
        if not plays or not len(plays):
            return await ctx.reply('Ten użytkownik nie posiada żadnych wyników')

        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.set_author(name=f"Top 5 gracza {user.username}",
                         url=f'https://osu.ppy.sh/u/{user.user_id}',
                         icon_url=f'https://osu.ppy.sh/images/flags/{user.country}.png')

        embed.set_thumbnail(url=f'https://a.ppy.sh/{user.user_id}?.jpeg')
        embed.description = ''
        for play in plays:
            accuracy = (play.count_300 * 300 + play.count_100 * 100 + play.count_50 * 50) / 300
            accuracy = round(accuracy, 2)
            embed.description += f"""
            **[{"artist"} - {"song"} [{"diff"}]](https://osu.ppy.sh/b/{"id"}) +{play.mods.short_name()}** ({"stars"})
            ● {"todo completion"} ● **{round(play.pp, 2)}PP** {"todo pp for fc"}
            ● {'**FC**' if play.perfect else f'({play.max_combo}/{"beatmapcombo"})x'} {accuracy}%
            ● [{play.count_300}/{play.count_100}/{play.count_50}/{play.count_miss}] {play.score}
            ● Score set {str(play.date)}
            """

        await ctx.send(embed=embed)
