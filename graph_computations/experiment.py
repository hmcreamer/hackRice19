import graph_computations.random_graphs as rg
import networkx as nx
import numpy as np

class Experiment:
    def __init__(self, N, ):
        # initialize graph
        er = nx.erdos_renyi_graph(N, 0.25)
        self.N = N
        self.edges = np.array(nx.adjacency_matrix(er).todense())

        # Give each node an agent type - fake, neutral, not fake
        self.agents = [np.random.choice([-1, 0, 1]) for _ in range(N)]

        # Give each node an initial state - what kind of info do they carry
        self.states = [np.random.choice([-1, 0, 1]) for _ in range(N)]

        self.transmission_probs = {
            -1: {-1: 0.5, 0: 0.3, 1: 0.2},
            0: {-1: 0.0, 0: 0.0, 1: 0.0},
            1: {-1: 0.2, 0: 0.3, 1: 0.5},
        }

        # will store a history
        self.history = [self.states]

    def update(self):
        """ Returns state at next time step """
        N = self.N
        random = np.random.rand(N, N)
        new_states = np.zeros((N,N))

        for i in range(N):
            for j in range(N):
                prob_new_state = self.transmission_probs[self.agents[i]][self.states[j]]
                j_update = self.states[i]
                j_same = self.states[j]

                # Make update if by random
                new_states[j] = j_update if random[i][j] < prob_new_state else j_same
        return new_states

    def run(self, steps):
        for i in range(steps):
            new_states = self.update()
            self.history.append(new_states)
            self.states = new_states
        return self.history