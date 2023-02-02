from nextcord.ext import commands
from nextcord import Colour, Embed
import nextcord
import asyncio

from pychan import database
#from .embedModal import EmbedModal
from .categoryModal import CategoryModal


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

class AddCategoryAndAnswer(nextcord.ui.View):
    def __init__(self, viewYouCanEdit: nextcord.Message, question: str, answers: list[str]):
        super().__init__()
        self.value = None
        self.newCategory = False
        self.category = ""
        self.correct = ""

        self.viewYouCanEdit = viewYouCanEdit
        self.question = question
        self.answers = answers
        # todo zrobic tak ze jak c d sa puste to ich nie dawac | jak c puste a d cos ma to zamien d na c
        self.selectOdpPopr = nextcord.ui.StringSelect(
            min_values = 1,
            max_values = 1,
            placeholder = "Wybierz poprawną odpowiedź",
            options=[
                nextcord.SelectOption(label="A"),
                nextcord.SelectOption(label="B"),
                nextcord.SelectOption(label="C"),
                nextcord.SelectOption(label="D")
            ])
        self.add_item(self.selectOdpPopr)

        # todo pobieranie kategorii z bazy
        self.selectCategory = nextcord.ui.StringSelect(
            min_values = 0,
            max_values = 1,
            placeholder = "Wybierz kategorie",
            options=[
                nextcord.SelectOption(label="JAIO"),
                nextcord.SelectOption(label="Systemy Operacyjne"),
                nextcord.SelectOption(label="C++"),
                nextcord.SelectOption(label="Podstawy Elektroniki")
            ])
        self.add_item(self.selectCategory)

    @nextcord.ui.button(label = "Dodaj kategorię", style=nextcord.ButtonStyle.blurple)
    async def addCategoryB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        #this modal should change first value of our strlist
        #todo
        semaf = asyncio.Semaphore(1)
        modal = CategoryModal(semaf)
        await semaf.acquire()
        await interaction.response.send_modal(modal)
        #await modal.wait()
        async with semaf:
            self.category = modal.categoryStr
    
    @nextcord.ui.button(label = "Gotowe", style=nextcord.ButtonStyle.green)
    async def endAdding(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        
        #psarwdz czy nie wybrano opcji c lub d jak jej nie podano
        try:
            if len(self.selectCategory.values) != 0: #not empty
                self.category = self.selectCategory.values[0]
            elif self.category == "":
                raise KeyError("Nie wybrano kategorii")

            if len(self.selectOdpPopr.values) == 0:
                raise KeyError("Nie wybrano poprawnej odpowiedzi")
        except KeyError as keyE:
            await interaction.send(embed=Embed(title=keyE.args[0]))
            return

        result = [self.question, self.answers, self.selectOdpPopr.values[0], self.category]
        final_view = successfulQuestion(result)
        await self.viewYouCanEdit.edit(view = final_view, embed = final_view.embed)


        #todo dodawanie do bazy
        self.stop()

class successfulQuestion(nextcord.ui.View):
    def __init__(self, result: list[str]):
        super().__init__()
        self.value = None
        
        description = "Pytanie: " + result[0] + "\n"

        abcd = ["A: ", "B: ", "C: ", "D: "]
        for i, ans in enumerate(result[1]):
            description += abcd[i]
            description += ans
            description += "\n"
        description += f"Poprawna: {result[2]}\n Kategoria: {result[3]}"

        self.embed = Embed( title = "Udało się dodać pytanie",
                            description = description,
                            color = Colour.green()
                            )

class startQuiz(nextcord.ui.View):
    def __init__(self, question: database.QuizQuestion):
        super().__init__()
        self.value = None
        self.question = question
        self.embed = Embed( title = question.question,
                            color = Colour.blurple()
                            )
        self.listOfButtons = []

#todo move this to modals file
class EmbedModal(nextcord.ui.Modal):
    def __init__(self, viewYouCanEdit: nextcord.Message):
        super().__init__("Dodaj pytnie do quizu!")
        
        self.viewYouCanEdit = viewYouCanEdit

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
        #pass data and change view
        #to pewnie w try
        newEmbed = nextcord.Embed(
                title = f"Jeszcze chwila!",
                description = "Dodaj poprawną odpowiedź oraz kategorię",
                color = nextcord.Colour.green(), 
            )
        
        answers = [self.embedOdpA.value, self.embedOdpB.value,]
        if self.embedOdpC.value != "":
            answers.append(self.embedOdpC.value)
        if self.embedOdpD.value != "":
            answers.append(self.embedOdpD.value)
    
        newView = AddCategoryAndAnswer(self.viewYouCanEdit,
                                    self.embedTitle.value, 
                                    answers)
        await self.viewYouCanEdit.edit(view = newView, embed=newEmbed)
        
        self.stop()


    '''second modal
    unused, but maybe someone will find a way to apply 2 modals...
    and StringSelect will be supported in Modals
    '''
 