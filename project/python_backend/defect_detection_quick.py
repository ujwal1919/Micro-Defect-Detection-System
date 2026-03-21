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
        
        # Try to load the quick trained model
        self.model_trained = False
        try:
            self.model = self._create_model()
            state_dict = torch.load('quick_trained_model.pth', map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.eval()
            self.model_trained = True
            print("Quick trained model loaded successfully!")
        except:
            print("Using computer vision only mode")
            self.model_trained = False
    
    def _create_model(self):
        class QuickDefectModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.backbone = models.resnet18(weights='IMAGENET1K_V1')
                self.backbone.fc = nn.Linear(512, 2)
            
            def forward(self, x):
                return self.backbone(x)
        return QuickDefectModel()
    
    def detect(self, image):
        """QUICK ACCURATE defect detection with trained model"""
        defects = []
        
        # Convert PIL to numpy for CV processing
        img_np = np.array(image)
        
        # ML Analysis with quick trained model
        ml_defects = []
        if self.model_trained:
            ml_defects = self._analyze_with_ml(image)
        
        # Computer Vision Analysis for specific defect types
        cv_defects = self._analyze_with_cv(img_np)
        
        # Combine results intelligently
        all_defects = ml_defects + cv_defects
        
        # Smart filtering to keep accurate defects
        defects = self._smart_filtering(all_defects, img_np)
        
        return defects
    
    def _analyze_with_ml(self, image):
        """ML-based defect detection with quick trained model"""
        defects = []
        
        try:
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                
                normal_prob = float(probabilities[0][0])
                defective_prob = float(probabilities[0][1])
                
                # Use ML prediction with good confidence
                if defective_prob > 0.5:  # Good threshold
                    # ML suggests defective, add general defect types
                    defect_types = ["short_circuit", "missing_hole", "open_circuit", "mouse_bite", "spur", "spurious_copper"]
                    
                    for defect_type in defect_types:
                        confidence = defective_prob * 0.6  # Good confidence
                        defects.append({
                            "type": defect_type,
                            "confidence": confidence,
                            "severity": "Critical" if confidence > 0.7 else "Moderate"
                        })
        
        except Exception as e:
            print(f"ML analysis failed: {e}")
        
        return defects
    
    def _analyze_with_cv(self, img_np):
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
                    
                    if min_distance < 80:  # Components are close
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
                    
                    if std_spacing < 30:  # Regular pattern
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
                            
                            if 15 < distance < 80:  # Gap in trace
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
                if 40 < area < 400:  # Small to medium size
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if 0.2 < circularity < 0.6:  # Irregular shape
                            x, y, w, h = cv2.boundingRect(contour)
                            aspect_ratio = w / h if h != 0 else 0
                            
                            if 0.1 < aspect_ratio < 6.0:  # Not too elongated
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
                if 8 < length < 40:  # Short lines
                    short_lines.append(line[0])
            
            if len(short_lines) > 1:  # Multiple short lines
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
                if 25 < area < 250:  # Small to medium size
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if circularity > 0.4:  # Roughly circular
                            spurious_contours.append(contour)
            
            if len(spurious_contours) > 0:  # Any spurious copper
                total_area = sum(cv2.contourArea(c) for c in spurious_contours)
                if total_area > 80:  # Significant spurious copper
                    confidence = min(0.8, total_area / 400)
                    defects.append({
                        "type": "spurious_copper",
                        "confidence": confidence,
                        "severity": "Moderate"
                    })
        
        return defects
    
    def _smart_filtering(self, all_defects, img_np):
        """Smart filtering for accurate results"""
        if not all_defects:
            return []
        
        # Remove duplicates by type
        defect_groups = {}
        for defect in all_defects:
            defect_type = defect["type"]
            if defect_type not in defect_groups:
                defect_groups[defect_type] = []
            defect_groups[defect_type].append(defect)
        
        # Keep only the best defect of each type
        final_defects = []
        for defect_type, defects in defect_groups.items():
            if len(defects) == 1:
                final_defects.append(defects[0])
            else:
                best_defect = max(defects, key=lambda x: x["confidence"])
                final_defects.append(best_defect)
        
        # Smart filtering based on image characteristics
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # Smart filtering
        if edge_density < 0.03:  # Very few edges - be strict
            final_defects = [d for d in final_defects if d["confidence"] > 0.7]
        elif edge_density > 0.25:  # Many edges - be strict
            final_defects = [d for d in final_defects if d["confidence"] > 0.6]
        else:
            final_defects = [d for d in final_defects if d["confidence"] > 0.5]
        
        return final_defects




