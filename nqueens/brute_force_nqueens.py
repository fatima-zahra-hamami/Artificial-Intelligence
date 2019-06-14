import sys

# global variable that is a counter for number of assignments
counter_ = 0


BOARD_SIZE = 20
 
def under_attack(col, queens):
    return col in queens or any(abs(col - x) == len(queens)-i for i,x in enumerate(queens))
 
def rsolve(queens,n):
    global counter_
    if n == len(queens):
        return queens
    else:
        for i in range(n):
            if not under_attack(i,queens):
                # increment counter 
                counter_ += 1
                newqueens = rsolve(queens+[i],n)
                if newqueens != []:
                    return newqueens
        return [] # FAIL

def print_board(queens):
    row = 0
    n = len(queens)
    for pos in queens:
        for i in range(pos):
            sys.stdout.write( ". ")
        sys.stdout.write( "Q ")
        for i in range((n-pos)-1):
            sys.stdout.write( ". ")
        print

        
import time

start = time.time()
ans = rsolve([],BOARD_SIZE)
end = time.time()
print("\ntime to solve: " + str(end-start))
print("\n")
print_board(ans)
print("\n")
print("For %d Queens, Number of assignments: %d" %(BOARD_SIZE,counter_))
print("\n")

