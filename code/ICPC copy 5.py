import sys
input = sys.stdin.readline

############ ---- Input Functions ---- ############
def inp(): # int
    return(int(input()))
def inlt(): # list int
    return(list(map(int,input().split())))
def insr(): # string
    s = input()
    return(list(s[:len(s) - 1]))
def invr(): # space separated int inputs
    return(map(int,input().split()))

cases = inp()

for c in range(cases):
    n = inp()
    arr_a = invr()
    arr_b = invr()

    dict_a = {}
    dict_b = {}
    for i in range(n):
        if arr_a[i] not in dict_a.keys():
            dict_a[arr_a[i]] = 1
        elif arr_a[i-1] == arr_a[i]:



