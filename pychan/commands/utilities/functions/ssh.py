from nextcord.ext import commands
import os
import time


class SSH(commands.Cog):
    """Class contains ssh methods
    """

    def __init__(self, bot):
        """Constructor method
        """
        self.bot = bot

    class CheckIfItsLeader:
        """Class contains check method
        """
        @staticmethod
        def check_if_it_is_leader(ctx):
            """Checks if message's author is a leader

            :param ctx: the context in which a command is called
            :type ctx: nextcord.ext.commands.Context
            :return: returns True if author is a leader
            :rtype: bool
            """
            return ctx.message.author.id == 375715270817480705 or ctx.message.author.id == 447026596575051787

    @commands.command(pass_context=True, name='ssh_update')
    @commands.check(CheckIfItsLeader.check_if_it_is_leader)
    async def ssh_update(self, ctx):
        """Updates repository on RaspberryPi

        :param ctx: the context in which a command is called
        :type ctx: nextcord.ext.commands.Context
        """
        os.system('bash /home/pi/SkniBot/bot_update.sh')
        mess = await ctx.send(f"Update zacznie się za {30} sekund")
        for x in range(30):
            time.sleep(1)
            await mess.edit(content=f"Update zacznie się za {30-x-1} sekund")
        await mess.edit(content=":zzz:")
        os.system("sudo reboot")
