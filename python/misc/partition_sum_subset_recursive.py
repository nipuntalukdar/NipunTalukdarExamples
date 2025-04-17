from copy import copy 

def check_sum(array, target):
  if sum(array)  == target:
    return True, array
  if len(array) == 1:
    return False, None
  if sum(array) < target:
    return False, None
  for i in range(len(array)):
    new_array = copy(array)
    val = new_array.pop(i)
    new_target = target - val  # include val in return
    if new_target >= 0:
      ret, arr = check_sum(new_array, new_target)
      if ret:
        return True, [val] + arr
    new_target = target # exclude val
    ret, arr = check_sum(new_array, new_target)
    if ret:
      return True, arr  
  return False, None
  
def divide_equal_subset(arr, k):
  sum_all = sum(arr)
  if sum_all % k != 0:
    return False
  
  target_sum = sum_all // k
  for a in arr:
    if a > target_sum:
      return False
  print(1)
  while arr:
    for i in range(len(arr)):
      new_array = copy(arr)
      val = new_array.pop(i)
      ret, new_array = check_sum(new_array, target_sum - val)
      if ret:
        arr.remove(val)
        for a in new_array:
          arr.remove(a)
        break
      else:
        return False
  return True
  

print(divide_equal_subset([2,0,0,1,1,3, 2],3))


