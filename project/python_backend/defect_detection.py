import torch
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
        """PERFECT BALANCED detection - Normal = 0 defects, Defective = real defects"""
        # Ensure image is RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert PIL to numpy for CV processing
        img_np = np.array(image)
        
        # ML Analysis - PRIMARY METHOD
        ml_result = None
        ml_confidence = 0.0
        normal_prob = 0.0
        defective_prob = 0.0
        
        if self.model_trained:
            try:
                ml_result, ml_confidence, normal_prob, defective_prob = self._analyze_with_ml(image)
            except Exception as e:
                print(f"ML analysis error: {e}")
                ml_result = None
                normal_prob = 0.5
                defective_prob = 0.5
        
        # STRATEGY 1: If ML says normal with high confidence (85%+), trust it - return 0 defects
        if ml_result == "normal" and ml_confidence > 0.85:
            return []  # No defects for normal images
        
        # STRATEGY 2: If ML says normal with medium confidence, still trust it if normal_prob > defective_prob
        if ml_result == "normal":
            if normal_prob > defective_prob + 0.10:  # 10% margin
                return []  # Trust normal, return 0 defects
        
        # STRATEGY 3: If ML says defective (75%+ confidence), use CV to find specific defects
        if ml_result == "defective" and ml_confidence > 0.75:
            cv_defects = self._analyze_with_cv(img_np)
            
            # Apply ML confidence weighting
            for defect in cv_defects:
                defect["confidence"] = defect["confidence"] * ml_confidence
            
            # Balanced filtering - less strict when ML is confident
            defects = self._balanced_filtering(cv_defects, img_np, ml_confidence, is_defective=True)
            return defects
        
        # STRATEGY 4: If ML is uncertain, check probabilities carefully
        if ml_result == "uncertain" or ml_result is None:
            # If normal_prob significantly higher, it's likely normal
            if normal_prob > defective_prob + 0.15:
                return []  # Trust normal, return 0 defects
            
            # If defective_prob is higher, check with CV (but be strict)
            elif defective_prob > normal_prob + 0.10:
                cv_defects = self._analyze_with_cv(img_np)
                # More strict for uncertain cases
                defects = self._balanced_filtering(cv_defects, img_np, max(ml_confidence, 0.6), is_defective=False)
                defects = [d for d in defects if d["confidence"] > 0.75]  # Strict for uncertain
                return defects
            else:
                # Very close probabilities - default to normal to avoid false positives
                return []  # Default to normal if truly uncertain
        
        # If model not trained, use CV only but be strict
        if not self.model_trained:
            cv_defects = self._analyze_with_cv(img_np)
            defects = self._balanced_filtering(cv_defects, img_np, 0.5, is_defective=False)
            defects = [d for d in defects if d["confidence"] > 0.75]
            return defects
        
        # Default: return empty (no defects)
        return []
    
    def _analyze_with_ml(self, image):
        """ML-based binary classification: Normal vs Defective"""
        try:
            # Ensure image is RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                
                normal_prob = float(probabilities[0][0])
                defective_prob = float(probabilities[0][1])
                
                # BALANCED thresholds: 85% for normal (strict), 75% for defective (balanced)
                if normal_prob > 0.85:  # 85% for normal - strict to avoid false positives
                    return "normal", normal_prob, normal_prob, defective_prob
                elif defective_prob > 0.75:  # 75% for defective - balanced to detect defects
                    return "defective", defective_prob, normal_prob, defective_prob
                else:
                    # Low confidence - uncertain
                    return "uncertain", max(normal_prob, defective_prob), normal_prob, defective_prob
        
        except Exception as e:
            print(f"ML analysis failed: {e}")
            return None, 0.0, 0.5, 0.5
    
    def _analyze_with_cv(self, img_np):
        """Computer Vision analysis - Returns ONE defect per type"""
        defects = []
        
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 1. SHORT CIRCUIT detection
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary)
        
        if num_labels > 2:
            areas = stats[1:, cv2.CC_STAT_AREA]
            large_components = [a for a in areas if 100 <= a <= 3000]
            
            if len(large_components) >= 2:
                component_centers = []
                for i in range(1, num_labels):
                    if areas[i-1] in large_components:
                        y, x = np.where(labels == i)
                        center = (int(np.mean(x)), int(np.mean(y)))
                        component_centers.append(center)
                
                if len(component_centers) >= 2:
                    min_distance = float('inf')
                    for i in range(len(component_centers)):
                        for j in range(i+1, len(component_centers)):
                            dist = np.sqrt((component_centers[i][0] - component_centers[j][0])**2 + 
                                         (component_centers[i][1] - component_centers[j][1])**2)
                            min_distance = min(min_distance, dist)
                    
                    if min_distance < 70:
                        confidence = min(0.9, 1.0 - (min_distance / 90))
                        if confidence > 0.65:  # Balanced threshold
                            defects.append({
                                "type": "short_circuit",
                                "confidence": confidence,
                                "severity": "Critical" if confidence > 0.75 else "Moderate"
                            })
        
        # 2. MISSING HOLE detection
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
                
                if std_spacing < 25:
                    large_gaps = [s for s in x_spacings if s > avg_spacing * 1.5]
                    if len(large_gaps) >= 2:
                        confidence = min(0.85, len(large_gaps) * 0.15)
                        if confidence > 0.60:  # Balanced threshold
                            defects.append({
                                "type": "missing_hole",
                                "confidence": confidence,
                                "severity": "Moderate"
                            })
        
        # 3. OPEN CIRCUIT detection
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
                
                if len(gap_distances) >= 3:
                    avg_gap = np.mean(sorted(gap_distances)[:5])
                    confidence = min(0.85, 1.0 - (avg_gap / 80))
                    if confidence > 0.65:  # Balanced threshold
                        defects.append({
                            "type": "open_circuit",
                            "confidence": confidence,
                            "severity": "Critical" if confidence > 0.75 else "Moderate"
                        })
        
        # 4. MOUSE BITE detection
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
            
            if len(mouse_bite_contours) >= 2:
                confidence = min(0.8, 0.5 + (len(mouse_bite_contours) * 0.05))
                if confidence > 0.60:  # Balanced threshold
                    defects.append({
                        "type": "mouse_bite",
                        "confidence": confidence,
                        "severity": "Moderate"
                    })
        
        # 5. SPUR detection
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=30, maxLineGap=6)
        
        if lines is not None:
            short_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                if 10 < length < 35:
                    short_lines.append(line[0])
            
            if len(short_lines) >= 3:
                confidence = min(0.8, len(short_lines) / 10)
                if confidence > 0.60:  # Balanced threshold
                    defects.append({
                        "type": "spur",
                        "confidence": confidence,
                        "severity": "Moderate"
                    })
        
        # 6. SPURIOUS COPPER detection
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
            
            if len(spurious_contours) >= 2:
                total_area = sum(cv2.contourArea(c) for c in spurious_contours)
                if total_area > 100:
                    confidence = min(0.8, total_area / 500)
                    if confidence > 0.60:  # Balanced threshold
                        defects.append({
                            "type": "spurious_copper",
                            "confidence": confidence,
                            "severity": "Moderate"
                        })
        
        return defects
    
    def _balanced_filtering(self, all_defects, img_np, ml_confidence, is_defective=True):
        """Balanced filtering: Less strict when ML is confident about defective, stricter for uncertain"""
        if not all_defects:
            return []
        
        # Step 1: Remove duplicates by type - keep only the best
        defect_groups = {}
        for defect in all_defects:
            defect_type = defect["type"]
            if defect_type not in defect_groups:
                defect_groups[defect_type] = []
            defect_groups[defect_type].append(defect)
        
        unique_defects = []
        for defect_type, defects in defect_groups.items():
            best_defect = max(defects, key=lambda x: x["confidence"])
            unique_defects.append(best_defect)
        
        # Step 2: Apply balanced confidence thresholds
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # If ML is confident about defective, be less strict with CV
        if is_defective and ml_confidence > 0.80:
            if edge_density < 0.10:
                min_confidence = 0.70  # Less strict
            elif edge_density > 0.40:
                min_confidence = 0.65  # Less strict
            else:
                min_confidence = 0.60  # Less strict
        else:
            # If uncertain or ML not confident, be stricter
            if edge_density < 0.10:
                min_confidence = 0.80  # Strict for normal-looking
            elif edge_density > 0.40:
                min_confidence = 0.75  # Strict for noisy
            else:
                min_confidence = 0.70  # Balanced
        
        # Factor in ML confidence
        min_confidence = max(min_confidence, 0.60 * ml_confidence)
        
        # Apply threshold
        filtered_defects = [d for d in unique_defects if d["confidence"] >= min_confidence]
        
        # Step 3: Sort and limit to 6 types
        filtered_defects.sort(key=lambda x: x["confidence"], reverse=True)
        if len(filtered_defects) > 6:
            filtered_defects = filtered_defects[:6]
        
        return filtered_defects
