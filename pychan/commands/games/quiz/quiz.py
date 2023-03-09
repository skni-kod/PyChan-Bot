from nextcord.ext import commands
from nextcord import Colour, Embed
import nextcord
from asyncio import sleep, Semaphore
from random import randint
from random import shuffle

from sqlalchemy import select

from pychan import database
from .modals import EmbedModal
from .views import startQuiz, AddCategoryAndAnswer

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.semaphore = Semaphore(1)

    @commands.group(name = "quiz", category = "Gry", pass_context = True)
    async def quiz(self, ctx: commands.Context):
        '''Komendy do quizu'''
        

    @quiz.command(name="start", pass_context = True)
    async def start(self, ctx):
        '''Rozpoczyna quiz'''

        embed = Embed(
                    title = f"Rozpoczynamy za ... 3",
                    color = Colour.green(),
                )
        viewYouCanEdit = await ctx.send(embed=embed)
        await sleep(1)

        for i in [2, 1]:
            embed.title = f"Rozpoczynamy za ... {i}"
            await viewYouCanEdit.edit(embed = embed)
            await sleep(1)
        
        points = [0]

        async with self.semaphore:
            # all_questions: list[database.QuizQuestion] = database.session.query(database.QuizQuestion).all()
            all_questions = database.session.scalars(select(database.QuizQuestion)).all()

        questions = list(all_questions)
        shuffle(questions)
        questions = questions[:5]

        for question in questions:
            quizView = startQuiz(question)

            for ans in question.answers:
                button = AnswerButton(ans, points)
                quizView.add_item(button)

            await viewYouCanEdit.edit(view=quizView, embed=quizView.embed)
            await quizView.wait()

        quiz_summary = Embed(title=f"Gratulacje, ilość punktów to: {points[0]}")
        await viewYouCanEdit.edit(view=None, embed=quiz_summary)
        
    
    @quiz.command(name="menu", pass_context = True)
    async def menu(self, ctx):
        '''Dodawanie pytan, ranking'''

        embed = Embed(
                title = f"Dodaj pytanie do bazy lub wyświetl ranking",
                color = Colour.green(), 
            )

        viewYouCanEdit = await ctx.send(embed=embed)
        starter = MenuButtons(viewYouCanEdit, self.semaphore)
        await viewYouCanEdit.edit(view=starter)

        await starter.wait()

class MenuButtons(nextcord.ui.View):
    def __init__(self, viewYouCanEdit: nextcord.Message, semaphore : Semaphore):
        super().__init__()
        self.value = None
        self.viewYouCanEdit = viewYouCanEdit
        self.semaphore = semaphore
        self.answers = []

    #add
    @nextcord.ui.button(label = "Dodaj", style=nextcord.ButtonStyle.blurple)
    async def addB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True

        mod = EmbedModal()
        await interaction.response.send_modal(mod)
        await mod.wait()

        newEmbed = nextcord.Embed(
                title = f"Jeszcze chwila!",
                description = "Dodaj poprawną odpowiedź oraz kategorię",
                color = nextcord.Colour.green(), 
            )
        
        newView = AddCategoryAndAnswer(self.viewYouCanEdit,
                                    mod.embedTitle.value, 
                                    mod.answers)
        await self.viewYouCanEdit.edit(view = newView, embed=newEmbed)
        await newView.wait()

        async with self.semaphore:
            database.session.add(newView.ready_question)
            database.session.commit()

        self.stop()

    #ranking
    @nextcord.ui.button(label = "Ranking", style=nextcord.ButtonStyle.red)
    async def rankingB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

class AnswerButton(nextcord.ui.Button):
    def __init__(self, answer: database.QuizAnswer, points: list[int]):
        super().__init__(style=nextcord.ButtonStyle.blurple, label = answer.answer)
        self.ButtonAnswer = answer
        self.points = points

    @nextcord.ui.button()
    async def callback(self, interaction: nextcord.Interaction):
        if(self.ButtonAnswer.correct):
            self.points[0] += 1
        self.view.stop()
 
