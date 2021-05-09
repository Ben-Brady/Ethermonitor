import re

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
    return f'The command {ctx.command.name} was invoked by ({ctx.author.id}) on {ctx.guild.name if ctx.guild else "Direct"} - "{Message}"'
