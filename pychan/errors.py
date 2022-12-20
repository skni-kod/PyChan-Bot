from nextcord import Color, Embed
from nextcord.ext.commands import BadArgument, Cog, CommandError, CommandNotFound, Context, MissingRequiredArgument


class Errors(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if isinstance(error, CommandNotFound):
            embed = Embed(color=Color.dark_purple())
            embed.add_field(name='Błąd',
                            value='Podana komenda nie istnieje',
                            inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, BadArgument):
            await ctx.send('Niepoprawny parametr')
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send('Brakuje wymaganego parametru')
        elif isinstance(error, Exception):
            await ctx.send('Coś poszło nie tak')
            print(error)
        else:
            print(error)
