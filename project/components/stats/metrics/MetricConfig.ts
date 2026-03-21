export const metricConfigurations = {
  surface_quality: {
    label: "Surface Quality",
    description: "Overall surface integrity and cleanliness of the chip",
    thresholds: { warning: 85, critical: 70 },
    color: "blue"
  },
  trace_consistency: {
    label: "Trace Consistency",
    description: "Uniformity and reliability of circuit traces",
    thresholds: { warning: 90, critical: 80 },
    color: "purple"
  },
  layer_alignment: {
    label: "Layer Alignment",
    description: "Precision of layer-to-layer alignment in manufacturing",
    thresholds: { warning: 95, critical: 85 },
    color: "green"
  },
  defect_density: {
    label: "Defect Density",
    description: "Concentration of defects per unit area",
    thresholds: { warning: 5, critical: 10 },
    color: "yellow"
  },
  edge_quality: {
    label: "Edge Quality",
    description: "Sharpness and precision of component edges",
    thresholds: { warning: 88, critical: 75 },
    color: "orange"
  },
  component_integrity: {
    label: "Component Integrity",
    description: "Overall health and reliability of components",
    thresholds: { warning: 92, critical: 82 },
    color: "red"
  }
};