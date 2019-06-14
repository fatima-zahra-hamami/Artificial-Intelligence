import random
from player import Player
from aiplayer import *
from connect5 import *
from options import *
import logging

class A20321645(AIPlayer):

    def __init__(self, name, color, difficulty=5):
        AIPlayer.__init__(self, name, color, difficulty)
        logging.basicConfig(filename='alpha_beta_performance.log',level=logging.INFO)
        # counter for evaluating # of nodes expanded on.
        #self.nodes_evaluated = 0

    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        # sleeping for about 1 second makes it looks like he's thinking
        #time.sleep(random.randrange(8, 17, 1)/10.0)
        #return random.randint(0, 6)

        ab = AlphaBeta(state)
        best_move, value = ab.bestMove(self.difficulty, state, self.color)
        self.nodes_evaluated += ab.nodes_evaluated
        print(self.nodes_evaluated)
        return best_move


class AlphaBeta(Minimax):

    def __init__(self, board):
        Minimax.__init__(self, board)
        self.nodes_evaluated = 0
        self.pruned_states = []

    def compute_pruned_nodes(self):
        total = 0
        #iterate over pruned_states
        # compute pruned nodes for each state
        # add to total
        # push to log file the total value
        return True

    def bestMove(self, depth, state, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """

        # set alpha and beta values
        a = -99999999
        b = 99999999

        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        # enumerate all legal moves
        legal_moves = {} # will map legal move states to their alpha values
        for col in range(options.getCols()):
            # if column i is a legal move...
            if self.isLegalMove(col, state):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(state, col, curr_player)
                # pass alpha and beta to the call
                legal_moves[col] = -self.search(depth-1, temp, opp_player,a,b)

        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move, best_alpha

    """
        This function is an improved verticalStreak that actually returns if something is a valid streak

        We use the same method as the superclass' verticalStreak in that we check upwards for instances of
        the players symbol (x or o), and then increment. However, when we reach the end of the streak, we
        check if the next space is an ' ' or not. If it is not,
            then we immedietly return failure (the parent's function, we return just break).
        after the loop, we finally check whether the streak is valid
    """
    def verticalStreak(self,row, col, state, streak):
        consecutiveCount = 0
        for i in range(row, options.getRows()):
            if state[i][col].lower() == state[row][col].lower():
                consecutiveCount += 1
            elif state[i][col].lower() != ' ':
                return 0
            else:
                if streak == 5:
                    consecutiveCount += 1
                break
        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    """
        This function enhances the superclass' horizontalStreak by returning true streaks.
        We use the same reasoning as that for our verticalStreak implementation except we
        verify with both the left and right bounds that they are either ' ' or our respective symbol (x or o)
    """
    def horizontalStreak(self,row, col, state, streak):
        consecutiveCount = 0
        left_bound = None
        if col != 0:
            left_bound = [row,col]
        right_bound = None
        for j in range(col, options.getCols()):
            if state[row][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            # immedietly return failure if not our symbol
            elif state[row][j] != ' ':
                return 0
                #left_bound = [row,j]
            else:
                # set the right bound if there is one
                if j != 8:
                    right_bound = [row,j]
                    break
        if streak == 5:
            if left_bound:
                if state[left_bound[0]][left_bound[1]-1]  == ' ':
                            consecutiveCount += 1
            if right_bound:
                #print(right_bound)
                if state[right_bound[0]][right_bound[1]+1]  == ' ':
                            consecutiveCount += 1

        #print(left_bound, right_bound)
        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def value(self, state, color):
        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]

        my_fours = self.checkForStreak(state, color, 5)
        my_threes = self.checkForStreak(state, color, 4)
        my_twos = self.checkForStreak(state, color, 3)

        # get the features of the opponent
        opp_fours = self.checkForStreak(state, o_color, 5)
        opp_threes = self.checkForStreak(state, o_color,4)
        opp_twos = self.checkForStreak(state, o_color,3)
        # if in a wining position, make the play immedietly
        if my_fours > 0:
            return 100000
        if opp_fours > 0:
            return -100000
        else:
            # weight the evaluation functon to be more aggressive when we have some streaks
            return 6*(my_threes*100 + my_twos*10) - 4*(opp_threes*100 + opp_twos*10)

    """
        The major difference in this is that search now takes alpha and beta parameters

        On every recursive call to search, we swap and negate alpha and beta to swap the
        perspective of who is makeing the move from alpha and beta.
    """
    def search(self, depth, state, curr_player, ALPHA, BETA):

        # temp varariables so we do not alter ALPHA and BETA
        alpha = ALPHA
        beta = BETA
        # increment counter
        #self.nodes_evaluated += 1

        # enumerate all legal moves from this state
        legal_moves = []
        for i in range(options.getCols()):
            # if column i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)

        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        # default starter value
        node_val = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            # we call search again, but we swap alpha and beta and negate them to
            # continue being able to use the single search function
            # by swapping and negating alhpa and beta, we change the perspecive of
            # who is making the move at each recusrive call
            node_val = max(node_val, -self.search(depth-1, child, opp_player,-beta,-alpha))
            # compare the returned value to beta. If >= beta, prune the subtree
            if node_val >= beta:
                return node_val
            alpha = max(alpha,node_val)
        return node_val
