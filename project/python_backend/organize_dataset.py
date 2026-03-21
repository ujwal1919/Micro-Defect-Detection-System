import os
import shutil
from PIL import Image
import logging
import re

logger = logging.getLogger(__name__)

class DatasetOrganizer:
    def __init__(self, source_dir, target_dir="data/training"):
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.defect_types = [
            "short_circuit",
            "trace_width_variation", 
            "surface_contamination",
            "layer_misalignment",
            "component_damage",
            "normal"
        ]
        
        # Create target directories
        for defect_type in self.defect_types:
            os.makedirs(os.path.join(target_dir, defect_type), exist_ok=True)
    
    def organize_by_filename(self):
        """Organize images based on filename patterns"""
        logger.info("Organizing dataset by filename patterns...")
        
        # Define filename patterns for each defect type
        patterns = {
            "short_circuit": [r"short", r"circuit", r"bridge"],
            "trace_width_variation": [r"trace", r"width", r"variation", r"thin", r"thick"],
            "surface_contamination": [r"contamination", r"dirt", r"stain", r"foreign"],
            "layer_misalignment": [r"misalignment", r"offset", r"shift", r"layer"],
            "component_damage": [r"damage", r"broken", r"crack", r"missing"],
            "normal": [r"normal", r"good", r"ok", r"clean", r"perfect"]
        }
        
        moved_count = 0
        skipped_count = 0
        
        for filename in os.listdir(self.source_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                source_path = os.path.join(self.source_dir, filename)
                
                # Check which defect type this image belongs to
                assigned = False
                filename_lower = filename.lower()
                
                for defect_type, pattern_list in patterns.items():
                    for pattern in pattern_list:
                        if re.search(pattern, filename_lower):
                            target_path = os.path.join(self.target_dir, defect_type, filename)
                            shutil.copy2(source_path, target_path)
                            logger.info(f"Moved {filename} to {defect_type}/")
                            moved_count += 1
                            assigned = True
                            break
                    if assigned:
                        break
                
                if not assigned:
                    logger.warning(f"Could not categorize {filename} - skipping")
                    skipped_count += 1
        
        logger.info(f"Organization complete: {moved_count} images moved, {skipped_count} skipped")
        return moved_count, skipped_count
    
    def organize_by_existing_structure(self):
        """Organize images if they're already in defect-type folders"""
        logger.info("Organizing dataset by existing folder structure...")
        
        moved_count = 0
        
        for defect_type in self.defect_types:
            source_folder = os.path.join(self.source_dir, defect_type)
            if os.path.exists(source_folder):
                target_folder = os.path.join(self.target_dir, defect_type)
                
                for filename in os.listdir(source_folder):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        source_path = os.path.join(source_folder, filename)
                        target_path = os.path.join(target_folder, filename)
                        shutil.copy2(source_path, target_path)
                        moved_count += 1
                        logger.info(f"Copied {filename} to {defect_type}/")
        
        logger.info(f"Organization complete: {moved_count} images copied")
        return moved_count
    
    def organize_manually(self, image_mapping):
        """Organize images based on manual mapping"""
        logger.info("Organizing dataset with manual mapping...")
        
        moved_count = 0
        
        for filename, defect_type in image_mapping.items():
            if defect_type in self.defect_types:
                source_path = os.path.join(self.source_dir, filename)
                target_path = os.path.join(self.target_dir, defect_type, filename)
                
                if os.path.exists(source_path):
                    shutil.copy2(source_path, target_path)
                    moved_count += 1
                    logger.info(f"Moved {filename} to {defect_type}/")
        
        logger.info(f"Organization complete: {moved_count} images moved")
        return moved_count
    
    def validate_images(self):
        """Validate all images in the organized dataset"""
        logger.info("Validating organized dataset...")
        
        total_images = 0
        valid_images = 0
        invalid_images = []
        
        for defect_type in self.defect_types:
            folder_path = os.path.join(self.target_dir, defect_type)
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        total_images += 1
                        try:
                            img_path = os.path.join(folder_path, filename)
                            with Image.open(img_path) as img:
                                img.verify()
                            valid_images += 1
                        except Exception as e:
                            invalid_images.append((filename, str(e)))
        
        logger.info(f"Validation complete: {valid_images}/{total_images} images are valid")
        if invalid_images:
            logger.warning(f"Invalid images: {invalid_images}")
        
        return valid_images, total_images, invalid_images
    
    def show_dataset_summary(self):
        """Show summary of organized dataset"""
        logger.info("Dataset Summary:")
        
        total_images = 0
        for defect_type in self.defect_types:
            folder_path = os.path.join(self.target_dir, defect_type)
            if os.path.exists(folder_path):
                count = len([f for f in os.listdir(folder_path) 
                           if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                logger.info(f"  {defect_type}: {count} images")
                total_images += count
        
        logger.info(f"  Total: {total_images} images")
        return total_images

def main():
    logging.basicConfig(level=logging.INFO)
    
    print("PCB Dataset Organizer")
    print("=" * 50)
    
    # Get source directory from user
    source_dir = input("Enter the path to your dataset folder: ").strip()
    
    if not os.path.exists(source_dir):
        print(f"Error: Directory '{source_dir}' does not exist!")
        return
    
    organizer = DatasetOrganizer(source_dir)
    
    print("\nHow is your dataset organized?")
    print("1. Images are already in folders by defect type")
    print("2. All images are in one folder with descriptive filenames")
    print("3. All images are in one folder (I'll help categorize)")
    
    choice = input("Enter your choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        organizer.organize_by_existing_structure()
    elif choice == "2":
        organizer.organize_by_filename()
    elif choice == "3":
        print("\nLet me scan your images first...")
        images = [f for f in os.listdir(source_dir) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"\nFound {len(images)} images:")
        for i, img in enumerate(images[:10]):  # Show first 10
            print(f"{i+1}. {img}")
        if len(images) > 10:
            print(f"... and {len(images)-10} more")
        
        print("\nFor each image, I'll try to categorize it automatically.")
        print("You can review and move images manually if needed.")
        organizer.organize_by_filename()
    else:
        print("Invalid choice!")
        return
    
    # Validate and show summary
    organizer.validate_images()
    organizer.show_dataset_summary()
    
    print("\nDataset organization complete!")
    print("You can now run: python train_model.py")

if __name__ == "__main__":
    main()





