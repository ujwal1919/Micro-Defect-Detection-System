import os
import shutil
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def organize_deeppcb_dataset():
    """Automatically organize DeepPCB dataset"""
    
    # Your dataset path
    source_dir = r"C:\Users\Ujwal Gowda KR\Downloads\DeepPCB-master\DeepPCB-master"
    
    # Target training directory
    target_dir = "project/python_backend/data/training"
    
    # Defect types
    defect_types = [
        "short_circuit",
        "trace_width_variation", 
        "surface_contamination",
        "layer_misalignment",
        "component_damage",
        "normal"
    ]
    
    print("🔧 PCB Dataset Organizer")
    print("=" * 50)
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"❌ Error: Dataset directory not found at: {source_dir}")
        print("Please check the path and try again.")
        return False
    
    print(f"📁 Source directory: {source_dir}")
    print(f"📁 Target directory: {target_dir}")
    
    # Create target directories
    for defect_type in defect_types:
        os.makedirs(os.path.join(target_dir, defect_type), exist_ok=True)
    
    # Scan source directory for images
    all_images = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                all_images.append(os.path.join(root, file))
    
    print(f"📊 Found {len(all_images)} images")
    
    if len(all_images) == 0:
        print("❌ No images found in the dataset!")
        return False
    
    # Organize images based on DeepPCB structure
    moved_count = 0
    
    # DeepPCB typically has subdirectories or specific naming patterns
    for img_path in all_images:
        filename = os.path.basename(img_path)
        folder_name = os.path.basename(os.path.dirname(img_path))
        
        # Determine defect type based on folder name or filename
        defect_type = None
        
        # Check folder name
        folder_lower = folder_name.lower()
        filename_lower = filename.lower()
        
        if any(keyword in folder_lower for keyword in ['short', 'circuit', 'bridge']):
            defect_type = "short_circuit"
        elif any(keyword in folder_lower for keyword in ['trace', 'width', 'variation']):
            defect_type = "trace_width_variation"
        elif any(keyword in folder_lower for keyword in ['contamination', 'dirt', 'stain']):
            defect_type = "surface_contamination"
        elif any(keyword in folder_lower for keyword in ['misalignment', 'offset', 'layer']):
            defect_type = "layer_misalignment"
        elif any(keyword in folder_lower for keyword in ['damage', 'broken', 'crack']):
            defect_type = "component_damage"
        elif any(keyword in folder_lower for keyword in ['normal', 'good', 'ok', 'clean']):
            defect_type = "normal"
        
        # Check filename if folder didn't match
        if not defect_type:
            if any(keyword in filename_lower for keyword in ['short', 'circuit', 'bridge']):
                defect_type = "short_circuit"
            elif any(keyword in filename_lower for keyword in ['trace', 'width', 'variation']):
                defect_type = "trace_width_variation"
            elif any(keyword in filename_lower for keyword in ['contamination', 'dirt', 'stain']):
                defect_type = "surface_contamination"
            elif any(keyword in filename_lower for keyword in ['misalignment', 'offset', 'layer']):
                defect_type = "layer_misalignment"
            elif any(keyword in filename_lower for keyword in ['damage', 'broken', 'crack']):
                defect_type = "component_damage"
            elif any(keyword in filename_lower for keyword in ['normal', 'good', 'ok', 'clean']):
                defect_type = "normal"
        
        # Default to normal if no match found
        if not defect_type:
            defect_type = "normal"
        
        # Copy image to target directory
        target_path = os.path.join(target_dir, defect_type, filename)
        
        # Handle duplicate filenames
        counter = 1
        original_target = target_path
        while os.path.exists(target_path):
            name, ext = os.path.splitext(original_target)
            target_path = f"{name}_{counter}{ext}"
            counter += 1
        
        try:
            shutil.copy2(img_path, target_path)
            print(f"✅ Moved {filename} → {defect_type}/")
            moved_count += 1
        except Exception as e:
            print(f"❌ Error moving {filename}: {e}")
    
    print(f"\n📊 Organization Complete!")
    print(f"✅ Successfully organized {moved_count} images")
    
    # Show summary
    print(f"\n📈 Dataset Summary:")
    total_images = 0
    for defect_type in defect_types:
        folder_path = os.path.join(target_dir, defect_type)
        if os.path.exists(folder_path):
            count = len([f for f in os.listdir(folder_path) 
                       if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            print(f"  {defect_type}: {count} images")
            total_images += count
    
    print(f"  Total: {total_images} images")
    
    # Validate images
    print(f"\n🔍 Validating images...")
    valid_count = 0
    invalid_count = 0
    
    for defect_type in defect_types:
        folder_path = os.path.join(target_dir, defect_type)
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img_path = os.path.join(folder_path, filename)
                        with Image.open(img_path) as img:
                            img.verify()
                        valid_count += 1
                    except Exception as e:
                        print(f"❌ Invalid image: {filename} - {e}")
                        invalid_count += 1
    
    print(f"✅ Valid images: {valid_count}")
    if invalid_count > 0:
        print(f"❌ Invalid images: {invalid_count}")
    
    print(f"\n🎉 Dataset organization complete!")
    print(f"📁 Organized dataset location: {target_dir}")
    print(f"\n🚀 Next step: Run training with:")
    print(f"   python project/python_backend/train_model.py")
    
    return True

if __name__ == "__main__":
    organize_deeppcb_dataset()





