import discord
from discord.ext import commands
from Core.Decorators.decorators import Decorator
from Core.Commands.Settings.Functions.get_server_prefix import GetServerPrefix


class Help(commands.Cog):
    """Class contains help methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @Decorator.pychan_decorator
    async def help(self, ctx):
        """Sends message with built-in funtions

        :param ctx: the context in which a command is called
        :type ctx: discord.ext.commands.Context
        """
        prefix = GetServerPrefix.get_server_prefix(self, ctx)
        embed = discord.Embed(title='Help',
                              description=f'Wpisz `{prefix}help <nazwa_komendy>` aby uzyskać więcej informacji.\n'
                                          '\n'
                                          'Dostępne komendy:',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Matematyka',
                        value='`zamiana`, `zamiana+`, `ieee754_32`, `ieee754_64`, `permutacje`, `booth`',
                        inline=False)
        embed.add_field(name='Obraz',
                        value='`ocr`, `apod`, `qr`',
                        inline=False)
        embed.add_field(name='SKNIKOD',
                        value='`listaCzlonkow`',
                        inline=False)
        embed.add_field(name='Tekst',
                        value='`ciekawostka`',
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
                              '`permutacje potega <wykładnik> <permutacja>` - Podnosi permutację do potęgi\n'
                              '`permutacje generuj <numer permutacji> <Sn>` - Generuje permutację na podstawie numeru w porządku leksykograficznym\n',
                        inline=False)
        embed.add_field(name='Aliasy komendy',
                        value='`permutacje`, `perm`, `p`',
                        inline=False)
        embed.add_field(name='Dodatkowe informacje',
                        value='Przykłady zapisu permutacji: `<5 2 3 1 4>` lub `(1 5 4)(2)(3)` lub `<5 1 3 2 4>#(4 2 3)#(1 2 5)`',
                        inline=False)
        await ctx.send(embed=embed)

    @help.command(name='booth')
    async def booth_help(self, ctx):
        embed = discord.Embed(title='Algorytm Booth\'a',
                              description='Mnoży dwie liczby całkowite z użyciem algorytmu Booth\'a i wyświetla kroki.',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Składnia',
                        value='`booth <P> <Q>` - gdzie P i Q to liczby całkowite',
                        inline=False)
        await ctx.send(embed=embed)

    @help.command(name='ocr')
    async def ocr_help(self, ctx):
        embed = discord.Embed(title='OCR',
                              description='Wyciąga tekst z obrazka i wysyła na czat \n'
                                          'Należy pamiętać o dołączeniu obrazka .jpg lub .png do wiadomości',
                              color=discord.Color.dark_purple())
        await ctx.send(embed=embed)

    @help.command(name='qr')
    async def qr_help(self, ctx):
        embed = discord.Embed(title='QR',
                              description='Tworzy kod QR\n'
                                          'Przyjmuje link do strony jako argument',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Składnia',
                        value='`qr <link>`',
                        inline=False)
        await ctx.send(embed=embed)

    @help.command(name='apod')
    async def apod_help(self, ctx):
        embed = discord.Embed(title='Astronomy picture of the day',
                              description='Wysyła astronomiczne zdjęcie lub film dnia wraz z opisem',
                              color=discord.Color.dark_purple())
        await ctx.send(embed=embed)

    @help.command(name='listaCzlonkow')
    async def get_members_projects_help(self, ctx):
        embed = discord.Embed(title='listaCzlonkow',
                              description='Wysyła plik txt z aktualną listą członków z rolą `Członek` i przypisanymi do nich projektami',
                              color=discord.Color.dark_purple())
        await ctx.send(embed=embed)

    @help.command(name='ciekawostka')
    async def facts_help(self, ctx):
        embed = discord.Embed(title='ciekawostka',
                              description='Wysyła losową ciekawostkę',
                              color=discord.Color.dark_purple())
        await ctx.send(embed=embed)


    
