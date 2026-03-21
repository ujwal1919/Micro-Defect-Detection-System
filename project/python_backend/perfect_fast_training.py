"""
PERFECT FAST TRAINING - Binary Classifier (Normal vs Defective)
Trains a fast, accurate model for perfect defect detection
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset, random_split
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import os
import numpy as np

class PerfectBinaryDataset(Dataset):
    """Binary dataset: 0 = Normal, 1 = Defective"""
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.images = []
        self.labels = []
        
        # Load normal images
        normal_dir = os.path.join(data_dir, "normal")
        if os.path.exists(normal_dir):
            normal_files = [f for f in os.listdir(normal_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            for file in normal_files:
                self.images.append(os.path.join(normal_dir, file))
                self.labels.append(0)  # 0 = Normal
        
        # Load defective images
        defective_dir = os.path.join(data_dir, "defective")
        if os.path.exists(defective_dir):
            defective_files = [f for f in os.listdir(defective_dir) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            for file in defective_files:
                self.images.append(os.path.join(defective_dir, file))
                self.labels.append(1)  # 1 = Defective
        
        print(f"Loaded {len([l for l in self.labels if l == 0])} normal images")
        print(f"Loaded {len([l for l in self.labels if l == 1])} defective images")
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        try:
            image = Image.open(self.images[idx]).convert('RGB')
            label = self.labels[idx]
            
            if self.transform:
                image = self.transform(image)
            
            return image, label
        except Exception as e:
            # Return a black image if loading fails
            image = Image.new('RGB', (224, 224), (0, 0, 0))
            if self.transform:
                image = self.transform(image)
            return image, self.labels[idx]

class PerfectBinaryModel(nn.Module):
    """ResNet18-based binary classifier"""
    def __init__(self):
        super().__init__()
        self.backbone = models.resnet18(weights='IMAGENET1K_V1')
        self.backbone.fc = nn.Linear(512, 2)  # 2 classes: Normal, Defective
        
    def forward(self, x):
        return self.backbone(x)

def train_perfect_model():
    """Train perfect binary classifier"""
    
    print("=" * 60)
    print("PERFECT FAST TRAINING - Binary Classifier")
    print("=" * 60)
    
    data_dir = "data/training"
    
    # Check if dataset exists
    if not os.path.exists(data_dir):
        print(f"ERROR: Dataset directory '{data_dir}' not found!")
        return False
    
    normal_dir = os.path.join(data_dir, "normal")
    defective_dir = os.path.join(data_dir, "defective")
    
    if not os.path.exists(normal_dir) or not os.path.exists(defective_dir):
        print(f"ERROR: 'normal' or 'defective' directories not found!")
        return False
    
    # Data transforms with augmentation for training
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(5),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # No augmentation for validation
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create full dataset
    print("\nLoading dataset...")
    full_dataset = PerfectBinaryDataset(data_dir, transform=train_transform)
    
    if len(full_dataset) == 0:
        print("ERROR: No images found in dataset!")
        return False
    
    # Split dataset: 80% train, 20% validation
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])
    
    # Update validation transform
    val_dataset.dataset.transform = val_transform
    
    print(f"Training samples: {len(train_dataset)}")
    print(f"Validation samples: {len(val_dataset)}")
    
    # Create data loaders
    batch_size = 32
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    
    # Create model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\nUsing device: {device}")
    
    model = PerfectBinaryModel().to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=3)
    
    # Training parameters
    num_epochs = 5  # Fast training - reduced for speed
    best_val_acc = 0.0
    patience = 3
    patience_counter = 0
    
    print(f"\nStarting training for {num_epochs} epochs...")
    print("-" * 60)
    
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
            
            if batch_idx % 20 == 0:
                train_acc = 100.0 * train_correct / train_total
                print(f'  Batch {batch_idx}/{len(train_loader)}, Loss: {loss.item():.4f}, Acc: {train_acc:.2f}%')
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        normal_correct = 0
        normal_total = 0
        defective_correct = 0
        defective_total = 0
        
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                loss = criterion(output, target)
                
                val_loss += loss.item()
                _, predicted = torch.max(output.data, 1)
                val_total += target.size(0)
                val_correct += (predicted == target).sum().item()
                
                # Per-class accuracy
                for i in range(target.size(0)):
                    if target[i] == 0:  # Normal
                        normal_total += 1
                        if predicted[i] == 0:
                            normal_correct += 1
                    else:  # Defective
                        defective_total += 1
                        if predicted[i] == 1:
                            defective_correct += 1
        
        # Calculate metrics
        train_acc = 100.0 * train_correct / train_total
        val_acc = 100.0 * val_correct / val_total
        normal_acc = 100.0 * normal_correct / normal_total if normal_total > 0 else 0
        defective_acc = 100.0 * defective_correct / defective_total if defective_total > 0 else 0
        
        print(f"\nEpoch {epoch+1}/{num_epochs} Results:")
        print(f"  Train - Loss: {train_loss/len(train_loader):.4f}, Acc: {train_acc:.2f}%")
        print(f"  Val   - Loss: {val_loss/len(val_loader):.4f}, Acc: {val_acc:.2f}%")
        print(f"  Normal Accuracy: {normal_acc:.2f}% ({normal_correct}/{normal_total})")
        print(f"  Defective Accuracy: {defective_acc:.2f}% ({defective_correct}/{defective_total})")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
            torch.save(model.state_dict(), 'quick_trained_model.pth')
            print(f"  [OK] New best model saved! Val Acc: {val_acc:.2f}%")
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"  Early stopping triggered (no improvement for {patience} epochs)")
                break
        
        scheduler.step(val_acc)
        print("-" * 60)
    
    print(f"\n{'='*60}")
    print(f"Training completed!")
    print(f"Best validation accuracy: {best_val_acc:.2f}%")
    print(f"Model saved as: quick_trained_model.pth")
    print(f"{'='*60}\n")
    
    return True

if __name__ == "__main__":
    success = train_perfect_model()
    if success:
        print("Training successful! Model is ready to use.")
    else:
        print("Training failed! Please check the dataset.")
