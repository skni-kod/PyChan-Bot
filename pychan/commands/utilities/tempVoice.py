from typing import Union

import nextcord
from nextcord.ext import commands
import asyncio
import datetime

class TempVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            vc = await ctx.guild.create_voice_channel(name=f"Temp Voice Channel {datetime.datetime.now().strftime('%H:%m')}", category=ctx.channel.category)
            await ctx.send(f"Stworzono {vc.mention}\nJeżeli nikogo nie będzie na kanale za {60*delete_after} minut, zostanie on usunięty")
            while True:
                await asyncio.sleep(delete_after*60) # in minutes
                if vc is None:
                    break
                if len(vc.members) == 0:
                    await vc.delete()
                    break
        except nextcord.Forbidden:
            await ctx.send("Nie mam permisji do stworzenia tego kanału")

    @tempvoice.command(
        help="Usuwa podany kanał głosowy, jeżeli nie podano kanału, to usuwa kanał na którym jesteś",
        aliases = ['d', 'usun', 'u']
    )
    async def delete(self, ctx: commands.Context, channel: Union[nextcord.VoiceChannel, nextcord.StageChannel, None]):
        if channel is None:
            channel = ctx.author.voice
        if channel is None:
            await ctx.send("Nie jesteś na kanale głosowym")
            return

        if not channel.name.startswith("Temp Voice Channel"):
            await ctx.send("To nie jest tymczasowy kanał głosowy")
            return

        try:
            await channel.delete()
            await ctx.send(f"Usunięto {channel.mention}")
        except nextcord.Forbidden:
            await ctx.send("Nie mam permisji do usunięcia tego kanału")

    @tempvoice.command()
    async def check_permission(self, ctx: commands.Context):
        if ctx.guild.me.guild_permissions.manage_channels:
            await ctx.send("Mam permisje do zarządzania kanałami")
        else:
            await ctx.send("Nie mam permisji do zarządzania kanałami")