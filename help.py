import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title='Help',
                              description='Wpisz `^help <nazwa_komendy>` aby uzyskać więcej informacji.\n'
                                          '\n'                                          
                                          'Dostępne komendy:',
                              color=discord.Color.dark_purple())
        embed.add_field(name='Matematyka',
                        value='`test`',
                        inline=False)

        await ctx.send(embed=embed)
