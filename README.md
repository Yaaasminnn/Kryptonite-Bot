# Kryptonite Bot

 A dynamic discord economy bot written in python.

# Features:

- Users can buy, sell, monitor and trade currency/cryptocurrency.

- Can transfer money among eachother as well.

- Cryptocurrencies are dynamically generated, and deleted

- Users can view the history of the currencies on a graph. 
- - (predictions made by the pc?)

# Commands
- ### User-based
- - bal
- - init
- - holdings
- - transfer
- - bank deposit/withdraw
- ### Crypto-based
- - buy/sell
- - view (name)
- - list currencies
- - history (1.2?)
- ### Other/lotto
- - lotto commands (lower, coinflip)
- - daily
- - help


# Deployment:
- requires pycord. 
``
git clone https://github.com/MonEmperor/Kryptonite-Bot # clone the repo
cd Kryptonite-Bot
``
- create a file named ``imp_info.json`` in ``src/kryptonite_bot``. there is a template in said directory. place your discord bot info there.
- - everything in the file is self-explanatory. the "owner id" key is for your discord user ID.
- lastly, create a file named ``crypto_currencies.json`` in the ``src/db`` directory. and make it look like this:
``
{
	"currencies": [],
	"count": 0
}
``
- now just run src/main.py using python3


# Todo:

- ### Add in the discord bot boilerplate.
- - Asyncronize the backend (1.2)
- - - just the class methods
- - show the value of our holdings, not just the shares (store that in json db)

- ### deploy to the rpi
- - backup script(for the database)
- - - log onscreen as well as to files?
- - - - or just other things to log? 
- - - have the pi use rsync and crontab?
- - - backup to my pc? local? cloud?
    
- ### Currency history can be seen via a visual graph (not in 1.1)

# Issues:
- at arbitrarily large values, python seems to round the numbers to '1e+X'
- - the issue seems to be json losing precision for higher values, but that wont be fixed by the initial release
- - idea: convert it to scientific notation?
- Cooldown message not appearing
- since you pay a tax, you must wait for the currency to rise before selling. however, because the price increase when you buy, it might be increasing at a faster rate than the purchase tax
- - raise tax rates since otherwise, increases are fine
- - compare the tax rate vs how much a currency value will increase
