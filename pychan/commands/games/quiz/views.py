import nextcord
from nextcord import Colour, Embed
from sqlalchemy import select

from pychan import database
from .modals import CategoryModal

class SelectCategoryView (nextcord.ui.View):
    def __init__(self, viewYouCanEdit: nextcord.Message):
        super().__init__()
        self.value = None
        self.category = ""

        self.viewYouCanEdit = viewYouCanEdit

        with database.session() as session:
            all_categories = session.scalars(select(database.QuizQuestion.category)).all()

            #set to not repeat the category
            category_set = set(all_categories)

            if len(category_set) == 0:
                category_set.add('Inne')

            self.selectCategory = nextcord.ui.StringSelect(
                min_values = 0,
                max_values = 1,
                placeholder = "Wybierz kategorie",
                options=[nextcord.SelectOption(label = categ) for categ in category_set])
            
            self.add_item(self.selectCategory)

    @nextcord.ui.button(label = "Dodaj kategorię", style=nextcord.ButtonStyle.blurple, row=2)
    async def addCategoryB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True

        modal = CategoryModal()
        await interaction.response.send_modal(modal)
        timeout = await modal.wait()

        if not timeout:
            self.category = modal.categoryStr
            self.stop()
    
    @nextcord.ui.button(label = "Gotowe", style=nextcord.ButtonStyle.green, row=2)
    async def endAdding(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True

        if self.category == "":
            if len(self.selectCategory.values) == 0:
                await interaction.send(embed=Embed(title="Nie wybrano kategorii"), delete_after=15)
                return
            else:
                self.category = self.selectCategory.values[0]
        
        self.stop()
class SelectAnswerView (nextcord.ui.View):
    def __init__(self, viewYouCanEdit: nextcord.Message, answers: list[str]):
        super().__init__()
        self.value = None
        self.correct = ""

        self.viewYouCanEdit = viewYouCanEdit
        self.answers = answers

        self.selectOdpPopr = nextcord.ui.StringSelect(
            min_values = 1,
            max_values = 1,
            placeholder = "Wybierz poprawną odpowiedź",
            options=[nextcord.SelectOption(label=odp) for odp in answers])
        self.add_item(self.selectOdpPopr)
    
    @nextcord.ui.button(label = "Gotowe", style=nextcord.ButtonStyle.green, row=2)
    async def endAdding(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        
        if len(self.selectOdpPopr.values) == 0:
            await interaction.send(embed=Embed(title="Nie wybrano poprawnej odpowiedzi"), delete_after=15)
            return

        self.correct = self.selectOdpPopr.values[0]
        self.stop()


class successfulQuestion(nextcord.ui.View):
    def __init__(self, question: str, answers: list[str], correct: str, category: str):
        super().__init__()
        self.value = None
        
        description = "Pytanie: " + question + "\n"

        abcd = ["A: ", "B: ", "C: ", "D: "]
        for i, ans in enumerate(answers):
            description += abcd[i]
            description += ans
            description += "\n"
        description += f"Poprawna: {correct}\n Kategoria: {category}"

        self.embed = Embed( title = "Udało się dodać pytanie",
                            description = description,
                            color = Colour.green()
                            )
        self.embed_for_all = Embed( title = "Udało się dodać pytanie",
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
        self.points = 0
        