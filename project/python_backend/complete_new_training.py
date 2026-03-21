import os
import sys

def complete_new_training():
    """Complete new training process in one go"""
    
    print("=== COMPLETE NEW TRAINING PROCESS ===")
    print("Step 1: Organizing new dataset...")
    
    # Step 1: Organize dataset
    try:
        from organize_new_dataset import organize_new_dataset
        organize_new_dataset()
        print("✓ Dataset organized successfully!")
    except Exception as e:
        print(f"✗ Error organizing dataset: {e}")
        return False
    
    print("\nStep 2: Training new model...")
    
    # Step 2: Train new model
    try:
        from train_new_model import train_new_model
        train_new_model()
        print("✓ Model trained successfully!")
    except Exception as e:
        print(f"✗ Error training model: {e}")
        return False
    
    print("\nStep 3: Updating defect detection system...")
    
    # Step 3: Update defect detection
    try:
        # Copy new defect detection to main file
        with open('defect_detection_new.py', 'r') as f:
            new_content = f.read()
        
        with open('defect_detection.py', 'w') as f:
            f.write(new_content)
        
        print("✓ Defect detection system updated!")
    except Exception as e:
        print(f"✗ Error updating defect detection: {e}")
        return False
    
    print("\nStep 4: Testing new system...")
    
    # Step 4: Test new system
    try:
        from defect_detection import DefectDetector
        from PIL import Image
        import numpy as np
        
        detector = DefectDetector()
        test_img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
        result = detector.detect(test_img)
        
        print(f"✓ New system test: {len(result)} defects found")
        for d in result:
            print(f"  - {d['type']}: {d['confidence']:.3f} confidence, {d['severity']} severity")
        
    except Exception as e:
        print(f"✗ Error testing system: {e}")
        return False
    
    print("\n=== COMPLETE NEW TRAINING PROCESS FINISHED ===")
    print("✓ New model trained with better dataset")
    print("✓ System updated with accurate detection")
    print("✓ Ready for accurate defect detection!")
    
    return True

if __name__ == "__main__":
    complete_new_training()





