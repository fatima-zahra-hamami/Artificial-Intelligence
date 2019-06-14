import sys
import timeit
import operator
import time
from collections import  deque

BOARD_SIZE = 20
counter_ = 0


# initialize the queens_dict data structure
# It is ordered by K:V where:
#     K is the the row of the queen 
#     V is the list of columns in the queen's domain
queens_dict = {x:[v for v in range(BOARD_SIZE)] for x in range(BOARD_SIZE)}

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
    This helper function checks is a single point is under attack by a SINGLE queen.
"""
def sq_under_attack(x,y,qX,qY):
    if y == qY:
        return True
    if abs(y - qY) == x - qX:
        return True
    return False


"""
    This function performs arc consistency.
    
    Inputs: queens_dict: the dictionary of queens to perform arc consistency on
            queens:      the list of queens to run arc consistency on
            
    this function runs the ac3 algorithm we learned in class
    
    We take a potential configuration of queens and perform arc consistency
    with a queue data structure. We use the queens list to figure out which
    potential queen we are checking for and populate the queue with all arcs associated 
    with the potential placement.
    
    Following this, we pop arsc from the queue and make their domains consistent with 
    one another
    
    If the domain of a queen ever becomes empty, we immedietly return Fail
"""
def ac3(queens_dict,queens):
    
    # A double ended queue data structure to contain the arcss to run AC on
    #     ** NOTE: we only use this as a normal queue and not a double ended queue
    arcs_queue = deque()
    # Figure out which queen we will run arc consistency for
    q = len(queens)-1
    
    # Loop to populate the queue with all the arcs associated with the current queen
    # we are running AC for
    for q1 in queens_dict.keys():
        if q1 > q:
            for q2 in queens_dict.keys(): 
                if q2 > q and q2 != q1:
                        #print("Pushing: (%d , %d) to the queue" % (q1,q2))
                        arcs_queue.append((q1,q2))

    while len(arcs_queue) > 0:
        # Pop an arc from the queue
        arc = arcs_queue.popleft()
        # get reference of which queens we are using
        queen1 = arc[0]
        queen2 = arc[1]
        
        # Call revise on the arc we just removed from the queue
        if revise(queens_dict,queen1,queen2):
            # if the domain of the queen we just revised is empty return false
            if len(queens_dict[queen1]) == 0:
                return False
            # if we removed something, re-add the neighbors to the queue as per the algorithm
            for neighbor in queens_dict.keys():
                if neighbor not in queens and neighbor > q:
                    arcs_queue.append((queen1,neighbor))
                    
    # if arc consistency passed, return True
    return True

"""
    this helper function updates the domain of the queens in queens_dict
    
    Inputs: queens_dict: the dictionary of queens we revise the domain on
            queens:      the potential allocation of queens that we are 
                         updating the domain for
                         
    ** NOTE: we call this function before we call ac3. We call it by placing the queen
             in a potential column (mandated by LCV) and check if the allocation is arc consistent
             
             if ac3 fails, we revert the domain by using its local copy so 
             so we do not have to do extraneous book keeping
"""
def update_domain(queens_dict,queens):
    # get the queen we just potentially allocated
    queen = len(queens)-1
    # get the col of the queen
    col = queens[len(queens)-1]
    for k,v in queens_dict.items():
        if k != queen:
            # A list to record all the values we are deleting
            to_del = []
            for i in range(len(v)):
                # check if the value in q2's domain is inconsistent with q1 
                if sq_under_attack(k,v[i],queen,col):
                    to_del.append(v[i])
            # Perform the deletions we recorded in to_del
            queens_dict[k] = [x for x in v if x not in to_del]
            
"""
    this helper function is used by ac3.
    Inpute: queens_dict
            q1: the queen whose domain we are trying to reduce
            q2: the queen to check for consistent values with q1
            
    For all values in q1's domain, if we cannot find a value that is consistent
    with it in q2's domain, then delete the value form q1's domain
"""
def revise(queens_dict,q1,q2):
    revised = False
    for i in queens_dict[q1]:
        satisfied = False
        for j in queens_dict[q2]:
            # check if the square is under attack
            if not sq_under_attack(q2,j,q1,i):
                satisfied = True
        if satisfied == False:
            # If we did not find a value consistent in q2's domain, then delete i from q1's domain
            queens_dict[q1].remove(i)
            revised=True
    return revised

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
    new_restrictions = 0
    col_restrictions = []
    col_rest = {}
    for potential_column in range(BOARD_SIZE):
        if potential_column not in queens:
            if not under_attack(potential_column,queens):
            
                # Where can the queen get given the position: ( len(queens) , potential_column)
                # These are ranges that we will iterate over so +1 to be inclusive of the bounds
                bottom_range = BOARD_SIZE - len(queens)
                left_range   = min(potential_column - 0, bottom_range)  + 1
                right_range  = min(BOARD_SIZE-left_range, bottom_range) + 1
                
                # determining newly restricted squares on the right diagonal of the position: 
                #(len(queens) , potential_column)

                for i in range(1,right_range):
                    #to_test = (len(queens)  + i,potential_column + i)
                    is_restricted = is_under_attack(len(queens) + i,potential_column + i, queens)
                    if not is_restricted:
                        if (len(queens) + i < BOARD_SIZE and len(queens) + i >=0 and potential_column + i < BOARD_SIZE and potential_column + i >= 0):
                            new_restrictions += 1

                # determining newly restricted squares on the left diagonal of the position: 
                #(len(queens) , potential_column)   
                
                for i in range(1, left_range):
                    #to_test = (len(queens) + i, potential_column - i)
                    is_restricted = is_under_attack(len(queens) + i, potential_column - i, queens)
                    if not is_restricted:
                        if (len(queens) + i < BOARD_SIZE and len(queens) + i >=0 and potential_column - i < BOARD_SIZE and potential_column - i >= 0):
                        
                            new_restrictions += 1

                # determining the newly restricted squares UNDER the position:
                #( len(queens) , potential_column)
                for i in range(1,bottom_range):
                    is_restricted = is_under_attack(len(queens) + i, potential_column, queens)
                    if not is_restricted:
                        if (len(queens) + i < BOARD_SIZE and len(queens) + i >=0 and potential_column < BOARD_SIZE and potential_column >= 0):
                            new_restrictions += 1

                col_rest[potential_column] = new_restrictions
                new_restrictions = 0

    return [x[0] for x in sorted(col_rest.items(), key=operator.itemgetter(1))]        

def rsolve(queens_dict,queens,n):
    global counter_
    if n == len(queens):
        return queens
    else:
        # figure out which queen we went to allocate
        queen = len(queens)
        
        # run LCV on the queen we are trying to allocate
        queens_dict[queen] = order_by_LCV(queens,BOARD_SIZE)
        
        # make a copy of the queens_dictionary in case we fail
        local_queens = dict(queens_dict)
        for i in queens_dict[queen]:
            
            # artifically update the domain of the queen so we can run arc consistency on it
            update_domain(queens_dict,queens+[i])
            inference = ac3(queens_dict,queens+[i])
            
            # if ar3 passes, allocate the queen and move on to the next one with the recursive call
            if inference:
                counter_ += 1
                newqueens=rsolve(queens_dict,queens+[i],BOARD_SIZE)
                if newqueens != []:
                    return newqueens
            # if we ever fail, we reset the queens_dict
            queens_dict = dict(local_queens)
        return []        

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

start = time.time()
ans = rsolve(queens_dict,[],BOARD_SIZE)
end = time.time()
print("\ntime to solve: " + str(end-start))
print("\n")
print_board(ans)
print("\n")
print("For %d Queens, Number of assignments: %d" %(BOARD_SIZE,counter_))
print("\n")
