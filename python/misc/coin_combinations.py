'''
For amount x,  and for coin c (x>=c), if (x - c) can be made in n ways,
then there is n ways to make sum x by adding the coin c

'''

def funct_coin_combination(amount, coins):
  if not coins:
    return 0
  if amount == 0:
    return 1
  coins.sort()
  if amount < coins[0]:
    return 0

  min_coins = [0] * (amount + 1)
  min_coins[0] = 1

  for coin in coins:
    for i in range(coin, amount + 1):
      min_coins[i] += min_coins[i - coin]

  return min_coins[amount]

print(funct_coin_combination(5, [1,2,5]))
print(funct_coin_combination(100, [1,50]))
