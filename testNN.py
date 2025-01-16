import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torch.optim.lr_scheduler import StepLR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# Define the model architecture
class SimpleNN(nn.Module):
    def __init__(self, hidden_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(3, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x

# Load and preprocess data
def load_data(filename):
    data = pd.read_csv(filename)
    data['BasFunc'] = pd.to_numeric(data['BasFunc'], errors='coerce')
    data['Input'] = pd.to_numeric(data['Input'], errors='coerce')
    data['RelVal'] = pd.to_numeric(data['RelVal'], errors='coerce')
    data.dropna(inplace=True)
    data['Input'] *= 27.2114
    data['Reference'] *= 27.2114
    features = data[['BasFunc', 'Input', 'RelVal']].values
    target = data['Reference'].values.astype(float)
    features_tensor = torch.tensor(features, dtype=torch.float32)
    target_tensor = torch.tensor(target, dtype=torch.float32).view(-1, 1)
    return TensorDataset(features_tensor, target_tensor)

# Split data into training and validation sets
def split_data(dataset, val_size=0.2):
    num_samples = len(dataset)
    indices = torch.randperm(num_samples).tolist()
    split = int(np.floor(val_size * num_samples))
    train_indices, val_indices = indices[split:], indices[:split]
    
    train_subset = torch.utils.data.Subset(dataset, train_indices)
    val_subset = torch.utils.data.Subset(dataset, val_indices)
    
    return train_subset, val_subset

# Training and evaluation function with early stopping
def train_and_evaluate(hidden_size, learning_rate, batch_size, num_epochs=10, patience=10):
    # Load and split data
    dataset = load_data('superset.csv')
    train_dataset, val_dataset = split_data(dataset)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    # Load and preprocess new input data
    new_data = pd.read_csv('testdataset.csv')
    new_data['BasFunc'] = pd.to_numeric(new_data['BasFunc'], errors='coerce')
    new_data['Input'] = pd.to_numeric(new_data['Input'], errors='coerce')
    new_data['RelVal'] = pd.to_numeric(new_data['RelVal'], errors='coerce')
    new_data.dropna(inplace=True)

    new_data['Input'] *= 27.2114
    new_data['Reference'] *= 27.2114

# Extract features and convert to tensor
    new_features = new_data[['BasFunc', 'Input', 'RelVal']].values
    new_targets = new_data['Reference'].values.astype(float)
    new_features_tensor = torch.tensor(new_features, dtype=torch.float32)
    new_targets_tensor = torch.tensor(new_targets,dtype=torch.float32)
    new_dataset = TensorDataset(new_features_tensor, new_targets_tensor)
    new_features_loader = DataLoader(new_dataset, batch_size=batch_size, shuffle=False)

    
    # Define the model, loss function, and optimizer
    model = SimpleNN(hidden_size)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
   # scheduler = StepLR(optimizer, step_size=10, gamma=0.1)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=10, verbose=True)
    # Lists to store losses
    train_losses = []
    val_losses = []
    test_losses = []    

    # Initialize early stopping parameters
    best_val_loss = float('inf')
    epochs_no_improve = 0

    # Train the model
    for epoch in range(num_epochs):
        model.train()
        epoch_train_loss = 0
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            epoch_train_loss += loss.item() * inputs.size(0)
        
        epoch_train_loss /= len(train_loader.dataset)
        train_losses.append(epoch_train_loss)

        # Validate the model
        model.eval()
        epoch_val_loss = 0
        with torch.no_grad():
            for inputs, targets in val_loader:
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                epoch_val_loss += loss.item() * inputs.size(0)
        
        epoch_val_loss /= len(val_loader.dataset)
        val_losses.append(epoch_val_loss)
        
        print(f'Epoch [{epoch+1}/{num_epochs}], Training Loss: {epoch_train_loss:.4f}, Validation Loss: {epoch_val_loss:.4f}')
        scheduler.step(epoch_val_loss) 
        # Check for improvement and early stopping
        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            epochs_no_improve = 0
            # Save the best model
            torch.save(model.state_dict(), 'Xray_Model.pth')
        else:
            epochs_no_improve += 1
        
        if epochs_no_improve >= patience:
            print("Early stopping triggered")
            break
 
    with torch.no_grad():
      epoch_test_loss = 0
      model.eval()
      for inputs, targets in new_features_loader:  
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        epoch_test_loss += loss.item() * inputs.size(0)
        #print(f'Test Loss: {test_loss.item():.4f}')
    epoch_test_loss /= len(new_features_loader.dataset)
    test_losses.append(epoch_test_loss)

   
    # Obtain predictions
    def get_predictions(loader):
        model.eval()
        all_preds = []
        all_targets = []
        with torch.no_grad():
            for inputs, targets in loader:
                outputs = model(inputs)
                all_preds.append(outputs.numpy())
                all_targets.append(targets.numpy())
        return np.concatenate(all_preds), np.concatenate(all_targets)

 # Get training and validation predictions
    train_preds, train_targets = get_predictions(train_loader)
    val_preds, val_targets = get_predictions(val_loader)
    test_preds, test_targets = get_predictions(new_features_loader)
    return train_losses, val_losses, test_losses, train_preds, train_targets, val_preds, val_targets, test_preds, test_targets

# Define hyperparameters
hidden_size = 16
learning_rate = 0.001
batch_size = 32
num_epochs = 30
patience = 10

# Train the model and get losses and predictions
train_losses, val_losses, test_losses, train_preds, train_targets, val_preds, val_targets, test_preds, test_targets = train_and_evaluate(
    hidden_size, learning_rate, batch_size, num_epochs, patience
)

model = SimpleNN(hidden_size)
criterion = nn.MSELoss()
model.load_state_dict(torch.load('Xray_Model.pth'))
model.eval()  # Set model to evaluation mode

# Load and preprocess new input data
new_data = pd.read_csv('testdataset_comp.csv')
new_data['BasFunc'] = pd.to_numeric(new_data['BasFunc'], errors='coerce')
new_data['Input'] = pd.to_numeric(new_data['Input'], errors='coerce')
new_data['RelVal'] = pd.to_numeric(new_data['RelVal'], errors='coerce')
new_data.dropna(inplace=True)

new_data['Input'] *= 27.2114

# Extract features and convert to tensor
new_features = new_data[['BasFunc', 'Input', 'RelVal']].values
new_features_tensor = torch.tensor(new_features, dtype=torch.float32)

# Run inference
with torch.no_grad():
    predictions = model(new_features_tensor)
    print(predictions)
    test_loss = criterion(predictions, new_features_tensor)
    print(f'Test Loss: {test_loss.item():.4f}')
    system = new_data['System'].values
    funct = new_data["Function"].values
    bas   = new_data["Basis"].values
    # Find the difference between predicted and actual values
    differences = predictions - new_data[['Input']].values
    print(f'Differences: {differences.numpy()}')
    print(f'Differences: {system}')

    for i in range(len(differences)):
      print(f'Differences: {differences[i].item()} {system[i]} {funct[i]} {bas[i]}')
    

# Plot losses
plt.figure(figsize=(12, 5))

# Plot training and validation loss
plt.subplot(1, 2, 1)
plt.plot(range(1, len(train_losses) + 1), train_losses, label='Training Loss')
plt.plot(range(1, len(val_losses) + 1), val_losses, label='Validation Loss')
#plt.plot(range(1, len(test_losses) + 1), test_losses, label='Test Loss')

plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training, Validation and Testing Loss Over Epochs')
plt.legend()
plt.grid(True)

# Scatter plot for training results
plt.subplot(1, 2, 2)
plt.scatter(train_targets, train_preds, label='Training Data', alpha=1.0)
plt.scatter(val_targets, val_preds, label='Validation Data', alpha=1.0)
plt.plot([min(train_targets.min(), val_targets.min()), max(train_targets.max(), val_targets.max())],
         [min(train_targets.min(), val_targets.min()), max(train_targets.max(), val_targets.max())],
         'k--', label='Perfect Prediction')
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.title('Predictions vs True Values')
plt.legend()
plt.grid(True)

# Save the figure
plt.savefig('training_validation_results_plot.png')  # Save as PNG file
plt.show()

