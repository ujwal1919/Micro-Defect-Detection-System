class AnalysisEngine:
    def __init__(self):
        self.recommendations_db = {
            "short_circuit": [
                "Inspect and replace affected components immediately",
                "Verify power distribution network integrity",
                "Implement additional isolation measures"
            ],
            "trace_width_variation": [
                "Recalibrate etching parameters",
                "Review mask alignment procedures",
                "Update design rules for trace widths"
            ],
            "surface_contamination": [
                "Enhance cleanroom protocols",
                "Upgrade filtration systems",
                "Implement additional inspection steps"
            ],
            "layer_misalignment": [
                "Recalibrate alignment systems",
                "Update alignment markers",
                "Implement additional alignment verification steps"
            ],
            "component_damage": [
                "Review handling procedures",
                "Update placement parameters",
                "Implement protective measures"
            ]
        }
    
    def analyze(self, defects):
        defect_counts = self._count_defects(defects)
        
        return {
            "criticalDefects": defect_counts["Critical"],
            "minorDefects": defect_counts["Minor"] + defect_counts["Moderate"],
            "passRate": self._calculate_pass_rate(defects),
            "defects": self._format_defects(defects),
            "metrics": self._calculate_metrics(defects),
            "recommendations": self._generate_recommendations(defects)
        }
    
    def _count_defects(self, defects):
        counts = {"Critical": 0, "Moderate": 0, "Minor": 0}
        for defect in defects:
            counts[defect["severity"]] += 1
        return counts
    
    def _calculate_pass_rate(self, defects):
        if not defects:
            return 100
        
        # Calculate weighted impact of each defect
        total_impact = 0
        for defect in defects:
            severity_weight = {
                "Critical": 0.6,
                "Moderate": 0.3,
                "Minor": 0.1
            }[defect["severity"]]
            
            total_impact += severity_weight * defect["confidence"]
        
        # Calculate pass rate
        pass_rate = 100 - (total_impact * 100)
        return max(0, min(100, int(pass_rate)))
    
    def _calculate_metrics(self, defects):
        if not defects:
            return {
                "surface_quality": "100%",
                "trace_consistency": "100%",
                "layer_alignment": "100%"
            }
        
        base_metrics = {
            "surface_quality": 100,
            "trace_consistency": 100,
            "layer_alignment": 100
        }
        
        # Impact weights for different defect types
        impact_weights = {
            "surface_contamination": {"surface_quality": 0.4},
            "component_damage": {"surface_quality": 0.5},
            "trace_width_variation": {"trace_consistency": 0.6},
            "layer_misalignment": {"layer_alignment": 0.7},
            "short_circuit": {
                "surface_quality": 0.3,
                "trace_consistency": 0.3
            }
        }
        
        for defect in defects:
            if defect["type"] in impact_weights:
                weights = impact_weights[defect["type"]]
                impact = defect["confidence"] * 100
                
                for metric, weight in weights.items():
                    base_metrics[metric] -= impact * weight
        
        return {
            key: f"{max(0, min(100, int(value)))}%"
            for key, value in base_metrics.items()
        }
    
    def _format_defects(self, defects):
        return [{
            "type": defect["type"].replace("_", " ").title(),
            "location": self._generate_location(defect),
            "severity": defect["severity"],
            "recommendation": self._get_primary_recommendation(defect["type"])
        } for defect in defects]
    
    def _generate_location(self, defect):
        locations = {
            "layer_misalignment": "Between Layer Interface",
            "surface_contamination": "Top Surface Layer",
            "trace_width_variation": "Signal Trace Layer",
            "component_damage": "Component Layer",
            "short_circuit": "Power Distribution Layer"
        }
        return locations.get(defect["type"], "Multiple Layers")
    
    def _generate_recommendations(self, defects):
        recommendations = set()
        severity_weights = {
            "Critical": 2,
            "Moderate": 1,
            "Minor": 0
        }
        
        for defect in defects:
            if defect["type"] in self.recommendations_db:
                severity_index = severity_weights[defect["severity"]]
                recommendations.add(
                    self.recommendations_db[defect["type"]][severity_index]
                )
        
        return list(recommendations)
    
    def _get_primary_recommendation(self, defect_type):
        if defect_type in self.recommendations_db:
            return self.recommendations_db[defect_type][0]
        return "Conduct detailed inspection"