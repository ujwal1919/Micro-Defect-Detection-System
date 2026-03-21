import numpy as np
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix
from typing import Dict, Any, List, Union

class DefectMetricsCalculator:
    def __init__(self, image_dimensions: tuple):
        self.image_dimensions = image_dimensions
        self.total_area = image_dimensions[0] * image_dimensions[1]

    def calculate_metrics(self, 
                         y_true: np.ndarray, 
                         y_pred: np.ndarray, 
                         defect_areas: np.ndarray) -> Dict[str, Any]:
        """
        Calculate comprehensive defect metrics
        """
        # Basic classification metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')
        conf_matrix = confusion_matrix(y_true, y_pred)

        # Quality metrics
        quality_metrics = self._calculate_quality_metrics(y_pred, defect_areas)
        
        # Combine all metrics
        return {
            # Classification performance
            'accuracy': round(float(accuracy), 4),
            'precision': round(float(precision), 4),
            'recall': round(float(recall), 4),
            'f1_score': round(float(f1), 4),
            'confusion_matrix': conf_matrix.tolist(),
            
            # Quality assessment
            'quality_score': quality_metrics['quality_score'],
            'reliability': quality_metrics['reliability'],
            'consistency': quality_metrics['consistency'],
            
            # Detailed metrics
            'defect_density': quality_metrics['defect_density'],
            'edge_quality': quality_metrics['edge_quality'],
            'component_integrity': quality_metrics['component_integrity'],
            
            # Performance metrics
            'performance': quality_metrics['performance'],
            'detailed_performance': quality_metrics['detailed_performance'],
            
            # Distribution analysis
            'defect_distribution': quality_metrics['defect_distribution'],
            'severity_levels': quality_metrics['severity_levels'],
            
            # Confidence metrics
            'confidence_intervals': quality_metrics['confidence_intervals']
        }

    def _calculate_quality_metrics(self, 
                                predictions: np.ndarray, 
                                defect_areas: np.ndarray) -> Dict[str, Any]:
        """
        Calculate detailed quality metrics
        """
        # Calculate defect density
        total_defect_area = np.sum(defect_areas)
        defect_density = (total_defect_area / self.total_area) * 100
        
        # Edge quality analysis
        edge_quality = self._calculate_edge_quality(predictions)
        
        # Component integrity analysis
        component_integrity = self._calculate_component_integrity(predictions)
        
        # Defect distribution analysis
        defect_distribution = self._calculate_defect_distribution(predictions)
        
        # Severity analysis
        severity_metrics = self._calculate_severity_metrics(defect_areas)
        
        # Calculate reliability score
        reliability_score = self._calculate_reliability_score(predictions, severity_metrics)
        
        # Calculate consistency score
        consistency_score = self._calculate_consistency_score(defect_distribution)
        
        # Calculate performance metrics
        performance_metrics = {
            'soldering_quality': self._calculate_soldering_quality(predictions, defect_areas),
            'alignment_accuracy': self._calculate_alignment_accuracy(predictions, defect_areas),
            'surface_finish': self._calculate_surface_quality(predictions, defect_areas)
        }
        
        # Calculate overall quality score
        quality_score = np.mean([
            reliability_score * 0.4,
            edge_quality * 0.2,
            component_integrity * 0.2,
            np.mean(list(performance_metrics.values())) * 0.2
        ])

        return {
            'quality_score': round(quality_score, 2),
            'reliability': round(reliability_score, 2),
            'consistency': round(consistency_score, 2),
            'performance': round(np.mean(list(performance_metrics.values())), 2),
            'defect_density': round(defect_density, 3),
            'edge_quality': round(edge_quality, 3),
            'component_integrity': round(component_integrity, 3),
            'defect_distribution': {k: round(v, 3) for k, v in defect_distribution.items()},
            'severity_levels': severity_metrics,
            'detailed_performance': {k: round(v, 3) for k, v in performance_metrics.items()},
            'confidence_intervals': self._calculate_confidence_intervals(predictions, defect_areas)
        }

    def _calculate_edge_quality(self, predictions: np.ndarray) -> float:
        """Calculate edge quality score"""
        edge_defects = np.sum(predictions == 'edge_defect')
        total_edges = (self.image_dimensions[0] + self.image_dimensions[1]) * 2
        return 100 - ((edge_defects / total_edges) * 100)

    def _calculate_component_integrity(self, predictions: np.ndarray) -> float:
        """Calculate component integrity score"""
        component_defects = np.sum(predictions == 'component_defect')
        return 100 - ((component_defects / len(predictions)) * 100)

    def _calculate_defect_distribution(self, predictions: np.ndarray) -> Dict[str, float]:
        """Calculate defect type distribution"""
        unique_defects, counts = np.unique(predictions, return_counts=True)
        return {defect: (count / len(predictions)) * 100 
                for defect, count in zip(unique_defects, counts)}

    def _calculate_severity_metrics(self, defect_areas: np.ndarray) -> Dict[str, int]:
        """Calculate severity levels of defects"""
        return {
            'critical': int(np.sum(defect_areas > 0.05 * self.total_area)),
            'moderate': int(np.sum((defect_areas > 0.01 * self.total_area) & 
                                 (defect_areas <= 0.05 * self.total_area))),
            'minor': int(np.sum(defect_areas <= 0.01 * self.total_area))
        }

    def _calculate_reliability_score(self, 
                                  predictions: np.ndarray, 
                                  severity_metrics: Dict[str, int]) -> float:
        """Calculate reliability score"""
        total_defects = len(predictions[predictions != 'no_defect'])
        if total_defects == 0:
            return 100.0
            
        weighted_severity = (
            (severity_metrics['critical'] * 1.0) +
            (severity_metrics['moderate'] * 0.6) +
            (severity_metrics['minor'] * 0.3)
        )
        return max(0, 100 - (weighted_severity * 100 / total_defects))

    def _calculate_consistency_score(self, defect_distribution: Dict[str, float]) -> float:
        """Calculate consistency score"""
        std_dev = np.std(list(defect_distribution.values()))
        return max(0, 100 - (std_dev * 10))

    def _calculate_soldering_quality(self, predictions: np.ndarray, defect_areas: np.ndarray) -> float:
        """Calculate soldering quality score"""
        solder_defects = predictions == 'solder_defect'
        if not np.any(solder_defects):
            return 100.0
        
        solder_area = np.sum(defect_areas[solder_defects])
        severity = np.mean(defect_areas[solder_defects])
        return max(0, 100 - (solder_area * severity * 100))

    def _calculate_alignment_accuracy(self, predictions: np.ndarray, defect_areas: np.ndarray) -> float:
        """Calculate alignment accuracy score"""
        alignment_defects = predictions == 'alignment_defect'
        if not np.any(alignment_defects):
            return 100.0
        
        misalignment_severity = np.mean(defect_areas[alignment_defects])
        return max(0, 100 - (misalignment_severity * 100))

    def _calculate_surface_quality(self, predictions: np.ndarray, defect_areas: np.ndarray) -> float:
        """Calculate surface quality score"""
        surface_defects = predictions == 'surface_defect'
        if not np.any(surface_defects):
            return 100.0
        
        surface_area = np.sum(defect_areas[surface_defects])
        return max(0, 100 - (surface_area * 100))

    def _calculate_confidence_intervals(self, 
                                     predictions: np.ndarray, 
                                     defect_areas: np.ndarray) -> Dict[str, float]:
        """Calculate confidence intervals for predictions"""
        return {
            'mean_confidence': round(np.mean(defect_areas) * 100, 3),
            'std_deviation': round(np.std(defect_areas) * 100, 3),
            'confidence_95': round(np.percentile(defect_areas, 95) * 100, 3)
        } 