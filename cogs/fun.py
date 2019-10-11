import discord
import aiohttp
from discord.ext import commands
from random import choice, randint
from cogs.utils.dataIO import DataIO
from urllib.parse import urlencode



class Fun:
    """Commands used 4Fun"""

    def __init__(self, bot):
        self.bot = bot
        self.memes = "data/memes.json"
        self.pepes = "data/pepes.json"

        dataIO = DataIO() 
        self.system_memes = dataIO.load_json(self.memes)
        self.system_pepes = dataIO.load_json(self.pepes)
        self.ball = ["As I see it, yes", "It is certain", "Most likely", "Me llamo Jeff", "I like doors", "Can I F*CK a door plz?", "You’re definitely going to die alone",
                     "Signs point to yes", "Without a doubt", "Yes", "Definitely", "Ask again later", "Better not tell you now", "Mother Misha", "Don't count on it",
                     "My reply is no", "Outlook not so good", "Very doubtful", "IDK", "At Least I Love You", "Dumb Question Ask Another", "I've Got a Headache", "F*CK OFF", "You Wish",
                     "You've Got To Be F*cking Kidding", "Bush Did 9/11", "You're Not the Brightest Individual", "Yeah And I'm Jesus", "Joey Salads, Just Joey Salads (and piss)", "Keep it PG - I need that revenue",
                     "Daddy Durv"]

    @commands.command(name="8ball", aliases=["8"])
    async def _ball(self, *args):
        """Ask the 8 Ball a question"""
        print(args)
        answer = randint(0, len(self.ball) - 1)
        await self.bot.say(self.ball[answer])

    @commands.command(name="say", aliases=["sey"])
    async def _say(self, *args):
        """Says what you ask the bot to say"""
        print(args)
        await self.bot.say(' '.join(args))

    @commands.group(name="memes")
    async def _memes(self, *args):
        """Sends a random meme"""
        await self.bot.say(choice(self.system_memes["memes"]))

    @commands.group(name="pepe")
    async def _pepe(self, *args):
        """Sends a random pepe"""
        await self.bot.say(choice(self.system_pepes["pepes"]))

    @commands.command(name="search", aliases=["scr"])
    async def _search(self, *args):
        """Searches google for your query"""
        print(args)
        await self.bot.say("https://www.google.co.uk/search?{}".format(urlencode({'q': ' '.join(args)})))

    @commands.command(name="badmeme", pass_context=True)
    async def _badmeme(self):
        """Sends a stale meme"""
        session = aiohttp.ClientSession()
        async with session.get("https://api.imgflip.com/get_memes") as r:
            result = await r.json()
            url = choice(result["data"]["memes"])
            url = url["url"]
            await self.bot.say(url)

    @commands.command(name="durv", pass_context=True)
    async def _durv(self):
        """Durv's latest video"""
        session = aiohttp.ClientSession()
        async with session.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=1&playlistId=UUsNU-z2Nxsm5xfSusglV9Zw&key=AIzaSyANeKzjbCdfm9LapeIzVUgCwQV3SemYpgE") as r:
            result = await r.json()
            url = result["items"][0]
            url = url["snippet"]
            url = url["resourceId"]
            url = url["videoId"]
            url = "https://www.youtube.com/watch?v=" + url
            await self.bot.say("**Here's Durv's Latest Video:**\n" + url)

    @commands.command(name="giphy", aliases=['gif'])
    async def _giphy(self, *, text: str = None):
        """Searches for random gif or for one you searched for"""
        if text is None:
            url = 'http://api.giphy.com/v1/gifs/random?&api_key=dc6zaTOxFJmzC'

            session = aiohttp.ClientSession()
            async with session.get(url) as r:
                result = await r.json()
                data = result["data"]
                data = data["image_url"]
                await self.bot.say(data)
        else:
            #text = ("".join(text))
            print(text)
            url = ("http://api.giphy.com/v1/gifs/search?q{}&api_key=dc6zaTOxFJmzC".format(urlencode({'': ''.join(text)})))

            session = aiohttp.ClientSession()
            async with session.get(url) as r:
                result = await r.json()
                if len(result["data"]) == 0:
                    await self.bot.say(":warning: No results came up for your search!")

                else:
                    data = choice(result["data"])
                    data = data["url"]
                    await self.bot.say(data)

    @commands.command(name="urban", aliases=["dict", "dictionary"])
    async def _urban(self, *, search_query: str):
        """Searches the urban dictionary for specified query"""

        search_query = "+".join(search_query)
        url = "http://api.urbandictionary.com/v0/define?term=" + search_query

        session = aiohttp.ClientSession()
        async with session.get(url) as data:
            result = await data.json()

        if result["list"]:
            definition = result['list'][0]['definition']
            msg = ("**Definition:**\n{}".format(definition))
            await self.bot.say(msg)

        else:
            await self.bot.say("Your search gave no results!")




def setup(bot):
    n = Fun(bot)
    bot.add_cog(n)
