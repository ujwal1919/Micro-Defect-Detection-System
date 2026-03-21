"""
Test the perfect accuracy fix - Normal images should show 0 defects
"""
import sys
import os
from defect_detection import DefectDetector
from PIL import Image

def test_perfect_accuracy():
    print("=" * 70)
    print("TESTING PERFECT ACCURACY - Normal = 0 defects, Defective = real defects")
    print("=" * 70)
    
    detector = DefectDetector()
    
    # Test with multiple normal images
    normal_dir = "data/training/normal"
    if os.path.exists(normal_dir):
        normal_files = [f for f in os.listdir(normal_dir) 
                       if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:5]  # Test 5 images
        
        print(f"\n[TEST 1] Testing {len(normal_files)} Normal Images:")
        normal_passed = 0
        normal_failed = 0
        
        for normal_file in normal_files:
            test_image_path = os.path.join(normal_dir, normal_file)
            try:
                test_image = Image.open(test_image_path)
                if test_image.mode != 'RGB':
                    test_image = test_image.convert('RGB')
                defects = detector.detect(test_image)
                if len(defects) == 0:
                    normal_passed += 1
                    print(f"  PASS: {normal_file} - 0 defects")
                else:
                    normal_failed += 1
                    print(f"  FAIL: {normal_file} - {len(defects)} false positives")
                    for d in defects:
                        print(f"    - {d['type']}: {d['confidence']:.2f}")
            except Exception as e:
                print(f"  ERROR: {normal_file} - {e}")
        
        print(f"\nNormal Images: {normal_passed} passed, {normal_failed} failed")
    
    # Test with defective images
    defective_dir = "data/training/defective"
    if os.path.exists(defective_dir):
        defective_files = [f for f in os.listdir(defective_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:3]  # Test 3 images
        
        print(f"\n[TEST 2] Testing {len(defective_files)} Defective Images:")
        defective_passed = 0
        defective_failed = 0
        
        for defective_file in defective_files:
            test_image_path = os.path.join(defective_dir, defective_file)
            try:
                test_image = Image.open(test_image_path)
                if test_image.mode != 'RGB':
                    test_image = test_image.convert('RGB')
                defects = detector.detect(test_image)
                if len(defects) > 0:
                    defective_passed += 1
                    print(f"  PASS: {defective_file} - {len(defects)} defects detected")
                    for i, d in enumerate(defects, 1):
                        print(f"    {i}. {d['type']}: {d['confidence']:.2f} ({d['severity']})")
                else:
                    defective_failed += 1
                    print(f"  FAIL: {defective_file} - No defects detected")
            except Exception as e:
                print(f"  ERROR: {defective_file} - {e}")
        
        print(f"\nDefective Images: {defective_passed} passed, {defective_failed} failed")
    
    print("\n" + "=" * 70)
    print("PERFECT ACCURACY TEST COMPLETED!")
    print("=" * 70)
    print("\nExpected Results:")
    print("  - Normal images: 0 defects (100% should pass)")
    print("  - Defective images: 1-6 defects (should detect real defects)")
    print("=" * 70)

if __name__ == "__main__":
    test_perfect_accuracy()
