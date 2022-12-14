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
        category="Others",
        help="to jest help"
    )
    async def chomsky(self, ctx, *, rules: str):


        def wprowadzanie_reguł():
            """
            tymczasowe wprowadzanie danych
            """
            global symbole_terminalne
            global Reguły_produkcji
            global oznaczenia_symboli
            symbole_terminalne = []
            Reguły_produkcji = []
            oznaczenia_symboli = []
            reguly = rules
            stan = str("początek")
            reguly.strip()
            x = ""
            x = reguly.replace(",", " ")
            x = x.replace(";", " ; ")
            x = x.replace(">", " > ")
            x = x.split()
            zmienna_pomocnicza = -1
            for i in range(0, len(x)):
                match x[i]:
                    case ";":
                        stan = ";"
                        zmienna_pomocnicza = zmienna_pomocnicza + 1
                    case ">":
                        stan = ">"
                    case _:
                        match stan:
                            case "początek":
                                symbole_terminalne.append(x[i])
                            case ";":
                                oznaczenia_symboli.append(x[i])
                                Reguły_produkcji.append([])
                            case ">":
                                Reguły_produkcji[zmienna_pomocnicza].append(x[i])

            # Nie zmieniać
            global symbole
            symbole = []
            for i in range(0, len(Reguły_produkcji)):
                for x in range(0, len(Reguły_produkcji[i])):
                    for a in range(0, len(Reguły_produkcji[i][x])):
                        if Reguły_produkcji[i][x][a] not in symbole:
                            symbole.append(Reguły_produkcji[i][x][a])

        def zmniejszanie_reguł():
            """
            Skracanie długości produkcji do pordukowania
            1-2 symboli
            """
            for i in range(0, len(Reguły_produkcji)):
                for x in range(0, len(Reguły_produkcji[i])):
                    if len(Reguły_produkcji[i][x]) == 1:
                        pass
                    elif len(Reguły_produkcji[i][x]) == 2:
                        pass
                    else:
                        while len(Reguły_produkcji[i][x]) > 2:
                            nowy_symbol_wejściowy = chr(random.randint(65, 91))
                            if nowy_symbol_wejściowy in oznaczenia_symboli:
                                nowy_symbol_wejściowy = chr(random.randint(65, 90))
                            else:

                                element = Reguły_produkcji[i][x][:-2] + nowy_symbol_wejściowy
                                lista_pomocnicza = [Reguły_produkcji[i][x][-2:]]
                                Reguły_produkcji.append(lista_pomocnicza)
                                Reguły_produkcji[i][x] = element
                            oznaczenia_symboli.append(nowy_symbol_wejściowy)

        def zamiana_symboli():
            """
            zamiana reguł produkcji produkujących 2 symbole w tym co najmniej 1 terminalny"
            """

            for i in range(0, len(symbole_terminalne)):
                zmienna_pomocnicza = 0
                for x in range(0, len(Reguły_produkcji)):
                    if len(Reguły_produkcji[x]) == 1 and Reguły_produkcji[x][0] == symbole_terminalne[i]:
                        zmienna_pomocnicza = 1

                if zmienna_pomocnicza == 0:
                    nowy_symbol_wejściowy = chr(random.randint(65, 90))
                    if nowy_symbol_wejściowy in oznaczenia_symboli:
                        nowy_symbol_wejściowy = chr(random.randint(65, 90))
                    else:
                        lista_pomocnicza = [symbole_terminalne[i]]
                        Reguły_produkcji.append(lista_pomocnicza)
                        oznaczenia_symboli.append(nowy_symbol_wejściowy)

            for i in range(0, len(Reguły_produkcji)):
                for x in range(0, len(Reguły_produkcji[i])):
                    for a in range(0, len(Reguły_produkcji[i][x])):
                        if Reguły_produkcji[i][x][a] in symbole_terminalne and len(Reguły_produkcji[i][x]) != 1:
                            for z in range(0, len(symbole_terminalne)):
                                for b in range(0, len(Reguły_produkcji)):
                                    for c in range(0, len(Reguły_produkcji[b])):
                                        if Reguły_produkcji[b][c] == symbole_terminalne[z] and len(
                                                Reguły_produkcji[b]) == 1:
                                            Reguły_produkcji[i][x] = Reguły_produkcji[i][x].replace(
                                                symbole_terminalne[z], oznaczenia_symboli[b])
                        else:
                            pass

        def lemat_1():
            """
            zastosowanie lematu 1
            """
            for i in range(0, len(Reguły_produkcji)):
                for x in range(0, len(Reguły_produkcji[i])):
                    for a in range(0, len(Reguły_produkcji[i][x])):
                        if len(Reguły_produkcji[i][x]) == 1:
                            for b in range(0, len(Reguły_produkcji)):
                                if Reguły_produkcji[i][x] == oznaczenia_symboli[b]:
                                    Reguły_produkcji[i].pop(x)
                                    x = x - 1
                                    for c in range(0, len(Reguły_produkcji[b])):
                                        Reguły_produkcji[i].append(Reguły_produkcji[b][c])

        def usuwanie_lambdy():
            """
            usnięcie lambdy
            """
            # lambda tymczasowo oznaczona symbolem ^
            for i in range(0, len(Reguły_produkcji)):
                for x in range(0, len(Reguły_produkcji[i])):
                    if "^" in Reguły_produkcji[i][x]:
                        for a in range(0, len(Reguły_produkcji)):
                            for b in range(0, len(Reguły_produkcji[a])):
                                if oznaczenia_symboli[i] in Reguły_produkcji[a][b]:
                                    Reguły_produkcji[a][b] = Reguły_produkcji[a][b].replace(oznaczenia_symboli[i],
                                                                                            Reguły_produkcji[i][x])
                                    Reguły_produkcji[i].pop(x)
            for i in range(0, len(Reguły_produkcji)):
                for x in range(0, len(Reguły_produkcji[i])):
                    if "^" in Reguły_produkcji[i][x]:
                        Reguły_produkcji[i][x] = Reguły_produkcji[i][x].replace("^", "")

        def usuwanie_symbloi_bezużytecznych():
            """
            usuwanie syboli bezuzytecznych

            Nie skończone
            """
            symbole_bezużyteczne = []
            symbole_użyteczne = [oznaczenia_symboli[0]]
            for i in range(0, len(oznaczenia_symboli)):
                lista_pomocnicza = []
                for x in range(0, len(Reguły_produkcji[i])):
                    if oznaczenia_symboli[i] in Reguły_produkcji[i][x]:
                        lista_pomocnicza.append("0")
                    else:
                        lista_pomocnicza.append("1")
                if "1" not in lista_pomocnicza:
                    symbole_bezużyteczne.append(oznaczenia_symboli[i])

            for i in range(0, len(symbole_użyteczne)):
                index = oznaczenia_symboli.index(symbole_użyteczne[i])
                for x in range(0, len(Reguły_produkcji[index])):
                    for a in range(0, len(Reguły_produkcji[index][x])):
                        if Reguły_produkcji[index][x][a] in oznaczenia_symboli:
                            symbole_użyteczne.append(Reguły_produkcji[index][x][a])

            for i in range(0, len(symbole)):
                if symbole[i] not in symbole_użyteczne and symbole[i] not in symbole_terminalne and symbole[
                    i] not in symbole_bezużyteczne:
                    symbole_bezużyteczne.append(symbole[i])

            for i in range(0, len(symbole)):
                if symbole[i] not in symbole_użyteczne:
                    symbole_bezużyteczne.append(symbole[i])

            for u in range(0, len(symbole_bezużyteczne)):
                i = 0
                x = 0
                while i < len(Reguły_produkcji):
                    while x < len(Reguły_produkcji[i]):
                        if symbole_bezużyteczne[u] in Reguły_produkcji[i][x]:
                            Reguły_produkcji[i].pop(x)
                            x = x - 1
                        x = x + 1
                    if symbole_bezużyteczne[u] == oznaczenia_symboli[i]:
                        Reguły_produkcji.pop(i)
                        oznaczenia_symboli.pop(i)
                        i = i - 1
                    i = i + 1

        wprowadzanie_reguł()
        usuwanie_lambdy()
        zmniejszanie_reguł()
        zamiana_symboli()
        lemat_1()
        usuwanie_symbloi_bezużytecznych()


        embed = nextcord.Embed(
            title=f"Gramatyka Chomsky'ego",
            color=nextcord.Color.yellow(),
            description=""
        )

        for i in range(0, len(Reguły_produkcji)):
            embed.description += f"{oznaczenia_symboli[i]} -> "
            for x in range(0, len(Reguły_produkcji[i]) - 1):
                embed.description += f"{Reguły_produkcji[i][x]} | "
            embed.description += f"{Reguły_produkcji[i][-1]}\n"

        await ctx.send(embed=embed)
