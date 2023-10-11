import nextcord
from nextcord.ext import commands
import random

class Chomsky(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        name="chomsky",
        usage="<reguly>",
        category="Nauka",
        help="""Funkcja do przekształcanie reguł produkcji do postaci Chomskiego reguły należy podać w postaci:
                (symbole terminalne);(symbol produkujący reguły)>(reguły produkowane)
                reguły i symbole należy odzlenać przecinkiem przykładowy zapis:
                x,y,z;S>YS,Yx,X;Y>Yx;X>xy,XZ;Z>Zz,x
                lambde zapisywać symbolem '^'
             """
    )
    async def chomsky(self, ctx, *, rules: str):


        terminal_symbols = []
        production_rules = []
        start_symbols = []
        input_rules = rules
        stan = str("początek")
        input_rules.strip()
        input_rules = input_rules.replace(",", " ")
        input_rules = input_rules.replace(";", " ; ")
        input_rules = input_rules.replace(">", " > ")
        input_rules = input_rules.split()
        zmienna_pomocnicza = -1
        for i in range(0, len(input_rules)):
            match input_rules[i]:
                case ";":
                    stan = ";"
                    zmienna_pomocnicza = zmienna_pomocnicza + 1
                case ">":
                    stan = ">"
                case _:
                    match stan:
                        case "początek":
                            terminal_symbols.append(input_rules[i])
                        case ";":
                            start_symbols.append(input_rules[i])
                            production_rules.append([])
                        case ">":
                            production_rules[zmienna_pomocnicza].append(input_rules[i])

        # Nie zmieniać
        symbols = []
        for i in range(0, len(production_rules)):
            for x in range(0, len(production_rules[i])):
                for a in range(0, len(production_rules[i][x])):
                    if production_rules[i][x][a] not in symbols:
                        symbols.append(production_rules[i][x][a])

        """
        Skracanie długości produkcji do pordukowania
        1-2 symboli
        """
        for i in range(0, len(production_rules)):
            for x in range(0, len(production_rules[i])):
                if len(production_rules[i][x]) == 1:
                    pass
                elif len(production_rules[i][x]) == 2:
                    pass
                else:
                    while len(production_rules[i][x]) > 2:
                        new_sybol = chr(random.randint(65, 91))
                        if new_sybol in start_symbols:
                            new_sybol = chr(random.randint(65, 90))
                        else:

                            element = production_rules[i][x][:-2] + new_sybol
                            temp_list = [production_rules[i][x][-2:]]
                            production_rules.append(temp_list)
                            production_rules[i][x] = element
                        start_symbols.append(new_sybol)

        """
        zamiana reguł produkcji produkujących 2 symbole w tym co najmniej 1 terminalny"
        """

        for i in range(0, len(terminal_symbols)):
            zmienna_pomocnicza = 0
            for x in range(0, len(production_rules)):
                if len(production_rules[x]) == 1 and production_rules[x][0] == terminal_symbols[i]:
                    zmienna_pomocnicza = 1

            if zmienna_pomocnicza == 0:
                new_sybol = chr(random.randint(65, 90))
                if new_sybol in start_symbols:
                    new_sybol = chr(random.randint(65, 90))
                else:
                    temp_list = [terminal_symbols[i]]
                    production_rules.append(temp_list)
                    start_symbols.append(new_sybol)

        for i in range(0, len(production_rules)):
            for x in range(0, len(production_rules[i])):
                for a in range(0, len(production_rules[i][x])):
                    if production_rules[i][x][a] in terminal_symbols and len(production_rules[i][x]) != 1:
                        for z in range(0, len(terminal_symbols)):
                            for b in range(0, len(production_rules)):
                                for c in range(0, len(production_rules[b])):
                                    if production_rules[b][c] == terminal_symbols[z] and len(
                                            production_rules[b]) == 1:
                                        production_rules[i][x] = production_rules[i][x].replace(
                                            terminal_symbols[z], start_symbols[b])
                    else:
                        pass

        """
        zastosowanie lematu 1
        """
        for i in range(0, len(production_rules)):
            for x in range(0, len(production_rules[i])):
                for a in range(0, len(production_rules[i][x])):
                    if len(production_rules[i][x]) == 1:
                        for b in range(0, len(production_rules)):
                            if production_rules[i][x] == start_symbols[b]:
                                production_rules[i].pop(x)
                                x = x - 1
                                for c in range(0, len(production_rules[b])):
                                    production_rules[i].append(production_rules[b][c])

        """
        usnięcie lambdy
        """
        # lambda tymczasowo oznaczona symbolem ^
        for i in range(0, len(production_rules)):
            for x in reversed(range(0, len(production_rules[i]))):
                if "^" in production_rules[i][x]:
                    for a in range(0, len(production_rules)):
                        for b in range(0, len(production_rules[a])):
                            if start_symbols[i] in production_rules[a][b]:
                                production_rules[a][b] = production_rules[a][b].replace(start_symbols[i],
                                                                                        production_rules[i][x])
                                production_rules[i].pop(x)
        for i in range(0, len(production_rules)):
            for x in reversed(range(0, len(production_rules[i]))):
                if "^" in production_rules[i][x]:
                    production_rules[i][x] = production_rules[i][x].replace("^", "")

        """
        usuwanie syboli bezuzytecznych

        """
        useless_symbols = []
        usefull_symbols = [start_symbols[0]]
        for i in range(0, len(start_symbols)):
            temp_list = []
            for x in range(0, len(production_rules[i])):
                if start_symbols[i] in production_rules[i][x]:
                    temp_list.append("0")
                else:
                    temp_list.append("1")
            if "1" not in temp_list:
                useless_symbols.append(start_symbols[i])

        for i in range(0, len(usefull_symbols)):
            index = start_symbols.index(usefull_symbols[i])
            for x in range(0, len(production_rules[index])):
                for a in range(0, len(production_rules[index][x])):
                    if production_rules[index][x][a] in start_symbols:
                        usefull_symbols.append(production_rules[index][x][a])

        for i in range(0, len(symbols)):
            if symbols[i] not in usefull_symbols and symbols[i] not in terminal_symbols and symbols[
                i] not in useless_symbols:
                useless_symbols.append(symbols[i])

        for i in range(0, len(symbols)):
            if symbols[i] not in usefull_symbols:
                useless_symbols.append(symbols[i])

        for u in range(0, len(useless_symbols)):
            i = 0
            x = 0
            while i < len(production_rules):
                while x < len(production_rules[i]):
                    if useless_symbols[u] in production_rules[i][x]:
                        production_rules[i].pop(x)
                        x = x - 1
                    x = x + 1
                if useless_symbols[u] == start_symbols[i]:
                    production_rules.pop(i)
                    start_symbols.pop(i)
                    i = i - 1
                i = i + 1



        embed = nextcord.Embed(
            title=f"Gramatyka Chomsky'ego",
            color=nextcord.Color.yellow(),
            description=""
        )

        for i in range(0, len(production_rules)):
            embed.description += f"{start_symbols[i]} -> "
            for x in range(0, len(production_rules[i]) - 1):
                embed.description += f"{production_rules[i][x]} | "
            embed.description += f"{production_rules[i][-1]}\n"

        await ctx.send(embed=embed)
