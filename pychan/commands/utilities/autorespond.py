from nextcord import Message
from nextcord.ext.commands import Bot, Cog, Context, group
from sqlalchemy import select
from pychan.database import Autoresponse, Session

class Autorespond(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group(name="autorespond")
    async def autorespond(self, ctx: Context):
        '''Zarządzanie automatyczymi odpowiedziami na wiadomości'''
        if ctx.invoked_subcommand is None:
            await ctx.send_help("autorespond")

    @autorespond.command("dodaj")
    async def dodaj(self, ctx: Context, trigger: str, *, response: str):
        if ctx.guild is None:
            return

        with Session() as session:
            autoresponse = Autoresponse(guild_id=ctx.guild.id, trigger=trigger, response=response)
            session.add(autoresponse)
            session.commit()

        await ctx.reply(f'W porządku! Od dziś będę odpowiadać `{response}` kiedy ktoś powie `{trigger}`')

    @Cog.listener()
    async def on_message(self, msg: Message):
        if msg.author.bot:
            return

        if msg.guild == None:
            return

        responses = None
        with Session() as session:
            stmt = select(Autoresponse).filter_by(guild_id=msg.guild.id, trigger=msg.content)
            responses = session.scalars(stmt).all()

        for response in responses:
            await msg.reply(response.response)



