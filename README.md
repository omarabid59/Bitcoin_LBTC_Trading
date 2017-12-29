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



# COMMENTS
Did you find this script useful? Do you have suggestions for improvement? Send me an email or checkout my website `me.omarabid4.com` for more information.
