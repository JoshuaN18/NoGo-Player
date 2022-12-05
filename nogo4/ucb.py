from math import log, sqrt
INFINITY = float("inf")

def mean(stats, i: int) -> float:
    return stats[i][0] / stats[i][1]


def ucb(stats, C: float, i: int, n: int) -> float:
    if stats[i][1] == 0:
        return INFINITY
    return mean(stats, i) + C * sqrt(log(n) / stats[i][1])


def findBest(stats, C: float, n: int) -> int:
    best = -1
    bestScore = -INFINITY
    for i in range(len(stats)):
        score = ucb(stats, C, i, n)
        if score > bestScore:
            bestScore = score
            best = i
    assert best != -1
    return best

def bestArm(stats) -> int:  # Most-pulled arm
    best = -1
    bestScore = -INFINITY
    for i in range(len(stats)):
        if stats[i][1] > bestScore:
            bestScore = stats[i][1]
            best = i
    assert best != -1
    return best


def runUcb(player, board, C, moves, toplay):
    stats = [[0, 0] for _ in moves]
    num_simulation = len(moves) * player.sim
    for n in range(num_simulation):
        moveIndex = findBest(stats, C, n)
        result = player.simulate(board, moves[moveIndex], toplay)
        if result == toplay:
            stats[moveIndex][0] += 1  # win
        stats[moveIndex][1] += 1
    bestIndex = bestArm(stats)
    best = moves[bestIndex]
    #writeMoves(board, moves, stats)
    return best