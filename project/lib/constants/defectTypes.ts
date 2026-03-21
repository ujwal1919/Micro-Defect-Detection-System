export const DEFECT_TYPES = {
    SHORT_CIRCUIT: {
      label: "Short Circuit",
      description: "Unintended connection between circuit elements",
      severity: {
        critical: "Risk of component damage",
        moderate: "Performance degradation",
        minor: "Minimal impact"
      }
    },
    TRACE_WIDTH: {
      label: "Trace Width Variation",
      description: "Inconsistent width in circuit traces",
      severity: {
        critical: "Signal integrity issues",
        moderate: "Potential reliability concerns",
        minor: "Within acceptable range"
      }
    },
    LAYER_MISALIGNMENT: {
      label: "Layer Misalignment",
      description: "Improper alignment between chip layers",
      severity: {
        critical: "Severe connection issues",
        moderate: "Partial misalignment",
        minor: "Slight offset"
      }
    },
    SURFACE_CONTAMINATION: {
      label: "Surface Contamination",
      description: "Presence of unwanted particles or residue",
      severity: {
        critical: "Severe contamination",
        moderate: "Moderate debris",
        minor: "Light residue"
      }
    },
    COMPONENT_DAMAGE: {
      label: "Component Damage",
      description: "Physical damage to chip components",
      severity: {
        critical: "Component failure",
        moderate: "Partial damage",
        minor: "Cosmetic issues"
      }
    }
  };
  
  export type DefectType = keyof typeof DEFECT_TYPES;