import cv2
import numpy as np
from PIL import Image

class ImageProcessor:
    def __init__(self):
        self.preprocessing_steps = [
            self._normalize,
            self._enhance_contrast,
            self._denoise,
            self._detect_defects
        ]
    
    def preprocess(self, image):
        # Convert PIL Image to numpy array
        img_array = np.array(image)
        
        # Ensure image is in RGB format
        if len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif len(img_array.shape) == 3 and img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        # Apply each preprocessing step
        processed_image = img_array
        for step in self.preprocessing_steps:
            processed_image = step(processed_image)
        
        # Ensure final image is in RGB format
        if len(processed_image.shape) == 2:
            processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2RGB)
        
        return Image.fromarray(processed_image)
    
    def _normalize(self, image):
        # Normalize each channel separately
        normalized = np.zeros_like(image, dtype=np.float32)
        for i in range(3):
            channel = image[:,:,i]
            normalized[:,:,i] = cv2.normalize(
                channel, 
                None, 
                0, 
                255, 
                cv2.NORM_MINMAX
            )
        return normalized.astype(np.uint8)
    
    def _enhance_contrast(self, image):
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE with adaptive clip limit
        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8,8)
        )
        l = clahe.apply(l)
        
        # Merge channels
        enhanced = cv2.merge((l,a,b))
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
    
    def _denoise(self, image):
        # Apply bilateral filter for edge-preserving denoising
        return cv2.bilateralFilter(
            image,
            d=9,      # Diameter of pixel neighborhood
            sigmaColor=75,  # Filter sigma in color space
            sigmaSpace=75   # Filter sigma in coordinate space
        )
    
    def _detect_defects(self, image):
        # This method should only enhance the image, not draw contours
        # Contours will be drawn later in the visualization step
        return image