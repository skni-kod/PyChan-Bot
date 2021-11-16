import requests
import discord
from discord.ext import commands
from apod_token import apod_token

class ApodImage(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='apod')
    async def apod(self, ctx):
        data = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={apod_token}")
        #imgurl = data.json()['hdurl']
        imgurl = "https://www.youtube.com/watch?v=7NykS2kv_k8&list=TLGGNhcYlATJB8kxNjExMjAyMQ&t=4s"

        embed = discord.Embed(title='Astronomy picture of the day',
                            description= data.json()['explanation'],
                            color=discord.Color.dark_purple())

        if("youtube.com" in imgurl):
            #await ctx.send(imgurl)
            TestVideoEmbed = {}
            TestVideoEmbed['type'] = 'video'
            TestVideoEmbed['url'] = 'https://www.youtube.com/watch?v=7NykS2kv_k8&list=TLGGNhcYlATJB8kxNjExMjAyMQ&t=4s'
            VideoDict = {}
            VideoDict['height'] = 480
            VideoDict['proxy_url'] = 'https://www.youtube.com/watch?v=7NykS2kv_k8&list=TLGGNhcYlATJB8kxNjExMjAyMQ&t=4s'
            VideoDict['url'] = 'https://www.youtube.com/watch?v=7NykS2kv_k8&list=TLGGNhcYlATJB8kxNjExMjAyMQ&t=4s'
            VideoDict['width'] = 480
            TestVideoEmbed['video'] = VideoDict
            CreatedEmbed = discord.embeds.Embed.from_dict(TestVideoEmbed)
            await ctx.send(embed = CreatedEmbed)
        else:
            embed.set_image(url = imgurl)

        await ctx.send(embed = embed)



        