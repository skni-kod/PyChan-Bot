import nextcord
from nextcord import Colour, Embed
import asyncio

from pychan import database
from .modals import CategoryModal

#zastap semafory ta 1 funkcja kek

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