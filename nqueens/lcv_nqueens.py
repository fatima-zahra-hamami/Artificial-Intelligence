import sys
import timeit
import operator



BOARD_SIZE = 20
counter_ = 0

"""
    Queen data structure where we initialize it with the row of the queen
"""
class Queen:
    def __init__(self,row):
        self.row = row
        self.columns = None
        self.col = None
    
    def remove_column(self,col):
        self.columns.remove(col)
        
# Generating Queen data structures
"""
    Initialize a dictionary of Queen objects ordered by K:V 
    where K is the row of the queen
    and V is the actual Queen object
"""
queens_ = {}
for i in range(BOARD_SIZE):
    queens_[i] = Queen(row=i)
    
def under_attack(col, queens):
    return col in queens or any(abs(col - x) == len(queens)-i for i,x in enumerate(queens))

"""
    This helper function checks if the passed point is under attack.
    The difference between this function and under_attack(col,queens)
    is that this function checks if any point you pass is under attack
    by the queens array
    
    point = (row,col)
"""
def is_under_attack(row, col, queens):
    if col in queens:
        return True
    for j,k in enumerate(queens):
        if abs(col - k) == row - j:
            return True
    return False
    
              
"""
    This is the order by least constraining value function that takes the list of queens and board size
    as input and returns a list of candidate columns ordered from increasing # of conflicts associated 
    with placing a queen in a given column.

    We first figure out where the queen can reach if it were placed in a column
    and check every point it if can reach if it is a newly restricted square. If
    it is, we count record it as a new restriction in our dictionary of K:V pairs 
    where K is the column and V is the number of restrictions associated 
    with placing the queen at the column

    we return this dictionary by converting it into a list of ordered columns
"""
def order_by_LCV(queens,n):
    # a counter to record the number of new restrictions if a queen was placed at a given position
    new_restrictions = 0
    # a dictionary (K:V) where K is the column and V is the number of restrictions associated with placing 
    # the queen at the column
    col_rest = {}
    for potential_column in range(BOARD_SIZE):
        # ignore columns that are already used by previously allocated queens
        if potential_column not in queens:
            if not under_attack(potential_column,queens):
            
                # Where can the queen get given the position: ( len(queens) , potential_column)
                # These are ranges that define where the queen can reach if it was placed here 
                bottom_range = BOARD_SIZE - len(queens)
                left_range   = min(potential_column - 0, bottom_range)  + 1
                right_range  = min(BOARD_SIZE-left_range, bottom_range) + 1
                
                # determining newly restricted squares on the right diagonal of the position: 
                #(len(queens) , potential_column)
                for i in range(1,right_range):
                    is_restricted = is_under_attack(len(queens) + i,potential_column + i, queens)
                    # if the point is not already restricted by a previously allocated queen, then 
                    # do a bounds check and increment the counter
                    if not is_restricted:
                        # bounds check
                        if (len(queens) + i < BOARD_SIZE and len(queens) + i >=0 and potential_column + i < BOARD_SIZE and potential_column + i >= 0):
                            new_restrictions += 1

                # determining newly restricted squares on the left diagonal of the position: 
                #(len(queens) , potential_column)   
                for i in range(1, left_range):
                    #to_test = (len(queens) + i, potential_column - i)
                    is_restricted = is_under_attack(len(queens) + i, potential_column - i, queens)
                    if not is_restricted:
                        # bounds check
                        if (len(queens) + i < BOARD_SIZE and len(queens) + i >=0 and potential_column - i < BOARD_SIZE and potential_column - i >= 0):
                        
                            new_restrictions += 1

                # determining the newly restricted squares UNDER the position:
                #( len(queens) , potential_column)
                for i in range(1,bottom_range):
                    is_restricted = is_under_attack(len(queens) + i, potential_column, queens)
                    if not is_restricted:
                        # bounds check
                        if (len(queens) + i < BOARD_SIZE and len(queens) + i >=0 and potential_column < BOARD_SIZE and potential_column >= 0):
                            new_restrictions += 1
                # set K:V pair for the queen we just checked
                col_rest[potential_column] = new_restrictions
                # reset the restrictions counter 
                new_restrictions = 0

     # sort the col_rest dictionary and convert it into a list of column indexes 
     # ordered from increasing # of conflicts
    return [x[0] for x in sorted(col_rest.items(), key=operator.itemgetter(1))]        

def rsolve(queens,n):
    global counter_
    if n == len(queens):
        return queens
    else:
        # get a reference of which queen we are about to allocate
        queen = queens_[len(queens)]
        # run LCV and set the queen's columns based on the results of LCV
        queen.columns = order_by_LCV(queens,n)
        for i in queen.columns:
            if not under_attack(i,queens):
                counter_ += 1
                queen.col=i
                newqueens = rsolve(queens+[queen.col],n)
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
