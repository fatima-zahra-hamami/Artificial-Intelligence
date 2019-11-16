The goal of the N-Queens game is to place N queens on an NxN chess board so no queen can attack another queen. We can view the problem space as a large tree, and the objective is to traverse this tree until we reach a solution. The problem space is exponential in the number of queens (n^n). The naive solution is to do a depth first traversal of this problem space which is not feasable. To effectively solve this problem, we implement the arc-consistency algorithm. Arc-consistency will prune the problem space and make our deapth first traversal much more efficient. The idea is that once we place a queen on the board, we prune the "domains" of the remaining queens and continue to do so (with backtracking) until the domain's of all queens are consistent with one another

Contents: 

    - brute_force_nqueens.py 
        - The original code provided to us. 
          This file is for the first question and just 
          shows how i added the counter to count the number of assignments
    - lcv_nqueens.py
        - This file contains my implementation of the LCV heuristic and is used
          just for question 2.
    - arc_consistency_nqueens.py
        - This file contains my implenentation of the arc consistency algorithm on top
          of the LCV implementation I used earlier. This file is used just for question 3
          
To run either of the 3 files, just enter the following into the terminal: 
    - python file_name.py
    
** To edit the number of queens to test for each file, just open the file with
   some text editor and modify line 7 on each file from BOARD_SIZE = old_val to BOARD_SIZE = new_val
   
The output prints the board, the number of queens, the time it took to solve, 
and the number of assignments it took to solve the problem

Optimized the brute force by reducing the total number of placements of Qeens until a solution is found

    8 Queens:  brute-force: 113,      AC3: 15
    10 Queens: brute-force: 102,      AC3: 10
    20 Queens: brute-force: 199,500,  AC3: 27
