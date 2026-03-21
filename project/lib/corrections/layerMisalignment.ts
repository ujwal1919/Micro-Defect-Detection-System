import { Defect } from "@/types/analysis";

export const layerMisalignmentCorrections = {
  high: [
    {
      title: "Immediate Actions",
      steps: [
        "Stop production line immediately",
        "Check and recalibrate alignment pins and fixtures",
        "Verify registration marks on all layers",
        "Inspect tooling holes for wear or damage"
      ],
      equipment: ["Optical alignment system", "Registration verification tools"],
      timeEstimate: "1-2 hours"
    }
  ],
  moderate: [
    {
      title: "Equipment Adjustments",
      steps: [
        "Calibrate optical alignment system",
        "Check servo motors and positioning mechanisms",
        "Verify pressure settings for layer bonding"
      ],
      equipment: ["Calibration tools", "Pressure gauges"],
      timeEstimate: "30-45 minutes"
    }
  ],
  low: [
    {
      title: "Process Modifications",
      steps: [
        "Adjust layer registration parameters",
        "Update alignment offset values",
        "Document changes made"
      ],
      equipment: ["Alignment software", "Documentation tools"],
      timeEstimate: "15-30 minutes"
    }
  ]
}; 