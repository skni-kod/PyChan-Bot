import discord
from discord.ext import commands
from discord import Embed
from discord.utils import get
from typing import Optional

from Core.Decorators.decorators import Decorator
from Core.Commands.Settings.Functions.get_server_prefix import GetServerPrefix



class Help(commands.Cog):
    """Class contains help methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f'{command}',
                description=f'{command.help}',
                      colour=discord.Color.dark_purple())
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, name='help')
    @Decorator.pychan_decorator
    async def help(self, ctx, cmd: Optional[str]):
        """Sends message with built-in funtions

        :param ctx: the context in which a command is called
        :type ctx: discord.ext.commands.Context
        """
        prefix = GetServerPrefix.get_server_prefix(self, ctx)

        if cmd is None:
            commands = dict()

            for command in self.bot.commands:
                category = ''
                try:
                    category = command.__original_kwargs__['category']
                except Exception as e:
                    print(e)
                if category:
                    try:
                        if category in commands:
                            commands[category].append(command.name)
                        else:
                            commands[category] = []
                            commands[category].append(command.name)
                    except Exception as e:
                        print(e)

            embed = discord.Embed(title='Help',
                        description=f'Wpisz `{prefix}help <nazwa_komendy>` aby uzyskać więcej informacji.\n'
                        '\n'
                        'Dostępne komendy:',
                        color=discord.Color.dark_purple())

            for key in sorted(commands.keys()):
                text = ''
                for name in sorted(commands[key][:-1]):
                    text += f'`{name}`, '
                text += f'`{sorted(commands[key])[-1]}`'
                embed.add_field(name=key, value=text, inline=False)

            await ctx.send(embed=embed)

        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)
            else:
                raise discord.ext.commands.errors.CommandNotFound
