from nextcord.ext.commands import Context


def check_sknikod(ctx: Context):
    return ctx.guild and ctx.guild.id == 381092165729910786
