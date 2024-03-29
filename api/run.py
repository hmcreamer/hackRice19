from flask import Flask
from flask import render_template
import networkx as nx
import numpy as np
import copy
import json
# import torch

app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
    return render_template('index.html', message="Please route to /simulate to see our simulated environment")

@app.route('/simulate')
def start_exp():
    """ The endpoint that we hit from our webapp in order to create our simulated environment"""
    experiment = Experiment(25)
    initial = experiment.get_initial()
    hist, statehist = experiment.get_hist(25)
    statehistjson = json.dumps(statehist)
    print(hist)
    # print(initial)
    all_agents = json.dumps(experiment.agents.tolist())
    return render_template('test.html', graph=initial, history = hist, agents=all_agents, statehistory = statehistjson)

def run_exp(experiment):
    """ Helper function for running our experiment """
    trans_hist = experiment.to_api(10)
    #redirect user to new templste with completed experiment data


def initialize_matrix(matrix):
    """ Initializes our matrix to a format that can be read by the front end"""
    nodes = []
    edges = []
    n = matrix.shape
    for i in range(matrix.shape[0]):
        id_entry = {"id" : i}
        nodes.append({"data" : id_entry})
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 1:
                edge_entry = {}
                edge_entry["id"] = str(i) + ',' + str(j)
                edge_entry["weight"] = 1
                edge_entry["source"] = str(i)
                edge_entry["target"] = str(j)
                edges.append({"data" : edge_entry})
    print("edges")
    print(edges)
    return nodes, edges


def send_data_for_tick(matrix):
    """ Converts our data on the edges to a format that can interpreted by the front end """
    new_path = []
    # If the value is 1, then the color will be changed to red. If the value is -1, the color will be changed to blue
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 1:
                key = str(i) + ',' + str(j)
                new_path.append([key, "red"])
            elif matrix[i][j] == -1:
                key = str(i) + ',' + str(j)
                new_path.append([key, "blue"])
    return new_path

def process_list_tick_matrices(list):
    """ Converts our data on the changes in the state matrices to a format that can interpreted by the front end """
    all_paths = [send_data_for_tick(matrix) for matrix in list]
    file_path = "../api/tickdata.json"
    with open(file_path, "w") as json_file:
        json.dump(all_paths, json_file)
    return json.dumps(all_paths)

def send_node_change_data(nodes):
    """ Converts our data on the nodes to a format that can interpreted by the front end """
    node_colors = []
    for node in nodes:
        if node == 1:
            node_colors.append("red")
        elif node == -1:
            node_colors.append("blue")
        else:
            node_colors.append("black")
    return node_colors

""" 
A class for an experiment within our simulated social network environment.

Arguments:
     N (int): the number of nodes in the graph
     agent_probs: list of probabilities for each agent type

"""
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
        self.edges = self.edges + np.identity(N)

        # Give each node an agent type - fake, neutral, not fake
        self.agents = np.array([np.random.choice([-1, 0, 1], p=agent_probs) for _ in range(N)])

        # Give each node an initial state - what kind of info do they carry
        self.states = self.agents.copy()

        # state then agent type
        self.transmission_probs = {
            -1: {-1: 0.9, 0: 0.35, 1: 0.1},
            0: {-1: 0.0, 0: 0.0, 1: 0.0},
            1: {-1: 0.1, 0: 0.35, 1: 0.9},
        }

        # will store a history
        self.state_history = []
        self.transmission_history = []
        self.edge_weight_history = []

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
                prob_new_state = prob_new_state * self.edges[i][j]
                j_update = self.states[i]

                if random[i][j] < prob_new_state:
                    transmission_matrix[i][j] = j_update

                edge_weight_matrix[i][j] = prob_new_state
        # print(transmission_matrix)
        for j in range(N):
            # nodes wont send to themselves
            identity = sum(transmission_matrix[:, j])
            # print(j, identity)
            if identity > 0:
                new_states[j] = 1
            elif identity < 0:
                new_states[j] = -1

        # print("new_states", new_states)
        return new_states, transmission_matrix, edge_weight_matrix

    def run(self, steps):
        """ Runs a simulation of the interaction of the nodes in the social network we have created. This simulation is
            run 'steps' number of times
         """
        for i in range(steps):
            new_states, transmission_matrix, edge_weight_matrix = self.update()

            self.state_history.append(self.states.tolist())
            self.transmission_history.append(transmission_matrix)
            self.edge_weight_history.append(edge_weight_matrix)
            self.states = new_states.copy()
        return self.state_history, self.transmission_history, self.edge_weight_history

    def get_hist(self, steps):
        """ Returns the history of the states, edges, and edge weights of our network """
        state_hist, trans_hist, edge_weight_hist = self.run(steps)
        return process_list_tick_matrices(trans_hist), state_hist

    def get_initial(self):
        """ Returns the initial states and edges of our network """
        nodes, edges = initialize_matrix(self.edges)
        graph_dict = {'nodes': nodes, 'edges': edges}
        file_path = "../api/data.json"
        with open(file_path, "w") as json_file:
            json.dump(graph_dict, json_file)

        print("graph dict")
        print(graph_dict)
        return json.dumps(graph_dict)

    # def get_pytorch_data(self, generations, file_name):
    #     result = self.run(generations)
    #     torch.save({
    #         "state_hist": result[0],
    #         "trans_hist": result[1],
    #         "edge_hist": result[2]
    #     }, file_name)

experiment = Experiment(100)
#experiment.get_hist()