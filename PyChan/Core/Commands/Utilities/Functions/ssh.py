from discord.ext import commands
import os
import time

def check_if_it_is_me(ctx):
    return ctx.message.author.id == 375715270817480705 or ctx.message.author.id == 447026596575051787


class Ssh(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='ssh_update')
    @commands.check(check_if_it_is_me)
    async def ssh_update(self, ctx):
        os.system('sudo bash /home/pi/bot_update.sh')
        mess = await ctx.send(f"Update zacznie się za {30} sekund")
        for x in range(30):
            time.sleep(1)
            await mess.edit(content=f"Update zacznie się za {30-x-1} sekund")
        await mess.edit(content=":zzz:")
        os.system("sudo reboot")


