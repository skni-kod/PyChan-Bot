import nextcord
from nextcord import Colour, Embed

from pychan import database
from .modals import CategoryModal

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

        # todo pobieranie kategorii z bazy do StringSelect
        all_questions: list[database.QuizQuestion] = database.session.query(database.QuizQuestion).all()
        #set to not repeat the category, albo sqlem wyciagnij??
        category_set = {que.category for que in all_questions}

        self.selectCategory = nextcord.ui.StringSelect(
            min_values = 0,
            max_values = 1,
            placeholder = "Wybierz kategorie",

            options=[
            
                nextcord.SelectOption(label = categ) for categ in category_set
                
                # nextcord.SelectOption(label="JAIO"),
                # nextcord.SelectOption(label="Systemy Operacyjne"),
                # nextcord.SelectOption(label="C++"),
                # nextcord.SelectOption(label="Podstawy Elektroniki")
            ])
        self.add_item(self.selectCategory)

    @nextcord.ui.button(label = "Dodaj kategorię", style=nextcord.ButtonStyle.blurple)
    async def addCategoryB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True

        modal = CategoryModal()
        await interaction.response.send_modal(modal)
        
        #below line to check if getting correct category
        await modal.wait()

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

        self.correct = self.selectOdpPopr.values[0]
        result = [self.question, self.answers, self.correct, self.category]
        final_view = successfulQuestion(result)
        await self.viewYouCanEdit.edit(view = final_view, embed = final_view.embed)


        #dodawanie do bazy
        question = database.QuizQuestion(question=self.question, category=self.category)
        letterToNum = {"A": 0, "B": 1, "C": 2, "D": 3}
        numToCorrect = {letterToNum[self.correct]: True}
        correct_list = []
        for x in range(len(self.answers)):
            correct_list.append(numToCorrect.get(x, False))
        question.answers = [database.QuizAnswer(answer=a , correct=s) for (a,s) in zip(self.answers, correct_list)]

        #!!!!!!!!!!!!!!!!!
        #uncomment when ready
        #database.session.add(question)
        #database.session.commit()

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
        self.points = 0


        