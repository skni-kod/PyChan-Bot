from nextcord.ext import commands

from .osrs import Osrs
from .osu import Osu
from .lol import LoL

import config

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        if len(config.osu_token):
            self.bot.add_cog(Osu(bot))
        else:
            print("Osu! API token not found. Related commands will not be loaded")

        if len(config.riot_token):
            self.bot.add_cog(LoL(bot))
        else:
            print("Riot API token not found. Related commands will not be loaded")

        self.bot.add_cog(Osrs(bot))
