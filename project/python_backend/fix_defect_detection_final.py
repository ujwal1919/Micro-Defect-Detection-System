"""
FINAL FIX: Rewrite defect_detection.py to return maximum 6 defects (one per type)
"""
import os

# Read the current file
with open('defect_detection.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the _analyze_with_cv method
old_cv_method = '''    def _analyze_with_cv(self, img_np):
        """Computer Vision analysis for specific defect types"""
        defects = []
        
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        
        # 1. SHORT CIRCUIT detection
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary)
        
        if num_labels > 2:
            areas = stats[1:, cv2.CC_STAT_AREA]
            large_components = [a for a in areas if 100 <= a <= 3000]
            
            if len(large_components) > 1:
                component_centers = []
                for i in range(1, num_labels):
                    if areas[i-1] in large_components:
                        y, x = np.where(labels == i)
                        center = (int(np.mean(x)), int(np.mean(y)))
                        component_centers.append(center)
                
                if len(component_centers) > 1:
                    min_distance = float('inf')
                    for i in range(len(component_centers)):
                        for j in range(i+1, len(component_centers)):
                            dist = np.sqrt((component_centers[i][0] - component_centers[j][0])**2 + 
                                         (component_centers[i][1] - component_centers[j][1])**2)
                            min_distance = min(min_distance, dist)
                    
                    if min_distance < 80:
                        confidence = min(0.9, 1.0 - (min_distance / 100))
                        defects.append({
                            "type": "short_circuit",
                            "confidence": confidence,
                            "severity": "Critical" if confidence > 0.7 else "Moderate"
                        })
        
        # 2. MISSING HOLE detection
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, 
                                  param1=50, param2=30, minRadius=5, maxRadius=40)
        
        if circles is not None:
            hole_centers = circles[0]
            if len(hole_centers) > 1:
                x_coords = [hole[0] for hole in hole_centers]
                x_coords.sort()
                x_spacings = np.diff(x_coords)
                
                if len(x_spacings) > 0:
                    avg_spacing = np.mean(x_spacings)
                    std_spacing = np.std(x_spacings)
                    
                    if std_spacing < 30:
                        large_gaps = [s for s in x_spacings if s > avg_spacing * 1.3]
                        if len(large_gaps) > 0:
                            confidence = min(0.8, len(large_gaps) * 0.2)
                            defects.append({
                                "type": "missing_hole",
                                "confidence": confidence,
                                "severity": "Moderate"
                            })
        
        # 3. OPEN CIRCUIT detection
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            trace_contours = [c for c in contours if 80 < cv2.contourArea(c) < 1500]
            
            if len(trace_contours) > 2:
                for i, contour1 in enumerate(trace_contours):
                    for j, contour2 in enumerate(trace_contours[i+1:], i+1):
                        M1 = cv2.moments(contour1)
                        M2 = cv2.moments(contour2)
                        
                        if M1['m00'] != 0 and M2['m00'] != 0:
                            cx1, cy1 = int(M1['m10']/M1['m00']), int(M1['m01']/M1['m00'])
                            cx2, cy2 = int(M2['m10']/M2['m00']), int(M2['m01']/M2['m00'])
                            distance = np.sqrt((cx1-cx2)**2 + (cy1-cy2)**2)
                            
                            if 15 < distance < 80:
                                confidence = min(0.8, 1.0 - (distance / 100))
                                defects.append({
                                    "type": "open_circuit",
                                    "confidence": confidence,
                                    "severity": "Critical" if confidence > 0.6 else "Moderate"
                                })
        
        # 4. MOUSE BITE detection
        if contours:
            for contour in contours:
                area = cv2.contourArea(contour)
                if 40 < area < 400:
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if 0.2 < circularity < 0.6:
                            x, y, w, h = cv2.boundingRect(contour)
                            aspect_ratio = w / h if h != 0 else 0
                            
                            if 0.1 < aspect_ratio < 6.0:
                                confidence = min(0.8, circularity * 1.2)
                                defects.append({
                                    "type": "mouse_bite",
                                    "confidence": confidence,
                                    "severity": "Moderate"
                                })
        
        # 5. SPUR detection
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40, minLineLength=25, maxLineGap=8)
        
        if lines is not None:
            short_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                if 8 < length < 40:
                    short_lines.append(line[0])
            
            if len(short_lines) > 1:
                confidence = min(0.8, len(short_lines) / 8)
                defects.append({
                    "type": "spur",
                    "confidence": confidence,
                    "severity": "Moderate"
                })
        
        # 6. SPURIOUS COPPER detection
        bright_spots = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)[1]
        bright_contours, _ = cv2.findContours(bright_spots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if bright_contours:
            spurious_contours = []
            for contour in bright_contours:
                area = cv2.contourArea(contour)
                if 25 < area < 250:
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if circularity > 0.4:
                            spurious_contours.append(contour)
            
            if len(spurious_contours) > 0:
                total_area = sum(cv2.contourArea(c) for c in spurious_contours)
                if total_area > 80:
                    confidence = min(0.8, total_area / 400)
                    defects.append({
                        "type": "spurious_copper",
                        "confidence": confidence,
                        "severity": "Moderate"
                    })
        
        return defects'''

new_cv_method = '''    def _analyze_with_cv(self, img_np):
        """Computer Vision analysis - Returns ONE defect per type (max 6 total)"""
        defects = []
        
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 1. SHORT CIRCUIT detection - ONE only
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary)
        
        if num_labels > 2:
            areas = stats[1:, cv2.CC_STAT_AREA]
            large_components = [a for a in areas if 100 <= a <= 3000]
            
            if len(large_components) > 1:
                component_centers = []
                for i in range(1, num_labels):
                    if areas[i-1] in large_components:
                        y, x = np.where(labels == i)
                        center = (int(np.mean(x)), int(np.mean(y)))
                        component_centers.append(center)
                
                if len(component_centers) > 1:
                    min_distance = float('inf')
                    for i in range(len(component_centers)):
                        for j in range(i+1, len(component_centers)):
                            dist = np.sqrt((component_centers[i][0] - component_centers[j][0])**2 + 
                                         (component_centers[i][1] - component_centers[j][1])**2)
                            min_distance = min(min_distance, dist)
                    
                    if min_distance < 70:  # Stricter
                        confidence = min(0.9, 1.0 - (min_distance / 90))
                        if confidence > 0.75:  # Only if high confidence
                            defects.append({
                                "type": "short_circuit",
                                "confidence": confidence,
                                "severity": "Critical" if confidence > 0.8 else "Moderate"
                            })
        
        # 2. MISSING HOLE detection - ONE only
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, 
                                  param1=50, param2=30, minRadius=5, maxRadius=40)
        
        if circles is not None and len(circles[0]) > 2:
            hole_centers = circles[0]
            x_coords = [hole[0] for hole in hole_centers]
            x_coords.sort()
            x_spacings = np.diff(x_coords)
            
            if len(x_spacings) > 0:
                avg_spacing = np.mean(x_spacings)
                std_spacing = np.std(x_spacings)
                
                if std_spacing < 25:  # Stricter
                    large_gaps = [s for s in x_spacings if s > avg_spacing * 1.5]
                    if len(large_gaps) >= 2:  # Need 2+ gaps
                        confidence = min(0.85, len(large_gaps) * 0.15)
                        if confidence > 0.70:  # Only if high confidence
                            defects.append({
                                "type": "missing_hole",
                                "confidence": confidence,
                                "severity": "Moderate"
                            })
        
        # 3. OPEN CIRCUIT detection - ONE only (combine all gaps)
        if contours:
            trace_contours = [c for c in contours if 100 < cv2.contourArea(c) < 1500]
            
            if len(trace_contours) > 3:
                gap_distances = []
                for i, contour1 in enumerate(trace_contours):
                    for j, contour2 in enumerate(trace_contours[i+1:], i+1):
                        M1 = cv2.moments(contour1)
                        M2 = cv2.moments(contour2)
                        
                        if M1['m00'] != 0 and M2['m00'] != 0:
                            cx1, cy1 = int(M1['m10']/M1['m00']), int(M1['m01']/M1['m00'])
                            cx2, cy2 = int(M2['m10']/M2['m00']), int(M2['m01']/M2['m00'])
                            distance = np.sqrt((cx1-cx2)**2 + (cy1-cy2)**2)
                            
                            if 20 < distance < 70:
                                gap_distances.append(distance)
                
                if len(gap_distances) >= 3:  # Need 3+ gaps
                    avg_gap = np.mean(sorted(gap_distances)[:5])  # Top 5 gaps
                    confidence = min(0.85, 1.0 - (avg_gap / 80))
                    if confidence > 0.70:  # Only if high confidence
                        defects.append({
                            "type": "open_circuit",
                            "confidence": confidence,
                            "severity": "Critical" if confidence > 0.75 else "Moderate"
                        })
        
        # 4. MOUSE BITE detection - ONE only (combine all contours)
        if contours:
            mouse_bite_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if 50 < area < 350:
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if 0.25 < circularity < 0.55:
                            x, y, w, h = cv2.boundingRect(contour)
                            aspect_ratio = w / h if h != 0 else 0
                            if 0.2 < aspect_ratio < 5.0:
                                mouse_bite_contours.append(contour)
            
            if len(mouse_bite_contours) >= 3:  # Need 3+ contours
                confidence = min(0.8, 0.5 + (len(mouse_bite_contours) * 0.05))
                if confidence > 0.70:  # Only if high confidence
                    defects.append({
                        "type": "mouse_bite",
                        "confidence": confidence,
                        "severity": "Moderate"
                    })
        
        # 5. SPUR detection - ONE only
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=30, maxLineGap=6)
        
        if lines is not None:
            short_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                if 10 < length < 35:
                    short_lines.append(line[0])
            
            if len(short_lines) >= 3:  # Need 3+ short lines
                confidence = min(0.8, len(short_lines) / 10)
                if confidence > 0.70:  # Only if high confidence
                    defects.append({
                        "type": "spur",
                        "confidence": confidence,
                        "severity": "Moderate"
                    })
        
        # 6. SPURIOUS COPPER detection - ONE only (combine all spots)
        bright_spots = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)[1]
        bright_contours, _ = cv2.findContours(bright_spots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if bright_contours:
            spurious_contours = []
            for contour in bright_contours:
                area = cv2.contourArea(contour)
                if 30 < area < 200:
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if circularity > 0.5:
                            spurious_contours.append(contour)
            
            if len(spurious_contours) >= 2:  # Need 2+ spots
                total_area = sum(cv2.contourArea(c) for c in spurious_contours)
                if total_area > 100:
                    confidence = min(0.8, total_area / 500)
                    if confidence > 0.70:  # Only if high confidence
                        defects.append({
                            "type": "spurious_copper",
                            "confidence": confidence,
                            "severity": "Moderate"
                        })
        
        return defects'''

# Replace the method
if old_cv_method in content:
    content = content.replace(old_cv_method, new_cv_method)
    
    # Also fix the _smart_filtering method to ensure max 6
    old_filtering = '''        # Maximum 6 defect types (one per type) - this should now be enforced
        if len(filtered_defects) > 6:
            filtered_defects = filtered_defects[:6]
        
        return filtered_defects'''
    
    new_filtering = '''        # Maximum 6 defect types (one per type) - ENFORCE STRICTLY
        # Already filtered to one per type above, but double-check and limit to 6
        filtered_defects.sort(key=lambda x: x["confidence"], reverse=True)
        if len(filtered_defects) > 6:
            filtered_defects = filtered_defects[:6]
        
        return filtered_defects'''
    
    if old_filtering in content:
        content = content.replace(old_filtering, new_filtering)
    
    # Save the fixed file
    with open('defect_detection.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Fixed defect_detection.py - now returns max 6 defects (one per type)")
else:
    print("WARNING: Could not find old method. Writing complete fixed file...")
    # Write complete fixed file
    fixed_content = '''import torch
import torchvision.transforms as transforms
from PIL import Image
import torchvision.models as models
import torch.nn as nn
import numpy as np
import cv2

class DefectDetector:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Load the trained model
        self.model_trained = False
        try:
            self.model = self._create_model()
            state_dict = torch.load('quick_trained_model.pth', map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.eval()
            self.model_trained = True
            print("Perfect trained model loaded successfully!")
        except Exception as e:
            print(f"Model loading failed: {e}")
            print("Using computer vision only mode")
            self.model_trained = False
    
    def _create_model(self):
        class PerfectBinaryModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.backbone = models.resnet18(weights='IMAGENET1K_V1')
                self.backbone.fc = nn.Linear(512, 2)
            
            def forward(self, x):
                return self.backbone(x)
        return PerfectBinaryModel()
    
    def detect(self, image):
        """PERFECT ACCURATE defect detection - Maximum 6 defect types"""
        defects = []
        
        # Convert PIL to numpy for CV processing
        img_np = np.array(image)
        
        # ML Analysis - PRIMARY METHOD (most accurate)
        ml_result = None
        ml_confidence = 0.0
        if self.model_trained:
            ml_result, ml_confidence = self._analyze_with_ml(image)
        
        # If ML says normal with high confidence, return empty (no defects)
        if ml_result == "normal" and ml_confidence > 0.8:
            return []
        
        # If ML says defective or uncertain, use CV to find specific defect types
        if ml_result == "defective" or ml_result == "uncertain":
            cv_defects = self._analyze_with_cv(img_np)
            
            # Apply ML confidence weighting to CV defects
            if ml_result == "defective":
                for defect in cv_defects:
                    defect["confidence"] = defect["confidence"] * ml_confidence
            
            # Smart filtering - remove duplicates, limit to 6 types
            defects = self._smart_filtering(cv_defects, img_np, ml_confidence)
        
        # If model not trained, use CV only (fallback) - be very strict
        if not self.model_trained:
            cv_defects = self._analyze_with_cv(img_np)
            defects = self._smart_filtering(cv_defects, img_np, 0.5)
            defects = [d for d in defects if d["confidence"] > 0.75]
        
        # Final safety check: Maximum 6 defect types
        if len(defects) > 6:
            defects.sort(key=lambda x: x["confidence"], reverse=True)
            defects = defects[:6]
        
        return defects
    
    def _analyze_with_ml(self, image):
        """ML-based binary classification: Normal vs Defective"""
        try:
            # Ensure image is RGB (3 channels)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                
                normal_prob = float(probabilities[0][0])
                defective_prob = float(probabilities[0][1])
                
                # Higher confidence threshold for accuracy (80% instead of 70%)
                if defective_prob > 0.8:  # 80% confidence threshold - more strict
                    return "defective", defective_prob
                elif normal_prob > 0.8:  # 80% confidence threshold - more strict
                    return "normal", normal_prob
                else:
                    # Low confidence - use CV as backup with lower weight
                    return "uncertain", max(normal_prob, defective_prob)
        
        except Exception as e:
            print(f"ML analysis failed: {e}")
            return None, 0.0
    
    def _analyze_with_cv(self, img_np):
        """Computer Vision analysis - Returns ONE defect per type (max 6 total)"""
        defects = []
        
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 1. SHORT CIRCUIT detection - ONE only
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary)
        
        if num_labels > 2:
            areas = stats[1:, cv2.CC_STAT_AREA]
            large_components = [a for a in areas if 100 <= a <= 3000]
            
            if len(large_components) > 1:
                component_centers = []
                for i in range(1, num_labels):
                    if areas[i-1] in large_components:
                        y, x = np.where(labels == i)
                        center = (int(np.mean(x)), int(np.mean(y)))
                        component_centers.append(center)
                
                if len(component_centers) > 1:
                    min_distance = float('inf')
                    for i in range(len(component_centers)):
                        for j in range(i+1, len(component_centers)):
                            dist = np.sqrt((component_centers[i][0] - component_centers[j][0])**2 + 
                                         (component_centers[i][1] - component_centers[j][1])**2)
                            min_distance = min(min_distance, dist)
                    
                    if min_distance < 70:  # Stricter
                        confidence = min(0.9, 1.0 - (min_distance / 90))
                        if confidence > 0.75:  # Only if high confidence
                            defects.append({
                                "type": "short_circuit",
                                "confidence": confidence,
                                "severity": "Critical" if confidence > 0.8 else "Moderate"
                            })
        
        # 2. MISSING HOLE detection - ONE only
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, 
                                  param1=50, param2=30, minRadius=5, maxRadius=40)
        
        if circles is not None and len(circles[0]) > 2:
            hole_centers = circles[0]
            x_coords = [hole[0] for hole in hole_centers]
            x_coords.sort()
            x_spacings = np.diff(x_coords)
            
            if len(x_spacings) > 0:
                avg_spacing = np.mean(x_spacings)
                std_spacing = np.std(x_spacings)
                
                if std_spacing < 25:  # Stricter
                    large_gaps = [s for s in x_spacings if s > avg_spacing * 1.5]
                    if len(large_gaps) >= 2:  # Need 2+ gaps
                        confidence = min(0.85, len(large_gaps) * 0.15)
                        if confidence > 0.70:  # Only if high confidence
                            defects.append({
                                "type": "missing_hole",
                                "confidence": confidence,
                                "severity": "Moderate"
                            })
        
        # 3. OPEN CIRCUIT detection - ONE only (combine all gaps)
        if contours:
            trace_contours = [c for c in contours if 100 < cv2.contourArea(c) < 1500]
            
            if len(trace_contours) > 3:
                gap_distances = []
                for i, contour1 in enumerate(trace_contours):
                    for j, contour2 in enumerate(trace_contours[i+1:], i+1):
                        M1 = cv2.moments(contour1)
                        M2 = cv2.moments(contour2)
                        
                        if M1['m00'] != 0 and M2['m00'] != 0:
                            cx1, cy1 = int(M1['m10']/M1['m00']), int(M1['m01']/M1['m00'])
                            cx2, cy2 = int(M2['m10']/M2['m00']), int(M2['m01']/M2['m00'])
                            distance = np.sqrt((cx1-cx2)**2 + (cy1-cy2)**2)
                            
                            if 20 < distance < 70:
                                gap_distances.append(distance)
                
                if len(gap_distances) >= 3:  # Need 3+ gaps
                    avg_gap = np.mean(sorted(gap_distances)[:5])  # Top 5 gaps
                    confidence = min(0.85, 1.0 - (avg_gap / 80))
                    if confidence > 0.70:  # Only if high confidence
                        defects.append({
                            "type": "open_circuit",
                            "confidence": confidence,
                            "severity": "Critical" if confidence > 0.75 else "Moderate"
                        })
        
        # 4. MOUSE BITE detection - ONE only (combine all contours)
        if contours:
            mouse_bite_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if 50 < area < 350:
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if 0.25 < circularity < 0.55:
                            x, y, w, h = cv2.boundingRect(contour)
                            aspect_ratio = w / h if h != 0 else 0
                            if 0.2 < aspect_ratio < 5.0:
                                mouse_bite_contours.append(contour)
            
            if len(mouse_bite_contours) >= 3:  # Need 3+ contours
                confidence = min(0.8, 0.5 + (len(mouse_bite_contours) * 0.05))
                if confidence > 0.70:  # Only if high confidence
                    defects.append({
                        "type": "mouse_bite",
                        "confidence": confidence,
                        "severity": "Moderate"
                    })
        
        # 5. SPUR detection - ONE only
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=30, maxLineGap=6)
        
        if lines is not None:
            short_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                if 10 < length < 35:
                    short_lines.append(line[0])
            
            if len(short_lines) >= 3:  # Need 3+ short lines
                confidence = min(0.8, len(short_lines) / 10)
                if confidence > 0.70:  # Only if high confidence
                    defects.append({
                        "type": "spur",
                        "confidence": confidence,
                        "severity": "Moderate"
                    })
        
        # 6. SPURIOUS COPPER detection - ONE only (combine all spots)
        bright_spots = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)[1]
        bright_contours, _ = cv2.findContours(bright_spots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if bright_contours:
            spurious_contours = []
            for contour in bright_contours:
                area = cv2.contourArea(contour)
                if 30 < area < 200:
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if circularity > 0.5:
                            spurious_contours.append(contour)
            
            if len(spurious_contours) >= 2:  # Need 2+ spots
                total_area = sum(cv2.contourArea(c) for c in spurious_contours)
                if total_area > 100:
                    confidence = min(0.8, total_area / 500)
                    if confidence > 0.70:  # Only if high confidence
                        defects.append({
                            "type": "spurious_copper",
                            "confidence": confidence,
                            "severity": "Moderate"
                        })
        
        return defects
    
    def _smart_filtering(self, all_defects, img_np, ml_confidence):
        """Smart filtering: Remove duplicates, apply confidence thresholds, limit to 6 types"""
        if not all_defects:
            return []
        
        # Step 1: Remove duplicates by type - keep only the best (highest confidence) of each type
        defect_groups = {}
        for defect in all_defects:
            defect_type = defect["type"]
            if defect_type not in defect_groups:
                defect_groups[defect_type] = []
            defect_groups[defect_type].append(defect)
        
        # Keep only the best defect of each type
        unique_defects = []
        for defect_type, defects in defect_groups.items():
            best_defect = max(defects, key=lambda x: x["confidence"])
            unique_defects.append(best_defect)
        
        # Step 2: Apply image-based filtering
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # Adjust confidence threshold based on image characteristics
        if ml_confidence < 0.5:
            ml_confidence = 0.5  # Minimum weight
        
        if edge_density < 0.08:  # Very few edges - likely normal image
            min_confidence = max(0.80, 0.85 * ml_confidence)  # Very strict, minimum 0.80
        elif edge_density > 0.35:  # Very many edges - might be noisy
            min_confidence = max(0.75, 0.80 * ml_confidence)  # Strict, minimum 0.75
        else:
            min_confidence = max(0.70, 0.70 * ml_confidence)  # Moderate, minimum 0.70
        
        # Apply minimum confidence threshold
        filtered_defects = [d for d in unique_defects if d["confidence"] >= min_confidence]
        
        # Step 3: Sort by confidence and limit to maximum 6 types
        filtered_defects.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Maximum 6 defect types (one per type) - ENFORCE STRICTLY
        if len(filtered_defects) > 6:
            filtered_defects = filtered_defects[:6]
        
        return filtered_defects'''
    
    with open('defect_detection.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    print("SUCCESS: Wrote complete fixed defect_detection.py")
