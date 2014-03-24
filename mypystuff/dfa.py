import random
import numpy as np
import networkx as nx
import pygraphviz as pgv
import matplotlib.pyplot as plt
from collections import defaultdict, deque

class DFA(object):
    def __init__(self, T, accept = None, start_state = 0):
        self.T = T
        if accept is None:
            self.accept = [len(trans) - 1]
        else:
            self.accept = accept
        self.start_state = start_state
        self.state = start_state

    def transition(self, symbol):
        return self.T[self.state, symbol]

    def reset(self):
        self.state = self.start_state

    def step(self, symbol):
        self.state = self.transition(symbol)
    
    def accepting(self):
        return self.state in self.accept

    def accepts_str(self, string):
        self.reset()
        for symbol in string:
            self.step(symbol)
        return self.state in self.accept

    def nextsymbolpredict(self, seq, N = 200, steps = 100):
        '''
        self.reset()
        for x in seq:
            self.step(x)
        Q = deque([(self.T[self.state, i], i) for i in range(len(self.T[0]))])
        visited = set([state for state, symbol in Q])
        while Q:
            state, symbol = Q.popleft()
            for nextsymbol, nextstate in enumerate(self.T[state]):
                if nextstate in self.accept:
                    return symbol
                elif nextstate not in visited:
                    Q.append((nextstate, symbol))
                    visited.add(nextstate)
        return random.choice([0, 1])
        '''
        nsymbols = len(self.T[0])
        d = defaultdict(int)
        for i in range(N):
            self.reset()
            first = np.random.randint(nsymbols)
            self.step(first)
            for t in range(1, steps):
                if self.accepting():
                    d[first] += 1./t
                    break
                self.step(np.random.randint(nsymbols))
        if len(d):
            return max(d.items(), key = lambda x: x[1])[0]
        return np.random.randint(nsymbols)

    def gen(self, maxlen = 100):
        while True:
            self.reset()
            symbols = []
            for i in range(maxlen):
                s = np.random.randint(len(self.T[0]))
                symbols.append(s)
                self.step(s)
                if self.accepting():
                    if random.random() < 0.5:
                        return symbols

def connected(dfa):
    from collections import deque
    Q = deque([0])
    visited = set([0])
    states = set(range(len(dfa.T)))
    while Q:
        s = Q.popleft()
        visited.add(s)
        if visited & states == states:
            return True
        for i in dfa.T[s]:
            if i not in visited:
                Q.append(i)
    return False

def rand_connected_dfa(nsymbols, nstates, p = 0.5):
    while True:
        T = np.random.randint(0, nstates, (nstates, nsymbols))
        accept = set(np.arange(nstates)[np.random.random(nstates) < p])
        while not len(accept):
            accept = set(np.arange(nstates)[np.random.random(nstates) < p])
        dfa = DFA(T.astype(int), accept)
        if connected(dfa):
            return dfa

def draw(dfa, fname):
    prog = ['neato', 'dot'][1]
    edgedict = defaultdict(list)
    if prog == 'neato':
        G = pgv.AGraph(directed = True, size = '20,20', nodesep = '1.0', overlap = 'false')
    elif prog == 'dot':
        G = pgv.AGraph(directed = True, nodesep = '0.2', overlap = 'false')
    
    for i in range(len(dfa.T)):
        if i in dfa.accept:
            G.add_node(str(i), shape = 'doublecircle')
        else:
            G.add_node(str(i))

    for src, outgoing in enumerate(dfa.T):
        for symbol, target in enumerate(outgoing):
            edgedict[(src, target)].append(symbol)
    
    for (src, target), symbols in edgedict.items():
        G.add_edge(src, target, label = '{' + '|'.join(map(str, symbols)) + '}', weight = '10')

    G.layout(prog = prog)
    G.draw(fname)

if __name__ == '__main__':
    dfa = rand_connected_dfa(2, 5, p = 0.1)
    print dfa.T
    draw(dfa, 'testimg.pdf')
    while True:
        print dfa.gen()
