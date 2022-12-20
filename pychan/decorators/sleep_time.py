import nextcord


class SleepTime:
    @classmethod
    async def sleep_time(cls, ctx):
        """Bot complains that it is tired """
        embed = nextcord.Embed(title='',
                               description='',
                               color=nextcord.Color.dark_purple())
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/763164789458337802/831593468656222268/anime_sleepy.png')
        await ctx.send('Zmęczona jestem, napisz później :sleeping:')
        await ctx.send(embed=embed)
