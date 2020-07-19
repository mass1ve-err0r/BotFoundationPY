from textwrap import wrap
from os import remove
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw, PILLOW_VERSION
from datetime import datetime
from discord import Embed, Colour, TextChannel, File
from discord.ext import commands


class Memer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mhotline")
    @commands.guild_only()
    async def meme_drake(self, ctx, first: str, second: str, style: str = "r"):
        timestamp = datetime.now().strftime("%H_%M_%S")
        outname = timestamp + ".jpg"
        img = Image.open(Path(__file__).parent / "../MemeBase/DrakeHotline.jpg")
        xcord1 = 648
        ycord1 = 112
        xcord2 = 648
        ycord2 = 783
        drawable = ImageDraw.Draw(img)
        font = None
        if style == "i":
            font = ImageFont.truetype("os_italic.ttf", 60)
        elif style == "b":
            font = ImageFont.truetype("os_bold.ttf", 60)
        else:
            font = ImageFont.truetype("os.ttf", 60)
        wrapped1 = "\n".join(wrap(first, width=15))
        wrapped2 = "\n".join(wrap(second, width=15))
        drawable.multiline_text((xcord1, ycord1), wrapped1, (0, 0, 0), font=font)
        drawable.multiline_text((xcord2, ycord2), wrapped2, (0, 0, 0), font=font)
        img.save(outname)
        await ctx.message.delete()
        await ctx.send(file=File(outname))
        try:
            remove(outname)
        except OSError:
            pass

    @commands.command(name="mspongebob")
    @commands.guild_only()
    async def meme_spongebob(self, ctx, toptext: str, style: str = "r"):
        timestamp = datetime.now().strftime("%H_%M_%S")
        outname = timestamp + ".jpg"

        spongetext = ""
        for idx, ch in enumerate(toptext):
            if idx % 2 == 0 and ch != ' ':
                spongetext += str(ch).upper()
            else:
                spongetext += str(ch)

        img = Image.open(Path(__file__).parent / "../MemeBase/Spongebob_UPLOW.jpg")
        xcord = 17
        ycord = 17
        drawable = ImageDraw.Draw(img)
        font = None
        if style == "i":
            font = ImageFont.truetype("os_italic.ttf", 50)
        elif style == "b":
            font = ImageFont.truetype("os_bold.ttf", 50)
        else:
            font = ImageFont.truetype("os.ttf", 50)
        wrapped1 = "\n".join(wrap(spongetext, width=20))
        drawable.multiline_text((xcord+1, ycord+2), wrapped1, (128, 128, 128), font=font)
        drawable.multiline_text((xcord, ycord), wrapped1, (0, 0, 0), font=font)
        img.save(outname)
        await ctx.message.delete()
        await ctx.send(file=File(outname))
        try:
            remove(outname)
        except OSError:
            pass

    @commands.command(name="mexit")
    @commands.guild_only()
    async def meme_car(self, ctx, goal: str, instead: str, victim: str = "me"):
        timestamp = datetime.now().strftime("%H_%M_%S")
        outname = timestamp + ".jpg"

        xcord_v = 392
        xcord_g = 194
        xcord_i = 413
        ycord_v = 584
        ycord_g = 117
        ycord_i = 112
        img = Image.open(Path(__file__).parent / "../MemeBase/CarExitMeme.jpg")
        drawable = ImageDraw.Draw(img)
        font_v = ImageFont.truetype("os.ttf", 45)
        font_g = ImageFont.truetype("os.ttf", 30)
        font_i = ImageFont.truetype("os.ttf", 30)
        wrapped_v = "\n".join(wrap(victim, width=15))
        wrapped_g = "\n".join(wrap(goal, width=10))
        wrapped_i = "\n".join(wrap(instead, width=10))
        drawable.multiline_text((xcord_v, ycord_v), wrapped_v, (255, 255, 255), font=font_v)
        drawable.multiline_text((xcord_g, ycord_g), wrapped_g, (255, 255, 255), font=font_g)
        drawable.multiline_text((xcord_i, ycord_i), wrapped_i, (255, 255, 255), font=font_i)
        img.save(outname)

        await ctx.message.delete()
        await ctx.send(file=File(outname))
        try:
            remove(outname)
        except OSError:
            pass

    @commands.command(name="mbrain")
    @commands.guild_only()
    async def meme_brain(self, ctx, first: str = None, second: str = None, third: str = None, fourth: str = None):
        if first is None or second is None or third is None or fourth is None:
            return

        timestamp = datetime.now().strftime("%H_%M_%S")
        outname = timestamp + ".jpg"

        xcord = 11
        ycord1 = 18
        ycord2 = 340
        ycord3 = 635
        ycord4 = 930
        img = Image.open(Path(__file__).parent / "../MemeBase/GalaxyBrain.jpg")
        drawable = ImageDraw.Draw(img)
        font = ImageFont.truetype("os.ttf", 45)
        wrapped1 = "\n".join(wrap(first, width=15))
        wrapped2 = "\n".join(wrap(second, width=15))
        wrapped3 = "\n".join(wrap(third, width=15))
        wrapped4 = "\n".join(wrap(fourth, width=15))
        drawable.multiline_text((xcord, ycord1), wrapped1, (0, 0, 0), font=font)
        drawable.multiline_text((xcord, ycord2), wrapped2, (0, 0, 0), font=font)
        drawable.multiline_text((xcord, ycord3), wrapped3, (0, 0, 0), font=font)
        drawable.multiline_text((xcord, ycord4), wrapped4, (0, 0, 0), font=font)
        img.save(outname)

        await ctx.message.delete()
        await ctx.send(file=File(outname))
        try:
            remove(outname)
        except OSError:
            pass

    @commands.command(name="mobama")
    @commands.guild_only()
    async def meme_obama(self, ctx, title: str = None, front: str = None, back: str = None):
        if title is None or front is None or back is None:
            return

        timestamp = datetime.now().strftime("%H_%M_%S")
        outname = timestamp + ".jpg"

        xcord1 = 20
        ycord1 = 20
        xcord2 = 102
        ycord2 = 531
        xcord3 = 680
        ycord3 = 335
        img = Image.open(Path(__file__).parent / "../MemeBase/ObamaMedal.jpg")
        drawable = ImageDraw.Draw(img)
        font = ImageFont.truetype("os.ttf", 45)
        wrapped1 = "\n".join(wrap(title, width=40))
        wrapped2 = "\n".join(wrap(front, width=15))
        wrapped3 = "\n".join(wrap(back, width=15))
        drawable.multiline_text((xcord1, ycord1), wrapped1, (0, 0, 0), font=font)
        drawable.multiline_text((xcord1+2, ycord1+2), wrapped1, (255, 255, 255), font=font)
        drawable.multiline_text((xcord2, ycord2), wrapped2, (255, 255, 255), font=font)
        drawable.multiline_text((xcord3, ycord3), wrapped3, (255, 255, 255), font=font)
        img.save(outname)

        await ctx.message.delete()
        await ctx.send(file=File(outname))
        try:
            remove(outname)
        except OSError:
            pass


def setup(bot):
    bot.add_cog(Memer(bot))
