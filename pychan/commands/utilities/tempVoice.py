from typing import Union
import nextcord
from nextcord.ext import commands, tasks
import asyncio
import datetime


class TempVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.list = {}

    @commands.group(
        pass_context=True,
        name="tempvoice",
        category="Inne",
        usage="create <czas w minutach>\ndelete <kanał>",
        help="""Tworzy tymczasowy kanał na długość podaną przez użytkownika"""
    )
    async def tempvoice(self, ctx: commands.Context):

        if ctx.invoked_subcommand is None:
            await ctx.send_help('tempvoice')

        pass


    @tempvoice.command(
        help="Tworzy tymczasowy kanał głosowy na długość podaną przez użytkownika, domyślnie 30 minut",
        aliases = ['c', 'stworz', 's']
    )
    async def create(self, ctx: commands.Context, delete_after: int = 30):

        try:
            if ctx.author.id in self.list:
                await ctx.reply("Możesz stworzyć tylko jeden tymczasowy kanał na raz")
                return

            vc = await ctx.guild.create_voice_channel(name=f"Temp Voice Channel {datetime.datetime.today().strftime('%H:%M')}", category=ctx.channel.category)
            self.list[ctx.author.id] = vc.id
            await ctx.reply(f"Stworzono {vc.mention}\nJeżeli nikogo nie będzie na kanale za {delete_after} minut, zostanie on usunięty")
            while True:
                await asyncio.sleep(delete_after*60) # in minutes
                if vc is None:
                    break
                if len(vc.members) == 0:
                    try:
                        await vc.delete()
                        self.list.pop(ctx.author.id)
                    except nextcord.NotFound:
                        #Channel was deleted earlier
                        if ctx.author.id in self.list:
                            self.list.pop(ctx.author.id)
                        pass
                    break
        except nextcord.Forbidden:
            await ctx.reply("Nie mam permisji do stworzenia tego kanału")

    @tempvoice.command(
        help="Usuwa podany kanał głosowy, jeżeli nie podano kanału, to usuwa kanał na którym jesteś",
        aliases = ['d', 'usun', 'u']
    )
    async def delete(self, ctx: commands.Context, channel: Union[nextcord.VoiceChannel, nextcord.StageChannel, None]):
        if channel is None:
            channel = ctx.author.voice.channel
        if channel is None:
            await ctx.reply("Nie jesteś na kanale głosowym")
            return

        if not channel.name.startswith("Temp Voice Channel"):
            await ctx.reply("To nie jest tymczasowy kanał głosowy")
            return

        try:
            await ctx.reply(f"Usunięto {channel.name}")
            #Find channel in limit list and delete it
            key = self.get_user_id_from_channel_id(channel.id)
            if key:
                self.list.pop(key)
            await channel.delete()
        except nextcord.Forbidden:
            await ctx.reply("Nie mam permisji do usunięcia tego kanału")

    @tempvoice.command(
        help="Sprawdź czy bot ma permisje do zarządzania kanałami",
    )
    async def check_permission(self, ctx: commands.Context):
        if ctx.guild.me.guild_permissions.manage_channels:
            await ctx.reply("Mam permisje do zarządzania kanałami")
        else:
            await ctx.reply("Nie mam permisji do zarządzania kanałami")

    @tasks.loop(hours=1)
    async def check_temp_voice(self):
        for guild in self.bot.guilds:
            for channel in guild.voice_channels:
                if self.check_if_temp_voice_empty(channel) and self.is_channel_overdue(channel):
                    # TODO
                    # Implement if no issues are found during testing

                    # Danger !!!
                    """
                    key = self.get_user_id_from_channel_id(channel.id)
                    if key:
                        self.list.pop(key)
                    await channel.delete()
                    """

                    print(f"Channel {channel.name} should be deleted")


    @commands.Cog.listener()
    async def on_ready(self):
        self.check_temp_voice.start()

    def check_if_temp_voice_empty(self, channel: nextcord.VoiceChannel) -> bool:
        """Checks if channel is a temp voice channel and if there is no memebers connected to it"""
        return len(channel.members) <= 0 and channel.name.startswith("Temp Voice Channel")
    
    def is_channel_overdue(self, channel: nextcord.VoiceChannel) -> bool:
        """Checks if channel is older than 1 hour"""
        return datetime.datetime.now(datetime.UTC) - channel.created_at > datetime.timedelta(hours=1)

    def get_user_id_from_channel_id(self, channel_id: int) -> Union[int, None]:
        """
        Returns user_id of a temp voice channel author
        Returns None if no author is found
        """
        for key in self.list:
            if self.list[key] == channel_id:
                return key

        return None