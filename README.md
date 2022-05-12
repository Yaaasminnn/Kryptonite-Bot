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
- - history (1.1?)
- ### Other/lotto
- - lotto commands (higher, lower, betting etc) (1.1)
- - daily
- - help

# Todo:

- ### finish crypto features
- - can add shares to the total.
- - - will be automatically done every month (1.1)
 
- ### Experiment with currencies and their stability when trading with charts.
- - test with all the max constants(need to resolve the json issue) (1.1)

- ### Add in the discord bot boilerplate.
- - Asyncronize the backend (1.1)
- - - just the class methods 
- - cache currencies and relaod constants every minute
- - front end(lots of embeds (prob not in 1.0)
- Crypto currency and "Other" functionality
- - - help command
- - make everything from floats to ints/100
- - show the value of our holdings, not just the shares (store that in json db)

- ### deploy to the rpi
- - backup script(for the database)
- - - log onscreen as well as to files?
- - - - or just other things to log? 
- - - have the pi use rsync and crontab?
- - - backup to my pc? local? cloud?

- ### Create webpages (not in 1.0)
- - show info on any currency
- - show info on a user?
    
- ### Currency history can be seen via a visual graph (not in 1.0)

- ### Gambling features (not in 1.0, but will be added ASAP)

- ### Release v1.0

# Issues:
- at arbitrarily large values, python seems to round the numbers to '1e+X'
- - the issue seems to be json losing precision for higher values, but that wont be fixed by the initial release
- - idea: convert it to scientific notation?
- Cooldown message not appearing
- since you pay a tax, you must wait for the currency to rise before selling. however, because the price increase when you buy, it might be increasing at a faster rate than the purchase tax
- - raise tax rates since otherwise, increases are fine
- - compare the tax rate vs how much a currency value will increase
