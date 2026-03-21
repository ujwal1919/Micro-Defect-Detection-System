import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import os
import numpy as np
from sklearn.model_selection import train_test_split

class PCBDefectDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.images = []
        self.labels = []
        
        # Load normal images
        normal_dir = os.path.join(data_dir, "normal")
        if os.path.exists(normal_dir):
            for file in os.listdir(normal_dir):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    self.images.append(os.path.join(normal_dir, file))
                    self.labels.append(0)  # 0 for normal
        
        # Load defective images
        defective_dir = os.path.join(data_dir, "defective")
        if os.path.exists(defective_dir):
            for file in os.listdir(defective_dir):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    self.images.append(os.path.join(defective_dir, file))
                    self.labels.append(1)  # 1 for defective
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        image_path = self.images[idx]
        image = Image.open(image_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

class ImprovedDefectModel(nn.Module):
    def __init__(self, num_classes=2):
        super().__init__()
        # Use ResNet50 for better feature extraction
        self.backbone = models.resnet50(weights='IMAGENET1K_V1')
        # Replace the final layer
        self.backbone.fc = nn.Linear(2048, num_classes)
        
    def forward(self, x):
        return self.backbone(x)

def train_new_model():
    """Train a new model with the organized dataset"""
    
    print("Starting new model training...")
    
    # Check if dataset exists
    if not os.path.exists("data/training"):
        print("Error: Dataset not found! Please run organize_new_dataset.py first.")
        return False
    
    # Data transforms
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create dataset
    full_dataset = PCBDefectDataset("data/training", transform=train_transform)
    
    # Split dataset
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])
    
    # Update validation dataset transform
    val_dataset.dataset.transform = val_transform
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False, num_workers=2)
    
    print(f"Training samples: {len(train_dataset)}")
    print(f"Validation samples: {len(val_dataset)}")
    
    # Create model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = ImprovedDefectModel(num_classes=2).to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
    
    # Training loop
    num_epochs = 20
    best_val_acc = 0.0
    
    print(f"Training on device: {device}")
    print(f"Starting training for {num_epochs} epochs...")
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = torch.max(output.data, 1)
            train_total += target.size(0)
            train_correct += (predicted == target).sum().item()
            
            if batch_idx % 10 == 0:
                print(f'Epoch {epoch+1}/{num_epochs}, Batch {batch_idx}/{len(train_loader)}, Loss: {loss.item():.4f}')
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                loss = criterion(output, target)
                
                val_loss += loss.item()
                _, predicted = torch.max(output.data, 1)
                val_total += target.size(0)
                val_correct += (predicted == target).sum().item()
        
        # Calculate accuracies
        train_acc = 100.0 * train_correct / train_total
        val_acc = 100.0 * val_correct / val_total
        
        print(f'Epoch {epoch+1}/{num_epochs}:')
        print(f'  Train Loss: {train_loss/len(train_loader):.4f}, Train Acc: {train_acc:.2f}%')
        print(f'  Val Loss: {val_loss/len(val_loader):.4f}, Val Acc: {val_acc:.2f}%')
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), 'new_trained_model.pth')
            print(f'  New best model saved! Val Acc: {val_acc:.2f}%')
        
        scheduler.step()
    
    print(f"\nTraining completed!")
    print(f"Best validation accuracy: {best_val_acc:.2f}%")
    print(f"Model saved as: new_trained_model.pth")
    
    return True

if __name__ == "__main__":
    train_new_model()





