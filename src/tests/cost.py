a = 50 # the number of shares we buy at a time. compound value?
tot_a = 10_000 # the total number of shares to be bought
s = 54_500 # the total number of shares
v = 25 # the initial share price. this can be changed
v_og = 25 # a copy of the initial share price. this will not be changed
cost = 0
tax = 0

for i in range(int(tot_a/a)):
    v += (v*a)/s**2 # the new value after 50 shares

    tax += 0.12*(a * v)

    cost += a * v
    print(f"value: {v}, cost: {cost}, tax: {tax}")

print(f"\nwithout tax: {cost}")
print(f"with tax: {cost + tax}")