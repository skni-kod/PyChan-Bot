import nextcord
import asyncio
class CategoryModal(nextcord.ui.Modal):
    '''Modal to add new category'''
    def __init__(self, semaphore: asyncio.Semaphore):
        super().__init__("Dodaj kategorię!")
        self.categoryStr = ""
        self.category = nextcord.ui.TextInput(
            label = "Kategoria", min_length = 1, max_length = 124,
            required = True, placeholder = "Tutaj wpisz nową kategorię")
        self.add_item(self.category)

        self.semaphore = semaphore

    async def callback(self, interaction: nextcord.Interaction):
        print("modal dodajj")

        self.categoryStr = self.category.value
        self.semaphore.release()
        self.stop()