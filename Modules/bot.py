import logging

import discord
from discord.ext import commands

logging.basicConfig(
    filename=f"./Logs/main.log",
    filemode='a',
    format='%(asctime)s  [%(name)s] %(filename)s.%(funcName)s | %(levelname)s - %(message)s',
    level=logging.INFO) 
logging.info('New Session Started')


bot = commands.Bot(command_prefix = '!-')
Addresses  = {}

@bot.event
async def on_ready():
    print('Bot ready')
    await bot.change_presence(activity=discord.Game(name="Help: --h"))

@bot.event
async def on_command_error(ctx:commands.Context, error):
    breakpoint()
    Session = logging.getLogger("CommandError")
    if isinstance(error, commands.CommandOnCooldown):
        Session.info(f'{ctx.command.name} on Cooldown for {round(error.retry_after,4)} by {ctx.author.id}')
        await ctx.send(f'> {ctx.author.mention} You Are On Cooldown ({round(error.retry_after,2)}s): https://bit.ly/3twEGE0')
    elif isinstance(error,commands.CommandNotFound):
        Session.info(f'Invalid Command {ctx.message.content} by {ctx.author.id}')
    else:
        Session.warning(f'({ctx.author.id}) - "{ctx.message.content}"{str(error)}')

