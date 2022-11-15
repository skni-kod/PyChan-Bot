import nextcord
from nextcord.ext import commands


class QR(commands.Cog):
    """Class contains QR generator method"""

    def __init__(self, bot):
        """Constructor method"""
        self.bot = bot

    @commands.command(
        pass_context=True, 
        name="qr", 
        category="Obraz",
        usage = "<link do obrazu>",
        help = """
               Generuje kod QR z podanego linku do obrazu.
               """
        )
    async def qr(self, ctx, arg):
        embed = nextcord.Embed()
        embed.set_image(url="https://www.qrtag.net/api/qr_6.png?url=" + str(arg))
        await ctx.send(embed=embed)