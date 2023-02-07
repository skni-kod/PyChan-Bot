import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ui import View, StringSelect, Button
from Core.Commands.Games.Functions.TicTacToe_functions import *

class TicTacToe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="tictactoe",
        aliases=['kik'],
        category="Gry",
        help="""
            Minigra w kółko i krzyżyk
            """
    )
    async def kik(self, ctx: commands.Context):
        options = [
            nextcord.SelectOption(label="Łatwy", value=1),
            nextcord.SelectOption(label="Trudny", value=2)
        ]
        select = StringSelect(options=options, placeholder="Wybierz poziom trudności")
        view = View()
        view.add_item(select)
        select.callback = start_game
        await ctx.reply("Wybierz poziom trudności, aby zacząć", view=view)
