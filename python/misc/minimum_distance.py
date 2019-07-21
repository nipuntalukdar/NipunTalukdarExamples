'''
Given the distance between cities, find the shortest distance between 
city 0 and city N-1

Take a matrix of N*N size and matrix[i][j] represents the cost 
of travel from city i to city j

min_distance finds the minimum distance between 0 and N-1 th city

min_distance_any_two finds the minimum distance between any 2 cities.
Here we pass an array of cities where first element is the start city,
and the last element is the end city and the middle elements are all
other cities. For example, if there are 6 cities and we want t0 find
the distance between 3rd and 5th cities, then we will pass the array,
[2,0,1,3,5,4]  

THIS algorithm assumes the cost between 2 cities in both direction are 
constant

'''


def min_distance(cities, startcity, endcity, distance_matrix):
    if startcity == endcity:
        distance = 0
        #endcity node must be included
        cities.append(endcity)
        i = 0
        while i < (len(cities) -1):
            distance += distance_matrix[cities[i]][cities[i+1]]
            i += 1
        cities.pop()
        return distance
    #include startcity node
    cities.append(startcity)
    distance1 = min_distance(cities, startcity+1, endcity, distance_matrix)
    if startcity != 0:
        #cannot exclude start city, but other cities may be excluded
        cities.pop()
        distance2 = min_distance(cities, startcity+1, endcity, distance_matrix)
        return min(distance2, distance1)
    else:
        return distance1

def min_distance_any_two(cities, startcity, distance_matrix, destcities):
    if startcity == len(destcities) -1:
        distance = 0
        #endcity node must be included
        cities.append(destcities[startcity])
        i = 0
        while i < (len(cities) -1):
            distance += distance_matrix[cities[i]][cities[i+1]]
            i += 1
        cities.pop()
        return distance
    #include startcity node
    cities.append(destcities[startcity])
    distance1 = min_distance_any_two(cities, startcity + 1,
        distance_matrix, destcities)
    if startcity != 0:
        #cannot exclude start city, but other cities may be excluded
        cities.pop()
        distance2 = min_distance_any_two(cities,  startcity + 1,
            distance_matrix,destcities)
        return min(distance2, distance1)
    else:
        return distance1

dist_matrix = [[0, 25, 20, 10, 105],
               [25, 0, 30, 40, 80],
               [20, 30, 0, 70, 1900],
               [10, 40, 70, 0, 100],
               [105, 80, 1900, 100, 0]]

print min_distance([],0, 4, dist_matrix)
print min_distance_any_two([], 0, dist_matrix, [4,1,0,3,2])

