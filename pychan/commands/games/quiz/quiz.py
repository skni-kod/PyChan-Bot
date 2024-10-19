from nextcord.ext import commands
from nextcord import Colour, Embed
import nextcord
from asyncio import sleep, Semaphore
from random import shuffle

from sqlalchemy import select
from pychan import database
from .modals import EmbedModal
from .views import *

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

        with database.Session() as session:
            all_questions = session.scalars(select(database.QuizQuestion)).all()

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

            quiz_summary = Embed(title=f"Gratulacje, ilość punktów to: {points[0]} / 5")
            await viewYouCanEdit.edit(view=None, embed=quiz_summary)
        
    
    @quiz.command(name="menu", pass_context = True)
    async def menu(self, ctx):
        '''Dodawanie pytan, ranking'''

        embed = Embed(
                title = f"Dodaj pytanie do bazy",
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
        if await mod.wait():
            return

        self.answers = mod.answers

        newEmbed = nextcord.Embed(
                title = f"Jeszcze chwila!",
                description = "Dodaj poprawną odpowiedź oraz kategorię",
                color = nextcord.Colour.green(), 
            )
        
        selectAnswerView = SelectAnswerView(self.viewYouCanEdit, self.answers)
        await self.viewYouCanEdit.edit(view=selectAnswerView, embed=newEmbed)
        if await selectAnswerView.wait():
            return

        selectCategoryView = SelectCategoryView(self.viewYouCanEdit)
        await self.viewYouCanEdit.edit(view=selectCategoryView)
        if await selectCategoryView.wait():
            return
        
        final_view = successfulQuestion(
            question=mod.embedTitle.value,
            answers=self.answers,
            correct=selectAnswerView.correct,
            category=selectCategoryView.category
        )
        await self.viewYouCanEdit.edit(view = final_view, embed = final_view.embed_for_all)
        await interaction.followup.send(embed=final_view.embed, ephemeral = True)

        readyQuestion = database.QuizQuestion(
            question=mod.embedTitle.value,
            category=selectCategoryView.category,
            guild_id=interaction.guild_id
        )
        ansToBool = {selectAnswerView.correct: True}
        correct_list = []
        for ans in self.answers:
            correct_list.append(ansToBool.get(ans, False))
        readyQuestion.answers = [database.QuizAnswer(answer=a , correct=s) for (a,s) in zip(self.answers, correct_list)]
        
        with database.Session() as session:
            with session.begin():
                session.add(readyQuestion)
            # inner context calls session.commit(), if there were no exceptions
        
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
