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



