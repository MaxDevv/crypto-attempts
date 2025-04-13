import polars as pl

df = pl.read_csv("historical-price-data/ETH_1min.csv")

moneroPrices = df.get_column("Open")[1_000_000:4_000_000][::20]
# with open("historical-price-data/ethereum-descending-chrongraphical", "r") as f:
#     moneroPrices = [float(i) for i in f.read().split("\n") if i != ""]

# len = 4_235_499

# prices
# s = [ ]
# for idx, i in enumerate(moneroPrices):
#     if (idx % 1) != 0:
#         continue
#     if ((idx + 2) < len(moneroPrices)):
#         s.append(((i, moneroPrices[idx + 1], moneroPrices[idx + 2])))


# print(s)
def simulate(ratio, log = False):
    toInvest, toWithdraw = ratio[0], ratio[1]
    investPercentage, withdrawPercentage = toInvest/100, toWithdraw/100
    balance = 100
    investment = 0
    peakTotal = balance + (investment * s[0][1])
    for idx, price in moneroPrices:
        # toInvest = investPercentage * balance
        # toWithdraw = withdrawPercentage * balance
        if idx == 0:
            continue
        pastPrice = moneroPrices[idx - 1]
        if (pastPrice > price):
            investment += ((toInvest/price) if balance >= toInvest else 0)
            balance -= (toInvest if balance >= toInvest else 0)
        else:
            balance += (toWithdraw if investment >= (toWithdraw/price) else 0)
            investment -= ((toWithdraw/price) if investment >= (toWithdraw/price) else 0)
            
        peakTotal = ((balance + (investment * price)) if (balance + (investment * price)) > peakTotal else peakTotal)
        if log:
            print(pastPrice, price, futurePrice, balance, investment,  balance + (investment * price))
        # investment *= (price / pastPrice)
    finalBal = balance + (investment * price)
    return finalBal


# varying ratio
def simulate(ratio, log = False):
    balance = 100
    investment = 0
    for idx, price in enumerate(moneroPrices):
        # toInvest = investPercentage * balance
        # toWithdraw = withdrawPercentage * balance
        if idx == 0:
            continue
        pastPrice = moneroPrices[idx - 1]
        
        # toInvest = balance * ratio[0] * (pastPrice/price) /100
        # toWithdraw = investment * ratio[1] * (price/pastPrice) /100
        toInvest = ratio[0]
        toWithdraw = ratio[1]
        if (pastPrice > price):
            investment += ((toInvest/price) if balance >= toInvest else 0)
            balance -= (toInvest if balance >= toInvest else 0)
        else:
            balance += (toWithdraw if investment >= (toWithdraw/price) else 0)
            investment -= ((toWithdraw/price) if investment >= (toWithdraw/price) else 0)
            
        # peakTotal = ((balance + (investment * price)) if (balance + (investment * price)) > peakTotal else peakTotal)
        if log:
            print(pastPrice, price, futurePrice, balance, investment,  balance + (investment * price))
        # investment *= (price / pastPrice)
    finalBal = balance + (investment * price)
    return finalBal

bestRatio = (5, 5)
bestVal = simulate(bestRatio)
print(bestVal)
for i in range(1, 101, 5):
    for x in range(1, 101, 5):
        val = simulate((i, x))
        if val > bestVal:
            bestRatio = (i, x)
            print(i, x, val)
            bestVal = val

print(bestRatio, bestVal)
# best for ETH 1m was 6:1 ratio
