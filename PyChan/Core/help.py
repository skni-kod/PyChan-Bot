from nextcord import Color, Embed
from nextcord.ext.commands import Group, HelpCommand, Cog, Command
from typing import Mapping, Optional, List


class PyChanHelp(HelpCommand):
    async def send_bot_help(self, mapping: Mapping[Optional[Cog], List[Command]]):
        embed = Embed(title="Pomoc", color=Color.dark_purple())
        embed.description = f"Wpisz `{self.context.prefix}help <nazwa_komendy>` aby uzyskać więcej informacji.\n"
        embed.description += "Dostępne komendy:"
        
        fields: dict[str, List[Command]] = {}
        for cog_commands in mapping.values():
            for command in cog_commands:
                category = command.extras.get('category') or command.__original_kwargs__.get('category') or 'Inne' 
                if category not in fields.keys():
                    fields[category] = []
                fields[category].append(command)

        categories = sorted(fields.keys())
        if 'Inne' in categories:
            categories.append(categories.pop(categories.index('Inne')))

        for category in categories:
            content = ', '.join(list(map(lambda c: f'`{c.name}`', fields[category])))
            content = content[0:1024]
            embed.add_field(name=category, value=content, inline=False)

        return await self.get_destination().send(embed=embed)

    async def send_command_help(self, command: Command):
        command_str = command.name
        if command.parent:
            command_str = command.full_parent_name + ' ' + command.name

        embed = Embed(title=command_str, color=Color.dark_purple())
        embed.description = command.help or "Brak opisu"
        if command.signature:
            embed.add_field(name="Sposób użycia", value=f'`{self.context.prefix}{command_str} {command.signature}`')

        if len(command.aliases) > 0:
            embed.add_field(name="Aliasy komendy", value=', '.join(list(map(lambda a: f'`{a}`', command.aliases))))

        return await self.get_destination().send(embed=embed)

    async def send_group_help(self, group: Group):
        embed = Embed(title=group.name, color=Color.dark_purple())
        embed.description = f'Wpisz `{self.context.prefix}help {group.name} <komenda>` aby dowiedzieć się więcej o danej podkomendzie'
        embed.add_field(name="Dostępne podkomendy", value=', '.join(list(map(lambda c: f'`{c.name}`', group.all_commands.values()))))

        if len(group.aliases) > 0:
            embed.add_field(name="Aliasy komendy", value=', '.join(list(map(lambda a: f'`{a}`', group.aliases))))

        return await self.get_destination().send(embed=embed)

    async def subcommand_not_found(self, command: Command, string: str):
        return f'Komenda `{command.qualified_name}` nieposiada podkomendy `{string}`'

    async def command_not_found(self, string: str):
        return f'Komenda `{string}` nie istnieje'

