from nextcord.ext import commands
from nextcord import Colour, Embed
import nextcord

class Quiz(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name = "quiz", category = "Gry")
    async def quiz(self, ctx: commands.Context):
        '''Komendy do  quizu'''

    #TODO statystki, dodawanie pytan
    @quiz.command(name="start", pass_context = True)
    async def start(self, ctx):
        '''Rozpoczyna quiz'''

        embed = Embed(
                title = f"Rozpocznij quiz",
                color = Colour.green(), 
            )

        starter = StartButton()

        await ctx.send(view=starter, embed=embed)
        #await nextcord.InteractionResponse.send_message(view=starter, embed=embed)
        await starter.wait()


class StartButton(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label = "Start", style=nextcord.ButtonStyle.green)
    async def startB(self, button: nextcord.ui.Button, interaction: nextcord.InteractionResponse):
        await interaction.send_message('inicjalizuje draus.exe', ephemeral=False)
        self.value = True
        self.stop()
