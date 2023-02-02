from datetime import datetime
from io import BytesIO
import nextcord
from nextcord.ext import commands

from pychan.checks import check_sknikod


class GetMembersProjects(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        name="listaCzlonkow",
        category="SKNIKOD",
        help="Wysyła plik txt z aktualną listą członków z rolą `Członek` i przypisanymi do nich projektami"
    )
    @commands.check(check_sknikod)
    async def get_members_projects(self, ctx):
        with BytesIO() as file:
            async with ctx.channel.typing():
                for member in ctx.guild.members:
                    if member.bot:
                        continue

                    for role in member.roles:
                        if role.name == "Członek":
                            name = member.display_name.replace(
                                '"', " ").split()
                            if len(name) > 2:
                                file.write(
                                    f"{name[0]};{name[2]};{name[1]};".encode())
                            elif len(name) == 2:
                                file.write(f"{name[0]};{name[1]};;".encode())
                            else:
                                file.write(
                                    f"{member.display_name} error".encode())
                            for role2 in member.roles[1:]:
                                if "Projekt" in role2.name:
                                    str = role2.name.replace("Projekt - ", "")
                                    file.write(f"{str}, ".encode())
                            file.write(b"\n")
            file.seek(0)
            await ctx.send(file=nextcord.File(fp=file, filename=f"listaCzlonkow{datetime.today().date()}.txt"))
