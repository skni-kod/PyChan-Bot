from nextcord.ext import commands

from Core.Commands.Games.Functions.osrs import Osrs
from Core.Commands.Games.Functions.osu import Osu
from Core.Commands.Games.Functions.LoL import LoL
from Core.Commands.Games.Functions.TfT import TfT

import config

class Games(commands.Cog):
    """Class contains gaming methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot
        
        if len(config.osu_token):
            self.bot.add_cog(Osu(bot))
        else:
            print("Osu! API token not found. Related commands will not be loaded")

        if len(config.riot_token):
            self.bot.add_cog(LoL(bot))
        else:
            print("Riot API token not found. Related commands will not be loaded")

        if len(config.riot_token_TFT):
            self.bot.add_cog(TfT(bot))
        else:
            print("Riot API token TFT not found. Related commands will not be loaded")
            
        self.bot.add_cog(Osrs(bot))
