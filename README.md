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
- - - will be automatically done every month
 
- ### Experiment with currencies and their stability when trading with charts.
- - test with the current trade functions 
- - test with all the max constants(need to resolve the json issue)

- ### Add in the discord bot boilerplate.
- - Asyncronize the backend
- - cache currencies and relaod constants every minute
- - front end(lots of embeds)
- - - prob not in 1.0 
- - Crypto currency and "Other" functionality
- - - dynamically adds currencies 
- - protection against bots
- - make everything from floats to ints/100

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
- the issue seems to be json losing precision for higher values, but that wont be fixed by the initial release
- idea: convert it to scientific notation?
