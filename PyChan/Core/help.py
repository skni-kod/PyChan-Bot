from nextcord import Color, Embed
from nextcord.ext.commands import HelpCommand, Cog, Command
from typing import Mapping, Optional, List

class HelpField():
    def __init__(self, ) -> None:
        pass

class PyChanHelp(HelpCommand):
    async def send_bot_help(self, mapping: Mapping[Optional[Cog], List[Command]]):
        embed = Embed(title="Pomoc", color=Color.dark_purple())
        embed.description = "Dostępne komendy:"
        
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
        embed = Embed(title=command.name, color=Color.dark_purple())
        embed.description = command.help or "Brak opisu"
        if command.signature:
            embed.add_field(name="Sposób użycia", value=f'`{command.name} {command.signature}`')

        return await self.get_destination().send(embed=embed)
