import nextcord
from nextcord.ext import commands
from typing import List


class RolesDropdown(nextcord.ui.Select):
    def __init__(self, roles: List[nextcord.Role]):
        options = [
            nextcord.SelectOption(label=role.name, value=str(role.id))
            for role in roles
        ]
        super().__init__(placeholder="Wybierz rolę", options=options)

    async def callback(self, interaction: nextcord.Interaction):
        selected_role_id = int(self.values[0])
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        selected_role = guild.get_role(selected_role_id)

        if selected_role in member.roles:
            await member.remove_roles(selected_role)
            await interaction.response.send_message(f"Usunięto {selected_role.name} role.", ephemeral=True)
        else:
            await member.add_roles(selected_role)
            await interaction.response.send_message(f"Dodano {selected_role.name}", ephemeral=True)


class RolesDropdownView(nextcord.ui.View):
    def __init__(self, roles: List[nextcord.Role]):
        super().__init__()
        self.add_item(RolesDropdown(roles))



class DropdownRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = {}


    #TODO: Add admin check
    @nextcord.slash_command(guild_ids=[381092165729910786])
    async def add_roles(self, interaction: nextcord.Interaction, role: nextcord.Role):
        if role > interaction.guild.me.top_role or role > interaction.user.top_role:
            await interaction.response.send_message("Nie możesz dodać tej roli", ephemeral=True)
            return

        # TODO: Add database integration

        if not interaction.guild.id in self.roles:
            self.roles[interaction.guild.id] = [role]
        else:
            self.roles[interaction.guild.id].append(role)
        view = RolesDropdownView(self.roles[interaction.guild.id])
        await interaction.send("Dodano rolę do bazy danych", view=view, ephemeral=True)

    @nextcord.slash_command(guild_ids=[381092165729910786])
    async def dropdown_roles(self, interaction: nextcord.Interaction):
        await interaction.send("Wybierz rolę z rozwijanej listy", view=RolesDropdownView(self.roles[interaction.guild.id]), ephemeral=True)