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
        if self.category.value != "":
            self.categoryStr = self.category.value
            await interaction.response.send_message(embed = nextcord.Embed(title="Dodano nową kategorię",
                                                        color=nextcord.Colour.green()), delete_after=15)
        self.stop()

class EmbedModal(nextcord.ui.Modal):
    '''Modal to add new question with answers'''
    def __init__(self):
        super().__init__("Dodaj pytnie do quizu!")
        self.answers = []

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
        self.answers = [self.embedOdpA.value, self.embedOdpB.value,]
        if self.embedOdpC.value != "":
            self.answers.append(self.embedOdpC.value)
        if self.embedOdpD.value != "":
            self.answers.append(self.embedOdpD.value)
        self.stop()

