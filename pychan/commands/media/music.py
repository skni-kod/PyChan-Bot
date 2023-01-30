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
        self.YDL_OPTIONS = {'format': 'bestaudio',
                            'noplaylist': 'True', 'youtube_include_dash_manifest': False}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.queue = []
        self.queue_embed = []
        self.queue_ctx = []

    def get_colour(self, id):
        """Function returns main colour of song thumbnail"""
        url = f'https://img.youtube.com/vi/{id}/default.jpg'
        fd = urlopen(url)
        f = BytesIO(fd.read())
        color_thief = ColorThief(f)
        rgb = list(color_thief.get_palette(color_count=6))
        which_palette = int(len(rgb) / 2)
        colour = Color.from_rgb(
            rgb[which_palette][0], rgb[which_palette][1], rgb[which_palette][2])
        return colour

    async def manage_queue(self):
        if len(self.queue) > 0:
            voice = get(self.bot.voice_clients, guild=self.queue_ctx[0].guild)
            voice.play(FFmpegOpusAudio(self.queue[0], **self.FFMPEG_OPTIONS), after=lambda p: self.manage_queue())
            await self.queue_ctx[0].send(embed=self.queue_embed[0])
            self.queue.pop(0)
            self.queue_embed.pop(0)
            self.queue_ctx.pop(0)
        else:
            self.queue.pop(0)
            self.queue_embed.pop(0)
            self.queue_ctx.pop(0)

    @commands.group(
        name="muzyka",
        category="Media"
    )
    async def playing_music(self, ctx: commands.Context):
        '''Komendy związane z graniem muzyki'''
        pass

    @playing_music.command(
        name='join',
        usage='',
        help="""Bot dołącza do kanału głosowego gdzie jest użytkownik"""
    )
    async def join(self, ctx):
        if not ctx.guild.voice_client in self.bot.voice_clients:
            channel = ctx.author.voice.channel
            await channel.connect()

    @playing_music.command(
        name='disconnect',
        usage='',
        help="""Bot opuszcza kanał głosowy"""
    )
    async def disconnect(self, ctx):
        if ctx.guild.voice_client in self.bot.voice_clients:
            await ctx.voice_client.disconnect()

    @playing_music.command(
        name='play',
        usage='<link YT do piosenki> lub <słowa kluczowe>',
        help="""Bot dołącza do kanału głosowego gdzie jest użytkownik i gra muzykę"""
    )
    async def play(self, ctx, *, args):
        if not ctx.guild.voice_client in self.bot.voice_clients:
            channel = ctx.author.voice.channel
            await channel.connect()
        
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            if validators.url(args) != 1:
                args = unidecode(args)
                info = ydl.extract_info(
                    f"ytsearch: {args}", download=False)
                title = info["entries"][0]["title"]
                id = info["entries"][0]["id"]
                thumbnail = f'https://img.youtube.com/vi/{id}/0.jpg'
                duration = timedelta(
                    seconds=info['entries'][0]['duration'])
                URL = info["entries"][0]["url"]
            else:
                if '/shorts/' in args:
                    args = "https://www.youtube.com/watch?v=" + \
                        str(args[-11:])
                info = ydl.extract_info(args, download=False)
                title = info['title']
                id = info["id"]
                thumbnail = f'https://img.youtube.com/vi/{id}/0.jpg'
                duration = timedelta(seconds=info['duration'])
                URL = info['formats'][0]['url']
            embed = nextcord.Embed(
                title=title, description=f"Czas trwania: {duration}", color=self.get_colour(id))
            embed.set_thumbnail(url=thumbnail)
            self.queue_embed.append(embed)
            self.queue.append(URL)
            self.queue_ctx.append(ctx)
        if voice.is_playing() == False:
            await self.manage_queue()
        else:
            await ctx.send(embed=nextcord.Embed(title="**Już coś gram, ale piosenka została dodana do kolejki! 🎵**", color=Color.blue()))
            

    @playing_music.command(
        name='skip',
        usage='',
        help="""Bot pomija piosenkę"""
    )
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_playing() and ctx.guild.voice_client in self.bot.voice_clients:
                voice.stop()
                await ctx.send(embed=nextcord.Embed(title="**Piosenka pominięta! 😢**", color=Color.dark_gold()))
            else:
                await ctx.send(embed=nextcord.Embed(title="**Aktualnie nie gram muzyki!**", color=Color.dark_green()))
        except:
            await ctx.send(embed=nextcord.Embed(title="**Aktualnie nie gram muzyki!**", color=Color.dark_green()))
