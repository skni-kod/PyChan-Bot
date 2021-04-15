import discord
from discord.ext import commands, tasks

from Core.Commands.Utilities.Functions.ssh import Ssh
from Database.database import Database

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_cog(Ssh(bot))
        self.check_connect_with_db.start()

    @tasks.loop(minutes=60)
    async def check_connect_with_db(self):
        response = Database.check_connect_with_db()
        if response is not True:
            print(f'[MongoDB error] {response}')
            admin1 = await self.bot.fetch_user(447026596575051787)
            admin2 = await self.bot.fetch_user(375715270817480705)
            await admin1.send(f'[MongoDB error] {response}')
            await admin2.send(f'[MongoDB error] {response}')

    @check_connect_with_db.before_loop
    async def before_check_connect_with_db(self):
        await self.bot.wait_until_ready()