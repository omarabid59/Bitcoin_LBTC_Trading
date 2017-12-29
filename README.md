# Bitcoin Trading 
This program is designed for those that are looking to make a profit from trading cryptocurrencies. 

The **idea** is simple. Buy at a low price and sell at a high price! To do this, all you have to do is buy from a crypto-exchange (such as QuadrigaCX) and then sell at a 10% or so profit margin on LocalBitcoins.

**Problem:** There are several issues that make this difficult.

 1. Bitcoin and cash deposit fees make it difficult to figure out the exact profit.
 2. You could be selling at a loss OR end up wasting your time with transactions that will not make you much money.
 3. There is a constant need to setup a buy/sell order on the corresponding crypto-exchange.
 4. There's a need to transfer the bitcoins back to localbitcoins so you can continue trading.

**Solution:** This application introduces a GUI that solves all these problems by

 5. Providing an estimate of the profit from each transaction.
 6. Automate buying at a suggested price from the crypto-exchange.
 7. Automate transferring bitcoins back to localbitcoins from crypto-exchange.

# USAGE

 1. Go to KEYS.txt and update your keys from Localbitcoin and QuadrigaCX.
 2. If you don't already have these please generate them.
 3. Remember, these keys are PRIVATE. Do not share them with anyone.
 4. Open up a terminal and enter this command
```
> python TradingGUI.py
```
You should see something like this returned back to you:
```
> Success. Retrieved Data
```
Then, a GUI like the one below should pop up
![enter image description here](https://github.com/omarabid59/Bitcoin_LBTC_Trading/blob/master/TradingGUI.png)

The GUI is divided into four sections

 1. In the top left hand quadrant, the total value of your BTC and CAD money in your QuadrigaCX and LocalBitcoins account is listed. You may also transfer bitcoins to and from the two accounts using the buttons provided.
 2. In the top right hand quadrant, the current **OPEN TRADES** with any clients are listed and a **NET PROFIT** is calculated. You are also notified how much money you have to transfer to recirculate your funds. You also so a **Quadriga Open Orders** that you have opened but are till pending.
 3. In the bottom right hand quadrant, the fields are automatically filled in for you that indicates how much bitcoins you have to purchase and at what price. All you have to do is press the buy/sell button and you are good to go.
 4. In the bottom left hand quadrant, the recent buy and sell orders on Quadriga are listed to give you a sense of the current market conditions.

# COLLABORATORS 
I'd like to thank my business partner and good friend Vassil for building this project and getting operations to move through smoothly.

# COMMENTS
Did you find this script useful? Do you have suggestions for improvement? Send me an email or checkout my [website](me.omarabid4.com) for more information.
