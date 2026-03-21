from ...ml.models.defect_model import DefectDetectionModel
from ...ml.utils.metrics import DefectMetricsCalculator
from fastapi import APIRouter, UploadFile, HTTPException
import numpy as np
from PIL import Image
import io
import torch
import cv2
import base64

# Initialize model
model = DefectDetectionModel()
model.load_state_dict(torch.load('path/to/model/weights.pth'))
model.eval()

async def process_image(image: UploadFile) -> np.ndarray:
    """Process uploaded image into numpy array"""
    contents = await image.read()
    img = Image.open(io.BytesIO(contents))
    img = img.convert('RGB')
    img = img.resize((224, 224))  # Standard size for model
    return np.array(img)

def calculate_defect_areas(predictions: np.ndarray) -> np.ndarray:
    """Calculate area for each detected defect"""
    # Convert predictions to binary mask
    defect_mask = predictions > 0.5  # Assuming predictions are probability scores
    
    # Calculate area as percentage of total image area
    total_pixels = predictions.shape[0] * predictions.shape[1]
    defect_areas = np.sum(defect_mask, axis=(1, 2)) / total_pixels
    
    return defect_areas

def format_defects(predictions: np.ndarray) -> list:
    """Format defect predictions into a list of defect objects"""
    defect_types = ['no_defect', 'edge_defect', 'component_defect', 'solder_defect', 'surface_defect']
    defect_probs = predictions if len(predictions.shape) > 1 else np.expand_dims(predictions, 0)
    
    formatted_defects = []
    for i, probs in enumerate(defect_probs):
        defect_type = defect_types[np.argmax(probs)] if len(probs.shape) > 0 else defect_types[int(probs)]
        confidence = float(np.max(probs)) if len(probs.shape) > 0 else 1.0
        
        formatted_defects.append({
            "id": str(i),
            "type": defect_type,
            "confidence": confidence,
            "severity": "high" if confidence > 0.8 else "medium" if confidence > 0.5 else "low"
        })
    
    return formatted_defects

def create_annotated_image(image: np.ndarray, predictions: np.ndarray) -> str:
    """Create annotated image with defect predictions"""
    # Create a copy of the image for annotation
    annotated = image.copy()
    
    # Add defect overlays (simplified example)
    defect_mask = predictions > 0.5
    annotated[defect_mask] = cv2.addWeighted(annotated[defect_mask], 0.7, np.array([255, 0, 0]), 0.3, 0)
    
    # Convert to base64
    _, buffer = cv2.imencode('.png', cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
    return f"data:image/png;base64,{base64.b64encode(buffer).decode()}"

def create_heatmap(predictions: np.ndarray) -> str:
    """Create heatmap visualization of predictions"""
    # Generate heatmap
    heatmap = cv2.applyColorMap(
        (predictions * 255).astype(np.uint8),
        cv2.COLORMAP_JET
    )
    
    # Convert to base64
    _, buffer = cv2.imencode('.png', heatmap)
    return f"data:image/png;base64,{base64.b64encode(buffer).decode()}"

router = APIRouter()

@router.post("/analyze")
async def analyze_image(image: UploadFile):
    try:
        # Process image and get predictions
        image_array = await process_image(image)
        predictions = model.predict(image_array)
        defect_areas = calculate_defect_areas(predictions)
        
        # Initialize metrics calculator
        calculator = DefectMetricsCalculator(image_dimensions=image_array.shape[:2])
        
        # Create mock ground truth for development (replace with actual ground truth later)
        ground_truth = np.zeros_like(predictions)  # Assuming binary classification
        
        # Calculate metrics
        metrics = calculator.calculate_metrics(
            y_true=ground_truth,
            y_pred=predictions,
            defect_areas=defect_areas
        )
        
        # Format response
        return {
            "status": "success",
            "data": {
                "defects": format_defects(predictions),
                "metrics": metrics,
                "annotatedImage": create_annotated_image(image_array, predictions),
                "heatmap": create_heatmap(predictions)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 