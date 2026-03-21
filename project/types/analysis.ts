export interface DefectLocation {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface Defect {
  type: string;
  severity: string | number;
  confidence: string | number;
  bbox: {
    x: number;
    y: number;
    width: number;
    height: number;
  } | null;
}

export interface DetailedMetrics {
  defect_density: string;
  edge_quality: string;
  component_integrity: string;
  [key: string]: string | number;
}

export interface Analysis {
  selectedDefect: Defect;
  criticalDefects: number;
  minorDefects: number;
  passRate: number;
  defects: Array<{
    bbox: { x: number; y: number; width: number; height: number; };
    type: string;
    severity: string | number;
    confidence: string | number;
  }>;
  metrics: Metrics;
  recommendations: string[];
  annotatedImage?: string; // Base64 encoded image with defects highlighted
  heatmap?: string; // Base64 encoded overall defect heatmap
  imageUrl: string;
}

export interface Metrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  confusion_matrix: number[][];
  quality_score: number;
  reliability: number;
  consistency: number;
  performance: number;
  defect_density: number;
  edge_quality: number;
  component_integrity: number;
  detailed_performance: {
    soldering_quality: number;
    alignment_accuracy: number;
    surface_finish: number;
  };
  defect_distribution: { [key: string]: number };
  severity_levels: {
    critical: number;
    moderate: number;
    minor: number;
  };
  confidence_intervals: {
    mean_confidence: number;
    std_deviation: number;
    confidence_95: number;
  };
}
