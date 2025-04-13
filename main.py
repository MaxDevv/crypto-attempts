

with open("/root/Code/crypto-attempts/monero-descending-chrongraphical") as f:
    moneroPrices = f.readlines()
    moneroPrices = [float(i) for i in moneroPrices]
    # prices
s = [ ]
for idx, i in enumerate(moneroPrices):
    if (idx % 1) != 0:
        continue
    if ((idx + 2) < len(moneroPrices)):
        s.append(((i, moneroPrices[idx + 1], moneroPrices[idx + 2])))


# print(s)
def simulate(ratio, log = False):
    toInvest, toWithdraw = ratio[0], ratio[1]
    investPercentage, withdrawPercentage = toInvest/100, toWithdraw/100
    balance = 100
    investment = 0
    peakTotal = balance + (investment * s[0][1])
    for pastPrice, price, futurePrice in s:
        # toInvest = investPercentage * balance
        # toWithdraw = withdrawPercentage * balance
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

bestRatio = (50, 50)
bestVal = simulate(bestRatio)
for i in range(1, 101, 5):
    for x in range(1, 101, 5):
        if simulate((i, x)) > bestVal:
            bestRatio = (i, x)
            print(i, x)
            bestVal = simulate(bestRatio)

print(bestRatio, bestVal)
# print(simulate((1, 2), True))