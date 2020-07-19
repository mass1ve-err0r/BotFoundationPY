import asyncio
import random
from secrets import randbelow
from Models.dicewareMap import dicewareMap
from collections import defaultdict
from datetime import datetime
from discord import Embed, Colour
from discord.ext import commands


class Gamer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._mathsterrace_ongoing = False
        self._know_your_keyboard_ongoing = False

    # <editor-fold  desc="[EQ Solver]">
    @commands.command(name="mathsterrace")
    @commands.guild_only()
    async def mathsterrace(self, ctx, wins: int, difficulty: str):
        if wins < 0:
            embedx = Embed(title="Mathster Race - GameError", colour=Colour(0x6DC8E2))
            embedx.set_footer(text="Prototype X1")
            embedx.add_field(name="*Game Status*", value="No wins defined / Negative Number!", inline=False)
            await ctx.send(embed=embedx)
            return
        elif self._mathsterrace_ongoing:
            embedx = Embed(title="Mathster Race - GameError", colour=Colour(0x6DC8E2))
            embedx.set_footer(text="Prototype X1")
            embedx.add_field(name="*Game Status*", value="A Game's already running!", inline=False)
            await ctx.send(embed=embedx)
            return

        _mathsterrace_ongoing = True
        ops = []
        _varsNum = 0
        if difficulty == "hard":
            ops = ['+', "*", "^", '-']
            _varsNum = random.randint(4, 7)
        elif difficulty == "medium":
            ops = ['+', "*", "/", '-']
            _varsNum = 3
        elif difficulty == "easy":
            ops = ['+']
            _varsNum = 2
        else:
            # Add error & ret
            return

        def _inline_check(channel, rv):
            def inner_check(message):
                if message.channel.id == channel and message.content.isdigit() and message.author != self.bot.user:
                    return rv == int(message.content)
            return inner_check

        participants = {}
        participants = defaultdict(lambda: 0, participants)

        embedx00 = Embed(title="Mathsterrace - Fast paced math quiz", colour=Colour(0x6DC8E2))
        embedx00.set_footer(text="Prototype X1")
        embedx00.add_field(name="*Needed Wins*",  value=str(wins), inline=False)
        await ctx.send(embed=embedx00)

        _loop = True
        while _loop:
            eval_str = ""
            for i in range(0, _varsNum):
                opsNum = random.randint(0, len(ops)-1)
                eval_str += str(random.randint(1, 99999)) + ops[opsNum]
                print(eval_str)

            eval_str = eval_str[:-1]
            rv = eval(eval_str)

            embedx0 = Embed(title="Solve the following EQ !", colour=Colour(0x6DC8E2))
            embedx0.set_footer(text="Prototype X1")
            embedx0.add_field(name="*Equation*", value=eval_str, inline=False)
            await ctx.send(embed=embedx0)

            try:
                msg = await self.bot.wait_for('message', check=_inline_check(ctx.channel.id, rv), timeout=60)

                embedx1 = Embed(title="Point !", colour=Colour(0x6DC8E2))
                embedx1.set_footer(text="Prototype X1")
                embedx1.add_field(name="*Equation*", value=eval_str, inline=False)
                embedx1.add_field(name="*Answer*", value=msg.content, inline=False)
                embedx1.add_field(name="*Solver (Nerd)*", value="<@" + str(msg.author.id) + ">", inline=False)
                await ctx.send(embed=embedx1)

            except asyncio.TimeoutError:
                break

            participants[msg.author.id] += 1
            for key in participants.keys():
                if participants[key] == wins:
                    _loop = False
                    break

        _mathsterrace_ongoing = False
        embedx2 = Embed(title="Mathsterrace End Results", colour=Colour(0x6DC8E2))
        embedx2.set_footer(text="Prototype X1")
        embedx2.add_field(name="Needed wins", value=str(wins), inline=False)
        outstr = ""
        for key, val in participants.items():
            outstr += "<@" + str(key) + ">" + " : " + str(val)
        if outstr:
            embedx2.add_field(name="*Scoreboard*", value=outstr, inline=False)
        else:
            embedx2.add_field(name="*Scoreboard*", value="No Contest !", inline=False)
        await ctx.send(embed=embedx2)
        return
    # </editor-fold>

    # <editor-fold desc="[Spelling Game]">
    @commands.command(name="kyk")
    @commands.guild_only()
    async def know_your_keyboard(self, ctx, wins: int):
        if wins < 0:
            embedx = Embed(title="Know You Keyboard! - GameError", colour=Colour(0x6DC8E2))
            embedx.set_footer(text="Prototype X1")
            embedx.add_field(name="*Game Status*", value="No wins defined / Negative Number!", inline=False)
            await ctx.send(embed=embedx)
            return
        elif self._know_your_keyboard_ongoing:
            embedx = Embed(title="Know You Keyboard! - GameError", colour=Colour(0x6DC8E2))
            embedx.set_footer(text="Prototype X1")
            embedx.add_field(name="*Game Status*", value="A Game's already running!", inline=False)
            await ctx.send(embed=embedx)
            return

        _know_your_keyboard_ongoing = True

        async def getRandomNumber(exclusive_max: int, singular: bool) -> int:
            if singular:
                rv_singular = randbelow(exclusive_max)
                return rv_singular
            rv_s: str = ""
            rNums = []
            for i in range(0, 5):
                num: int = randbelow(exclusive_max)
                if num == 0:
                    num = 1
                rNums.append(num)
            for i in rNums:
                rv_s += str(i)
            return int(rv_s)

        def _inline_check(channel, word):
            def inner_check(message):
                if message.channel.id == channel and message.author != self.bot.user:
                    return message.content == word
            return inner_check

        participants = {}
        participants = defaultdict(lambda: 0, participants)

        _loop = True
        round_cnt = 0
        while _loop:

            wordIdx = await getRandomNumber(7, False)
            word = dicewareMap.get(wordIdx)

            embedx1 = Embed(title="Spell The Word!", colour=Colour(0x6DC8E2))
            embedx1.set_footer(text="Prototype X1 | Round: " + str(round_cnt))
            embedx1.add_field(name="*Word*", value=word, inline=False)
            await ctx.send(embed=embedx1)

            try:
                msg = await self.bot.wait_for('message', check=_inline_check(ctx.channel.id, word), timeout=60)

                await ctx.send("SPELLED! by: " + "<@" + str(msg.author.id) + ">")
            except asyncio.TimeoutError:
                break

            round_cnt += 1
            participants[msg.author.id] += 1
            for key in participants.keys():
                if participants[key] == wins:
                    _loop = False
                    break

        _know_your_keyboard_ongoing = False
        participants = {k: v for k, v in sorted(participants.items(), key=lambda item: item[1])}
        embedx3 = Embed(title="KnowYourKeyboard End Results", colour=Colour(0x6DC8E2))
        embedx3.set_footer(text="Prototype X1")
        embedx3.add_field(name="Needed wins", value=str(wins), inline=False)
        outstr = ""
        for key, val in participants.items():
            outstr += "<@" + str(key) + ">" + " : " + str(val) + "\n"
        if outstr:
            embedx3.add_field(name="*Scoreboard*", value=outstr, inline=False)
        else:
            embedx3.add_field(name="*Scoreboard*", value="No Contest !", inline=False)
        await ctx.send(embed=embedx3)
        return
    # </editor-fold>

    @know_your_keyboard.error
    @mathsterrace.error
    async def common_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            embedx = Embed(title="Command Invocation Error", colour=Colour(0x000001))
            embedx.add_field(name="dmesg", value="Argument number mismatch! Please check your command.")
            await ctx.send(embed=embedx, delete_after=5)
        elif isinstance(error, commands.MissingRole):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            return
        else:
            embedx = Embed(title="Command Error", colour=Colour(0x000001))
            embedx.add_field(name="dmesg", value="Unknown error, contact Bot Administrator!")
            await ctx.send(embed=embedx, delete_after=5)


def setup(bot):
    bot.add_cog(Gamer(bot))
