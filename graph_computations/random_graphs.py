import networkx as nx
import numpy as np

N = 5

# Create random graph
er = nx.erdos_renyi_graph(N, 0.25)
edges = np.array(nx.adjacency_matrix(er).todense())
print(f'Random Graph: \n{edges}\n')

# Give each node an bias - fake, neutral, not fake
# Give each node an intial state - what kind of info do they carry
node_bias = [np.random.choice([-1, 0, 1]) for _ in range(N)]
node_state = [np.random.choice([-1, 0, 1]) for _ in range(N)]

# Update probability
prob_dict = {
    -1: {-1: 0.5, 0: 0.3, 1: 0.2},
    0: {-1: 0.0, 0: 0.0, 1: 0.0},
    1: {-1: 0.2, 0: 0.3, 1: 0.5},
}


def update(n_state, n_bias):
    """ Returns state at next time step """
    random = np.random.rand(N, N)

    for i in range(N):
        for j in range(N):
            prob_new_state = prob_dict[n_bias[i]][n_state[j]]
            j_update = n_state[i]
            j_same = n_state[j]

            # Make update if by random
            n_state[j] = j_update if random[i][j] < prob_new_state else j_same


print(f'Initial State: {node_state}')
update(node_state, node_bias)
print(f'Updated State: {node_state}')
