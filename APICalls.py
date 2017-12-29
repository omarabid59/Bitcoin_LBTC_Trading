import urllib2
import urllib
import json
import time
import hmac
import hashlib
import base64
import datetime
from lbcapi import api

def getVarFromFile(filename):
    import imp
    f = open(filename)
    global data
    data = imp.load_source('data', '', f)
    f.close()
    return data
def appendTrade(account_name, amount_cad, btc_price, profit, date):
    print ("TO DO: appendTrade")

# Grab the keys from a text file.
CONSTANTS = getVarFromFile('KEYS.txt')


######## LBTC KEY CONSTANTS. READ ONLY ACCESS   ########
hmac_key = CONSTANTS.hmac_key
hmac_secret = CONSTANTS.hmac_secret

######## QUADRIGA KEY CONSTANTS. WRITE ACCESS GRANTED. DO NOT PUT SECRET KEYS HERE!! #######
qkey = CONSTANTS.qkey
qsecret = CONSTANTS.qsecret
qclientID = CONSTANTS.clientID

###################### GUI SECURITY PIN. Prevents accidental orders ###############
SECURITY_PIN = '1234'

########## QUADRIGA FEE SCHEDULE CONSTANTS ##########
depositFee = 0.015 # 1.5%
tradeFee = 0.005  # 0.5%
quadrigaWithdrawalFee = 0.00
######LOCAL BITCOIN FEE SCHEDULE CONSTANTS ##########
btc_trading_fee = 0.01







#####################################################################################################################
############################################## Quadriga Function Calls ##############################################
#####################################################################################################################

############# GET QuadrigaCX PRICE ######################
# Required header. For some reason gives a 403 error without this.
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

## GET THE QUADRIGA SIGNATURE ##
def genSignature (key,noonce, secret,clientID):
    thing_to_hash = noonce + clientID + key
    signature = hmac.new(secret, msg=thing_to_hash, digestmod=hashlib.sha256).hexdigest()
    return signature

def getBalance(key,secret,clientID):
    noonce = str(int(time.time()))  # A unique integer
    signature = genSignature(key,noonce,secret,clientID)
    # PACKAGE INTO JSON FOR SENDING AS A POST
    values = {'key': key,
              'nonce': noonce,
              'signature': signature}
    data = urllib.urlencode(values)
    url = 'https://api.quadrigacx.com/v2/balance'
    req = urllib2.Request(url, data=data, headers=hdr)
    response = urllib2.urlopen(req)
    return json.loads(response.read())

def buyBTC(key,secret,clientID,amount_cad,buy_price):
    noonce = str(int(time.time()))  # A unique integer
    signature = genSignature(key,noonce,secret,clientID)
    # PACKAGE INTO JSON FOR SENDING AS A POST
    values = {'key': key,
              'nonce': noonce,
              'signature': signature,
              'amount' : amount_cad,
              'price' : buy_price,
              'book' : 'btc_cad'}
    data = urllib.urlencode(values)
    url = 'https://api.quadrigacx.com/v2/buy'
    req = urllib2.Request(url, data=data, headers=hdr)
    response = urllib2.urlopen(req)
    return response.read()
def sellBTC(key,secret,clientID,amount_cad,buy_price):
    noonce = str(int(time.time()))  # A unique integer
    signature = genSignature(key,noonce,secret,clientID)
    # PACKAGE INTO JSON FOR SENDING AS A POST
    values = {'key': key,
              'nonce': noonce,
              'signature': signature,
              'amount' : amount_cad,
              'price' : buy_price,
              'book' : 'btc_cad'}
    data = urllib.urlencode(values)
    url = 'https://api.quadrigacx.com/v2/sell'
    req = urllib2.Request(url, data=data, headers=hdr)
    response = urllib2.urlopen(req)
    return response.read()

def getBTCMarketData():
    quadrigaData = urllib2.Request("https://api.quadrigacx.com/v2/ticker?book=btc_cad", headers=hdr)
    quadrigaData = urllib2.urlopen(quadrigaData)
    quadrigaData = quadrigaData.read()
    return json.loads(quadrigaData)
def getBTGMarketData():
    quadrigaData = urllib2.Request("https://api.quadrigacx.com/v2/ticker?book=btg_cad", headers=hdr)
    quadrigaData = urllib2.urlopen(quadrigaData)
    quadrigaData = quadrigaData.read()
    return json.loads(quadrigaData)
def getETHMarketData():
    quadrigaData = urllib2.Request("https://api.quadrigacx.com/v2/ticker?book=eth_cad", headers=hdr)
    quadrigaData = urllib2.urlopen(quadrigaData)
    quadrigaData = quadrigaData.read()
    return json.loads(quadrigaData)
def getBCHMarketData():
    quadrigaData = urllib2.Request("https://api.quadrigacx.com/v2/ticker?book=bch_cad", headers=hdr)
    quadrigaData = urllib2.urlopen(quadrigaData)
    quadrigaData = quadrigaData.read()
    return json.loads(quadrigaData)

def sendBTC(key,secret,clientID, amount_btc, sendingAddress):
    noonce = str(int(time.time()))  # A unique integer
    signature = genSignature(key, noonce, secret, clientID)
    # PACKAGE INTO JSON FOR SENDING AS A POST
    values = {'key': key,
              'nonce': noonce,
              'signature': signature,
              'amount': amount_btc,
              'address': sendingAddress}
    data = urllib.urlencode(values)
    url = 'https://api.quadrigacx.com/v2/bitcoin_withdrawal'
    req = urllib2.Request(url, data=data, headers=hdr)
    # VASKO This function returns a file-like object with three additional methods".
    # One of which is getCode() - Return the HTTP Status code of the response.
    response = urllib2.urlopen(req)
    return response.read()

def getQuadrigaOpenOrders(key,secret,clientID):
    noonce = str(int(time.time()))  # A unique integer
    signature = genSignature(key,noonce,secret,clientID)
    # PACKAGE INTO JSON FOR SENDING AS A POST
    values = {'key': key,
              'nonce': noonce,
              'signature': signature,
              'book' : 'btc_cad'}
    data = urllib.urlencode(values)
    url = 'https://api.quadrigacx.com/v2/open_orders'
    req = urllib2.Request(url, data=data, headers=hdr)
    response = urllib2.urlopen(req)
    return json.loads(response.read())


def cancelTrade(key,secret,clientID,t_id):
    noonce = str(int(time.time()))  # A unique integer
    signature = genSignature(key, noonce, secret, clientID)
    # PACKAGE INTO JSON FOR SENDING AS A POST
    values = {'key': key,
              'nonce': noonce,
              'signature': signature,
              'id': t_id}
    data = urllib.urlencode(values)
    url = 'https://api.quadrigacx.com/v2/cancel_order'
    req = urllib2.Request(url, data=data, headers=hdr)
    response = urllib2.urlopen(req)
    return json.loads(response.read())


def getOrderBook(group=1):  #From API this is GET request but we using POST
    values = {'book' : 'btc_cad',
              'grou' : group}
    data = urllib.urlencode(values)
    #Note this is a GET request
    url = 'https://api.quadrigacx.com/v2/order_book'
    # public function (no authentication required)
    req = urllib2.Request(url, data=data, headers=hdr)
    response = urllib2.urlopen(req)
    json_order_book = json.loads(response.read())

    n_orders = 10
    bids = json_order_book['bids'][0:n_orders]
    asks = json_order_book["asks"][0:n_orders]
    timestamp =float(json_order_book['timestamp'])
    dt = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')  #local time

    portionOfBookOrders = {"dt": dt, "bids" : bids, "asks" : asks}

    return portionOfBookOrders

def getUserTransactions(key, secret, clientID,limit):
    noonce = str(int(time.time()))  # A unique integer
    signature = genSignature(key, noonce, secret, clientID)
    # PACKAGE INTO JSON FOR SENDING AS A POST
    values = {'key': key,
            'nonce': noonce,
            'signature': signature,
            'limit': limit}
    data = urllib.urlencode(values)
    url = 'https://api.quadrigacx.com/v2/user_transactions'
    req = urllib2.Request(url, data=data, headers=hdr)
    response = urllib2.urlopen(req)
    return json.loads(response.read())

def lookupOrder(key, secret, clientID,id):
    noonce = str(int(time.time()))  # A unique integer
    signature = genSignature(key, noonce, secret, clientID)
    # PACKAGE INTO JSON FOR SENDING AS A POST
    values = {'key': key,
            'nonce': noonce,
            'signature': signature,
            'id': id}
    data = urllib.urlencode(values)
    url = 'https://api.quadrigacx.com/v2/lookup_order'
    req = urllib2.Request(url, data=data, headers=hdr)
    response = urllib2.urlopen(req)
    return json.loads(response.read())

def getQuadrigaDepositAddress(key, secret, clientID):
    noonce = str(int(time.time()))  # A unique integer
    signature = genSignature(key, noonce, secret, clientID)
    # PACKAGE INTO JSON FOR SENDING AS A POST
    values = {'key': key,
            'nonce': noonce,
            'signature': signature,
            }
    data = urllib.urlencode(values)
    url = 'https://api.quadrigacx.com/v2/bitcoin_deposit_address'
    req = urllib2.Request(url, data=data, headers=hdr)
    response = urllib2.urlopen(req)
    return json.loads(response.read())

def getQuadrigaNetBTC(key, secret, clientID,date):
    print "TODO"


def cancelAllOpenTrades():
    print('TO DO: cancelAllOpenTrades')


#####################################################################################################################
################################################ LBTC Function Calls ################################################
#####################################################################################################################
# GET THE LBTC DATA (username, etc.)
def getLBTCData():
    conn = api.hmac(hmac_key, hmac_secret)
    return conn.call('GET', '/api/dashboard/').json()
def get_lbtc_balance():
    conn = api.hmac(hmac_key, hmac_secret)
    data =  conn.call('GET', '/api/wallet-balance/').json()
    return data['data']['total']['balance']
def getLBTCUserName():
    conn = api.hmac(hmac_key, hmac_secret)
    data = conn.call('GET', '/api/myself/').json()
    myUserName = data['data']['username']
    print('Username: ' + myUserName)
    return myUserName
def getRecievingLBTCAddress():
    conn = api.hmac(hmac_key, hmac_secret)
    data = conn.call('GET', '/api/wallet-addr/').json()
    return data['data']['address']

def getOpenOrders(lBTCdata,myUserName,quadrigaBTCPerDollar): 
    net_revenue = 0.0
    json_object = {}
    json_object['data'] = {}
    order_index = 0
    total_amount_to_purchase = 0 # Indicates how much we should purchase from Quadriga
    for thisTrade in lBTCdata['data']['contact_list']:
        client_username = thisTrade['data']['buyer']['username']
        # Make sure we only list sell orders.
        if (client_username == myUserName):
            continue
        total_btc_sold = float(thisTrade['data']['amount_btc']) + float(thisTrade['data']['fee_btc'])
        amount_cad = float(thisTrade['data']['amount'])
        # The 'amount_cad' above gives the total revenue. That's key as that's the amount of $ we have available to buy.
        exchange_rate_lbtc = amount_cad / total_btc_sold
        usableDollarAmount = min(amount_cad * (1 - depositFee), amount_cad - 5)
        # using "last" trade as BTC market value
        bitcoinsBought = (usableDollarAmount / quadrigaBTCPerDollar) * (1 - tradeFee - quadrigaWithdrawalFee)

        bitcoinProfit = bitcoinsBought - total_btc_sold
        dollarProfit = bitcoinProfit * quadrigaBTCPerDollar
        # Package each Order as a JSON so we can display it to our GUI.
        temp_json_data = {
            "client": client_username,
            "deposit_amount_cad": amount_cad,
            "etransfer_fee":max(depositFee * amount_cad, 5),
            "bitcoins_bought":bitcoinsBought,
            "bitcoins_sold":total_btc_sold,
            "btc_profit":bitcoinProfit,
            "cad_profit":dollarProfit,
            "usable_dollar_amount":usableDollarAmount,
            "exchange_rate_lbtc":exchange_rate_lbtc
        }
        json_object['data'][order_index] = temp_json_data
        order_index +=1

        net_revenue += bitcoinProfit
        total_amount_to_purchase += usableDollarAmount

    json_object['net_revenue_btc'] = net_revenue
    json_object['net_revenue_cad'] = round(net_revenue * quadrigaBTCPerDollar, 2)
    json_object['total_purchase_amount'] = round(total_amount_to_purchase, 2)
    return json_object



