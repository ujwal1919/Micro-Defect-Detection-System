import os
import shutil
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def create_training_structure():
    """Create the directory structure for training data"""
    base_dir = "data/training"
    defect_types = [
        "short_circuit",
        "trace_width_variation", 
        "surface_contamination",
        "layer_misalignment",
        "component_damage",
        "normal"
    ]
    
    for defect_type in defect_types:
        dir_path = os.path.join(base_dir, defect_type)
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")
    
    # Create a README file with instructions
    readme_content = """
# PCB Defect Detection Training Data

## Directory Structure
- short_circuit/ - Images with short circuit defects
- trace_width_variation/ - Images with trace width variations
- surface_contamination/ - Images with surface contamination
- layer_misalignment/ - Images with layer misalignment
- component_damage/ - Images with component damage
- normal/ - Images without defects (good PCBs)

## Data Requirements
- Image formats: PNG, JPG, JPEG
- Minimum resolution: 224x224 pixels
- Recommended: 500+ images per defect type
- Balanced dataset: Similar number of images per class

## Data Collection Tips
1. Use high-quality PCB images
2. Include various lighting conditions
3. Include different PCB types and manufacturers
4. Ensure clear visibility of defects
5. Use consistent image preprocessing

## Training Instructions
1. Place your images in the appropriate directories
2. Run: python train_model.py
3. The trained model will be saved as 'best_model.pth'
"""
    
    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    logger.info(f"Created README at: {readme_path}")

def validate_images(directory):
    """Validate images in a directory"""
    valid_extensions = ('.png', '.jpg', '.jpeg')
    valid_images = []
    invalid_images = []
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(valid_extensions):
            try:
                img_path = os.path.join(directory, filename)
                with Image.open(img_path) as img:
                    img.verify()  # Verify it's a valid image
                valid_images.append(filename)
            except Exception as e:
                invalid_images.append((filename, str(e)))
    
    return valid_images, invalid_images

def check_dataset_balance(base_dir="data/training"):
    """Check if the dataset is balanced"""
    defect_types = [
        "short_circuit",
        "trace_width_variation", 
        "surface_contamination",
        "layer_misalignment",
        "component_damage",
        "normal"
    ]
    
    counts = {}
    for defect_type in defect_types:
        dir_path = os.path.join(base_dir, defect_type)
        if os.path.exists(dir_path):
            valid_images, _ = validate_images(dir_path)
            counts[defect_type] = len(valid_images)
        else:
            counts[defect_type] = 0
    
    logger.info("Dataset balance:")
    for defect_type, count in counts.items():
        logger.info(f"  {defect_type}: {count} images")
    
    return counts

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create training structure
    create_training_structure()
    
    # Check if data exists and validate
    if os.path.exists("data/training"):
        check_dataset_balance()
    else:
        logger.info("Training data directory created. Please add your PCB images.")
