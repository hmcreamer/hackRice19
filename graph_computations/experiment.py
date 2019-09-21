import api.data_transfer as df

import networkx as nx
import numpy as np
import copy


class Experiment:
    def __init__(self, N,
                 agent_probs=(.1, .8, .1),
                 ):
        """ Initializes an instance of the experiment class to model dynamic graph systems

        Arguments:
             N (int): the number of nodes in the graph
             agent_probs: list of probabilities for each agent type

        """
        # initialize graph
        er = nx.erdos_renyi_graph(N, 0.25)
        self.N = N
        self.edges = np.array(nx.adjacency_matrix(er).todense())

        # Give each node an agent type - fake, neutral, not fake
        self.agents = np.array([np.random.choice([-1, 0, 1], p=agent_probs) for _ in range(N)])

        # Give each node an initial state - what kind of info do they carry
        self.states = self.agents.copy()

        # state then agent type
        self.transmission_probs = {
            -1: {-1: 0.5, 0: 0.3, 1: 0.2},
            0: {-1: 0.0, 0: 0.0, 1: 0.0},
            1: {-1: 0.2, 0: 0.3, 1: 0.5},
        }

        # will store a history
        self.state_history = [self.states]
        self.transmission_history = [np.zeros((N,N))]

    def set_transmission_probs(self, transmission_dict):
        """ sets a new probability dict for transmission_dict """
        pass

    def update(self):
        """ Returns state at next time step """
        N = self.N
        random = np.random.rand(N, N)
        new_states = np.zeros(N)
        transmission_matrix = np.zeros((N,N))

        for i in range(N):
            for j in range(N):
                prob_new_state = self.transmission_probs[self.agents[i]][self.states[j]]
                j_update = self.states[i]
                j_same = self.states[j]

                if random[i][j] < prob_new_state:
                    transmission_matrix[i][j] = j_update
                else:
                    transmission_matrix[i][j] = j_same

        for j in range(N):
            identity = sum(transmission_matrix[:][j])
            if identity > 0:
                new_states[j] = 1
            elif identity < 0:
                new_states[j] = -1
            else:
                new_states[j] = 0

        return new_states, transmission_matrix

    def run(self, steps):
        for i in range(steps - 1):
            new_states, transmission_matrix = self.update()

            self.state_history.append(new_states)
            self.transmission_history.append(transmission_matrix)
            self.states = new_states
        return self.state_history, self.transmission_history

    def get_hist(self, steps):
        trans_hist = self.run(steps)[1]
        return trans_hist

    def get_initial(self):
        return df.initialize_matrix(self.edges)





experiment = Experiment(100)
print(experiment.agents)
print(experiment.run(10)[0])