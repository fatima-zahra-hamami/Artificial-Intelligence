from connect5 import *

def main():
    """ Play a game!
    """

    g = Game()
    g.printState()
    player1 = g.players[0]
    player2 = g.players[1]

    win_counts = [0, 0, 0] # [p1 wins, p2 wins, ties]

    exit = False
    while not exit:
        while not g.finished:
            g.nextMove()

        g.findFives()
        g.printState()

        if g.winner == None:
            win_counts[2] += 1

        elif g.winner == player1:
            win_counts[0] += 1

        elif g.winner == player2:
            win_counts[1] += 1

        # used this code to answer the HW questions. Would just print out the # of evaluated nodes
        """print("nodes evaluated for %s: %d" % (player1.name, player1.nodes_evaluated))
        print("nodes evaluated for %s: %d" % (player2.name, player2.nodes_evaluated))
        print("total number of nodes evaluated: %d" % (player1.nodes_evaluated+player2.nodes_evaluated))"""

        # Log file I used for debugging
        """file = open("alpha_beta_performance.txt", "a")
        file.write("%s: %d at depth %d\n" % (player1.name, player1.nodes_evaluated,player1.difficulty))
        file.write("%s: %d at depth %d\n" % (player2.name, player2.nodes_evaluated, player2.difficulty))
        file.write("Total number of nodes evaluated for minimax vs minimax: %d" % (player1.nodes_evaluated+player2.nodes_evaluated))
        file.close()"""

        printStats(player1, player2, win_counts)

        while True:
            play_again = str(input("Would you like to play again? "))

            if play_again.lower() == 'y' or play_again.lower() == 'yes':
                g.newGame()
                g.printState()
                break
            elif play_again.lower() == 'n' or play_again.lower() == 'no':
                print("Thanks for playing!")
                exit = True
                break
            else:
                print("I don't understand... "),

def printStats(player1, player2, win_counts):
    print("{0}: {1} wins, {2}: {3} wins, {4} ties".format(player1.name,
        win_counts[0], player2.name, win_counts[1], win_counts[2]))

if __name__ == "__main__": # Default "main method" idiom.
    main()
