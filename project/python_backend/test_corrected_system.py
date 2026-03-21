"""
Test the corrected defect detection system
"""
import sys
import os
from defect_detection import DefectDetector
from PIL import Image

def test_system():
    print("=" * 70)
    print("TESTING CORRECTED DEFECT DETECTION SYSTEM")
    print("=" * 70)
    
    detector = DefectDetector()
    
    if not detector.model_trained:
        print("WARNING: Model not loaded! Using CV-only mode.")
    
    # Test with normal image
    normal_dir = "data/training/normal"
    if os.path.exists(normal_dir):
        normal_files = [f for f in os.listdir(normal_dir) 
                       if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if normal_files:
            test_image_path = os.path.join(normal_dir, normal_files[0])
            print(f"\n[TEST 1] Testing Normal Image: {normal_files[0]}")
            test_image = Image.open(test_image_path)
            defects = detector.detect(test_image)
            print(f"Detected Defects: {len(defects)}")
            if len(defects) == 0:
                print("PASS: Normal image correctly identified (0 defects)")
            else:
                print(f"FAIL: Found {len(defects)} false positives:")
                for d in defects:
                    print(f"  - {d['type']}: {d['confidence']:.2f} ({d['severity']})")
    
    # Test with defective image
    defective_dir = "data/training/defective"
    if os.path.exists(defective_dir):
        defective_files = [f for f in os.listdir(defective_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if defective_files:
            test_image_path = os.path.join(defective_dir, defective_files[0])
            print(f"\n[TEST 2] Testing Defective Image: {defective_files[0]}")
            test_image = Image.open(test_image_path)
            defects = detector.detect(test_image)
            print(f"Detected Defects: {len(defects)}")
            
            if len(defects) > 6:
                print(f"FAIL: Too many defects detected ({len(defects)} > 6)")
            elif len(defects) > 0:
                print(f"PASS: Defective image detected ({len(defects)} defects, max 6)")
            else:
                print("FAIL: No defects detected in defective image")
            
            print("\nDetected Defect Types:")
            for i, d in enumerate(defects, 1):
                print(f"  {i}. {d['type']}: {d['confidence']:.2f} ({d['severity']})")
    
    print("\n" + "=" * 70)
    print("KEY IMPROVEMENTS:")
    print("  - Maximum 6 defect types (one per type)")
    print("  - Duplicate removal by type")
    print("  - Stricter confidence thresholds (80% ML, 70%+ CV)")
    print("  - Image-based filtering")
    print("  - ML confidence weighting")
    print("=" * 70)

if __name__ == "__main__":
    test_system()
