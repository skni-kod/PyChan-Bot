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
                        value='`zamiana`, `zamiana+`, `ieee754_32`, `ieee754_64`, `permutacje`',
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

    @help.command(name='permutacje')
    async def permutacje_help(self, ctx):
        embed = discord.Embed(title='permutacje',
                              description='Szereg funkcji służących do obliczania permutacji',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Składnia',
                        value='`permutacje info <permutacja>` - wyświetla informacje o permutacji\n'
                              '`permutacje losuj <Sn>` - losuje permutacje w podanym Sn\n'
                              '`permutacje potega <permutacja> <wykładnik>` - Podnosi permutację do potęgi\n'
                              '`permutacje generuj <numer permutacji> <Sn>` - Generuje permutację na podstawie numeru w porządku leksykograficznym\n',
                        inline=False)
        embed.add_field(name='Aliasy komendy',
                        value='`permutacje`, `perm`, `p`',
                        inline=False)
        embed.add_field(name='Dodatkowe informacje',
                        value='Przykłady zapisu permutacji: `<5 2 3 1 4>` lub `(1 5 4)(2)(3)` lub `<5 1 3 2 4>#(4 2 3)#(1 2 5)`',
                        inline=False)
        await ctx.send(embed=embed)
