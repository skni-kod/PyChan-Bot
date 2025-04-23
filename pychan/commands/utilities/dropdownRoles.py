import nextcord
from nextcord.ext import commands
from typing import List
from sqlalchemy import select
from pychan import database


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

        if not selected_role:
            await interaction.response.send_message("Nie można znaleźć tej roli", ephemeral=True)
            return

        if selected_role in member.roles:
            await member.remove_roles(selected_role)
            await interaction.response.send_message(f"Usunięto {selected_role.name} role.", ephemeral=True)
        else:
            await member.add_roles(selected_role)
            await interaction.response.send_message(f"Dodano {selected_role.name}", ephemeral=True)


class RolesDropdownRemove(RolesDropdown):
    async def callback(self, interaction: nextcord.Interaction):
        selected_role_id = int(self.values[0])
        guild = interaction.guild

        selected_role = guild.get_role(selected_role_id)

        if not remove_guild_role(selected_role):
            await interaction.response.send_message("Nie można usunąć tej roli", ephemeral=True)
            return
        await interaction.response.send_message(f"Usunięto {selected_role.name} rolę z bazy danych.", ephemeral=True)

class RolesDropdownView(nextcord.ui.View):
    def __init__(self, roles: List[nextcord.Role]):
        super().__init__()
        self.add_item(RolesDropdown(roles))

class RolesDropdownRemoveView(nextcord.ui.View):
    def __init__(self, roles: List[nextcord.Role]):
        super().__init__()
        self.add_item(RolesDropdownRemove(roles))


def get_guild_roles(guild: nextcord.Guild) -> List[nextcord.Role]:
    roles = []
    with database.Session() as session:
        result = session.execute(select(database.GuildDropdownRoles).where(
            database.GuildDropdownRoles.guild_id == str(guild.id)
        )).scalars().all()

        if not result:
            return roles

    for role in result:
        role_id = int(role.role_id)
        discord_role = guild.get_role(role_id)
        if discord_role:
            roles.append(discord_role)
    return roles

def add_guild_role(role: nextcord.Role) -> bool:
    with database.Session() as session:
        try:
            new_role = database.GuildDropdownRoles(guild_id=str(role.guild.id), role_id=str(role.id))
            session.add(new_role)
            session.commit()
        except Exception:
            session.rollback()
            return False
    return True

def remove_guild_role(role: nextcord.Role) -> bool:
    with database.Session() as session:
        result = session.execute(
            database.GuildDropdownRoles.__table__.delete().where(
                database.GuildDropdownRoles.guild_id == str(role.guild.id),
                database.GuildDropdownRoles.role_id == str(role.id)
            )
        )
        if result.rowcount == 0:
            return False
        session.commit()
    return True


class DropdownRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #TODO: Add admin check and remove guild_id
    @nextcord.slash_command(guild_ids=[381092165729910786])
    async def add_roles(self, interaction: nextcord.Interaction, role: nextcord.Role):
        if role > interaction.guild.me.top_role or role > interaction.user.top_role:
            await interaction.response.send_message("Nie możesz dodać tej roli", ephemeral=True)
            return

        if not add_guild_role(role):
            await interaction.response.send_message(f"Rola {role.name} już istnieje w bazie danych", ephemeral=True)
            return
        await interaction.send(f"Dodano {role.name} do bazy danych", ephemeral=True)

    # TODO: Add admin check and remove guild_id
    @nextcord.slash_command(guild_ids=[381092165729910786])
    async def remove_role(self, interaction: nextcord.Interaction):
        roles = get_guild_roles(interaction.guild)

        await interaction.send("Wybierz rolę do usunięcia", view=RolesDropdownRemoveView(roles), ephemeral=True)


    # TODO: remove guild_id
    @nextcord.slash_command(guild_ids=[381092165729910786])
    async def dropdown_roles(self, interaction: nextcord.Interaction):
        roles = get_guild_roles(interaction.guild)

        if not roles:
            await interaction.response.send_message("Nie znaleziono ról w bazie danych", ephemeral=True)
            return

        await interaction.send("Wybierz rolę z rozwijanej listy", view=RolesDropdownView(roles), ephemeral=True)

