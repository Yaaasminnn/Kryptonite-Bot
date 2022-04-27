import csv
from utils.crypto_currency import *
import utils.json_utils
"""
Tester for the Cryptocurrency class.
Dev: lvlon-Emperor
Date: 2022-04-25 2:30 am
objective:
    simulates a currency over the course of a month. assuming no trading.
    simulates a currency over the course of a month with trading.
    
    takes the results and outputs them to a .csv file
"""

fields = ["time(min)", "value", "Vmax_mag", "Tmax_mag", "threshold"] # the fields used in the csv file

def simulate_notrade(time_period=43200):
    """
    Over the course of a month, simulate the currency.

    for loop that iterates for 43200 intervals(number of minutes in a month).
    in said loop, load database, load the first currency, simulate it and save, then repeat
    """

    filename = "simulated_no_trade.csv"
    rows = []

    for i in range(time_period):
        db = utils.json_utils.load_json("db/crypto_currencies.json") # loads all currencies

        try:
            coin = CryptoCurrency(db["currencies"][0]) # creates the coin
            coin.simulate() # simulates the coin

            rows.append([ # appends the values to the rows
                i,
                coin.currency["value"],
                coin.currency["Vmax_mag"],
                coin.currency["Tmax_mag"],
                coin.currency["threshold"]
            ])

            print(f"Iteration: {i}    ||    Value: {coin.currency['value']}")
        except IndexError: print("Coin value crashed");break

    save_to_file(filename, rows)

def simulate_with_trade(): pass

def save_to_file(filename, rows):
    with open(f"tests/{filename}", "w") as file:
        writer = csv.writer(file) # creates the csv writer object

        # write the fields
        writer.writerow(fields)

        # write the data rows
        writer.writerows(rows)
    print(f"Saved {filename}!")

if __name__ == '__main__':
    db = utils.json_utils.load_json("db/crypto_currencies.json")

    for dict in db["currencies"]: # deletes all existing currencies
        coin = CryptoCurrency(dict)
        coin.delete()

    new = CryptoCurrency()


    simulate_notrade()