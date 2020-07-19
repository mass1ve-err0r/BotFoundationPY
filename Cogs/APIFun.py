import asyncio
import random
from iso3166 import countries as countryconv
from quickchart import QuickChart
from requests import get
from datetime import datetime
from discord import Embed, Colour
from discord.ext import commands


class APIFun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # <editor-fold  desc="[Animal Info + Pictures]">
    @commands.command(name="anifact")
    @commands.guild_only()
    async def gib_cat_fact(self, ctx, animal: str):
        dt = datetime.now()
        baseURL = "https://cat-fact.herokuapp.com/facts/random?animal_type=" + animal

        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None, get, baseURL)
        response_data = await future1
        data = {}
        try:
            data = response_data.json()
        except Exception:
            embedx0 = Embed(title="API Error!", colour=Colour(0x6DC8E2), timestamp=dt)
            embedx0.set_footer(text="Prototype X1")
            embedx0.add_field(name="Contact Info",value="Bot admin:\nmass1ve_err0r#0098", inline=False)
            await ctx.send(embed=embedx0)
            return

        title = "Random " + animal + " fact"
        embedx1 = Embed(title=title, colour=Colour(0x6DC8E2), timestamp=dt)
        embedx1.set_footer(text="Prototype X1")
        embedx1.add_field(name="**Fact**", value=str(data['text']), inline=False)
        embedx1.add_field(name="**Verified Fact**", value=str(data['status']['verified']), inline=False)
        await ctx.message.delete()
        await ctx.send(embed=embedx1)

    @commands.command("catpls")
    @commands.guild_only()
    async def gib_neko(self, ctx):
        phrases = ["NEKO !!!",
                   "Look at this cutie!",
                   "Another little tiger",
                   "Cats Cats Cats Cats!",
                   "Meow??",
                   "Cat coming right up!",
                   ]
        dt = datetime.now()
        baseURL = "https://aws.random.cat/meow"

        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None, get, baseURL)
        response_data = await future1
        data = response_data.json()

        if not bool(data):
            await ctx.send("API not available!", delete_after=5)
            return

        titlex = phrases[random.randint(0, 5)]
        embedx1 = Embed(title=titlex, colour=Colour(0x6DC8E2), timestamp=dt)
        embedx1.set_footer(text="Prototype X1")
        embedx1.set_image(url=data['file'])
        await ctx.message.delete()
        await ctx.send(embed=embedx1)

    @commands.command(name="doggopls")
    @commands.guild_only()
    async def gib_doggo(self, ctx):
        phrases = ["DOGGO !!!",
                   "Here's another Doggo!",
                   "Look at this gud boi",
                   "Look at this cute doggo!",
                   "Bro watch out for this one",
                   ]
        dt = datetime.now()
        baseURL = "https://random.dog/woof.json"

        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None, get, baseURL)
        response_data = await future1
        data = response_data.json()

        if not bool(data):
            await ctx.send("API not available!", delete_after=5)
            return

        titlex = phrases[random.randint(0, 4)]
        embedx1 = Embed(title=titlex, colour=Colour(0x6DC8E2), timestamp=dt)
        embedx1.set_footer(text="Prototype X1")
        embedx1.set_image(url=data['url'])
        await ctx.message.delete()
        await ctx.send(embed=embedx1)
    # </editor-fold>

    # <editor-fold desc="[Random APIs]">
    @commands.command(name="graph")
    @commands.guild_only()
    async def graph_data(self, ctx, title: str, labels: str, data: str):
        dt = datetime.now()
        labels_list = labels.split(",")
        data_list_str = data.split(",")

        if len(labels_list) != len(data_list_str):
            await ctx.send("Unequal amounts of data! (Labels != Data)")
            return

        data_list = [int(x) for x in data_list_str]

        qc = QuickChart()
        qc.width = 600
        qc.height = 400
        qc.device_pixel_ratio = 2.0
        qc.background_color = "#000000"
        qc.config = {
            "type": "bar",
            "data": {
                "labels": labels_list,
                "datasets": [{
                    "label": title,
                    "data": data_list
                }]
            }
        }
        end_url = qc.get_url()

        titlex = "The Results:"
        embedx1 = Embed(title=titlex, colour=Colour(0x6DC8E2), timestamp=dt)
        embedx1.set_footer(text="Prototype X1")
        embedx1.set_image(url=end_url)
        await ctx.message.delete()
        await ctx.send(embed=embedx1)

    @commands.command(name="origin")
    @commands.guild_only()
    async def guess_origin(self, ctx, name: str):
        dt = datetime.now()
        baseURL = "https://api.nationalize.io?name="

        if name is None:
            await ctx.send("Name not specified !", delete_after=5)
            return

        targetURL = baseURL + name
        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None, get, targetURL)
        response_data = await future1
        data = response_data.json()

        if not bool(data['country']):
            await ctx.send("Name invalid !", delete_after=5)
            return

        embedx1 = Embed(title="Origin Estimation", colour=Colour(0x6DC8E2), timestamp=dt)
        embedx1.set_footer(text="Prototype X1")
        embedx1.add_field(name="**Name**", value=name, inline=False)
        origin_str = ""
        for entry in data['country']:
            origin_str += "- Country: " + countryconv.get(entry['country_id']).name + "\nProbability: " + str(entry['probability']) + "%\n"
        embedx1.add_field(name="**Probabilities**", value=origin_str, inline=False)
        await ctx.message.delete()
        await ctx.send(embed=embedx1)

    @commands.command(name="xkcd")
    @commands.guild_only()
    async def get_xkcd_comic(self, ctx):
        dt = datetime.now()
        comicNum = str(random.randint(1, 2322))
        targetURL = "http://xkcd.com/" + comicNum + "/info.0.json"

        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None, get, targetURL)
        response_data = await future1
        data = response_data.json()

        if not bool(data['img']):
            await ctx.send("Error during fetch !", delete_after=5)
            return

        titlex = "xkcd Comic #" + comicNum
        embedx1 = Embed(title=titlex, colour=Colour(0x6DC8E2), timestamp=dt)
        embedx1.set_footer(text="Prototype X1")
        embedx1.set_image(url=data['img'])
        await ctx.message.delete()
        await ctx.send(embed=embedx1)

    @commands.command(name="joke")
    @commands.guild_only()
    async def get_joke_random(self, ctx):
        dt = datetime.now()
        targetURL = "https://official-joke-api.appspot.com/jokes/random"

        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None, get, targetURL)
        response_data = await future1
        data = response_data.json()

        outstr = data['setup'] + "\n- "
        outstr += "_" + data['punchline'] + "_"
        joke_nr = str(data['id'])
        embedx1 = Embed(title="Joke coming up!", colour=Colour(0x6DC8E2), timestamp=dt)
        embedx1.set_footer(text="Prototype X1")
        embedx1.add_field(name="**Joke #" + joke_nr + "**", value=outstr, inline=False)
        await ctx.send(embed=embedx1)

    @commands.command(name="trivia")
    @commands.guild_only()
    async def trivia_game(self, ctx):
        dt = datetime.now()
        targetURL = "https://opentdb.com/api.php?amount=1&difficulty=medium"

        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None, get, targetURL)
        response_data = await future1
        data = response_data.json()

        if data['response_code'] != 0:
            await ctx.send("Error during API call !")
            return

        await ctx.message.delete()
        embedx1 = Embed(title="Trivia Time!", colour=Colour(0x6DC8E2), timestamp=dt)
        embedx1.set_footer(text="Prototype X1")
        embedx1.add_field(name="*Category*", value=data['results'][0]['category'], inline=False)
        embedx1.add_field(name="*Question*", value=data['results'][0]['question'], inline=False)
        if data['results'][0]['type'] == "multiple":
            choices = data['results'][0]['incorrect_answers']
            choices.append(data['results'][0]['correct_answer'])
            random.shuffle(choices)
            outstr = ""
            for entry in choices:
                outstr += "- " + entry + "\n"
            embedx1.add_field(name="*Choices*", value=outstr, inline=False)
        else:
            embedx1.add_field(name="*Choices*", value="True or False", inline=False)
        await ctx.send(embed=embedx1)
        await ctx.send("You have 2 Minutes!")

        # await ctx.send("DEBUG KEY")
        print(data['results'][0]['correct_answer'])

        def check(channel):
            def inner_check(message):
                return message.channel.id == channel and message.content.lower() == data['results'][0]['correct_answer'].lower() and message.author != self.bot.user
                    # return message.content and message.author.id
            return inner_check

        try:
            msg = await self.bot.wait_for('message', check=check(ctx.channel.id), timeout=120)
            embedx2 = Embed(title="Trivia - Solved!", colour=Colour(0x6DC8E2), timestamp=dt)
            embedx2.set_footer(text="Prototype X1")
            embedx2.add_field(name="*Original Question*", value=data['results'][0]['question'], inline=False)
            embedx2.add_field(name="*Answer*", value=data['results'][0]['correct_answer'], inline=False)
            embedx2.add_field(name="*Solver (Nerd)*", value="<@" + str(msg.author.id) + ">", inline=False)
            await ctx.send(embed=embedx2)
            return
        except asyncio.TimeoutError:
            embedx2 = Embed(title="Trivia - Times Up!", colour=Colour(0x6DC8E2), timestamp=dt)
            embedx2.set_footer(text="Prototype X1")
            embedx2.add_field(name="*Original Question*", value=data['results'][0]['question'], inline=False)
            embedx2.add_field(name="*Answer*", value=data['results'][0]['correct_answer'], inline=False)
            await ctx.send(embed=embedx2)
            return

    # </editor-fold>


def setup(bot):
    bot.add_cog(APIFun(bot))
