import os
import discord
import asyncio
from webserver import keep_alive
from discord.ext import commands
from background_tasks import bg_tasks
from utils import check_command


async def determine_prefix(bot, message):
    if message.guild.id == 437048931827056642:
        return "."
    return "?"

bot = commands.Bot(
    command_prefix='?',
    case_insensitive=True
)


# regex to find most print statements \n\s*print\([^()]*\)
class initialized:
    def __init__(self):
        self.started = False

    def __call__(self):
        if not self.started:
            self.started = True
            return False
        else:
            return True


started = initialized()

extensions = [
    'Commands.dev_cmds',
    'Commands.data_tweaking',
    # 'Other.Starboard.main',
    'Commands.moderation',
    'Moderation.main',
    'Commands.fun',
    'Commands.help',
    # 'Mail.main',
    'Other.logger'
]

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    bot.add_check(check_command)
    await bot.change_presence(
        activity=discord.Activity(
            name='everything', type=discord.ActivityType(3)
        )
    )
    print(len(bot.commands))
    if not started():
        await bot.loop.create_task(bg_tasks(bot))

    print('ready')


@bot.event
async def on_command_error(ctx, error):
    if type(error) == commands.errors.CheckFailure:
        await ctx.author.send(f"You cant use `{ctx.prefix}{ctx.command}` here...")
    else:
        raise error

keep_alive(bot)
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)
