from nextcord.ext import commands
from nextcord import Colour, Embed
import nextcord

from pychan import database
from .modals import EmbedModal
from .views import startQuiz

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "quiz", category = "Gry", pass_context = True)
    async def quiz(self, ctx: commands.Context):
        '''Wyswietla menu quizu'''
        
        embed = Embed(
                title = f"Rozpocznij quiz, dodaj pytanie do bazy lub wyświetl ranking",
                color = Colour.green(), 
            )

        viewYouCanEdit = await ctx.send(embed=embed)
        starter = MenuButtons(viewYouCanEdit)
        await viewYouCanEdit.edit(view=starter)

        await starter.wait()
        

class MenuButtons(nextcord.ui.View):
    def __init__(self, viewYouCanEdit: nextcord.Message):
        super().__init__()
        self.value = None
        self.viewYouCanEdit = viewYouCanEdit
        

    #start
    @nextcord.ui.button(label = "Start", style=nextcord.ButtonStyle.green)
    async def startB(self, bbutton: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True

        points = [0]
        all_questions: list[database.QuizQuestion] = database.session.query(database.QuizQuestion).all()
        quesitions = all_questions[:5]
        for question in quesitions:
            quizView = startQuiz(question)

            for ans in question.answers:
                button = AnswerButton(ans, points)
                quizView.add_item(button)

            await self.viewYouCanEdit.edit(view=quizView, embed=quizView.embed)
            await quizView.wait()
            print(points[0],"koncowe")

        quiz_summary = Embed(title=f"Gratulacje, ilość punktów to: {points[0]}")
        await self.viewYouCanEdit.edit(view=None, embed=quiz_summary)
        self.stop()

    #add
    @nextcord.ui.button(label = "Dodaj", style=nextcord.ButtonStyle.blurple)
    async def addB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True

        mod = EmbedModal(self.viewYouCanEdit)
        await interaction.response.send_modal(mod)

        #self.stop()

    #ranking
    @nextcord.ui.button(label = "Ranking", style=nextcord.ButtonStyle.red)
    async def rankingB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        #self.stop()

class AnswerButton(nextcord.ui.Button):
    def __init__(self, answer: database.QuizAnswer, points: list[int]):
        super().__init__(style=nextcord.ButtonStyle.blurple, label = answer.answer)
        self.ButtonAnswer = answer
        self.points = points

    @nextcord.ui.button()
    async def callback(self, interaction: nextcord.Interaction): #button dodaj i zalatw interaction
        print(self.ButtonAnswer.answer)
        print(self.ButtonAnswer.correct)

        if(self.ButtonAnswer.correct):
            self.points[0] += 1
        # moze tak lepiej self.view.points += 1
        self.view.stop()
        


    '''second modal
    unused, but maybe someone will find a way to apply 2 modals...
    and StringSelect will be supported in Modals
    '''
 