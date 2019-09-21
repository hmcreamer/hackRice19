import api.data_transfer as df

import networkx as nx
import numpy as np
import copy
import json


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
            -1: {-1: 0.6, 0: 0.3, 1: 0.1},
            0: {-1: 0.0, 0: 0.0, 1: 0.0},
            1: {-1: 0.1, 0: 0.3, 1: 0.6},
        }

        # will store a history
        self.state_history = []
        self.transmission_history = []
        self.edge_weight_history = []

    def set_transmission_probs(self, transmission_dict):
        """ sets a new probability dict for transmission_dict """
        pass

    def update(self):
        """ Returns state at next time step """
        N = self.N
        random = np.random.rand(N, N)
        new_states = np.zeros(N)
        transmission_matrix = np.zeros((N,N))
        edge_weight_matrix = np.zeros((N,N))

        for i in range(N):
            for j in range(N):
                prob_new_state = self.transmission_probs[self.agents[i]][self.states[j]]
                j_update = self.states[i]
                j_same = self.states[j]

                if random[i][j] > prob_new_state:
                    transmission_matrix[i][j] = j_update
                else:
                    transmission_matrix[i][j] = j_same

                edge_weight_matrix[i][j] = prob_new_state
        print(transmission_matrix)
        for j in range(N):
            # nodes wont send to themselves
            identity = sum(transmission_matrix[:,j])
            print(j, identity)
            if identity > 0:

                new_states[j] = 1
            elif identity < 0:

                new_states[j] = -1

        print("new_states", new_states)
        return new_states, transmission_matrix, edge_weight_matrix

    def run(self, steps):
        for i in range(steps):
            new_states, transmission_matrix, edge_weight_matrix = self.update()

            self.state_history.append(self.states)
            self.transmission_history.append(transmission_matrix)
            self.edge_weight_history.append(edge_weight_matrix)
            self.states = new_states.copy()
        return self.state_history, self.transmission_history, self.edge_weight_history

    def get_hist(self, steps):
        trans_hist = self.run(steps)[1]
        return trans_hist

    def get_initial(self):
        nodes, edges = df.initialize_matrix(self.edges)
        graph_dict = {'nodes': nodes, 'edges': edges}
        file_path = "../api"
        with open(file_path, "w") as json_file:
            json.dump(graph_dict, json_file)
        return simplejson.dumps(graph_dict)

#experiment = Experiment(10)
#print(experiment.states)
#print(experiment.run(2)[0])
