#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above
import numpy
from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from board import GoBoard
from sys import stdin, stdout, stderr
import numpy as np
from ucb import runUcb
from pattern_util import PatternUtil
import random


class Go0:
    def __init__(self):
        """
        NoGo player that selects moves randomly from the set of legal moves.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "Go0"
        self.version = 1.0
        self.selection = "rr"
        self.policy = "random"
        self.sim = 10
        self.limit = 100



    def get_move(self, board, color):
        # return GoBoardUtil.generate_random_move(board, color, 
        #                                         use_eye_filter=False)
        cboard = board.copy()
        emptyPoints = board.get_empty_points()
        moves = []
        for p in emptyPoints:
            if board.is_legal(p, color):
                moves.append(p)
        # If there are no more legal moves
        if not moves:
            return None
        if self.selection == 'ucb':
            C = 0.4
            best = runUcb(self, cboard, C, moves, color)

            return best
        else:
            # This is for rr
            moveWins = []
            for move in moves:
                wins = self.simulateMove(cboard, move, color)
                moveWins.append(wins)
            #writeMoves(cboard, moves, moveWins, self.args.sim)

            return select_best_move(board, moves, moveWins)

    def simulateMove(self, board, move, toplay) -> int:
        """
        Run self.sim simulations for a given move. Returns number of wins.
        """
        wins = 0
        for _ in range(self.sim):
            result = self.simulate(board, move, toplay)
            if result == toplay:
                wins += 1
        return wins
    
    def simulate(self, board, move, toplay):
        """
        Run a simulated game for a given move.
        """
        cboard: GoBoard = board.copy()
        cboard.play_move(move, toplay)
        opp = GoBoardUtil.opponent(toplay)
        return self.playGame(cboard, opp)

    def playGame(self, board, color):
        """
        Run a simulation game.
        """
        for _ in range(self.limit):
            color = board.current_player

            if self.policy == 'random':
                move = GoBoardUtil.generate_random_move(board, color, True)
                if move == None:
                    return GoBoardUtil.opponent(color)
            else:
                legal_moves = GoBoardUtil.generate_legal_moves(board, color)
                if len(legal_moves) == 0:
                    return GoBoardUtil.opponent(color)
                values = []
                for move in legal_moves:
                    value = PatternUtil.get_value(board, color, move)
                    values.append(float(value))
                #maxIndex = values.index(max(values))

                move = random.choices(legal_moves, values)[0]
                
            board.play_move(move, color)

        return None
    def respond(self, response=""):
        """ Send response to stdout """
        stdout.write("+ {}\n\n".format(response))
        stdout.flush()

def select_best_move(board, moves, moveWins):
    max_child: int = np.argmax(moveWins)
    return moves[max_child]


def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(Go0(), board)
    con.start_connection()

if __name__ == "__main__":
    run()
