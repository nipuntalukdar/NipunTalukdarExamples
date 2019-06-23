'''

There are N gas stations along a circular route, 
where the amount of gas at station i is gas[i].
You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from 
station i to its next station (i+1). You begin the journey with an empty tank at one of the 
gas stations.

Return the minimum starting gas station   s index if you can travel around the circuit once,
otherwise return -1


You can only travel in one direction. i to i+1, i+2, ... n-1, 0, 1, 2..


Completing the circuit means starting at i and ending up at i again.


Input :
      Gas :   [1, 2]
      Cost :  [2, 1]

Output : 1

If you start from index 0, you can fill in gas[0] = 1 amount of gas. Now your tank has 1 unit of gas. But you need cost[0] = 2 gas to travel to station 1.
If you start from index 1, you can fill in gas[1] = 2 amount of gas. Now your tank has 2 units of gas. You need cost[1] = 1 gas to get to station 0. So, you travel to station 0 and still have 1 unit of gas left over. You fill in gas[0] = 1 unit of additional gas, making your current gas = 2. It costs you cost[0] = 2 to get to station 1, which you do and complete the circuit.

NOW THE SOLUTION
================================
start from station 0 and check that the total cost is always less the total
amount of gas we take at each station. If the total cost becomes more, we take
the difference of total gain and total cost. Let us call it loss. Then we start
from the next station and continue till the new total cost remain smaller than
the new total gain. At the last station we check:
if  (new total gain - new total cost )>= loss seen so far:
    return the start index of station
else:
    return -1
'''

def first_gs_index(gain, cost):
    if len(gain) != len(cost):
       return -1
    if len(gain) == 0:
        return -1
    totalcost = sum(cost) 
    totalgain = sum(gain)
    if totalcost > totalgain:
       return -1
    loss_encoutered_till = 0
    gain_till = 0
    least_index = 0
    count = 0
    while count < len(gain):
        gain_till += gain[count] - cost[count]
        if gain_till < 0:
            loss_encoutered_till += abs(gain_till)
            least_index = count + 1
            gain_till = 0
        count += 1

    if gain_till >= loss_encoutered_till:
        return least_index
    return -1

# test run
print first_gs_index([1,2,4,50,2,1,20], [2, 10,10,6,96,6,6])

