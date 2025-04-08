from copy import copy

coins = None
sorted_coins = None

def form_coins_map(coin_array):
  global coins, sorted_coins
  if not coin_array: return
  coins = set(coin_array)
  sorted_coins = list(coins)
  sorted_coins.sort()

def find_min_coins(amount, all_coins):
  form_coins_map(all_coins)
  if amount < sorted_coins[0]:
    return -1
  if amount in coins:
    return 1
  min_coins = []
  array_size = amount - sorted_coins[0] + 1
  i = 0
  while i < array_size:
    if (i + sorted_coins[0]) in coins:
      min_coins.append(1)
    else:
      min_coins.append(-1)
    i += 1

  i = 0
  while i < len(min_coins):
    if min_coins[i] != 1:
      j = i -1
      while j >= 0:
        if min_coins[j] != -1:
          amount_1 = j + sorted_coins[0]
          amount_2 = i + sorted_coins[0] - amount_1
          if amount_2 >= sorted_coins[0]:
            if min_coins[amount_2 - sorted_coins[0]] != -1:
              temp = min_coins[j] + min_coins[amount_2 - sorted_coins[0]]
              if min_coins[i] == -1:
                min_coins[i] = temp
              else:
                min_coins[i] = min(min_coins[i], temp)
        j -= 1
    i +=1 
  return min_coins[array_size - 1]


print(find_min_coins(11, [1,2,5]))

