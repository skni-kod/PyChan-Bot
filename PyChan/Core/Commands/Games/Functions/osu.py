from nextcord.ext import commands
from nextcord import Color, Embed
from ossapi import Ossapi, GameMode, UserLookupKey
from config import osu_token


class Osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._osu = Ossapi(osu_token)

    @commands.group(name="osu")
    async def osu(self, _: commands.Context):
        pass

    @osu.command(name="profil", pass_context=True)
    async def profil(self, ctx: commands.Context, *, username: str):
        user = self._osu.get_user(username, GameMode.STD)
        if not user:
            return await ctx.reply('Taki gracz nie istnieje!')

        embed = Embed(color=Color.dark_purple())
        embed.set_author(name=f"Profil {user.username}",
                         url=f'https://osu.ppy.sh/u/{user.user_id}',
                         icon_url=f'https://osu.ppy.sh/images/flags/{user.country}.png')

        embed.description = (f'**Ranga globanla:** #{user.rank} (#{user.country_rank} {user.country})\n' 
                             f'**PP:** {user.pp_raw}\n'
                             f'**Celność:** {round(user.accuracy or 0, 2)}%\n'
                             f'**Liczba zagrań:** {user.playcount}\n'
                             f'**Poziom:** {user.level}')

        embed.set_footer(text=f'Dołączył {str(user.join_date)}')
        embed.set_thumbnail(url=f'https://a.ppy.sh/{user.user_id}?.jpeg')

        await ctx.send(embed=embed)

    @osu.command(name="top", pass_context=True)
    async def osutop(self, ctx: commands.Context, *, username: str):
        user = self._osu.get_user(username, GameMode.STD)
        if not user:
            return await ctx.reply('Taki gracz nie istnieje!')

        plays = self._osu.get_user_best(user.user_id, limit=5, user_type=UserLookupKey.ID)
        if not plays or not len(plays):
            return await ctx.reply('Ten użytkownik nie posiada żadnych wyników')

        embed = Embed(color=Color.dark_purple())
        embed.set_author(name=f"Top 5 gracza {user.username}",
                         url=f'https://osu.ppy.sh/u/{user.user_id}',
                         icon_url=f'https://osu.ppy.sh/images/flags/{user.country}.png')

        embed.set_thumbnail(url=f'https://a.ppy.sh/{user.user_id}?.jpeg')
        embed.description = ''

        for play in plays:
            beatmaps = self._osu.get_beatmaps(beatmap_id=play.beatmap_id)
            if not len(beatmaps):
                return await ctx.reply('Nie odnaleziono mapy')

            beatmap = beatmaps.pop()
            accuracy = (play.count_300 * 300 + play.count_100 * 100 + play.count_50 * 50)
            accuracy /= (play.count_300 + play.count_100 + play.count_50 + play.count_miss) * 300
            accuracy = round(accuracy * 100, 2)

            combo = 'FC' if play.perfect else f'x{play.max_combo}/{beatmap.max_combo}'
            hits = f'[{play.count_300}/{play.count_100}/{play.count_50}/{play.count_miss}]'
            pp = round(play.pp, 2)

            embed.description += (f'**[{beatmap.artist} - {beatmap.title} [{beatmap.version}]]'
                                  f'(https://osu.ppy.sh/b/{beatmap.beatmap_id}) '
                                  f'+{play.mods.short_name()}** '
                                  f'**{round(beatmap.star_rating, 2)}**★\n'
                                  f'● **{play.rank}** ● **{pp}PP** ● **{accuracy}%**\n'
                                  f'● {play.score} | {combo} | {hits}\n'
                                  f'● {str(play.date)}\n')

        await ctx.send(embed=embed)

    @osu.command(name="ostatni", pass_context=True)
    async def ostatni(self, ctx: commands.Context, *, username):
        user = self._osu.get_user(username, GameMode.STD)
        if not user:
            return await ctx.reply('Taki gracz nie istnieje!')

        recent_plays = self._osu.get_user_recent(user.user_id, mode=GameMode.STD, limit=1,
                                          user_type=UserLookupKey.ID)
        if not len(recent_plays):
            return await ctx.reply('Nie odnaleziono żadnych wyników')
        recent = recent_plays.pop()

        beatmap = self._osu.get_beatmaps(beatmap_id=recent.beatmap_id)
        if not beatmap or not len(beatmap):
            return await ctx.reply('Mapa którą zagrał gracz nie istnieje!')
        beatmap = beatmap[0]

        embed = Embed(color=Color.dark_purple())
        embed.set_author(
            name=f'{beatmap.artist} - {beatmap.title} [{beatmap.version}] +{recent.mods.short_name()} {round(beatmap.star_rating, 2)}★',
            url=f'https://osu.ppy.sh/b/{beatmap.beatmap_id}',
            icon_url=f'https://a.ppy.sh/{user.user_id}?.jpeg')

        combo = 'FC' if recent.perfect else f'x{recent.max_combo}/{beatmap.max_combo}'
        hits = f'[{recent.count_300}/{recent.count_100}/{recent.count_50}/{recent.count_miss}]'
        pp = round(recent.pp, 2) if recent.pp else 0
        accuracy = (recent.count_300 * 300 + recent.count_100 * 100 + recent.count_50 * 50)
        accuracy /= (recent.count_300 + recent.count_100 + recent.count_50 + recent.count_miss) * 300
        accuracy = round(accuracy * 100, 2)

        embed.description = (f'● **{recent.rank}** ● **{pp}PP** ● **{accuracy}%**\n'
                             f'● {recent.score} | {combo} | {hits}')

        embed.set_thumbnail(url=f'https://b.ppy.sh/thumb/{beatmap.beatmapset_id}l.jpg')
        embed.set_footer(text=str(recent.date))

        await ctx.send(embed=embed)
