from nextcord.ext import commands
import json

import Database

class QuizTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Dodawanie pytań
    @commands.command()
    async def quiztest(self, ctx: commands.Context):
        question = Database.QuizQuestion(question="Hello?", category="Test")
        Database.session.add(question)
        Database.session.commit()

    # Dodawanie odpowiedzi
    @commands.command()
    async def quiztest2(self, ctx: commands.Context):
        questions: list[Database.QuizQuestion] = Database.session.query(Database.QuizQuestion).all()
        questions[0].answers.append(Database.QuizAnswer(answer="Tak", correct=True))
        questions[0].answers.append(Database.QuizAnswer(answer="Nie", correct=False))
        Database.session.commit()

    # Wyświetlanie pytań z odpowniedziami
    @commands.command()
    async def quiztest3(self, ctx: commands.Context):
        questions: list[Database.QuizQuestion] = Database.session.query(Database.QuizQuestion).all()
        for q in questions:
            print(q.question)
            for a in q.answers:
                print('-', a.answer)
