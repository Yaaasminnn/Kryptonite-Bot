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
        #pretty_print(self.user)
        #self.save()

    def create_accounts(self):
        """
        Creates the 2 crypto accounts.

        Creates a Tax free account and a regular account.
        """
        accounts = []
        accounts.append( # regular account
            {
                "tax_free": False,
                "name": "ntfa",
                "balance": 0,
                "holdings": {},
                "num_holdings": 0,
                "tax_rate":1.12,
                "max_tradable_dollars": 50_000,
                "max_tradable_shares": 1000
            }
        )
        accounts.append( # tax-free account
            {
                "tax_free": True,
                "name": "tfa",
                "balance":0,
                "holdings": {},
                "num_holdings": 0,
                "tax_rate":1,
                "max_tradable_dollars": 10_000,
                "max_tradable_shares": 1000,
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
        not_in_db=[]
        for i, account in enumerate(self.user["accounts"]): # we enumerate so we can delete the account index easily

            for j in account["holdings"]: # we iterate backwards because we are modifying an index as we iterate through it
                in_db=False
                for crypto in crypto_db["currencies"]: # if the specific holding exists, we break
                    if j == crypto["name"]:
                        in_db = True
                        break

                if not in_db:
                    not_in_db.append(j)

            for k in not_in_db:
                del_dict_key(self.user["accounts"][i]["holdings"], key=k)

            not_in_db=[]

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

    def c_buy(self, account_name:str, num:int, token_val:int, token_name:str):
        # determines which account to use.
        if account_name == "tfa": account_index = 1
        else: account_index = 0

        value = self.user["accounts"][account_index]["tax_rate"] * (num*token_val) # determines the value

        # checks if the user's account balance is >= the value of the purchase
        if self.user["accounts"][account_index]["balance"] < value:
            return f"Insufficient balance.\nBalance: {self.user['accounts'][account_index]['balance']}\nNeeded: {value}"

        # subtracts value from the bank balance
        self.user["accounts"][account_index]["balance"] -= value

        # Adds the holdings to the account. if the holding does not exist, create it
        if token_name not in self.user["accounts"][account_index]["holdings"]:
            self.user["accounts"][account_index]["holdings"][token_name] = 0
        self.user["accounts"][account_index]["holdings"][token_name]+=num

    def c_sell(self, account_name:str, num:float, token_val:int, token_name:str):
        """
        Sell function. Modifies the user's account balance

        When selling, the account's balance is increased by the num_shares*token_val.
        additionally, the holding is decreased. if the holding value reaches 0, the holding is released.
        """
        # determines which account to use.
        if account_name == "tfa": account_index = 1
        else: account_index = 0

        # checks that the user has enough shares to sell. if not generate an error code.
        shares_owned = self.user["accounts"][account_index]["holdings"][token_name]
        if num > shares_owned:
            return f"number of shares to sell exceeds number of shares owned.\nto sell: {num}\nowned:{shares_owned}"

        # adds the money to the bank balance
        self.user["accounts"][account_index]["balance"] += num*token_val # we take the min to ensure they dont sell more than they have

        # subtracts the number of shares sold from the account's holdings
        self.user["accounts"][account_index]["holdings"][token_name] -= num

        # if the number of owned tokens reach 0, remove it
        if self.user["accounts"][account_index]["holdings"][token_name] == 0:
            del_dict_key(self.user["accounts"][account_index]["holdings"], key=token_name)

    def wallet_modify(self): pass

    def bank_modify(self): pass

    def transfer(self): pass

    def check_limit(self): pass

if __name__ == '__main__':
    os.chdir("/home/loona/programming/Kryptonite-Bot/src")

    new = User(1)

    """# testing sell
    kbx_value = 10
    kbx_name = "kbx"
    new.user["accounts"][1]["holdings"][kbx_name] =1
    new.user["accounts"][1]["balance"] = 10
    new.c_sell("tfa", num=1, token_val=kbx_value, token_name=kbx_name)
    new.save()"""

    # tesing buy
    kbx_value = 10
    kbx_name = "kbx"
    # tax free
    new.user["accounts"][1]["balance"] = 10
    print(new.c_buy("tfa", 1, kbx_value, kbx_name))
    # taxed
    new.user["accounts"][0]["balance"] = 10
    print(new.c_buy("ntfa", 1, kbx_value, kbx_name))


    # sell
    new.c_sell("tfa", 1, kbx_value, kbx_name)

    new.save()
