import nextcord
from nextcord.ext import commands
from nextcord import Embed
from nextcord.utils import get
from typing import Optional

from Core.Decorators.decorators import Decorator
from Core.Commands.Settings.Functions.get_server_prefix import GetServerPrefix


class Help(commands.Cog):
    """Class contains help methods"""

    def __init__(self, bot):
        """Constructor method"""
        self.bot = bot
        self.commands = {}

    async def cmd_help(self, ctx, command):
        embed = Embed(
            title=f"{command}",
            description=f"{command.help}",
            colour=nextcord.Color.dark_purple(),
        )
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, name="help")
    @Decorator.pychan_decorator
    async def help(self, ctx, cmd: Optional[str]):
        """Sends message with built-in funtions

        :param ctx: the context in which a command is called
        :type ctx: nextcord.ext.commands.Context
        """
        prefix = GetServerPrefix.get_server_prefix(self, ctx)
        if cmd is None:
            if not self.commands:
                for command in self.bot.commands:
                    category = ""
                    try:
                        category = command.__original_kwargs__["category"]
                    except Exception as e:
                        print(
                            f'Invoked "help" command. No "category" keyword in command {command.name}'
                        )
                    if category:
                        try:
                            if category in self.commands:
                                self.commands[category].append(command.name)
                            else:
                                self.commands[category] = []
                                self.commands[category].append(command.name)
                        except Exception as e:
                            print(e)

                print(self.commands)

            embed = nextcord.Embed(
                title="Help",
                description=f"Wpisz `{prefix}help <nazwa_komendy>` aby uzyskać więcej informacji.\n"
                "\n"
                "Dostępne komendy:",
                color=nextcord.Color.dark_purple(),
            )

            for key in sorted(self.commands.keys()):
                text = ""
                for name in sorted(self.commands[key])[:-1]:
                    text += f"`{name}`, "
                text += f"`{sorted(self.commands[key])[-1]}`"
                embed.add_field(name=key, value=text, inline=False)

            await ctx.send(embed=embed)

        else:
            if command := get(self.bot.commands, name=cmd):
                try:
                    help_dict = command.__original_kwargs__["help_"]
                except Exception as e:
                    await ctx.send("Help nie został dodany!")
                    return

                embed = nextcord.Embed(
                    title=help_dict["title"],
                    description=help_dict["description"],
                    color=nextcord.Color.dark_purple(),
                )

                if "fields" in help_dict:
                    for field in help_dict["fields"]:
                        embed.add_field(
                            name=field["name"], value=field["value"], inline=False
                        )

                await ctx.send(embed=embed)

            else:
                raise nextcord.ext.commands.errors.CommandNotFound