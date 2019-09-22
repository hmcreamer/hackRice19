import torch
import numpy as np
from torch_geometric.data import Data, DataLoader, NeighborSampler


def get_loader():
    # Load data made with API's run experiment methods
    saved_data = torch.load('./data/1k_50_data.pth')
    print('Loaded .pth data')

    # Get relevant arrays to train on
    state_hist, edge_hist = saved_data['state_hist'], saved_data['edge_hist']
    agents = saved_data['agents']

    """
    Create node feature input:
    
    x  = [[state of node_0, user type of node_0],
          [state of node_1, user type of node_1],
          ...
          [state of node_v, user type of node_v]]
    """

    x = np.zeros((len(state_hist[0]), len(state_hist)))
    for i, row in enumerate(state_hist):
        for j, col in enumerate(row):
            x[j][i] = state_hist[i][j]

    x += 2 # Shift dist to avoid errors
    x = torch.tensor(x, dtype=torch.float)
    print(f'nodes x steps: {x.shape}')

    """
    edge_index = [[s_0, s_1, ..., s_e],
                  [d_0, d_1, ..., d_e]]
    ex:
        edge_index = torch.tensor([[0, 0, 1, 1, 2], [1, 1, 0, 2, 1]])
    """

    edge_index = [[], []]
    attrs = []
    for i, row in enumerate(edge_hist[-1]):
        for j, col in enumerate(row):
            if edge_hist[-1][i][j] > 0 and j < i:
                # Non-zero weight and only view connection once
                edge_index[0].append(i)
                edge_index[1].append(j)
                # Also save edge weight
                attrs.append(edge_hist[-1][i][j])

    edge_index = torch.tensor(edge_index, dtype=torch.long)
    print(f'Edge Index Shape: {edge_index.shape}')

    """
    edge_attr = [[edge_0_data_sent],
                 [edge_1_data_sent],
                 ...
                 [edge_e_data_sent]]
    """

    edge_attr = torch.tensor(attrs, dtype=torch.float)
    print(f'Edge Attributes Shape: {edge_attr.shape}')

    """
    y = [
      node_0_y,
      ...,
      node_n_y,
    ]
    """
    agents = (np.array(agents) == -1) * 1

    y = torch.tensor(agents)
    print(f'y Shape: {y.shape}')

    # Add into pytorch geometric's Data class
    data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y)
    data.train_mask = torch.Tensor(x.shape[0]).uniform_() < 0.8
    data.test_mask = torch.tensor(1 - data.train_mask.numpy(), dtype=torch.uint8)
    data.train_mask = torch.tensor(1 - data.test_mask.numpy(), dtype=torch.uint8)

    loader = NeighborSampler(data, size=0.6, num_hops=2, batch_size=32, shuffle=True, add_self_loops=True)
    return loader, data

if __name__ == '__main__':
    get_loader()