import os
from discord import Game
from datetime import datetime
from discord.ext import commands

# dotenv
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix='?')
bot.remove_command("help")

# Disabled Cogs: AntiSpam, Logger, Filter, OptionalFilters and Music
extensions = ['Cogs.Administrators',
              'Cogs.Moderators',
              'Cogs.APIFun',
              'Cogs.Fun',
              'Cogs.Maintenance']

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)
        print("[+]: Added " + extension)


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print('Logged in at: {0}'.format(datetime.now()))
    print('We have logged in as {0.user}'.format(bot))
    # bot.load_extension('Cogs.Music')  # we need a late init for this!
    await bot.change_presence(activity=Game(name="nothing, but nice to meet you! I'm Siri !"))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("[-]: Command not found ?")
        return

bot.run(os.environ.get('TOKEN'))
