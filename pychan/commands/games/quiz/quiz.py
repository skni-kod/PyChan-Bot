from nextcord.ext import commands
from nextcord import Colour, Embed
import nextcord

from pychan import database
from .modals import EmbedModal
from .views import startQuiz

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

        viewYouCanEdit = await ctx.send(embed=embed)
        starter = MenuButtons(viewYouCanEdit)
        await viewYouCanEdit.edit(view=starter)
        
        #await nextcord.Interaction.response.send_message(view=starter, embed=embed)
        #  
        await starter.wait()
        

class MenuButtons(nextcord.ui.View):
    def __init__(self, viewYouCanEdit: nextcord.Message):
        super().__init__()
        self.value = None
        self.viewYouCanEdit = viewYouCanEdit

    #start
    @nextcord.ui.button(label = "Start", style=nextcord.ButtonStyle.green)
    async def startB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        #await interaction.response.send_message('inicjalizuje draus.exe', ephemeral=False)
        self.value = True

        question = database.QuizQuestion(question="W celu odczytania tekstu wpisanego w oknie edycji należy użyć funkcji:", category="Systemy Operacyjne")
        question.answers.append(database.QuizAnswer(answer="GetWindowText", correct=True))
        question.answers.append(database.QuizAnswer(answer="SetWindowText", correct=False))
        question.answers.append(database.QuizAnswer(answer="sscanf", correct=False))

        quizView = startQuiz(question)
        for i, ans in enumerate(question.answers):
            button = nextcord.ui.Button(style=nextcord.ButtonStyle.blurple,
                                        label=ans.answer)
            quizView.listOfButtons.append(button)
            quizView.add_item(button)

        await self.viewYouCanEdit.edit(view=quizView, embed=quizView.embed)
        self.stop()

    #add
    @nextcord.ui.button(label = "Dodaj", style=nextcord.ButtonStyle.blurple)
    async def addB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True

        mod = EmbedModal(self.viewYouCanEdit)
        await interaction.response.send_modal(mod)

        self.stop()

    #ranking
    @nextcord.ui.button(label = "Ranking", style=nextcord.ButtonStyle.red)
    async def rankingB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

#todo move this to modals file



    '''second modal
    unused, but maybe someone will find a way to apply 2 modals...
    and StringSelect will be supported in Modals
    '''
 