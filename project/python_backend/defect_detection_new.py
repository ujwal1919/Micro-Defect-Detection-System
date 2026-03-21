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
        
        # Try to load the new trained model
        self.model_trained = False
        try:
            self.model = self._create_model()
            state_dict = torch.load('new_trained_model.pth', map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.eval()
            self.model_trained = True
            print("New trained model loaded successfully!")
        except:
            print("Using computer vision only mode")
            self.model_trained = False
    
    def _create_model(self):
        class ImprovedDefectModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.backbone = models.resnet50(weights='IMAGENET1K_V1')
                self.backbone.fc = nn.Linear(2048, 2)
            
            def forward(self, x):
                return self.backbone(x)
        return ImprovedDefectModel()
    
    def detect(self, image):
        """ACCURATE defect detection with new trained model"""
        defects = []
        
        # Convert PIL to numpy for CV processing
        img_np = np.array(image)
        
        # ML Analysis with new trained model
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
        """ML-based defect detection with new trained model"""
        defects = []
        
        try:
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                
                normal_prob = float(probabilities[0][0])
                defective_prob = float(probabilities[0][1])
                
                # Use ML prediction with good confidence
                if defective_prob > 0.6:  # Good threshold
                    # ML suggests defective, add general defect types
                    defect_types = ["short_circuit", "missing_hole", "open_circuit", "mouse_bite", "spur", "spurious_copper"]
                    
                    for defect_type in defect_types:
                        confidence = defective_prob * 0.7  # Good confidence
                        defects.append({
                            "type": defect_type,
                            "confidence": confidence,
                            "severity": "Critical" if confidence > 0.8 else "Moderate"
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
            large_components = [a for a in areas if 200 <= a <= 5000]
            
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
                    
                    if min_distance < 60:  # Components are close
                        confidence = min(0.9, 1.0 - (min_distance / 80))
                        defects.append({
                            "type": "short_circuit",
                            "confidence": confidence,
                            "severity": "Critical" if confidence > 0.8 else "Moderate"
                        })
        
        # 2. MISSING HOLE detection
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, 
                                  param1=50, param2=30, minRadius=8, maxRadius=50)
        
        if circles is not None:
            hole_centers = circles[0]
            if len(hole_centers) > 1:
                x_coords = [hole[0] for hole in hole_centers]
                x_coords.sort()
                x_spacings = np.diff(x_coords)
                
                if len(x_spacings) > 0:
                    avg_spacing = np.mean(x_spacings)
                    std_spacing = np.std(x_spacings)
                    
                    if std_spacing < 25:  # Regular pattern
                        large_gaps = [s for s in x_spacings if s > avg_spacing * 1.5]
                        if len(large_gaps) > 0:
                            confidence = min(0.85, len(large_gaps) * 0.3)
                            defects.append({
                                "type": "missing_hole",
                                "confidence": confidence,
                                "severity": "Moderate"
                            })
        
        # 3. OPEN CIRCUIT detection
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Look for broken traces
            trace_contours = [c for c in contours if 100 < cv2.contourArea(c) < 2000]
            
            if len(trace_contours) > 2:
                # Check for gaps in traces
                for i, contour1 in enumerate(trace_contours):
                    for j, contour2 in enumerate(trace_contours[i+1:], i+1):
                        # Calculate distance between contours
                        M1 = cv2.moments(contour1)
                        M2 = cv2.moments(contour2)
                        
                        if M1['m00'] != 0 and M2['m00'] != 0:
                            cx1, cy1 = int(M1['m10']/M1['m00']), int(M1['m01']/M1['m00'])
                            cx2, cy2 = int(M2['m10']/M2['m00']), int(M2['m01']/M2['m00'])
                            distance = np.sqrt((cx1-cx2)**2 + (cy1-cy2)**2)
                            
                            if 20 < distance < 100:  # Gap in trace
                                confidence = min(0.8, 1.0 - (distance / 120))
                                defects.append({
                                    "type": "open_circuit",
                                    "confidence": confidence,
                                    "severity": "Critical" if confidence > 0.7 else "Moderate"
                                })
        
        # 4. MOUSE BITE detection
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            for contour in contours:
                area = cv2.contourArea(contour)
                if 50 < area < 500:  # Small to medium size
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        # Mouse bite has irregular shape
                        if 0.3 < circularity < 0.7:  # Irregular but not too irregular
                            x, y, w, h = cv2.boundingRect(contour)
                            aspect_ratio = w / h if h != 0 else 0
                            
                            if 0.2 < aspect_ratio < 5.0:  # Not too elongated
                                confidence = min(0.8, circularity)
                                defects.append({
                                    "type": "mouse_bite",
                                    "confidence": confidence,
                                    "severity": "Moderate"
                                })
        
        # 5. SPUR detection
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=30, maxLineGap=10)
        
        if lines is not None:
            # Look for short, isolated lines (spurs)
            short_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                if 10 < length < 50:  # Short lines
                    short_lines.append(line[0])
            
            if len(short_lines) > 2:  # Multiple short lines
                confidence = min(0.8, len(short_lines) / 10)
                defects.append({
                    "type": "spur",
                    "confidence": confidence,
                    "severity": "Moderate"
                })
        
        # 6. SPURIOUS COPPER detection
        bright_spots = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)[1]
        bright_contours, _ = cv2.findContours(bright_spots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if bright_contours:
            spurious_contours = []
            for contour in bright_contours:
                area = cv2.contourArea(contour)
                if 30 < area < 300:  # Small to medium size
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        if circularity > 0.5:  # Roughly circular
                            spurious_contours.append(contour)
            
            if len(spurious_contours) > 1:  # Multiple spurious copper
                total_area = sum(cv2.contourArea(c) for c in spurious_contours)
                if total_area > 100:  # Significant spurious copper
                    confidence = min(0.8, total_area / 500)
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
        if edge_density < 0.05:  # Very few edges - be strict
            final_defects = [d for d in final_defects if d["confidence"] > 0.8]
        elif edge_density > 0.3:  # Many edges - be strict
            final_defects = [d for d in final_defects if d["confidence"] > 0.7]
        else:
            final_defects = [d for d in final_defects if d["confidence"] > 0.6]
        
        return final_defects





