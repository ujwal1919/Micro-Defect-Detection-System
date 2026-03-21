DEFECT_TYPES = {
    "short_circuit": {
        "threshold": 0.35,
        "critical_threshold": 0.75,
        "min_area": 100,  # Minimum area for detection
        "max_area": 5000  # Maximum area for detection
    },
    "trace_width_variation": {
        "threshold": 0.30,
        "critical_threshold": 0.70,
        "min_width": 2,   # Minimum width variation
        "max_width": 20   # Maximum width variation
    },
    "surface_contamination": {
        "threshold": 0.25,
        "critical_threshold": 0.65,
        "min_contrast": 30,  # Minimum contrast difference
        "texture_threshold": 0.4  # Texture uniformity threshold
    },
    "layer_misalignment": {
        "threshold": 0.40,
        "critical_threshold": 0.80,
        "max_offset": 10,  # Maximum allowed layer offset
        "edge_threshold": 50  # Edge detection threshold
    },
    "component_damage": {
        "threshold": 0.45,
        "critical_threshold": 0.85,
        "damage_area_ratio": 0.1,  # Minimum damaged area ratio
        "edge_intensity": 100  # Edge intensity threshold
    }
}