from Core.Decorators.decorators import Decorator

import nextcord
from nextcord.ext import commands
from nextcord import FFmpegOpusAudio, Color
from nextcord.utils import get

from youtube_dl import YoutubeDL
import validators
from datetime import timedelta
from unidecode import unidecode

from urllib.request import urlopen
from colorthief import ColorThief
from io import BytesIO


class PlayingMusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'youtube_include_dash_manifest': False}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def get_colour(self, id):
        """Funkcja zwraca jeden z glownych kolorow na miniaturce piosenki"""
        url = f'https://img.youtube.com/vi/{id}/default.jpg'
        fd = urlopen(url)
        f = BytesIO(fd.read())
        color_thief = ColorThief(f)
        rgb = list(color_thief.get_palette(color_count=6))
        which_palette = int(len(rgb) / 2)
        colour = Color.from_rgb(rgb[which_palette][0], rgb[which_palette][1], rgb[which_palette][2])
        return colour

    @commands.group(
        name = "muzyka",
        category = "Muzyka"
    )
    
    async def playing_music(self, ctx: commands.Context):
        '''Komendy związane z dołączaniem do kanału'''
        pass

    @playing_music.command(
        name = 'join',
        usage = '',
        help = """Bot dołącza do kanału głosowego"""
    )

    @Decorator.pychan_decorator
    async def join(self, ctx):
        if not ctx.guild.voice_client in self.bot.voice_clients:
            channel = ctx.author.voice.channel
            await channel.connect()

    @playing_music.command(
        name = 'disconnect',
        usage = '',
        help = """Bot opuszcza kanał głosowy"""
    )

    @Decorator.pychan_decorator
    async def disconnect(self, ctx):
        if ctx.guild.voice_client in self.bot.voice_clients:
            await ctx.voice_client.disconnect()

    @playing_music.command(
        name = 'play',
        usage = '',
        help = """Bot gra muzykę"""
    )

    @Decorator.pychan_decorator
    async def play(self, ctx, *, args):
        if not ctx.guild.voice_client in self.bot.voice_clients:
            channel = ctx.author.voice.channel
            await channel.connect()

        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.send(embed=nextcord.Embed(title="**Juz cos gram! 🎵**", color=Color.blue()))
        else:
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                if validators.url(args) != 1:
                    args = unidecode(args)
                    info = ydl.extract_info(f"ytsearch: {args}", download=False)
                    title = info["entries"][0]["title"]
                    id = info["entries"][0]["id"]
                    thumbnail = f'https://img.youtube.com/vi/{id}/0.jpg'
                    duration = timedelta(seconds=info['entries'][0]['duration'])
                    URL = info["entries"][0]["url"]  

                else:
                    if '/shorts/' in args:
                        args = "https://www.youtube.com/watch?v=" + str(args[-11:])
                    info = ydl.extract_info(args, download=False)
                    title = info['title']
                    id = info["id"]
                    thumbnail =  f'https://img.youtube.com/vi/{id}/0.jpg'
                    duration = timedelta(seconds=info['duration'])
                    URL = info['formats'][0]['url']
                embed = nextcord.Embed(title=title, description=f"Czas trwania: {duration}", color=self.get_colour(id))
                embed.set_thumbnail(url=thumbnail)
                await ctx.send(embed=embed)

            voice.play(FFmpegOpusAudio(URL, **self.FFMPEG_OPTIONS))

    @playing_music.command(
        name = 'skip',
        usage = '',
        help = """Bot pomija piosenkę"""
    )

    @Decorator.pychan_decorator
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        try:
            voice.stop()
            await ctx.send(embed=nextcord.Embed(title="**Piosenka pominięta!**", color=Color.dark_gold()))
        except:
            await ctx.send(embed=nextcord.Embed(title="**Aktualnie nie gram muzyki!**", color=Color.dark_gold()))