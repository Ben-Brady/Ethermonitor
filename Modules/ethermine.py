import time
import json
import random
import logging
import requests
from typing import NamedTuple
from threading import Thread

EndPoint = 'https://api.ethermine.org'
Cache = {}

# ------------------------------------ #
#            Other Functions           #
# ------------------------------------ #
class _Miner(NamedTuple):       # A miner stats struct (Namedtuple = struct)
    AvgHashrate : int = 0       # The Average Effective Hashrate
    RptHashrate : int = 0       # The Miner's reported hashrate
    ValShares   : int = 0       # The recent valid shares
    BadShares   : int = 0       # The recent invalid shares
    USDRate     : float = 0.0   # The USD per Day rate
    Unpaid      : int = 0       # The unpaid amount
    PayoutErn   : int = 0       # The amount payed out

def _CacheWallet(Address,Stats,Session):
    Session.info(f'Added address to cache "{Address}"')
    
    Cache[Address] = Stats
    
    time.sleep((30*60))
    
    Cache.pop(Address)
    
    Session.info(f'Removed address from cache "{Address}"')

def GetStats(Address,Session):
    def Get(Index):
        var = JSON.get(Index,0) # Get the index from the JSON,
        if var == None:         # If the Var is none
            var = 0             # Replace it with a 0
        return var              # Then return it
    
    if Address in Cache:         # If the wallet is already cached
        Session.info(f'Address already in cache "{Address}"')
        return Cache[Address]    # Then use the cache insteaed.

    Session.info("Getting payouts from api.ethermine.org")
    with requests.get(EndPoint + f'/miner/{Address}/payouts') as r:
        Payouts = json.loads(r.text)['data']

    PayoutTotal = 0
    for x in Payouts:
        PayoutTotal += int(x['amount'])

    Session.info("Getting stats from api.ethermine.org")
    with requests.get(EndPoint + f'/miner/{Address}/currentStats') as r:
        JSON =  json.loads(r.text)['data']
    
    if type(JSON) != dict:  # If the JSON isn't a dict
        Session.info("Invalid Stats, using zeros")
        Stats = _Miner()     # then return a default miner
    else:
        def Get(Index):
            var = JSON.get(Index,0) # Get the index from the JSON,
            if var == None:         # If the Var is none
                var = 0             # Replace it with a 0
            return var              # Then return it

        Session.info("Calculating Stats")
        Stats = _Miner(
        AvgHashrate = int(Get('averageHashrate')),
        RptHashrate = int(Get('reportedHashrate')),
        ValShares   = int(Get('validShares')),
        BadShares   = int(Get('invalidShares')+Get('staleShares')),
        USDRate     = float(Get('usdPerMin')*1440),
        Unpaid      = int(Get('unpaid')),
        PayoutErn   = PayoutTotal
        )
    
    Thread(target=_CacheWallet,args=[Address,Stats,Session]).start()
    return Stats