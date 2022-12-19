import nextcord
from nextcord.ext import commands
from .permutations_functions import *


class Permutations(commands.Cog):
    """
        The class contains permutations method
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        invoke_without_command = True,
        pass_context = True,
        name = 'permutacje',
        aliases = ['p', 'perm'],
        category = 'Nauka',
        help = """
               Szereg funkcji służących do obliczania permutacji.
                
               Przykłady zapisu permutacji: `<5 2 3 1 4>` lub `(1 5 4)(2)(3)` lub `<5 1 3 2 4>#(4 2 3)#(1 2 5)`
               Symbol `#` oznacza mnożenie permutacji.
               """
    )
    async def permutacje(self, ctx):
        """
        Aggregates all the subcommands for the permutations command

        :param ctx: The context in which a command is called
        :type ctx: nextcord.ext.commands.Context
        """
        pass

    @permutacje.command(
        name='info',
        usage = '<permutacja>',
        help = """
               Wyświetla informacje o permutacji
               """
    )
    async def info(self, ctx, *, permstring):
        """
        Sends some basics info about permutation

        :param ctx: The context in which a command is called
        :type ctx: nextcord.ext.commands.Context

        :param permstring: Permutation as string
        :type permstring: string
        """
        perm = smart_input(permstring.rstrip())
        if perm == -1:
            await ctx.send(embed=nextcord.Embed(title="Błędny zapis permutacji!", color=nextcord.Color.dark_purple()))
            return

        embed = nextcord.Embed(title="Permutacja:",
                              description=f" ```{permstring}```",
                              color=nextcord.Color.dark_purple())
        embed.add_field(name="Postać jednowierszowa:",
                        value=f"```{perm2string(perm)}```",
                        inline=True)
        embed.add_field(name="Postać cyklowa:",
                        value=f"```{cycles2string(perm2cycles(perm))}```",
                        inline=True)
        embed.add_field(name="Postać cyklowa bez punktów stałych:",
                        value=f"```{cycles2string(perm2cycles_without_fixed(perm))}```",
                        inline=True)
        embed.add_field(name="Kanoniczna postać cyklowa:",
                        value=f"```{cycles2string(canonical_cycle_notation(perm))}```",
                        inline=True)
        embed.add_field(name="Numer permutacji:",
                        value=f"```{perm_number(perm)}```",
                        inline=True)
        embed.add_field(name="Następna permutacja:",
                        value=f"```{'To ostatnia permutacja w porządku leksykograficznym' if next_in_lex(perm) == -1 else perm2string(next_in_lex(perm))}```",
                        inline=True)
        embed.add_field(name="Poprzednia permutacja: ",
                        value=f"```{'To pierwsza permutacja w porządku leksykograficznym' if perm_number(perm) == 0 else perm2string(perm_from_number(perm_number(perm) - 1, len(perm)))}```",
                        inline=True)
        embed.add_field(name="Rząd permutacji:",
                        value=f"```{perm_order(perm)}```",
                        inline=True)
        embed.add_field(name="Typ permutacji:",
                        value=f"```{perm_type(perm)}```",
                        inline=True)
        embed.add_field(name=f"Liczba inwersji:",
                        value=f"```{all_inversions_count(perm)}```",
                        inline=True)
        embed.add_field(name=f"Wszystkie inwersje:",
                        value=f"```{cycles2string(all_inversions(perm))}```",
                        inline=False)
        embed.add_field(name="Wektor inwersji:",
                        value=f"```{inversion_vector(perm)}```",
                        inline=True)
        embed.add_field(name="Cykle parzystej długości:",
                        value=f"```{perm_cpd(perm)}```",
                        inline=True)
        embed.add_field(name="Cykle nieparzystej długości:",
                        value=f"```{perm_cpnd(perm)}```",
                        inline=True)
        embed.add_field(name="Znak permutacji:",
                        value=f"```{perm_sign(perm)}```",
                        inline=True)
        embed.add_field(name="Własności:",
                        value=f"```Nieporządek:  {'✅' if is_derangement(perm) else '❌ '}\n"
                              f"Inwolucja:    {'✅' if is_involution(perm) else '❌ '}\n"
                              f"Transpozycja: {'✅' if is_transposition(perm) else '❌ '}\n"
                              f"Jednocyklowa: {'✅' if is_onecyclic(perm) else '❌ '}\n"
                              f"Parzysta:     {'✅' if is_even(perm) else '❌ '}\n"
                              f"Nieparzysta:  {'✅' if is_odd(perm) else '❌ '}```",
                        inline=True)
        await ctx.send(embed=embed)

    @permutacje.command(
        name='potega', 
        aliases=["potęga"],
        usage = '<wykładnik> <permutacja>',
        help = """
               Podnosi permutację do danej potęgi
               """
    )
    async def potega(self, ctx, power: int, *, permstring):
        """
        Sends permutation raised to given power

        :param ctx: The context in which a command is called
        :type ctx: nextcord.ext.commands.Context

        :param power: Exponent of the power
        :type power: int

        :param permstring: Permutation as string
        :type permstring: string
        """
        perm = smart_input(permstring.rstrip())
        if perm == -1:
            await ctx.send(embed=nextcord.Embed(title="Błędny zapis permutacji!", color=nextcord.Color.dark_purple()))
            return

        order = perm_order(perm)
        embed = nextcord.Embed(title="Zadana permutacja:",
                              description=f"```({permstring}) ^ {power}```",
                              color=nextcord.Color.dark_purple())
        embed.add_field(name="Poermutacja po uproszczeniu:",
                        value=f"Jednowierszowo:\n```({perm2string(perm)}) ^ {power}```",
                        inline=True)
        embed.add_field(name="\u200b",
                        value=f"Cyklowo:\n```({cycles2string(perm2cycles(perm))}) ^ {power}```",
                        inline=True)

        if power not in [-1, 0, 1]:
            embed.add_field(name="Potęga modulo rząd:",
                            value=f"```{abs(power)} modulo {order} = {power % order}```",
                            inline=False)
        perm = perm_power(perm, abs(power))
        embed.add_field(name="Wynik operacji: ",
                        value=f"```{perm2string(perm)}```",
                        inline=False)

        if power < 0:
            perm = perm_inverse(perm)
            embed.add_field(name="Poermutacja po odwróceniu (^-1):",
                            value=f"Jednowierszowo:\n```{perm2string(perm)}```",
                            inline=True)
            embed.add_field(name="\u200b",
                            value=f"Cyklowo:\n```{cycles2string(perm2cycles(perm))}```",
                            inline=True)
        await ctx.send(embed=embed)

    @permutacje.command(
        name='losuj',
        usage = '<Sn>',
        help = """
               Losuje permutację w podanym Sn
               """
    )
    async def losuj(self, ctx, n: int):
        """
        Sends random permutation

        :param ctx: The context in which a command is called
        :type ctx: nextcord.ext.commands.Context

        :param n: Max number in permutation
        :type n: int
        """
        if n < 1 or n > 20:
            await ctx.send(embed=nextcord.Embed(title="Numer poza zakresem. Podaj liczbę od 1 do 20",
                                               color=nextcord.Color.dark_purple()))
            return

        perm = random_perm(n)
        embed = nextcord.Embed(title=f"Losowa permutacja w S{n}:",
                              description=f"Jednowierszowo:\n```{perm2string(perm)}```\n"
                                          f"Cyklowo:\n```{cycles2string(perm2cycles(perm))}```",
                              color=nextcord.Color.dark_purple())
        await ctx.send(embed=embed)

    @permutacje.command(
        name='generuj',
        usage = '<numer permutacji> <Sn>',
        help = """
               Generuje permutację na podstawie numeru w porządku leksykograficznym
               """
    )
    async def generuj(self, ctx, number: int, n: int):
        """
        Sends permutation generated from given number

        :param ctx: The context in which a command is called
        :type ctx: nextcord.ext.commands.Context

        :param number: Number of permutation
        :type number: int

        :param n: Max number in permutation
        :type n: int
        """
        if number > factorial(n) - 1 or number < 0:
            await ctx.send(
                embed=nextcord.Embed(title=f"Podany numer nie występuje w S{n}", color=nextcord.Color.dark_purple()))
            return
        perm = perm_from_number(number, n)
        embed = nextcord.Embed(title=f"Permutacja o numerze `{number}` w `S{n}`:",
                              description=f"Jednowierszowo:\n```{perm2string(perm)}```\n"
                                          f"Cyklowo:\n```{cycles2string(perm2cycles(perm))}```",
                              color=nextcord.Color.dark_purple())
        await ctx.send(embed=embed)
