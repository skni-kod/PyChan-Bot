import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title='Help',
                              description='Wpisz `^help <nazwa_komendy>` aby uzyskać więcej informacji.\n'
                                          '\n'
                                          'Dostępne komendy:',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Matematyka',
                        value='`zamiana`, `zamiana+`, `ieee754_32`, `ieee754_64`',
                        inline=False)

        await ctx.send(embed=embed)

    @help.command(name='zamiana')
    async def zamiana_help(self, ctx):
        embed = discord.Embed(title='Zamiana',
                              description='Zamienia liczbę z dowolnego systemu liczbowego na inny z przedziału <2,16>',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Składnia',
                        value='`zamiana <system z którego zamienamy> <do którego zamieniamy> <liczba>`',
                        inline=False)
        await ctx.send(embed=embed)

    @help.command(name='zamiana+')
    async def zamiana_z_rozpisaniem_help(self, ctx):
        embed = discord.Embed(title='Zamiana+',
                              description='Zamienia liczbę z dowolnego systemu liczbowego na inny z przedziału <2,16>, lecz wraz z rozpisaniem pisemnym zamiany liczb',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Składnia',
                        value='`zamiana+ <system z którego zamienamy> <do którego zamieniamy> <liczba>`',
                        inline=False)
        await ctx.send(embed=embed)

    @help.command(name='ieee754_32')
    async def ieee754_32_help(self, ctx):
        embed = discord.Embed(title='IEEE754 32bit',
                              description='Zamienia dowolną liczbę w systemie dziesiętnym w liczbę binarną przy użyciu zapisu liczby zmiennoprzecinkowej w standarcie IEEE754 32bit',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Składnia',
                        value='`ieee754_32 <liczba>`',
                        inline=False)
        await ctx.send(embed=embed)

    @help.command(name='ieee754_64')
    async def ieee754_64_help(self, ctx):
        embed = discord.Embed(title='IEEE754 64bit',
                              description='Zamienia dowolną liczbę w systemie dziesiętnym w liczbę binarną przy użyciu zapisu liczby zmiennoprzecinkowej w standarcie IEEE754 64bit',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Składnia',
                        value='`ieee754_64 <liczba>`',
                        inline=False)
        await ctx.send(embed=embed)
