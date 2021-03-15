import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Przechwytywanie błędu o braku komendy i innych błędów
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            embed = discord.Embed(color=discord.Color.dark_purple())
            embed.add_field(name='Błąd',
                            value='Podana komenda nie istnieje',
                            inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Niepoprawny parametr')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Brakuje wymaganego parametru')
        elif isinstance(error, Exception):
            await ctx.send('Coś poszło nie tak')
            print(error)
        else:
            print(error)

    # zdarzenia na wpisane słowa
    @commands.Cog.listener()
    async def on_message(self, message):
        # Kończy funkcje, jeśli wiadomość napisał bot
        if message.author.bot:
            return

        if str(message.content).lower() == 'pychan!':
            await message.channel.send('Wołałeś mnie Onii-chan?\n'
                                       'Napisz `^help`, aby dowiedzieć się jakie mam komendy')