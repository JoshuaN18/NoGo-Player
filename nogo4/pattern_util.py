from board_util import EMPTY, BORDER, BLACK, WHITE, GoBoardUtil
from sys import stdin, stdout, stderr
import linecache
class PatternUtil(object):

    @staticmethod
    def neighborhood_33(board, point):
        """
        Get the pattern around point.
        Returns
        -------
        pattern:
        A pattern in the same format as in the michi pattern base. 
        Refer to pattern.py for documentation of this format.
        """
        positions = [
            point - board.NS + 1,
            point - board.NS,
            point - board.NS - 1,
            
            point + 1,
            #point,
            point - 1,
            
            point + board.NS + 1,
            point + board.NS,
            point + board.NS - 1,
            
        ]

        pattern = ""
        for d in positions:
            if board.board[d] == BLACK:
                pattern += "1"
            elif board.board[d] == WHITE:
                pattern += "2"
            elif board.board[d] == EMPTY:
                pattern += "0"
            elif board.board[d] == BORDER:
                pattern += "3"
        return pattern

    @staticmethod
    def generate_pattern_moves(board, toPlay):
        emptyPoints = board.get_empty_points()
        moves = []
        for p in emptyPoints:
            if board.is_legal(p, toPlay):
                moves.append(p)
        if not moves:
            return None
        return moves, None

    @staticmethod
    def generate_random_moves(board, toPlay):
        emptyPoints = board.get_empty_points()
        moves = []
        for p in emptyPoints:
            if board.is_legal(p, toPlay):
                moves.append(p)
        if not moves:
            return None, None
        percentages = []
        for _ in range(len(moves)):
            percentages.append(1/len(moves))
        return moves, percentages
    
    @staticmethod
    def get_value(board, toPlay, move):
        pattern = PatternUtil.neighborhood_33(board, move)
        number = convert(pattern)
        line = linecache.getline('weights.txt', number + 1)

        return line.split(' ')[1].split('\n')[0]
    
def convert(pattern):
    sum = 0
    for i in range(len(pattern)):
        if pattern[-(i+1)] != '0':
            sum += int(pattern[-(i+1)]) * (4**i)
    return sum

def respond(response=""):
    """ Send response to stdout """
    stdout.write("+ {}\n\n".format(response))
    stdout.flush()