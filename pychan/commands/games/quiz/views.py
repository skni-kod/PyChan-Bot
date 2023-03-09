import nextcord
from nextcord import Colour, Embed

from pychan import database
from .modals import CategoryModal

class AddCategoryAndAnswer(nextcord.ui.View):
    def __init__(self, viewYouCanEdit: nextcord.Message, question: str, answers: list[str]):
        super().__init__()
        self.value = None
        self.category = ""
        self.correct = ""

        self.viewYouCanEdit = viewYouCanEdit
        self.question = question
        self.answers = answers
        self.ready_question : database.QuizQuestion

        self.selectOdpPopr = nextcord.ui.StringSelect(
            min_values = 1,
            max_values = 1,
            placeholder = "Wybierz poprawną odpowiedź",
            options=[nextcord.SelectOption(label=odp) for odp in answers])
        self.add_item(self.selectOdpPopr)

        all_questions: list[database.QuizQuestion] = database.session.query(database.QuizQuestion).all()
        #albo sqlem wyciagnij??

        #set to not repeat the category
        category_set = {que.category for que in all_questions}

        self.selectCategory = nextcord.ui.StringSelect(
            min_values = 0,
            max_values = 1,
            placeholder = "Wybierz kategorie",
            options=[nextcord.SelectOption(label = categ) for categ in category_set])
        
        self.add_item(self.selectCategory)

    @nextcord.ui.button(label = "Dodaj kategorię", style=nextcord.ButtonStyle.blurple)
    async def addCategoryB(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True

        modal = CategoryModal()
        await interaction.response.send_modal(modal)
        
        await modal.wait()

        self.category = modal.categoryStr
    
    @nextcord.ui.button(label = "Gotowe", style=nextcord.ButtonStyle.green)
    async def endAdding(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        
        try:
            if self.category == "":
                if len(self.selectCategory.values) == 0:
                    raise KeyError("Nie wybrano kategorii")
                else:
                    self.category = self.selectCategory.values[0]

            if len(self.selectOdpPopr.values) == 0:
                raise KeyError("Nie wybrano poprawnej odpowiedzi")
        except KeyError as keyE:
            await interaction.send(embed=Embed(title=keyE.args[0]), delete_after=15)
            return

        self.correct = self.selectOdpPopr.values[0]
        result = [self.question, self.answers, self.correct, self.category]
        final_view = successfulQuestion(result)
        await self.viewYouCanEdit.edit(view = final_view, embed = final_view.embed_for_all)
        await interaction.response.send_message(embed=final_view.embed, ephemeral = True)

        question = database.QuizQuestion(question=self.question, category=self.category)
        ansToBool = {self.correct:True}
        correct_list = []
        for ans in self.answers:
            correct_list.append(ansToBool.get(ans, False))
        question.answers = [database.QuizAnswer(answer=a , correct=s) for (a,s) in zip(self.answers, correct_list)]

        self.ready_question = question
        
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


        