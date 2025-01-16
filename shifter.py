import torch
import torch.nn as nn
import pandas as pd

# Define the model architecture
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(3, 16)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x

# Load the model
model = SimpleNN()
model.load_state_dict(torch.load('Xray_Model.pth'))
model.eval()  # Set model to evaluation mode

# Load and preprocess new input data
new_data = pd.read_csv('testdataset.csv')
new_data['BasFunc'] = pd.to_numeric(new_data['BasFunc'], errors='coerce')
new_data['Input'] = pd.to_numeric(new_data['Input'], errors='coerce')
new_data['RelVal'] = pd.to_numeric(new_data['RelVal'], errors='coerce')
new_data.dropna(inplace=True)

# Extract features and convert to tensor
new_features = new_data[['BasFunc', 'Input', 'RelVal']].values
new_features_tensor = torch.tensor(new_features, dtype=torch.float32)

# Run inference
with torch.no_grad():
    predictions = model(new_features_tensor)
    print(predictions)

