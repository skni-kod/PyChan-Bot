from tempfile import NamedTemporaryFile 
import nextcord
from nextcord.ext import commands


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
    async def get_members_projects(self, ctx: commands.Context):
        """
        Gets actual list of members and send txt file with name and projects assigned to them

        :param ctx: The context in which a command is called
        :type ctx: nextcord.ext.commands.Context
        """

        message = await ctx.send("Trwa pobieranie czlonkow...")
        file = NamedTemporaryFile(mode="r+")

        async with ctx.channel.typing():
            for member in ctx.guild.members:
                if member.bot:
                    continue

                for role in member.roles:
                    if role.name == "Członek":
                        name = member.display_name.replace('"', " ").split()

                        if len(name) > 2:
                            file.write(f"{name[0]};{name[2]};{name[1]};")
                        elif len(name) == 2:
                            file.write(f"{name[0]};{name[1]};;")
                        else:
                            file.write(f"{member.display_name} error")

                        for role2 in member.roles[1:]:
                            if "Projekt" in role2.name:
                                str = role2.name.replace("Projekt - ", "")
                                file.write(f"{str}, ")

                        file.write("\n")

        await message.delete()
        await ctx.send(file=nextcord.File(file.file, "listaCzlonkow.txt", force_close=True))

