from collections import OrderedDict
import logging,random
from pprint import pprint

import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from Modules.bot import bot,Addresses
from Modules import funcs,ethermine

@commands.cooldown(3,60,BucketType.user)
@bot.command(pass_context=True,name='leaderboard',aliases=['l'])
async def Leaderboard(ctx):
    Message = await ctx.send('> Loading...')
    
    Session = logging.getLogger(str(random.randint(100,999)))
    Session.info(funcs.CmdInvokeMessage(ctx))
    
    if not ctx.guild:                                                   # If the message isn't from a guild
        await ctx.send('> Cannot display leaderboard, not in a guild')  # TODO: Allow guild selection
    await ctx.send('Members:')
    for x in ctx.guild.members:
        await ctx.send(x.name)
    MemberIds = [x.id for x in ctx.guild.members]                       # Create a list of GuildMember IDs
    
    Stats = []                  #
    for id in MemberIds:        #
        if id in Addresses:     #
            Stats.append(id,ethermine.GetStats(Addresses[id],Session))
            
    Stats.sort(key=lambda x: x[1].AvgHashrate)
    Stats = OrderedDict(Stats)
    
    await ctx.send(Stats)