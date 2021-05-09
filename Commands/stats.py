import logging,random

import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from Modules.bot import bot,Addresses

from Modules import funcs
from Modules import ethermine,wallet

@commands.cooldown(3,10,BucketType.user)
@bot.command(pass_context=True,name='stats',aliases=['s'])
async def Statistics(ctx):
    Message = await ctx.send('> Loading...')
    Address = ctx.message.content[4:46].replace('\n','/n')
    
    Session = logging.getLogger(str(random.randint(100,999)))
    Session.info(funcs.CmdInvokeMessage(ctx))

            # ------------------------------------ #
            #          Address Selectiong          #
            # ------------------------------------ #

    if (not Address) and ctx.author.id in Addresses:    # If there is no address and If the user is registered
        Wallet = Addresses[ctx.author.id]               # Then set the wallet to that user's wallet
        Session.info(f'Auto-Select "{Wallet}"')         # and log it

    elif not Address:                                   # if there is no address and the user isn't registered
        #                                               # and send them an error message
        await Message.edit(content=f"""> Cannot auto-select Address as you are not registered""")
        Session.info('Auto-Select Rejetected')          # log it
        return                                          # and return

    elif funcs.CheckAddress(Address):                   # If there is an address it's a valid
        Wallet = Address                                # Then set the wallet to that address
        Session.info(f'Specific Address - "{Wallet}"')  # and log it

    else:                                                           # If the address provided is invalid
        Session.info(f'Speicifc Address Rejected - "{Address}"')    # Then log it
        await Message.edit(content='> Invalid Address Provided')    # and send an error message
        return                                                      # and exit


    Stats = ethermine.GetStats(Wallet,Session)  # Get the stats from ethermine
    # wallet.GetWalletInfo(Wallet,Session.name)      # Unused info

    try:  # Calcualte a possible 0 divsion
        ShareSuccess = round(100 - ((Stats.BadShares/Stats.ValShares) * 100),2)
    except ZeroDivisionError:   # If devide by zero
        ShareSuccess = 0        # Set to 0
    
    Session.info('Sent Ethermine Statistics Message')   # Log it and then
    await Message.edit(content=                         # Send Info Message
f"""
{ctx.author.mention}: *{Wallet}*
```
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Hashrate:
  Average Hashrate | {funcs.DisHashrate(Stats.AvgHashrate)} MH/s
  Current Hashrate | {funcs.DisHashrate(Stats.RptHashrate)} MH/s
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Shares:
      Valid Shares | {Stats.ValShares}
        Bad Shares | {Stats.BadShares}
     Share Success | {ShareSuccess}%
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Earnings:
     Payout Amount | {funcs.DisEtherium(Stats.PayoutErn)} ETH
     Unpaid Amount | {funcs.DisEtherium(Stats.Unpaid)} ETH
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
     Total Earning | {funcs.DisEtherium(Stats.Unpaid+Stats.PayoutErn)} ETH
       USD Per Day | ${round(Stats.USDRate,2)}
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
```""")