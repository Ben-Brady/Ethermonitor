import os
import re
import random
import logging
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from dotenv import load_dotenv
load_dotenv()

from Modules import ethermine,wallet

logging.basicConfig(
    filename=f"Log.log",
    filemode='a',
    format='%(asctime)s  [%(name)s] %(filename)s.%(funcName)s | %(levelname)s - %(message)s',
    level=logging.INFO)
logging.info('New Session Started')

bot = commands.Bot(command_prefix='--')
Ownership  = {}
ImageCache = {}

def DisHashrate(Rate):
    Hashrate = Rate / 1_000_000
    return round(Hashrate,2)

def DisEtherium(ETH):
    return round(ETH / (10**18),6)

def CheckAddress(Address):
    if Address[:2] == '0x':                             # If the address has the 0x prefix
        Address = Address[2:]                           # Then remove it
    return bool(re.match('^[a-fA-F0-9]{40}$',Address))  # Returns a bool re match


def CmdInvokeMessage(ctx):
    Message = (ctx.message.content).replace('\n','/n')
    return f'{bot.command_prefix}{ctx.command.name} command invoked by ({ctx.author.id}) - "{Message}"'

@bot.event
async def on_ready():
    print('Bot ready')
    await bot.change_presence(activity=discord.Game(name="Help: --h"))


bot.remove_command('help')
@commands.cooldown(10,60,BucketType.user)
@bot.command(name='help',aliases=['h'])
async def Help(ctx):
    Session = logging.getLogger(str(random.randint(100,999)))
    Session.info(CmdInvokeMessage(ctx))
    await ctx.author.create_dm()
    await ctx.author.dm_channel.send("""
```
--h:
    I think you figured this one out

--r *Address*:
    Registers that you own an etherium address

--s [*Address*]:
    Displays your ethermine mining stats
    Optional address parameter to display a specific address's stats
```""")

@bot.event
async def on_command_error(ctx:commands.Context, error):
    Session = logging.getLogger(str(random.randint(100,999)))
    if isinstance(error, commands.CommandOnCooldown):
        Session.info(f'{ctx.command.name} on Cooldown for {round(error.retry_after,4)} by {ctx.author.id}')
        await ctx.send(f'> You Are On Cooldown ({round(error.retry_after,2)}): https://cdn.discordapp.com/attachments/161297309978591233/840043926790340618/bucket.webm#')

@commands.cooldown(10,60,BucketType.user)
@bot.command(name='register',aliases=['r'])
async def Register(ctx):
    Address = ctx.message.content[4:46]
    
    Session = logging.getLogger(str(random.randint(100,999)))
    Session.info(CmdInvokeMessage(ctx))
    
    if Address:
        if CheckAddress(Address):
            Session.info(f'Valid Address Registered')
            await ctx.send(f"> Your registered that you own the Address: *{Address}*")
            Ownership[ctx.author.id] = Address
        else:
            Session.info(f'Address Rejected')
            await ctx.send("> The Address you provided was invalid")
    else:
        Session.info(f'No Address Provided')
        await ctx.send("> You need to enter an Address")


@commands.cooldown(3,10,BucketType.user)
@bot.command(name='stats',aliases=['s'])
async def Statistics(ctx):
    Message = await ctx.send('> Loading...')
    Address = ctx.message.content[4:46].replace('\n','/n')
    
    SessionName = str(random.randint(100,999))
    Session = logging.getLogger(SessionName)
    Session.info(CmdInvokeMessage(ctx))

            # ------------------------------------ #
            #          Address Selectiong          #
            # ------------------------------------ #

    if not Address:                                 # If there is no address
        if ctx.author.id in Ownership:              # If the user is registered
            Wallet = Ownership[ctx.author.id]       # Then set the wallet to that user's wallet
            Session.info(f'Auto-Select "{Wallet}"') # and log it
        else:                                       # If the user isn't registered
            #                                       # Then send an error message
            await Message.edit(content=f"""
> Cannot auto-select Address as you are not registered
> To register, use the command:
>     -r ***Address***
""")
            Session.info('Auto-Select Rejetected')  # log it
            return                                  # and return
            #                                           # If there is an address set
    elif CheckAddress(Address):                         # and it's a valid address
        Wallet = Address                                # Then set the wallet to that address
        Session.info(f'Specific Address - "{Wallet}"')  # and log it
    else:                                               # If the address is invalid
        Session.info(f'Speicifc Address Rejected - "{Address}"')    # Then log it
        await Message.edit(content='> Invalid Address Provided')    # and send an error message
        return                                                      # and exit


    Stats = ethermine.GetStats(Wallet,SessionName)  # Get the stats from ethermine
    # wallet.GetWalletInfo(Wallet,SessionName)      # Unused info

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
  Average Hashrate | {DisHashrate(Stats.AvgHashrate)} MH/s
  Current Hashrate | {DisHashrate(Stats.RptHashrate)} MH/s
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Shares:
      Valid Shares | {Stats.ValShares}
        Bad Shares | {Stats.BadShares}
     Share Success | {ShareSuccess}%
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Earnings:
     Payout Amount | {DisEtherium(Stats.PayoutErn)} ETH
     Unpaid Amount | {DisEtherium(Stats.Unpaid)} ETH
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
     Total Earning | {DisEtherium(Stats.Unpaid+Stats.PayoutErn)} ETH
       USD Per Day | ${round(Stats.USDRate,2)}
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
```""")

if __name__ == "__main__":
    bot.run(os.getenv("BOTTOKEN"))