import nextcord
from nextcord.ext import commands
try:
    import asyncpraw
    import asyncprawcore
except:
  print("not working no module install")
from config import reddit_client_id, reddit_client_secret, reddit_user_agent, reddit_refresh_token

export = { "reddit": None }
noRepeatsCache = []

class Reddit(commands.Cog):
    
    def _init_(self, bot):
        self.bot = bot
    
    @commands.command(
        pass_context=True,
        name="reddit",
        category="Tekst",
        usage="<subreddit>",
        help="""
             Wyświetla losowy post z danego subredditu
             """
    )
    async def reddit(self, ctx, *, sub: str):
        unsafeChannel = ctx.channel.is_nsfw()
        embed = nextcord.Embed(
                title=f"r/{sub}",
                color=nextcord.Color.red()
            )
        if(sub.startswith("r/")):
            sub = sub[2:]
        if(sub.endswith("/")):
            sub = sub[:-1]
        
        if(len(sub) == 0):
            embed.title = "Błąd"
            embed.description = "Nie podano nazwy subredditu."
            await ctx.send(embed=embed)
            return
            
        reddit = asyncpraw.Reddit(
                            client_id = reddit_client_id, 
                            client_secret = reddit_client_secret, 
                            user_agent = reddit_user_agent,
                            refresh_token = reddit_refresh_token)
        
        try:
            data = await reddit.subreddit(sub)
            await data.load()
        except asyncprawcore.exceptions.NotFound:
            embed.description = "Nie znaleziono takiego subredditu."
            await ctx.send(embed=embed)
            await reddit.close()
            return
        
        if(data.over18 and not unsafeChannel):
            embed.description = "Ten subreddit jest NSFW, a ten kanał nie. Spróbuj w kanale NSFW."
            await ctx.send(embed=embed)
            await reddit.close()
            return
        
        async for post in data.hot(limit=100):
            if(post.stickied):
                continue
            if(post.id in noRepeatsCache):
                continue
            noRepeatsCache.append(post.id)
            if(len(noRepeatsCache) > 20):
                noRepeatsCache.pop(0)
            embed.title = post.title
            embed.url = f"https://reddit.com{post.permalink}"
            if(post.is_self):
                embed.description = post.selftext
            else:
                embed.set_image(url=post.url)
            break
        
        await ctx.send(embed=embed)
        await reddit.close()