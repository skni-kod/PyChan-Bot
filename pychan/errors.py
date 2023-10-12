from nextcord import Color, Embed
from nextcord.ext.commands import BadArgument, Cog, CommandError, CommandInvokeError, CommandNotFound, Context, MissingPermissions, MissingRequiredArgument


class Errors(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        match error:
            case CommandNotFound():
                embed = Embed(color=Color.dark_purple())
                embed.add_field(name='Błąd',
                                value='Podana komenda nie istnieje',
                                inline=False)
                await ctx.send(embed=embed)
            case BadArgument():
                await ctx.send('Niepoprawny parametr')
            case MissingRequiredArgument():
                await ctx.send('Brakuje wymaganego parametru (`' + error.param.name + '`)')
            case MissingPermissions():
                embed = Embed(color=Color.dark_purple())
                embed.add_field(name='Brak uprawnień',
                                value='Brakujące uprawinienia to: `' +
                                ', '.join(error.missing_permissions) + '`',
                                inline=False)
                await ctx.send(embed=embed)
            case CommandInvokeError():
                await ctx.send(f'Coś poszło nie tak (`{error.original.__class__.__name__}`)')
                raise error.original
            case _:
                print("COŚ SERIO POSZŁO NIE TAK")
                raise error
