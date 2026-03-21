import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import os
import numpy as np
import shutil
from pathlib import Path

class QuickPCBDefectDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.images = []
        self.labels = []
        
        # Load all images and assign labels based on filename or directory
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(root, file)
                    self.images.append(img_path)
                    
                    # Simple labeling: if filename contains 'defect' or 'bad' -> defective, else normal
                    if any(keyword in file.lower() for keyword in ['defect', 'bad', 'fault', 'error', 'damage']):
                        self.labels.append(1)  # Defective
                    else:
                        self.labels.append(0)  # Normal
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        image_path = self.images[idx]
        image = Image.open(image_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

class QuickDefectModel(nn.Module):
    def __init__(self, num_classes=2):
        super().__init__()
        # Use ResNet18 for faster training
        self.backbone = models.resnet18(weights='IMAGENET1K_V1')
        self.backbone.fc = nn.Linear(512, num_classes)
        
    def forward(self, x):
        return self.backbone(x)

def quick_train_any_dataset():
    """Quick training for any PCB dataset"""
    
    print("=== QUICK TRAINING FOR ANY PCB DATASET ===")
    
    # Check if dataset exists
    dataset_path = r"C:\Users\Ujwal Gowda KR\Downloads\PCB_Defect_Detection-main\images"
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        return False
    
    print(f"Found dataset at: {dataset_path}")
    
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
    full_dataset = QuickPCBDefectDataset(dataset_path, transform=train_transform)
    
    if len(full_dataset) == 0:
        print("Error: No images found in dataset!")
        return False
    
    print(f"Found {len(full_dataset)} images")
    
    # Simple split - use first 80% for training, last 20% for validation
    train_size = max(1, int(0.8 * len(full_dataset)))
    val_size = len(full_dataset) - train_size
    
    # Create indices for split
    indices = list(range(len(full_dataset)))
    train_indices = indices[:train_size]
    val_indices = indices[train_size:]
    
    # Create subset datasets
    train_dataset = torch.utils.data.Subset(full_dataset, train_indices)
    val_dataset = torch.utils.data.Subset(full_dataset, val_indices)
    
    # Update validation dataset transform
    val_dataset.dataset.transform = val_transform
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False, num_workers=0)
    
    print(f"Training samples: {len(train_dataset)}")
    print(f"Validation samples: {len(val_dataset)}")
    
    # Create model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = QuickDefectModel(num_classes=2).to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Training loop
    num_epochs = 10  # Quick training
    best_val_acc = 0.0
    
    print(f"Training on device: {device}")
    print(f"Starting quick training for {num_epochs} epochs...")
    
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
        train_acc = 100.0 * train_correct / train_total if train_total > 0 else 0
        val_acc = 100.0 * val_correct / val_total if val_total > 0 else 0
        
        print(f'Epoch {epoch+1}/{num_epochs}:')
        print(f'  Train Loss: {train_loss/len(train_loader):.4f}, Train Acc: {train_acc:.2f}%')
        print(f'  Val Loss: {val_loss/len(val_loader):.4f}, Val Acc: {val_acc:.2f}%')
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), 'quick_trained_model.pth')
            print(f'  New best model saved! Val Acc: {val_acc:.2f}%')
    
    print(f"\nQuick training completed!")
    print(f"Best validation accuracy: {best_val_acc:.2f}%")
    print(f"Model saved as: quick_trained_model.pth")
    
    return True

if __name__ == "__main__":
    quick_train_any_dataset()




