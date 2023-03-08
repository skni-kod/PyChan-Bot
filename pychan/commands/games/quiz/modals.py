import nextcord
class CategoryModal(nextcord.ui.Modal):
    '''Modal to add new category'''
    def __init__(self):
        super().__init__("Dodaj kategorię!")
        self.categoryStr = ""
        self.category = nextcord.ui.TextInput(
            label = "Kategoria", min_length = 1, max_length = 99,
            required = True, placeholder = "Tutaj wpisz nową kategorię")
        self.add_item(self.category)

    async def callback(self, interaction: nextcord.Interaction):
        self.categoryStr = self.category.value
        self.stop()

#this import should be after CategoryModal(circular import error)
from .views import AddCategoryAndAnswer
class EmbedModal(nextcord.ui.Modal):
    '''Modal to add new question with answers'''
    def __init__(self, viewYouCanEdit: nextcord.Message):
        super().__init__("Dodaj pytnie do quizu!")
        
        self.viewYouCanEdit = viewYouCanEdit

        self.embedTitle = nextcord.ui.TextInput(
            label = "Pytanie", min_length = 3, max_length = 124,
            required = True, placeholder = "Tutaj wpisz pytanie",
            style = nextcord.TextInputStyle.paragraph)
        self.add_item(self.embedTitle)

        self.embedOdpA = nextcord.ui.TextInput(
            label = "A", min_length = 0, max_length = 99,
            required = True, placeholder = "Tutaj wpisz odpowiedź A")
        self.add_item(self.embedOdpA)

        self.embedOdpB = nextcord.ui.TextInput(
            label = "B", min_length = 0, max_length = 99,
            required = True, placeholder = "Tutaj wpisz odpowiedź B")
        self.add_item(self.embedOdpB)

        self.embedOdpC = nextcord.ui.TextInput(
            label = "C", min_length = 0, max_length = 99,
            required = False, placeholder = "Tutaj wpisz odpowiedź C")
        self.add_item(self.embedOdpC)

        self.embedOdpD = nextcord.ui.TextInput(
            label = "D", min_length = 0, max_length = 99,
            required = False, placeholder = "Tutaj wpisz odpowiedź D")
        self.add_item(self.embedOdpD)

    async def callback(self, interaction: nextcord.Interaction):
        #pass data and change view
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

