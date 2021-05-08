import os
from dotenv import load_dotenv
load_dotenv()

import json
import requests

EndPoint = "https://api.ethplorer.io"

ETHAuth = {'apiKey':os.getenv('ETHTOKEN')}

def GetWalletInfo(Address,SessionName):
    Parameters = {'apiKey':"EK-x7tbL-jnoZo1C-fEo7h"}
    with requests.get(EndPoint+"/getAddressInfo/0x"+Address
                    ,headers=ETHAuth) as r:
        return json.loads(r.text)

def GetTransactions(Address):
    with requests.get(EndPoint+"/getAddressTransactions/0x"+Address
                    ,headers=ETHAuth) as r:
        Transactions = json.loads(r.text)

    Out,In = [],[]
    for x in Transactions:
        if x['from'] == ('0x'+Address):
            Out.append(x)
        elif x['to'] == ('0x'+Address):
            In.append(x)

    return Out,In

def GetTransactionValue(Transaction):
    if not Transaction['success']:
        return 0
    else:
        Time   = Transaction['timestamp']
        Amount = Transaction['value']

        Header = {'X-CMC_PRO_API_KEY':os.getenv('ETHTOKEN')}
        return 20