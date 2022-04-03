import os
from json_utils import *
import datetime

class User:
    def __init__(self, uid:int):
        """
        Initializes the User.

        Takes in the user id and loads the respective file in db/users/[uid].json.
        Then, we verify all tokens the user has still exist, if not, we delete the non-existent ones.
        finally, we update the last time this user was accessed.

        we do not save afterward and that is up to the user to save the data after use.
        this is because the user can do many things(trade, gamble, transfer) after accessing their account.
        Thus, the program must load the userdata, trade/gamble/transfer and then save seperately.
        """
        try: # if the json file dosent already exist, create it
            self.user = load_json(f"db/users/{uid}.json")
        except:
            create_json(f"db/users/{uid}.json")
            self.user = load_json(f"db/users/{uid}.json")
            self.user["uid"] = uid
            self.user["wallet"] = 0.0
            self.user["bank"] = 0.0
            #self.user["last_accessed"] = str(datetime.datetime.now().replace(second=0, microsecond=0))
            self.create_accounts() # creates both crypto accounts

            # saves the user
            self.save()


        self.verify_holdings()
        self.update_last_accessed()
        pretty_print(self.user)

    def create_accounts(self):
        """
        Creates the 2 crypto accounts.

        Creates a Tax free account and a regular account.
        """
        accounts = []
        accounts.append( # regular account
            {
                "tax_free": False,
                "holdings": [],
                "num_holdings": 0
            }
        )
        accounts.append( # tax-free account
            {
                "tax_free": True,
                "holdings": [],
                "num_holdings": 0
            }
        )
        self.user["accounts"] = accounts

    def save(self):
        """
        Saves the Userdata.
        """
        update_json(f"db/users/{self.user['uid']}.json", self.user)

    def verify_holdings(self):
        """
        Verifies that all the tokens in a user's holdings still exist.

        runs through all holdings in both accounts. for every token in the holdings,
        check if it exists in the database. if not, delete it from the holdings.
        """
        crypto_db = load_json("db/crypto_currencies.json")
        for i, account in enumerate(self.user["accounts"]): # we enumerate so we can delete the account index easily

            for j in range(len(account["holdings"])-1, -1, -1): # we iterate backwards because we are modifying an index as we iterate through it
                in_db=False
                for crypto in crypto_db["currencies"]: # if the specific holding exists, we break
                    if account["holdings"][j]["name"] == crypto["name"]:
                        in_db = True
                        break

                if not in_db:
                    self.user["accounts"][i]["holdings"].pop(j)

    def update_last_accessed(self):
        """
        Sets last_accessed to the current datetime.

        This is to keep track of the last time this user was accessed.
        :return:
        """
        self.user["last_accessed"] = str(datetime.datetime.now().replace(second=0, microsecond=0))

    def trade(self): pass

    def bank_deposit(self): pass

    def bank_withdraw(self): pass

    def crypto_trade(self, account:str, num_shares:int, token:str, buy:bool):
        """
        Trades Crypto.

        num_shares >0
        buy is a boolean
        """
        pass

    def wallet_modify(self): pass

    def bank_modify(self): pass

    def transfer(self): pass

    def check_limit(self): pass

if __name__ == '__main__':
    os.chdir("/home/loona/programming/Kryptonite-Bot/src")

    new = User(1)
