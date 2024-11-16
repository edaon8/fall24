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


n, d = invr()
notes = []
for i in range(n):
    note = inp()
    notes.append(note)

notes.sort()
recordings = 1
curr_min = notes[0]
for i in range(n):
    if notes[i] > curr_min + d:
        curr_min = notes[i]
        recordings += 1

print(recordings)

