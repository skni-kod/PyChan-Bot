import discord
from discord.ext import commands
from Core.Commands.Maths.Functions.permutations_functions import *


class Permutations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='permutacje', aliases=['p', 'perm'])
    async def permutacje(self, ctx, fun, *, permstring=""):

        if fun == 'info':
            perm = smart_input(permstring.rstrip())
            if perm == -1:
                await ctx.send(embed=discord.Embed(title="Błędny zapis permutacji!",
                                                   color=discord.Color.dark_purple()))
                return

            embed = discord.Embed(title="Permutacja:",
                                  description=f" ```{permstring}```",
                                  color=discord.Color.dark_purple())
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
                            value=f"```{cycles2string(cannonical_cyclic_notation(perm))}```",
                            inline=True)
            embed.add_field(name="Numer permutacji:",
                            value=f"```{perm_number(perm)}```",
                            inline=True)
            embed.add_field(name="Następna permutacja:",
                            value=f"```{'To ostatnia permutacja w porządku leksykograficznym' if next_in_lex(perm) == -1 else perm2string(next_in_lex(perm))}```",
                            inline=True)
            embed.add_field(name="Poprzednia permutacja: ",
                            value=f"```{perm2string(perm_from_number(perm_number(perm) - 1, len(perm)))}```",
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
            embed.add_field(name="Wektor inwersi:",
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

        elif fun == 'potega':
            permstring = permstring.split()
            x = permstring.copy()
            try:
                power = int(x[-1])
            except:
                embed = discord.Embed(title="Nie podano potęgi jako liczby całkowitej",
                                      color=discord.Color.dark_purple())
                await ctx.send(embed=embed)
            else:
                x.pop()
                permstring = ' '.join(x)
                perm = smart_input(permstring.rstrip())

                if perm == -1:
                    await ctx.send(
                        embed=discord.Embed(title="Błędny zapis permutacji!",
                                            color=discord.Color.dark_purple()))
                    return

                order = perm_order(perm)
                embed = discord.Embed(title="Zadana permutacja:",
                                      description=f"```({permstring}) ^ {power}```",
                                      color=discord.Color.dark_purple())
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

        elif fun == "losuj":
            try:
                n = int(permstring)
            except:
                embed = discord.Embed(title="Podaj liczbę całkowitą, w której będzie losowana permutacja!",
                                      color=discord.Color.dark_purple())
                await ctx.send(embed=embed)
            else:
                if n < 1 or n > 20:
                    await ctx.send(embed=discord.Embed(title="Numer poza zakresem. Podaj liczbę od 1 do 20",
                                                       color=discord.Color.dark_purple()))
                    return
                perm = random_perm(n)
                embed = discord.Embed(title=f"Losowa permutacja w S{n}:",
                                      description=f"Jednowierszowo:\n```{perm2string(perm)}```\n"
                                                  f"Cyklicznie:\n```{cycles2string(perm2cycles(perm))}```",
                                      color=discord.Color.dark_purple())
                await ctx.send(embed=embed)

        elif fun == "generuj":
            args = permstring.split()
            if len(args) != 2:
                await ctx.send(embed=discord.Embed(title="Podaj poprawne argumenty: `^permutacje <numer> <Sn>`",
                                                   color=discord.Color.dark_purple()))
                return
            try:
                number = int(args[0])
                n = int(args[1])
            except:
                await ctx.send(embed=discord.Embed(title="Podaj poprawne argumenty: `^permutacje <numer> <Sn>`",
                                                   color=discord.Color.dark_purple()))
            else:
                if number > factorial(n) - 1 or number < 0:
                    await ctx.send(embed=discord.Embed(title=f"Podany numer nie występuje w S{n}",
                                                       color=discord.Color.dark_purple()))
                    return
                perm = perm_from_number(number, n)
                embed = discord.Embed(title=f"Permutacja o numerze `{number}` w `S{n}`:",
                                      description=f"Jednowierszowo:\n```{perm2string(perm)}```\n"
                                                  f"Cyklicznie:\n```{cycles2string(perm2cycles(perm))}```",
                                      color=discord.Color.dark_purple())
                await ctx.send(embed=embed)

        else:
            await ctx.send(embed=discord.Embed(title="Wspierane polecenia to ```^p info/potega/generuj/losuj```. Więcej informacji pod ```^help permutacje```",
                                               color=discord.Color.dark_purple()))
