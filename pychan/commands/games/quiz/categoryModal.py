import nextcord

class CategoryModal(nextcord.ui.Modal):
    '''Modal to add new category'''
    def __init__(self, strlist: list[str]):
        super().__init__("Dodaj kategorię!")
        self.strlist = strlist
        self.category = nextcord.ui.TextInput(
            label = "Kategoria", min_length = 3, max_length = 124,
            required = True, placeholder = "Tutaj wpisz nową kategorię")
        self.add_item(self.category)

    async def callback(self, interaction: nextcord.Interaction):
        self.strlist[0] = self.category.value