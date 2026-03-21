import torch
import torch.nn as nn
import torchvision.models as models
from ..config import DEFECT_TYPES

class DefectDetectionModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Use EfficientNetV2 as backbone
        self.backbone = models.efficientnet_v2_l(weights='IMAGENET1K_V1')
        backbone_output_features = 1280  # EfficientNetV2-L's fixed output features
        
        # Freeze early layers
        for param in list(self.backbone.parameters())[:-30]:
            param.requires_grad = False
        
        # Remove the original classifier
        self.backbone.classifier = nn.Identity()
        
        # Feature extractor with Layer Normalization instead of Batch Normalization
        self.feature_extractor = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(backbone_output_features, 1024),
            nn.LayerNorm(1024),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(1024, 512),
            nn.LayerNorm(512),
            nn.ReLU(),
            nn.Dropout(0.3),
        )
        
        # Simplified attention mechanism
        self.attention = nn.Sequential(
            nn.Linear(512, 512),
            nn.LayerNorm(512),
            nn.ReLU()
        )
        
        # Classifier with Layer Normalization
        self.classifier = nn.Sequential(
            nn.Linear(512, 256),
            nn.LayerNorm(256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(128, len(DEFECT_TYPES))
        )

    def forward(self, x):
        # Handle single sample case
        if x.dim() == 3:
            x = x.unsqueeze(0)  # Add batch dimension
            
        # Extract features
        x = self.backbone.features(x)
        x = self.feature_extractor(x)
        x = self.attention(x)
        x = self.classifier(x)
        
        return x

    def predict(self, x):
        self.eval()  # Set to evaluation mode
        with torch.no_grad():
            return self.forward(x)