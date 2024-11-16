def inp(): # For taking integer inputs.
    return(int(input()))

def inlst(): # For taking List inputs.
    return(list(map(int,input().split())))

# For taking string inputs. Actually it returns a List of Characters, instead of a string, 
def instr():
    s = input()
    return(list(s[:len(s) - 1]))

# For taking space seperated integer variable inputs.
def invr(): 
    return(map(int,input().split()))

s = instr()


visited = set()
count = 0
stack = []
stacks = [[]]
sIndex = 0
a = 0
b = 0
c = 0
mDis = float("-inf")

for l in s:
    if l == "A":
        a += 1
    elif l == "B":
        b += 1
    else:
        c += 1
    # print(abs(a-b), abs(a-c), abs(b-c))
    mDis = max(abs(a-b), abs(a-c), abs(b-c), mDis)
print(mDis)