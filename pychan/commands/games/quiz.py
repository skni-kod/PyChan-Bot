from nextcord.ext import commands
from nextcord import Colour, Embed
import nextcord

from pychan import database

class Quiz(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name = "quiz", category = "Gry")
    async def quiz(self, ctx: commands.Context):
        '''Komendy do  quizu'''

    #TODO statystki, dodawanie pytan
    @quiz.command(name="start", pass_context = True)
    async def start(self, ctx):
        '''Wyswietla menu quizu'''

        embed = Embed(
                title = f"Rozpocznij quiz, dodaj pytanie do bazy lub wyświetl ranking",
                color = Colour.green(), 
            )

        starter = MenuButtons()
        await ctx.send(view=starter, embed=embed)
        #await nextcord.InteractionResponse.send_message(view=starter, embed=embed)
        await starter.wait()
        

        
class MenuButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    #start
    @nextcord.ui.button(label = "Start", style=nextcord.ButtonStyle.green)
    async def startB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        #await interaction.response.send_message('inicjalizuje draus.exe', ephemeral=False)
        self.value = True
        self.stop()

    #add
    @nextcord.ui.button(label = "Dodaj", style=nextcord.ButtonStyle.blurple)
    async def addB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True

        await interaction.response.send_modal(EmbedModal())
        
        self.stop()



    #ranking
    @nextcord.ui.button(label = "Ranking", style=nextcord.ButtonStyle.red)
    async def rankingB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

class EmbedModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Dodaj pytnie do quizu!")

        self.embedTitle = nextcord.ui.TextInput(
            label = "Pytanie", min_length = 3, max_length = 124,
            required = True, placeholder = "Tutaj wpisz pytanie",
            style = nextcord.TextInputStyle.paragraph)
        self.add_item(self.embedTitle)

        self.embedOdpA = nextcord.ui.TextInput(
            label = "A", min_length = 0, max_length = 124,
            required = True, placeholder = "Tutaj wpisz odpowiedź A")
        self.add_item(self.embedOdpA)

        self.embedOdpB = nextcord.ui.TextInput(
            label = "B", min_length = 0, max_length = 124,
            required = True, placeholder = "Tutaj wpisz odpowiedź B")
        self.add_item(self.embedOdpB)

        self.embedOdpC = nextcord.ui.TextInput(
            label = "C", min_length = 0, max_length = 124,
            required = False, placeholder = "Tutaj wpisz odpowiedź C")
        self.add_item(self.embedOdpC)

        self.embedOdpD = nextcord.ui.TextInput(
            label = "D", min_length = 0, max_length = 124,
            required = False, placeholder = "Tutaj wpisz odpowiedź D")
        self.add_item(self.embedOdpD)


    async def callback(self, interaction: nextcord.Interaction):
        pytanie = self.embedTitle.value

        answers = ("Odp A: " + self.embedOdpA.value + "\nOdp B: " + self.embedOdpB.value +
                   "\nOdp C: " + self.embedOdpC.value + "\nOdp D: " + self.embedOdpD.value )

        desc = answers
        em = nextcord.Embed(title = pytanie, description = desc)
        return await interaction.response.send_message(embed = em)