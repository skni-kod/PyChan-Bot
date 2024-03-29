import nextcord
from nextcord.ext import commands


class QR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        name="qr",
        category="Media",
        usage="<link do obrazu>",
        help="""
               Generuje kod QR z podanego linku do obrazu.
               """
    )
    async def qr(self, ctx, arg):
        embed = nextcord.Embed()
        embed.set_image(
            url="https://www.qrtag.net/api/qr_6.png?url=" + str(arg))
        await ctx.send(embed=embed)
