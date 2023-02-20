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
        category="Others",
        help=""
    )
    async def chomsky(self, ctx, *, rules: str):
        def usuwanie_regul_bezuzytecznych(zmienna1, zmienna2, zmienna3):
            """
                sprawdzenie które symbole się redukuja
            """
            symbole_red = []
            for i in (range(len(zmienna2))):
                for x in range(len(zmienna1[i])):
                    if zmienna2[i] not in zmienna1[i][x]:
                        symbole_red.append(zmienna2[i])
                        break

            """
                sprawdzenie ktore symbole są produkowane
            """
            symbole_prod = [zmienna2[0]]
            while True:
                lista_pomocznicza = symbole_prod.copy()
                for i in range(0, len(symbole_prod)):
                    index = zmienna2.index(symbole_prod[i])
                    for x in range(len(zmienna1[index])):
                        for y in range(len(zmienna1[index][x])):
                            if zmienna1[index][x][y] in zmienna2 and zmienna1[index][x][y] not in symbole_prod:
                                symbole_prod.append(zmienna1[index][x][y])

                if lista_pomocznicza == symbole_prod:
                    break
            """
                sprawdzenie czy symbole sa uzyteczne oraz usuiecie symboli bezuzytecznych
            """
            for i in reversed(range(len(zmienna2))):
                if zmienna2[i] not in symbole_red:
                    symbole_prod.pop(i)

            for i in reversed(range(len(zmienna2))):
                if zmienna2[i] not in symbole_prod:
                    zmienna1.pop(i)
                    zmienna2.pop(i)
                    continue
                else:
                    for x in reversed(range(len(zmienna1[i]))):
                        for y in range(len(zmienna1[i][x])):
                            if zmienna1[i][x][y] not in symbole_prod and zmienna1[i][x][y] not in zmienna3:
                                zmienna1[i].pop(x)
                                break


        """
         wprowadzanie danych
        """
        terminalne = []
        reguly_prod = []
        symbole_pocz = []
        reguly = rules
        stan = str("początek")
        reguly.strip()
        reguly = reguly.replace(",", " ")
        reguly = reguly.replace(";", " ; ")
        reguly = reguly.replace(">", " > ")
        reguly = reguly.split()
        zmienna_pomocnicza = -1
        for i in range(0, len(reguly)):
            match reguly[i]:
                case ";":
                    stan = ";"
                    zmienna_pomocnicza = zmienna_pomocnicza + 1
                case ">":
                    stan = ">"
                case _:
                    match stan:
                        case "początek":
                            terminalne.append(reguly[i])
                        case ";":
                            symbole_pocz.append(reguly[i])
                            reguly_prod.append([])
                        case ">":
                            reguly_prod[zmienna_pomocnicza].append(reguly[i])

        """
            usuwanie lambdy
        """
        usuwanie_regul_bezuzytecznych(reguly_prod, symbole_pocz, terminalne)

        for i in range(len(reguly_prod)):
            for x in range(len(reguly_prod[i])):
                if "^" in reguly_prod[i][x]:
                    for a in range(len(reguly_prod)):
                        for b in range(len(reguly_prod[a])):
                            if symbole_pocz[i] in reguly_prod[a][b]:
                                reguly_prod[a][b] = reguly_prod[a][b].replace(symbole_pocz[i], reguly_prod[i][x])
                                reguly_prod[i].pop(x)
        for i in range(0, len(reguly_prod)):
            for x in range(0, len(reguly_prod[i])):
                if "^" in reguly_prod[i][x]:
                    reguly_prod[i][x] = reguly_prod[i][x].replace("^", "")

        """
            lemat 2
        """

        for i in range(len(reguly_prod)):
            lista_pomocznicza = []
            for x in range(len((reguly_prod[i]))):
                if reguly_prod[i][x][0] == symbole_pocz[i]:
                    lista_pomocznicza.append("alfa")
                else:
                    lista_pomocznicza.append("beta")

            if "alfa" not in lista_pomocznicza:
                continue
            else:
                reguly_prod.append([])
                while True:
                    nowy_symbol = chr(random.randint(65, 90))
                    if nowy_symbol not in symbole_pocz:
                        break
                symbole_pocz.append(nowy_symbol)
                for x in reversed(range(len(lista_pomocznicza))):
                    if lista_pomocznicza[x] == "alfa":
                        reguly_prod[-1].append(reguly_prod[i][x][1:] + symbole_pocz[-1])
                        reguly_prod[-1].append(reguly_prod[i][x][1:])
                    else:
                        reguly_prod[i].append(reguly_prod[i][x]+symbole_pocz[-1])
                        reguly_prod[i].append(reguly_prod[i][x])
                    reguly_prod[i].pop(x)

        """
            pozostale przeksztalcenia
        """
        while True:
            lista_pomocznicza = copy.deepcopy(reguly_prod)

            for i in range(len(terminalne)):
                flag = "0"
                for x in range(len(reguly_prod)):
                    if len(reguly_prod[x]) == 1 and reguly_prod[x][0] == terminalne[i]:
                        flag = "1"
                if flag == "1":
                    continue
                while True:
                    nowy_symbol = chr(random.randint(65, 90))
                    if nowy_symbol not in symbole_pocz:
                        break
                symbole_pocz.append(nowy_symbol)
                reguly_prod.append([terminalne[i]])

            for i in range(len(reguly_prod)):
                for x in range(len(reguly_prod[i])):
                    for y in range(1, len(reguly_prod[i][x])):
                        if reguly_prod[i][x][y] in terminalne:
                            for z in range(len(reguly_prod)):
                                if len(reguly_prod[z]) == 1 and reguly_prod[z][0] == reguly_prod[i][x][y]:
                                    reguly_prod[i][x] = reguly_prod[i][x].replace(reguly_prod[i][x][y], symbole_pocz[z])

            for i in range(len(reguly_prod)):
                for x in reversed(range(len(reguly_prod[i]))):
                    if reguly_prod[i][x][0] != symbole_pocz[i] and reguly_prod[i][x][0] in symbole_pocz:
                        for y in range(len(symbole_pocz)):
                            if symbole_pocz[y] == reguly_prod[i][x][0]:
                                for z in range(len(reguly_prod[y])):
                                    reguly_prod[i].append(reguly_prod[y][z]+reguly_prod[i][x][1:])
                                reguly_prod[i].pop(x)

            if reguly_prod == lista_pomocznicza:
                break

        usuwanie_regul_bezuzytecznych(reguly_prod, symbole_pocz, terminalne)

        embed = nextcord.Embed(
            title=f"Gramatyka Greybach",
            color=nextcord.Color.yellow(),
            description=""
        )

        for i in range(0, len(reguly_prod)):
            embed.description += f"{symbole_pocz[i]} -> "
            for x in range(0, len(reguly_prod[i]) - 1):
                embed.description += f"{reguly_prod[i][x]} | "
            embed.description += f"{reguly_prod[i][-1]}\n"

        await ctx.send(embed=embed)

