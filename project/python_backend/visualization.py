import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

class DefectVisualizer:
    def __init__(self):
        self.colors = {
            "Critical": (255, 0, 0),    # Red
            "Moderate": (255, 165, 0),  # Orange
            "Minor": (255, 255, 0)      # Yellow
        }
    
    def create_visualization(self, image, defects):
        # Convert PIL Image to numpy array
        img_array = np.array(image)
        
        # Create copies for different visualizations
        annotated = img_array.copy()
        heatmap = np.zeros_like(img_array, dtype=np.float32)  # Use float32 for calculations
        
        for defect in defects:
            color = self.colors[defect["severity"]]
            confidence = defect["confidence"]
            
            # Get defect region
            region = self._get_defect_region(img_array, defect)
            
            if region is not None:
                x, y, w, h = region
                
                # Draw on annotated image
                cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)
                
                # Add label
                label = f"{defect['type']} ({confidence:.0%})"
                cv2.putText(annotated, label, (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                # Update defect with bbox
                defect["bbox"] = {
                    "x": (x / annotated.shape[1]) * 100,
                    "y": (y / annotated.shape[0]) * 100,
                    "width": (w / annotated.shape[1]) * 100,
                    "height": (h / annotated.shape[0]) * 100
                }
                
                # Add to heatmap
                mask = np.zeros(img_array.shape[:2], dtype=np.float32)
                cv2.rectangle(mask, (x, y), (x + w, y + h), 1, -1)
                blurred_mask = cv2.GaussianBlur(mask, (99, 99), 30)
                
                # Normalize and apply color
                blurred_mask = cv2.normalize(blurred_mask, None, 0, 1, cv2.NORM_MINMAX)
                color_array = np.array(color, dtype=np.float32)
                
                for c in range(3):
                    heatmap[:, :, c] += blurred_mask * color_array[c] * confidence
        
        # Normalize heatmap to 0-255 range
        heatmap_min = np.min(heatmap)
        heatmap_max = np.max(heatmap)
        if heatmap_max > heatmap_min:
            heatmap = ((heatmap - heatmap_min) / (heatmap_max - heatmap_min) * 255).astype(np.uint8)
        else:
            heatmap = np.zeros_like(img_array, dtype=np.uint8)
        
        # Create final heatmap overlay
        overlay = cv2.addWeighted(img_array, 0.7, heatmap, 0.3, 0)
        
        return {
            "annotated": self._encode_image(annotated),
            "heatmap": self._encode_image(overlay)
        }
    
    def _get_defect_region(self, image, defect):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            return cv2.boundingRect(largest_contour)
        
        # Fallback: return center region
        h, w = image.shape[:2]
        return (w//4, h//4, w//2, h//2)
    
    def _encode_image(self, image):
        # Convert to PIL Image
        if isinstance(image, np.ndarray):
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Encode to base64
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=95)
        return base64.b64encode(buffer.getvalue()).decode()