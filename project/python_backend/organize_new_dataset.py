import os
import shutil
from pathlib import Path

def organize_new_dataset():
    """Organize the new PCB_DATASET into training format"""
    
    # Source and destination paths
    source_path = r"C:\Users\Ujwal Gowda KR\Downloads\archive\PCB_DATASET"
    dest_path = "data/training"
    
    # Create destination directories
    os.makedirs(f"{dest_path}/normal", exist_ok=True)
    os.makedirs(f"{dest_path}/defective", exist_ok=True)
    
    print("Organizing new PCB dataset...")
    
    # Copy normal PCB images (PCB_USED folder)
    normal_source = os.path.join(source_path, "PCB_USED")
    if os.path.exists(normal_source):
        normal_files = [f for f in os.listdir(normal_source) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"Found {len(normal_files)} normal PCB images")
        
        for i, file in enumerate(normal_files):
            src = os.path.join(normal_source, file)
            dst = os.path.join(f"{dest_path}/normal", f"normal_{i+1:03d}.jpg")
            shutil.copy2(src, dst)
            print(f"Copied normal image: {file}")
    
    # Copy defective images from all defect categories
    defective_count = 0
    defect_categories = ["Missing_hole", "Mouse_bite", "Open_circuit", "Short", "Spur", "Spurious_copper"]
    
    for category in defect_categories:
        category_path = os.path.join(source_path, "images", category)
        if os.path.exists(category_path):
            files = [f for f in os.listdir(category_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            print(f"Found {len(files)} {category} images")
            
            for file in files:
                src = os.path.join(category_path, file)
                dst = os.path.join(f"{dest_path}/defective", f"defective_{defective_count+1:03d}_{category.lower()}.jpg")
                shutil.copy2(src, dst)
                defective_count += 1
                print(f"Copied defective image: {file} -> {category.lower()}")
    
    print(f"\nDataset organization complete!")
    print(f"Normal images: {len(os.listdir(f'{dest_path}/normal'))}")
    print(f"Defective images: {len(os.listdir(f'{dest_path}/defective'))}")
    
    return True

if __name__ == "__main__":
    organize_new_dataset()





