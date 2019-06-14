The goal of the N-Queens game is to place N queens on an NxN chess board so no queen can attack another queen. We can view the problem space as a large tree, and the objective is to traverse this tree untill we have reached a solution. The problem space is exponential in the number of queens (n^n). The naive solution is to do a depth first traversal of this problem space which is not feasable. To effectively solve this problem, we implement the arc-consistency. Arc-consistency will drastically minimize the problem space and make our deapth first traversal much more efficient. The idea is that arc consistency will let us know ahead of time if it is worth traversing a path in the tree by "looking ahead" and checking whether or not including this path in the solution will lead to a potential future conflict

Optimized the brute force by reducing the total number of placements of Qeens until a solution is found

    8 Queens: brute-force: 113, AC3: 15
    10 Queens: brute-force: 102, AC3: 10
    20 Queens: brute-force: 199,500, AC3: 27
