import logging,random

import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from Modules.bot import bot,Addresses
from Modules import funcs

@commands.cooldown(10,60,BucketType.user)
@bot.command(pass_context=True,name='register',aliases=['r'],)
async def Register(ctx):
    Address = ctx.message.content[4:46]

    Session = logging.getLogger(str(random.randint(100,999)))
    Session.info(funcs.CmdInvokeMessage(ctx))

    if funcs.CheckAddress(Address):
        Session.info(f'Valid Address Registered')
        await ctx.send(f"> Your registered that you own the Address: *{Address}*")
        Addresses[ctx.author.id] = Address

    elif Address:
        Session.info(f'Address Rejected')
        await ctx.send("> The Address you provided was invalid")

    else:
        Session.info(f'No Address Provided')
        await ctx.send("> You need to enter an Address")