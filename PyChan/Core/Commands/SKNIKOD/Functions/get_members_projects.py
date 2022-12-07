import nextcord
from nextcord.ext import commands
import os


class GetMembersProjects(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context = True,
        name = "listaCzlonkow",
        category = "SKNIKOD",
        usage = " ",
        help = """
               Wysyła plik txt z aktualną listą członków z rolą `Członek` i przypisanymi do nich projektami
               """
    )
    async def get_members_projects(self, ctx):
        """
        Gets actual list of members and send txt file with name and projects assigned to them

        :param ctx: The context in which a command is called
        :type ctx: nextcord.ext.commands.Context
        """

        message = await ctx.send(
            f"Trwa pobieranie czlonkow {1}/{len(ctx.guild.members)}"
        )

        with open("listaCzlonkow.txt", "w", encoding="utf-8") as f:
            for i, member in enumerate(ctx.guild.members):
                await message.edit(
                    content=f"Trwa pobieranie członkow {i}/{len(ctx.guild.members)}"
                )

                if member.bot:
                    continue

                for role in member.roles:
                    if role.name == "Członek":
                        name = member.display_name.replace('"', " ").split()

                        if len(name) > 2:
                            f.write(f"{name[0]};{name[2]};{name[1]};")
                        elif len(name) == 2:
                            f.write(f"{name[0]};{name[1]};;")
                        else:
                            f.write(f"{member.display_name} error")

                        for role2 in member.roles[1:]:
                            if "Projekt" in role2.name:
                                str = role2.name.replace("Projekt - ", "")
                                f.write(f"{str}, ")

                        f.write("\n")

        await message.delete()
        with open("listaCzlonkow.txt", "rb") as file:
            await ctx.send(file=nextcord.File(file, "listaCzlonkow.txt"))

        os.remove("listaCzlonkow.txt")
