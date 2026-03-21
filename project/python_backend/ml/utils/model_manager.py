import torch
import os
from ml.models.defect_model import DefectDetectionModel
import logging

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, model_path="models/"):
        self.model_path = model_path
        self.model = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    def load_model(self, model_name="fast_model_final.pth"):
        """Load a trained model"""
        # Check both models/ directory and current directory
        model_file = os.path.join(self.model_path, model_name)
        if not os.path.exists(model_file):
            model_file = model_name  # Check current directory
        
        if not os.path.exists(model_file):
            logger.warning(f"Model file {model_name} not found. Using untrained model.")
            return self._create_untrained_model()
        
        try:
            # Create model instance
            self.model = DefectDetectionModel()
            
            # Load state dict
            state_dict = torch.load(model_file, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Successfully loaded model from {model_file}")
            return self.model
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return self._create_untrained_model()
    
    def _create_untrained_model(self):
        """Create an untrained model as fallback"""
        logger.warning("Creating untrained model - results will be random!")
        self.model = DefectDetectionModel()
        self.model.to(self.device)
        self.model.eval()
        return self.model
    
    def save_model(self, model, model_name="best_model.pth"):
        """Save a trained model"""
        os.makedirs(self.model_path, exist_ok=True)
        model_file = os.path.join(self.model_path, model_name)
        
        try:
            torch.save(model.state_dict(), model_file)
            logger.info(f"Model saved to {model_file}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def get_model(self):
        """Get the current model"""
        if self.model is None:
            return self.load_model()
        return self.model
