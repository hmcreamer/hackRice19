import torch
import torch.nn.functional as F
from data import get_loader
from model import SAGENet

data, loader = get_loader()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = SAGENet(data.x.shape[1], 1).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

print(f'Loaded model on: {device}')


"""
Define Training Loop
"""

def train():
    model.train()

    total_loss = 0
    for data_flow in loader(data.train_mask):
        print(data.x)
        optimizer.zero_grad()
        out = model(data.x.to(device), data_flow.to(device))
        print(out)
        print(data.y[data_flow.n_id])
        loss = F.binary_cross_entropy(out, data.y[data_flow.n_id].float().to(device))
        print(loss)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * data_flow.batch_size
    return total_loss / data.train_mask.sum().item()


"""
Define Test Loop
"""

def test(mask):
    model.eval()

    correct = 0
    for data_flow in loader(mask):
        pred = model(data.x.to(device), data_flow.to(device)).max(1)[1]
        correct += pred.eq(data.y[data_flow.n_id].to(device)).sum().item()
    return correct / mask.sum().item()

"""
Train over dataset!
"""

NUM_EPOCHS = 30

for epoch in range(NUM_EPOCHS):
    loss = train()
    test_acc = test(data.test_mask)
    print(f'Epoch: {epoch + 1}/{NUM_EPOCHS}, Loss: {loss}, Test: {test_acc}')

