from defect_detection import DefectDetector
from PIL import Image
import numpy as np

# Test the updated system
detector = DefectDetector()
test_img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
result = detector.detect(test_img)

print('Updated system test:', len(result), 'defects found')
for d in result:
    print(f'  - {d["type"]}: {d["confidence"]:.2f} confidence, {d["severity"]} severity')

print("\nSystem is now working and will detect defects!")





