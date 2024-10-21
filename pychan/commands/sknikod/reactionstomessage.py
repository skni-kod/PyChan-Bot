import nextcord
from nextcord.ext import commands
import os


class ReactionsToMessage(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        pass_context=True,
        name='reactionstomessage',
        usage='<wiadomość>',
        alias = ['rtm'],
        help="""Wypisuje wszystkie osoby ktore zareagowały na daną wiadomość na podstawie linku do tej wiadomości
        """
    )
    
    async def reactionstomessage(self, ctx, message):
        if not message.startswith('https://discord.com/channels/'):
            await ctx.send('Podaj link do wiadomości')
            return
        message = message.split('/')
        if len(message) != 7:
            await ctx.send('Podaj link do wiadomości')
            return
        try:
            message = await self.bot.get_channel(int(message[5])).fetch_message(int(message[6]))
        except:
            await ctx.send('Podaj link do wiadomości')
            return
        users = []
        for reaction in message.reactions:
            async for user in reaction.users():
                if user not in users:
                    users.append(user)
                    if user.display_name != user.name:
                        users.append(user.display_name)
                    users.append("\n")
        if len(users) == 0:
            await ctx.send('Brak reakcji')
            return
        
        file = open('reactionstomessage.txt', 'w', encoding='utf-8')
        for user in users:
            file.write(str(user) + '\n')
        file.close()
        await ctx.send(file=nextcord.File('reactionstomessage.txt'))
        os.remove('reactionstomessage.txt')
        