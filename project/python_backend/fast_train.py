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

class FastPCBDataset(Dataset):
    def __init__(self, data_dir, transform=None, max_samples=500):
        self.data_dir = data_dir
        self.transform = transform
        self.samples = []
        
        # Load only a subset for faster training
        normal_dir = os.path.join(data_dir, 'normal')
        if os.path.exists(normal_dir):
            images = [f for f in os.listdir(normal_dir) 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # Take only first max_samples images
            images = images[:max_samples]
            
            for img_file in images:
                self.samples.append({
                    'image_path': os.path.join(normal_dir, img_file),
                    'label': 0  # All normal images
                })
        
        logger.info(f"Loaded {len(self.samples)} samples for fast training")
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        image = Image.open(sample['image_path']).convert('RGB')
        label = sample['label']
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

class FastModelTrainer:
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
    
    def train(self, train_loader, epochs=10):
        for epoch in range(epochs):
            logger.info(f'Epoch {epoch+1}/{epochs}')
            
            train_loss, train_acc = self.train_epoch(train_loader)
            
            logger.info(f'Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%')
            
            # Save model every 5 epochs
            if (epoch + 1) % 5 == 0:
                torch.save(self.model.state_dict(), f'fast_model_epoch_{epoch+1}.pth')
                logger.info(f'Model saved: fast_model_epoch_{epoch+1}.pth')

def create_fast_transforms():
    """Create fast training transforms"""
    train_transform = transforms.Compose([
        transforms.Resize((128, 128)),  # Smaller image size
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform

def main():
    print("🚀 Fast PCB Training Mode")
    print("=" * 50)
    
    # Configuration for fast training
    data_dir = "data/training"
    batch_size = 64  # Larger batch size
    epochs = 10  # Fewer epochs
    max_samples = 500  # Use only 500 images
    
    # Check if data directory exists
    if not os.path.exists(data_dir):
        logger.error(f"Data directory {data_dir} not found!")
        return
    
    # Create transforms
    train_transform = create_fast_transforms()
    
    # Create dataset
    train_dataset = FastPCBDataset(data_dir, transform=train_transform, max_samples=max_samples)
    
    if len(train_dataset) == 0:
        logger.error("No images found!")
        return
    
    # Create data loader
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # Create lightweight model
    class FastDefectModel(nn.Module):
        def __init__(self):
            super().__init__()
            # Use smaller EfficientNet
            self.backbone = models.efficientnet_b0(weights='IMAGENET1K_V1')
            
            # Freeze most layers
            for param in list(self.backbone.parameters())[:-10]:
                param.requires_grad = False
            
            # Simple classifier
            self.backbone.classifier = nn.Sequential(
                nn.Dropout(0.2),
                nn.Linear(1280, 2)  # Binary: normal vs defect
            )
        
        def forward(self, x):
            return self.backbone(x)
    
    # Initialize model and trainer
    model = FastDefectModel()
    trainer = FastModelTrainer(model)
    
    print(f"📊 Training Configuration:")
    print(f"  Images: {len(train_dataset)}")
    print(f"  Batch Size: {batch_size}")
    print(f"  Epochs: {epochs}")
    print(f"  Device: {trainer.device}")
    
    # Estimate time
    if torch.cuda.is_available():
        estimated_time = epochs * 2  # ~2 minutes per epoch on GPU
        print(f"  Estimated Time: ~{estimated_time} minutes")
    else:
        estimated_time = epochs * 15  # ~15 minutes per epoch on CPU
        print(f"  Estimated Time: ~{estimated_time} minutes")
    
    print(f"\n🚀 Starting fast training...")
    
    # Train the model
    trainer.train(train_loader, epochs)
    
    # Save final model
    torch.save(model.state_dict(), 'fast_model_final.pth')
    logger.info('Final model saved: fast_model_final.pth')
    
    print(f"\n✅ Fast training complete!")
    print(f"📁 Model saved as: fast_model_final.pth")
    print(f"\n🔧 To use this model, update your defect_detection.py to load 'fast_model_final.pth'")

if __name__ == "__main__":
    main()





