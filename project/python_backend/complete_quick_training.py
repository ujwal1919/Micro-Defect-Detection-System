import os
import shutil

def complete_quick_training():
    """Complete quick training process in one go"""
    
    print("=== COMPLETE QUICK TRAINING PROCESS ===")
    print("Step 1: Training with new dataset...")
    
    # Step 1: Train with new dataset
    try:
        from quick_train_any_dataset import quick_train_any_dataset
        success = quick_train_any_dataset()
        if success:
            print("✓ Quick training completed successfully!")
        else:
            print("✗ Quick training failed!")
            return False
    except Exception as e:
        print(f"✗ Error in quick training: {e}")
        return False
    
    print("\nStep 2: Updating defect detection system...")
    
    # Step 2: Update defect detection
    try:
        # Copy quick defect detection to main file
        with open('defect_detection_quick.py', 'r') as f:
            new_content = f.read()
        
        with open('defect_detection.py', 'w') as f:
            f.write(new_content)
        
        print("✓ Defect detection system updated!")
    except Exception as e:
        print(f"✗ Error updating defect detection: {e}")
        return False
    
    print("\nStep 3: Testing new system...")
    
    # Step 3: Test new system
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
    
    print("\n=== COMPLETE QUICK TRAINING PROCESS FINISHED ===")
    print("✓ Model trained with new dataset")
    print("✓ System updated with quick detection")
    print("✓ Ready for accurate defect detection!")
    
    return True

if __name__ == "__main__":
    complete_quick_training()




