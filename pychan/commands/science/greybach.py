import nextcord
from nextcord.ext import commands
import copy
import random

class Greybach(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        name="greybach",
        usage="<reguly>",
        category="Nauka",
        help=""
    )
    async def chomsky(self, ctx, *, rules: str):
        def delete_useless_rules(r, s, t):
            """
                sprawdzenie które symbole się redukuja
            """
            reduction_symbols = []
            for i in (range(len(s))):
                for x in range(len(r[i])):
                    if s[i] not in r[i][x]:
                        reduction_symbols.append(s[i])
                        break

            """
                sprawdzenie ktore symbole są produkowane
            """
            symbols_produced = [s[0]]
            while True:
                lista_pomocznicza = symbols_produced.copy()
                for i in range(0, len(symbols_produced)):
                    index = s.index(symbols_produced[i])
                    for x in range(len(r[index])):
                        for y in range(len(r[index][x])):
                            if r[index][x][y] in s and r[index][x][y] not in symbols_produced:
                                symbols_produced.append(r[index][x][y])

                if lista_pomocznicza == symbols_produced:
                    break
            """
                sprawdzenie czy symbole sa uzyteczne oraz usuiecie symboli bezuzytecznych
            """
            for i in reversed(range(len(s))):
                if s[i] not in reduction_symbols:
                    symbols_produced.pop(i)

            for i in reversed(range(len(s))):
                if s[i] not in symbols_produced:
                    r.pop(i)
                    s.pop(i)
                    continue
                else:
                    for x in reversed(range(len(r[i]))):
                        for y in range(len(r[i][x])):
                            if r[i][x][y] not in symbols_produced and r[i][x][y] not in t:
                                r[i].pop(x)
                                break


        """
         wprowadzanie danych
        """
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
        temp = -1
        for i in range(0, len(input_rules)):
            match input_rules[i]:
                case ";":
                    stan = ";"
                    temp = temp + 1
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
                            production_rules[temp].append(input_rules[i])

        """
            usuwanie lambdy
        """
        delete_useless_rules(production_rules, start_symbols, terminal_symbols)

        for i in range(len(production_rules)):
            for x in range(len(production_rules[i])):
                if "^" in production_rules[i][x]:
                    for a in range(len(production_rules)):
                        for b in range(len(production_rules[a])):
                            if start_symbols[i] in production_rules[a][b]:
                                production_rules[a][b] = production_rules[a][b].replace(start_symbols[i], production_rules[i][x])
                                production_rules[i].pop(x)
        for i in range(0, len(production_rules)):
            for x in range(0, len(production_rules[i])):
                if "^" in production_rules[i][x]:
                    production_rules[i][x] = production_rules[i][x].replace("^", "")

        """
            lemat 2
        """

        for i in range(len(production_rules)):
            temp_list = []
            for x in range(len((production_rules[i]))):
                if production_rules[i][x][0] == start_symbols[i]:
                    temp_list.append("alfa")
                else:
                    temp_list.append("beta")

            if "alfa" not in temp_list:
                continue
            else:
                production_rules.append([])
                while True:
                    new_sybol = chr(random.randint(65, 90))
                    if new_sybol not in start_symbols:
                        break
                start_symbols.append(new_sybol)
                for x in reversed(range(len(temp_list))):
                    if temp_list[x] == "alfa":
                        production_rules[-1].append(production_rules[i][x][1:] + start_symbols[-1])
                        production_rules[-1].append(production_rules[i][x][1:])
                    else:
                        production_rules[i].append(production_rules[i][x]+start_symbols[-1])
                        production_rules[i].append(production_rules[i][x])
                    production_rules[i].pop(x)

        """
            pozostale przeksztalcenia
        """
        while True:
            temp_list = copy.deepcopy(production_rules)

            for i in range(len(terminal_symbols)):
                flag = "0"
                for x in range(len(production_rules)):
                    if len(production_rules[x]) == 1 and production_rules[x][0] == terminal_symbols[i]:
                        flag = "1"
                if flag == "1":
                    continue
                while True:
                    new_sybol = chr(random.randint(65, 90))
                    if new_sybol not in start_symbols:
                        break
                start_symbols.append(new_sybol)
                production_rules.append([terminal_symbols[i]])

            for i in range(len(production_rules)):
                for x in range(len(production_rules[i])):
                    for y in range(1, len(production_rules[i][x])):
                        if production_rules[i][x][y] in terminal_symbols:
                            for z in range(len(production_rules)):
                                if len(production_rules[z]) == 1 and production_rules[z][0] == production_rules[i][x][y]:
                                    production_rules[i][x] = production_rules[i][x].replace(production_rules[i][x][y], start_symbols[z])

            for i in range(len(production_rules)):
                for x in reversed(range(len(production_rules[i]))):
                    if production_rules[i][x][0] != start_symbols[i] and production_rules[i][x][0] in start_symbols:
                        for y in range(len(start_symbols)):
                            if start_symbols[y] == production_rules[i][x][0]:
                                for z in range(len(production_rules[y])):
                                    production_rules[i].append(production_rules[y][z]+production_rules[i][x][1:])
                                production_rules[i].pop(x)

            if production_rules == temp_list:
                break

        delete_useless_rules(production_rules, start_symbols, terminal_symbols)

        embed = nextcord.Embed(
            title=f"Gramatyka Greybach",
            color=nextcord.Color.yellow(),
            description=""
        )

        for i in range(0, len(production_rules)):
            embed.description += f"{start_symbols[i]} -> "
            for x in range(0, len(production_rules[i]) - 1):
                embed.description += f"{production_rules[i][x]} | "
            embed.description += f"{production_rules[i][-1]}\n"

        await ctx.send(embed=embed)