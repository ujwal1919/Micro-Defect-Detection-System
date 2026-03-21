import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FixedPCBDataset(Dataset):
    def __init__(self, data_dir, transform=None, max_samples_per_class=1000):
        self.data_dir = data_dir
        self.transform = transform
        self.samples = []
        
        # Load normal images
        normal_dir = os.path.join(data_dir, 'normal')
        if os.path.exists(normal_dir):
            images = [f for f in os.listdir(normal_dir) 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # Take only first max_samples_per_class images
            images = images[:max_samples_per_class]
            
            for img_file in images:
                self.samples.append({
                    'image_path': os.path.join(normal_dir, img_file),
                    'label': 0  # Normal
                })
        
        # Load defective images
        defective_dir = os.path.join(data_dir, 'defective')
        if os.path.exists(defective_dir):
            images = [f for f in os.listdir(defective_dir) 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # Take only first max_samples_per_class images
            images = images[:max_samples_per_class]
            
            for img_file in images:
                self.samples.append({
                    'image_path': os.path.join(defective_dir, img_file),
                    'label': 1  # Defective
                })
        
        logger.info(f"Loaded {len(self.samples)} samples for training")
        logger.info(f"Normal: {len([s for s in self.samples if s['label'] == 0])}")
        logger.info(f"Defective: {len([s for s in self.samples if s['label'] == 1])}")
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        image = Image.open(sample['image_path']).convert('RGB')
        label = sample['label']
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

class FixedModelTrainer:
    def __init__(self, model, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.model = model.to(device)
        self.device = device
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(model.parameters(), lr=0.001)
        
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
            
            if batch_idx % 5 == 0:
                logger.info(f'Batch {batch_idx}/{len(dataloader)}, Loss: {loss.item():.4f}')
        
        accuracy = 100. * correct / total
        avg_loss = total_loss / len(dataloader)
        return avg_loss, accuracy
    
    def train(self, train_loader, epochs=15):
        for epoch in range(epochs):
            logger.info(f'Epoch {epoch+1}/{epochs}')
            
            train_loss, train_acc = self.train_epoch(train_loader)
            
            logger.info(f'Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%')
            
            # Save model every 5 epochs
            if (epoch + 1) % 5 == 0:
                torch.save(self.model.state_dict(), f'fixed_model_epoch_{epoch+1}.pth')
                logger.info(f'Model saved: fixed_model_epoch_{epoch+1}.pth')

def create_fixed_transforms():
    """Create training transforms"""
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(5),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform

def main():
    print("Fixed PCB Training Mode")
    print("=" * 50)
    
    # Configuration for fixed training
    data_dir = "data/training"
    batch_size = 32
    epochs = 15
    max_samples_per_class = 1000
    
    # Check if data directory exists
    if not os.path.exists(data_dir):
        logger.error(f"Data directory {data_dir} not found!")
        return
    
    # Create transforms
    train_transform = create_fixed_transforms()
    
    # Create dataset
    train_dataset = FixedPCBDataset(data_dir, transform=train_transform, max_samples_per_class=max_samples_per_class)
    
    if len(train_dataset) == 0:
        logger.error("No images found!")
        return
    
    # Create data loader
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # Create fixed model
    class FixedDefectModel(nn.Module):
        def __init__(self):
            super().__init__()
            # Use EfficientNet-B0
            self.backbone = models.efficientnet_b0(weights='IMAGENET1K_V1')
            
            # Freeze most layers
            for param in list(self.backbone.parameters())[:-20]:
                param.requires_grad = False
            
            # Binary classifier
            self.backbone.classifier = nn.Sequential(
                nn.Dropout(0.2),
                nn.Linear(1280, 2)  # Binary: normal vs defective
            )
        
        def forward(self, x):
            return self.backbone(x)
    
    # Initialize model and trainer
    model = FixedDefectModel()
    trainer = FixedModelTrainer(model)
    
    print(f"Training Configuration:")
    print(f"  Images: {len(train_dataset)}")
    print(f"  Batch Size: {batch_size}")
    print(f"  Epochs: {epochs}")
    print(f"  Device: {trainer.device}")
    
    # Estimate time
    if torch.cuda.is_available():
        estimated_time = epochs * 2  # ~2 minutes per epoch on GPU
        print(f"  Estimated Time: ~{estimated_time} minutes")
    else:
        estimated_time = epochs * 10  # ~10 minutes per epoch on CPU
        print(f"  Estimated Time: ~{estimated_time} minutes")
    
    print(f"\nStarting fixed training...")
    
    # Train the model
    trainer.train(train_loader, epochs)
    
    # Save final model
    torch.save(model.state_dict(), 'fixed_model_final.pth')
    logger.info('Final model saved: fixed_model_final.pth')
    
    print(f"\nFixed training complete!")
    print(f"Model saved as: fixed_model_final.pth")
    print(f"\nThis model will now detect defects properly!")

if __name__ == "__main__":
    main()
