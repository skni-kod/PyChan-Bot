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
            accuracy = (play.count_300 * 300 + play.count_100 * 100 + play.count_50 * 50)
            accuracy /= (play.count_300 + play.count_100 + play.count_50 + play.count_miss) * 300
            accuracy = round(accuracy * 100, 2)
            embed.description += f"""
            **[{"artist"} - {"song"} [{"diff"}]](https://osu.ppy.sh/b/{"id"}) +{play.mods.short_name()}** ({"stars"})
            ● {"todo completion"} ● **{round(play.pp, 2)}PP** {"todo pp for fc"}
            ● {'**FC**' if play.perfect else f'({play.max_combo}/{"beatmapcombo"})x'} {accuracy}%
            ● [{play.count_300}/{play.count_100}/{play.count_50}/{play.count_miss}] {play.score}
            ● Score set {str(play.date)}
            """

        await ctx.send(embed=embed)

    @commands.command(pass_context=True, name='recent')
    async def recent(self, ctx: discord.ext.commands.Context, *username):
        username = ' '.join(username)

        user = self.osu.get_user(username, GameMode.STD)
        if not user:
            return await ctx.reply('Taki gracz nie istnieje!')

        recent = self.osu.get_user_recent(user.user_id, mode=ossapi.GameMode.STD, limit=1, user_type=ossapi.UserLookupKey.ID)
        if not recent or not len(recent):
            return await ctx.reply('Coś poszło nie tak')
        recent = recent[0]

        beatmap = self.osu.get_beatmaps(beatmap_id=recent.beatmap_id)
        if not beatmap or not len(beatmap):
            return await ctx.reply('Mapa którą zagrał gracz nie istnieje!')
        beatmap = beatmap[0]

        embed = discord.Embed(color=discord.Color.dark_purple())
        embed.set_author(
            name=f'{beatmap.artist} - {beatmap.title} [{beatmap.version}] +{recent.mods.short_name()} ({round(beatmap.star_rating, 2)})',
            url=f'https://osu.ppy.sh/b/{beatmap.beatmap_id}',
            icon_url=f'https://a.ppy.sh/{user.user_id}?.jpeg')

        combo = 'FC' if recent.perfect else f'x{recent.max_combo}/{beatmap.max_combo}'
        hits = f'[{recent.count_300}/{recent.count_100}/{recent.count_50}/{recent.count_miss}]'
        pp = round(recent.pp, 2) if recent.pp else 0
        accuracy = (recent.count_300 * 300 + recent.count_100 * 100 + recent.count_50 * 50)
        accuracy /= (recent.count_300 + recent.count_100 + recent.count_50 + recent.count_miss) * 300
        accuracy = round(accuracy * 100, 2)

        embed.description = f"""
        ● {recent.rank} | {accuracy}%
        ● {recent.score} | {combo} | {hits} | {pp}PP
        """

        embed.set_thumbnail(url=f'https://b.ppy.sh/thumb/{beatmap.beatmapset_id}l.jpg')
        embed.set_footer(text=str(recent.date))

        await ctx.reply(embed=embed)
