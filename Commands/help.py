import logging,random

import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from Modules.bot import bot
from Modules import funcs

@bot.remove_command('help')
@commands.cooldown(10,60,BucketType.user)
@bot.command(pass_context=True,name='help',aliases=['h'])
async def Help(ctx):
    Session = logging.getLogger(str(random.randint(100,999)))
    Session.info(funcs.CmdInvokeMessage(ctx))

    await ctx.author.create_dm()
    await ctx.author.dm_channel.send("""```
--h:
    I think you figured this one out

--r *Address*:
    Registers that you own an etherium address

--s [*Address*]:
    Displays your ethermine mining stats
    Optional address parameter to display a specific address's stats
```""")