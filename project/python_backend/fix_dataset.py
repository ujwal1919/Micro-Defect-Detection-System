import os
import shutil
from PIL import Image
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def organize_deeppcb_dataset_v2():
    """Automatically organize DeepPCB dataset into 'normal' and 'defective' categories."""

    # Your dataset path
    source_dir = r"C:\Users\Ujwal Gowda KR\Downloads\DeepPCB-master\DeepPCB-master"

    # Target training directory
    target_dir = "data/training"

    # Ensure target directories exist
    normal_target_dir = os.path.join(target_dir, 'normal')
    defective_target_dir = os.path.join(target_dir, 'defective')
    os.makedirs(normal_target_dir, exist_ok=True)
    os.makedirs(defective_target_dir, exist_ok=True)

    print("PCB DeepPCB Dataset Organizer (v2)")
    print("=" * 50)

    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Dataset directory not found at: {source_dir}")
        print("Please ensure the path is correct.")
        return False

    total_images_processed = 0
    normal_images_count = 0
    defective_images_count = 0
    invalid_images_count = 0

    # DeepPCB structure:
    # DeepPCB-master/
    # ├── test_images/
    # │   ├── 08010001_test.jpg
    # │   ├── ...
    # ├── template_images/
    # │   ├── 08010001_temp.jpg
    # │   ├── ...
    # └── defect_labels/
    #     ├── 08010001_label.png (binary mask for defects)
    #     ├── ...

    template_images_path = os.path.join(source_dir, 'template_images')
    test_images_path = os.path.join(source_dir, 'test_images')
    defect_labels_path = os.path.join(source_dir, 'defect_labels')

    if not (os.path.exists(template_images_path) and
            os.path.exists(test_images_path) and
            os.path.exists(defect_labels_path)):
        print(f"Error: DeepPCB expected subdirectories (template_images, test_images, defect_labels) not found in {source_dir}")
        print("Please ensure the DeepPCB dataset structure is correct.")
        return False

    print(f"Processing images from: {source_dir}")

    # Process template images as 'normal'
    for img_file in os.listdir(template_images_path):
        if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            src_path = os.path.join(template_images_path, img_file)
            dest_path = os.path.join(normal_target_dir, img_file)
            try:
                Image.open(src_path).verify() # Verify image integrity
                shutil.copy(src_path, dest_path)
                normal_images_count += 1
                total_images_processed += 1
            except Exception as e:
                logger.warning(f"Skipping invalid image {img_file}: {e}")
                invalid_images_count += 1

    # Process test images based on defect labels
    for img_file in os.listdir(test_images_path):
        if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            base_name = img_file.replace('_test.jpg', '')
            label_file = f"{base_name}_label.png"
            label_path = os.path.join(defect_labels_path, label_file)

            src_path = os.path.join(test_images_path, img_file)

            try:
                Image.open(src_path).verify() # Verify image integrity
                if os.path.exists(label_path):
                    # Check if the label image contains any white pixels (defects)
                    label_img = Image.open(label_path).convert('L')
                    if label_img.getbbox(): # If bounding box exists, there are non-black pixels
                        dest_path = os.path.join(defective_target_dir, img_file)
                        shutil.copy(src_path, dest_path)
                        defective_images_count += 1
                    else:
                        # No defects found in label, treat as normal
                        dest_path = os.path.join(normal_target_dir, img_file)
                        shutil.copy(src_path, dest_path)
                        normal_images_count += 1
                else:
                    # No label file, treat as normal (or log as unknown)
                    dest_path = os.path.join(normal_target_dir, img_file)
                    shutil.copy(src_path, dest_path)
                    normal_images_count += 1
                total_images_processed += 1
            except Exception as e:
                logger.warning(f"Skipping invalid image {img_file}: {e}")
                invalid_images_count += 1

    print("\nDataset Organization Complete!")
    print("=" * 50)
    print(f"Total images processed: {total_images_processed}")
    print(f"Normal images: {normal_images_count}")
    print(f"Defective images: {defective_images_count}")
    print(f"Invalid images skipped: {invalid_images_count}")
    print(f"Dataset organized into: {target_dir}")
    print("Ready for training!")
    
    return defective_images_count > 0

if __name__ == "__main__":
    organize_deeppcb_dataset_v2()
