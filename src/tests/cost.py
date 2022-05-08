"""
calculates the cost of a currency purchase.

issues:
    work with values lower than a
    work with values not divisible by a
"""
a = 50 # the number of shares we buy at a time. compound value?
tot_a = 100 # the total number of shares to be bought
s = 1116389 # the total number of shares
v = 25 # the initial share price. this can be changed
v_og = 25 # a copy of the initial share price. this will not be changed
cost = 0
tax = 0

#a = min(tot_a, a) # incase the number of shares is less than

for i in range(int(tot_a/a)):
    v += (v*a)/s # the new value after 50 shares. +/- for buying/selling respectively
    #v+= v*((v*a)/(v*s))

    #tax += 0.12*(a * v) # can be calculated afterward

    cost += a * v
    print(f"value: {v}, cost: {cost}, tax: {tax}")

print(f"\nwithout tax: {cost}")
print(f"with tax: {cost + tax}")
print(f"tax not compounded {cost * 1.12}")