import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import os
import json
import numpy as np
from ml.models.defect_model import DefectDetectionModel
from ml.config import DEFECT_TYPES
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PCBDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.samples = []
        self.defect_types = list(DEFECT_TYPES.keys())
        
        # Load dataset metadata
        self._load_dataset()
    
    def _load_dataset(self):
        """Load dataset from directory structure:
        data_dir/
        ├── short_circuit/
        ├── trace_width_variation/
        ├── surface_contamination/
        ├── layer_misalignment/
        ├── component_damage/
        └── normal/
        """
        for defect_type in self.defect_types:
            defect_dir = os.path.join(self.data_dir, defect_type)
            if os.path.exists(defect_dir):
                for img_file in os.listdir(defect_dir):
                    if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        self.samples.append({
                            'image_path': os.path.join(defect_dir, img_file),
                            'label': self.defect_types.index(defect_type)
                        })
        
        # Add normal samples (no defects)
        normal_dir = os.path.join(self.data_dir, 'normal')
        if os.path.exists(normal_dir):
            for img_file in os.listdir(normal_dir):
                if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.samples.append({
                        'image_path': os.path.join(normal_dir, img_file),
                        'label': len(self.defect_types)  # Normal class
                    })
        
        # If we only have normal images, create a binary classifier
        if len(self.samples) > 0 and all(sample['label'] == len(self.defect_types) for sample in self.samples):
            print("⚠️  Only normal images found. Creating binary classifier (normal vs defects).")
            # Reassign all labels to 0 (normal) for binary classification
            for sample in self.samples:
                sample['label'] = 0
        
        logger.info(f"Loaded {len(self.samples)} samples")
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        image = Image.open(sample['image_path']).convert('RGB')
        label = sample['label']
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

class ModelTrainer:
    def __init__(self, model, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.model = model.to(device)
        self.device = device
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
        self.scheduler = optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=100)
        
    def train_epoch(self, dataloader):
        self.model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(dataloader):
            data, target = data.to(self.device), target.to(self.device)
            
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            
            if batch_idx % 10 == 0:
                logger.info(f'Batch {batch_idx}/{len(dataloader)}, Loss: {loss.item():.4f}')
        
        accuracy = 100. * correct / total
        avg_loss = total_loss / len(dataloader)
        return avg_loss, accuracy
    
    def validate(self, dataloader):
        self.model.eval()
        total_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in dataloader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                loss = self.criterion(output, target)
                
                total_loss += loss.item()
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()
        
        accuracy = 100. * correct / total
        avg_loss = total_loss / len(dataloader)
        return avg_loss, accuracy
    
    def train(self, train_loader, val_loader, epochs=50):
        best_val_acc = 0
        
        for epoch in range(epochs):
            logger.info(f'Epoch {epoch+1}/{epochs}')
            
            # Training
            train_loss, train_acc = self.train_epoch(train_loader)
            
            # Validation
            val_loss, val_acc = self.validate(val_loader)
            
            # Learning rate scheduling
            self.scheduler.step()
            
            logger.info(f'Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%')
            logger.info(f'Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%')
            
            # Save best model
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save(self.model.state_dict(), 'best_model.pth')
                logger.info(f'New best model saved with validation accuracy: {val_acc:.2f}%')

def create_data_transforms():
    """Create data augmentation transforms for training"""
    train_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomCrop((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_transform

def main():
    # Configuration
    data_dir = "data/training"  # Relative to python_backend directory
    batch_size = 32
    epochs = 50
    
    # Check if data directory exists
    if not os.path.exists(data_dir):
        logger.error(f"Data directory {data_dir} not found!")
        logger.info("Please create the following directory structure:")
        logger.info("data/training/")
        logger.info("├── short_circuit/")
        logger.info("├── trace_width_variation/")
        logger.info("├── surface_contamination/")
        logger.info("├── layer_misalignment/")
        logger.info("├── component_damage/")
        logger.info("└── normal/")
        return
    
    # Create transforms
    train_transform, val_transform = create_data_transforms()
    
    # Create datasets
    train_dataset = PCBDataset(data_dir, transform=train_transform)
    val_dataset = PCBDataset(data_dir, transform=val_transform)
    
    # Split dataset (80% train, 20% val)
    train_size = int(0.8 * len(train_dataset))
    val_size = len(train_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        train_dataset, [train_size, val_size]
    )
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # Initialize model and trainer
    # Check if we have only normal images (binary classification)
    has_only_normal = len(train_dataset) > 0 and all(
        train_dataset[i][1] == len(DEFECT_TYPES) for i in range(min(10, len(train_dataset)))
    )
    
    if has_only_normal:
        print("🔧 Creating binary classifier for normal vs defects")
        
        class BinaryDefectModel(nn.Module):
            def __init__(self):
                super().__init__()
                # Use EfficientNetV2 as backbone
                self.backbone = models.efficientnet_v2_l(weights='IMAGENET1K_V1')
                backbone_output_features = 1280
                
                # Freeze early layers
                for param in list(self.backbone.parameters())[:-30]:
                    param.requires_grad = False
                
                self.backbone.classifier = nn.Identity()
                
                # Binary classifier
                self.classifier = nn.Sequential(
                    nn.AdaptiveAvgPool2d(1),
                    nn.Flatten(),
                    nn.Linear(backbone_output_features, 512),
                    nn.LayerNorm(512),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(512, 256),
                    nn.LayerNorm(256),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(256, 2)  # Binary: normal vs defect
                )
            
            def forward(self, x):
                if x.dim() == 3:
                    x = x.unsqueeze(0)
                x = self.backbone.features(x)
                x = self.classifier(x)
                return x
        
        model = BinaryDefectModel()
    else:
        model = DefectDetectionModel()
    
    trainer = ModelTrainer(model)
    
    # Train the model
    trainer.train(train_loader, val_loader, epochs)

if __name__ == "__main__":
    main()
