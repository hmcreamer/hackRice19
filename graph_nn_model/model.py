"""
GraphSAGE Model Implementation

https://arxiv.org/pdf/1706.02216.pdf
Inductive Representation Learning on Large Graphs. W.L. Hamilton, R. Ying, and J. Leskovec arXiv:1706.02216 [cs.SI], 2017.
"""

import torch
from torch_geometric.nn import SAGEConv, GATConv
import torch.nn.functional as F

class SAGENet(torch.nn.Module):
    def __init__(self, in_channels, out_channels):
        super(SAGENet, self).__init__()
        self.conv1 = SAGEConv(in_channels, 3, normalize=False)
        self.conv2 = SAGEConv(3, out_channels, normalize=False)

    def forward(self, x, data_flow):
        data = data_flow[0]
        x = x[data.n_id]
        x = F.relu(self.conv1((x, None), data.edge_index, size=data.size))
        x = F.dropout(x, p=0.5, training=self.training)
        data = data_flow[1]
        x = self.conv2((x, None), data.edge_index, size=data.size)
        return x
