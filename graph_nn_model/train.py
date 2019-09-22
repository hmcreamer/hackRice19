import torch
from data import get_loader
from model import SAGENet
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter()
NUM_EPOCHS = 100

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
loader, data = get_loader()
model = SAGENet(data.x.shape[1], 1).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
criterion = torch.nn.BCEWithLogitsLoss()

print(f'Loaded model on: {device}')


def train():
    model.train()

    total_loss = 0
    for data_flow in loader(data.train_mask):
        optimizer.zero_grad()
        out = model(data.x.to(device), data_flow.to(device))
        loss = criterion(out.squeeze(dim=1), data.y[data_flow.n_id].float().to(device))
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * data_flow.batch_size
    return total_loss / data.train_mask.sum().item()


for epoch in range(NUM_EPOCHS):
    loss = train()
    writer.add_scalar('Loss', loss, epoch)
    print(f'Epoch: {epoch + 1}/{NUM_EPOCHS}, Loss: {loss}')

