import numpy as np
import random
import matplotlib.pyplot as plt
import sys


class board:
    def __init__(self):
        self.board = np.zeros([9, 9], dtype=int)

    def __str__(self):
        return(str(self.board))

    def __repr__(self):
        return(str(self.board))

    def _fillZeros(self):
        u, c = np.unique(self.board, return_counts=True)
        toAdd = []
        for i in range(1, 10):
            curr = c[u == i]
            if curr.size > 0:
                toAdd += [i]*(9-int(curr))
            else:
                toAdd += [i]*9
        random.shuffle(toAdd)
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i, j] == 0:
                    self.board[i, j] = toAdd.pop()
        assert np.all(np.unique(self.board, return_counts=True)[1] == 9)

    def fromFile(self, fname):
        with open(fname, 'r') as f:
            for i, line in enumerate(f):
                for j, c in enumerate(line.strip()):
                    if c != '.':
                        self.board[i, j] = int(c)
        self._fillZeros()

    def score(self):
        score = 0
        for i in range(self.board.shape[0]):
            u = np.unique(self.board[i, :])
            score += (len(u)-self.board.shape[0])**2
            u = np.unique(self.board[:, i])
            score += (len(u)-self.board.shape[0])**2
        n = 3
        dim = self.board.shape[0]
        for i in range(0, dim, n):
            for j in range(0, dim, n):
                u = np.unique(self.board[i:i+n, j:j+n])
                score += (len(u)-self.board.shape[0])**2
        return score


class MC:
    def __init__(self, board, initialT, finalT, steps):
        self.board = board
        self.score = [board.score()]
        self.T = [initialT]
        self.Tini = initialT
        self.Tfinal = finalT
        self.step = 0
        self.steps = steps
        self.accept = []

    def _swap(self):
        a, b, c, d = np.random.randint(0, self.board.board.shape[0], 4)
        A = self.board.board[a, b]
        B = self.board.board[c, d]
        self.board.board[a, b] = B
        self.board.board[c, d] = A
        newScore = self.board.score()
        # print(self.score)
        score = self.score[-1]
        if newScore <= score:
            accept = 1
        else:
            accept = self._getAcceptance(newScore, score)
        self.accept.append(accept)
        if accept == 1:
            self.score.append(newScore)
        else:
            self.score.append(score)
            self.board.board[a, b] = A
            self.board.board[c, d] = B

    def _step(self):
        self._swap()
        self._newT()
        self.step += 1

    def _newT(self):
        # self.T.append((self.Tini-self.Tfinal)/self.steps * self.step)
        self.T.append(self.T[-1]-(self.T[-1]-self.Tfinal)/1e3)

    def run(self):
        while self.step <= (self.steps-1):
            self._step()
            if np.isclose(self.score[-1], 0):
                print('success')
                print(self.board)
                return
        print('fail')
        print(self.board)

    def _getAcceptance(self, newScore, score):
        P = np.exp(-(newScore-score)/self.T[-1])
        u = np.random.random()
        # print(P, u)
        if u <= P:
            return 1
        else:
            return 0


if __name__ == '__main__':
    b = board()
    b.fromFile(sys.argv[1])
    b.score()
    mc = MC(b, initialT=10, finalT=0.1, steps=1e6)
    mc.run()
    plt.figure(1)
    plt.plot(list(range(len(mc.T))), mc.T)
    plt.figure(2)
    plt.plot(list(range(len(mc.T))), mc.score)
    plt.show(block=False)
    input('Press Enter')
