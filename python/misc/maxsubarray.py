#-------------------------------------------------------------------------------
# Author:      NTalukdar
#
# Created:     30-01-2014
# Copyright:   (c) NTalukdar 2014
#-------------------------------------------------------------------------------
def max_subarray(arr):
    max_sofar = 0
    max_ending_here = 0
    for i in arr:
        max_ending_here = max(0, max_ending_here + i)
        max_sofar = max(max_sofar, max_ending_here)
    print(max_sofar)
def main():
    max_subarray([0, -1, -2 , 3, -1, -1,3])

if __name__ == '__main__':
    main()
