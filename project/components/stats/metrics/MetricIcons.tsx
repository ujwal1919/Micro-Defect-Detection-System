"use client";

import { 
  CircuitBoard, 
  Layers, 
  Ruler, 
  Microscope, 
  Zap,
  Component
} from "lucide-react";

export const MetricIcons = {
  surface: (className: string) => <Microscope className={className} />,
  trace: (className: string) => <CircuitBoard className={className} />,
  layer: (className: string) => <Layers className={className} />,
  density: (className: string) => <Ruler className={className} />,
  edge: (className: string) => <Zap className={className} />,
  component: (className: string) => <Component className={className} />
};