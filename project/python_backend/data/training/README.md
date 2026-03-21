
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
