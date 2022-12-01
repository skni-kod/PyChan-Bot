from typing import Dict, List
from typing_extensions import Self
from nextcord.colour import Color
from nextcord.embeds import Embed
from nextcord.ext import commands, tasks
from datetime import date, datetime, time, timedelta 
from nextcord.ext.commands.bot import Bot
from nextcord.ext.commands.context import Context
from nextcord.message import Message
from config import aoc_session_id
import requests

class Completion:
    def __init__(self, stars: str) -> None: # whatever
        self.stars = stars

    @classmethod
    def from_completion_days(cls, data) -> Self:
        stars = [' '] * 25
        icons = " ☆★"
        for i, day in data.items():
            stars[int(i) - 1] = icons[len(day)] 
        return Completion(''.join(stars))
            
class AoCMember:
    def __init__(self, id: int, local_score: int, global_score, name: str, stars: int, last_star_ts: int, completion: Completion) -> None:
        self.id: int = id
        self.local_score: int = local_score
        self.global_score = global_score 
        self.name: str = name
        self.stars: int = stars
        self.last_star_ts: int = last_star_ts
        self.completion: Completion = completion

class TrackedChannel:
    def __init__(self, leaderboard_id: int, messages: List[Message]) -> None:
        self.leaderboard_id = leaderboard_id
        self.messages = messages

# TODO:
# - split tracker into multiple messages to prevent going over the character limit
# - cache requests for potential duplicate trackers across different channels
# - formatting is stinky

class AoC(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.tracked_channels: Dict[int, TrackedChannel] = {}
        self.loop.start()

    def cog_unload(self) -> None:
        self.tracked_channels = {}
        self.loop.cancel()

    @commands.group(name='aoc')
    async def aoc(self, ctx: Context):
        '''Komendy służące do śledzenia prywatnego rankingu Advent of Code'''
        if not ctx.subcommand_passed:
            await ctx.send_help("aoc")

    @aoc.command(name='start')
    async def start(self, ctx: Context, leaderboard_id: int):
        '''Rozpoczyna śledzenie rankingu na tym kanale'''
        if self.tracked_channels.get(ctx.channel.id) is not None:
            msg = self.tracked_channels[ctx.channel.id].messages[0]
            await msg.reply(f"Ranking już jest śledzony! Wpisz `{ctx.prefix}aoc stop` aby wyłączyć śledzenie")
        else:
            self.tracked_channels[ctx.channel.id] = TrackedChannel(leaderboard_id, [await ctx.message.channel.send(":thumbsup:")])
            self.loop.restart()

    @aoc.command(name='stop')
    async def stop(self, ctx: Context):
        '''Zatrzymuje śledzenie rankinku na tym kanale'''
        if self.tracked_channels.get(ctx.channel.id) is not None:
            self.tracked_channels.pop(ctx.channel.id)
            await ctx.reply("Śledzenie zostało wstrzymane")
        else:
            await ctx.reply("Śledzenie nawet nie jest włączone!")

    @aoc.command(name='lista')
    async def list(self, ctx: Context):
        '''Wyświetla listę kanałów z śledzeniem rankingów'''
        embed = Embed(color=Color.dark_purple())
        embed.title = 'Kanały z aktywnym śledzeniem rankingów AoC'
        for channel_id, tracker in self.tracked_channels.items():
            msg = tracker.messages[0]
            embed.description = f'<#{channel_id}> → (Link) [https://discord.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}/]\n'
        await ctx.reply(embed=embed)

    @tasks.loop(minutes=15)
    async def loop(self):
        tomorrow = datetime.combine(date.today(), time(6, 0)) # timezone issue :clown:
        tomorrow += timedelta(days=1)
        for _, tracked_channel in self.tracked_channels.items():
            data = self.fetch_data(tracked_channel.leaderboard_id)
            extracted_data = self.parse_data(data)
            rows = self.get_rows(extracted_data)

            for msg in tracked_channel.messages:
                await msg.edit(content='```\n' + ''.join(rows) + '\n```' +
                               f'**Ostatnia aktualizacja** <t:{int(datetime.today().timestamp())}:R>\n' +
                               f'**Kolejne wyzwanie** <t:{int(tomorrow.timestamp())}:R>')

    def fetch_data(self, leaderboard_id):
        leaderboard_id = int(leaderboard_id)
        api_url = f"https://adventofcode.com/{datetime.today().year}/leaderboard/private/view/{leaderboard_id}.json"
        r = requests.get(api_url, cookies={"session": aoc_session_id})
        return r.json()
    
    def parse_data(self, data) -> List[AoCMember]:
        tab: List[AoCMember] = []
        for _, md in data['members'].items():
            member = AoCMember(md['id'], md['local_score'], md['global_score'], md['name'], md['stars'], md['last_star_ts'], Completion.from_completion_days(md['completion_day_level']))
            tab.append(member)
        tab = sorted(tab, key=lambda x: x.local_score, reverse=True)
        return tab

    def get_rows(self, data: List[AoCMember]) -> List[str]:
        rows = []
        row_format = '{:2} | {:18}| {:6} | {}\n'
        header = row_format.format(".", "Uczestnik", "Punkty", "Gwiazdki") 
        rows.append(header)
        for i, m in enumerate(data):
            rows.append(row_format.format(i + 1, m.name, m.local_score, m.completion.stars.rstrip()))
        return rows

