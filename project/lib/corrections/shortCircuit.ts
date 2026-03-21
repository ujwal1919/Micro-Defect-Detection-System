export const shortCircuitCorrections = {
  high: [
    {
      title: "Emergency Circuit Isolation",
      steps: [
        "Power down system immediately",
        "Use thermal imaging to locate hot spots",
        "Apply isolation compound",
        "Test circuit continuity",
        "Install protective barriers"
      ],
      equipment: [
        "Thermal camera",
        "Isolation compound",
        "Circuit tester",
        "Protective barriers",
        "ESD protection kit"
      ],
      timeEstimate: "2-3 hours"
    },
    {
      title: "Component Replacement Protocol",
      steps: [
        "Identify damaged components",
        "Remove affected parts",
        "Clean contact points",
        "Install new components",
        "Verify connections"
      ],
      equipment: [
        "Desoldering station",
        "Replacement parts",
        "Cleaning solution",
        "Soldering iron",
        "Multimeter"
      ],
      timeEstimate: "3-4 hours"
    },
    {
      title: "Circuit Path Reconstruction",
      steps: [
        "Map damaged circuit paths",
        "Remove compromised traces",
        "Lay new circuit paths",
        "Apply protective coating",
        "Test conductivity"
      ],
      equipment: [
        "Circuit mapping tool",
        "Trace removal kit",
        "Conductive ink",
        "Protective spray",
        "Conductivity tester"
      ],
      timeEstimate: "4-5 hours"
    },
    {
      title: "Power Distribution Repair",
      steps: [
        "Analyze power flow",
        "Isolate affected sectors",
        "Repair distribution paths",
        "Install surge protection",
        "Test power delivery"
      ],
      equipment: [
        "Power analyzer",
        "Sector isolation tools",
        "Repair kit",
        "Surge protectors",
        "Load tester"
      ],
      timeEstimate: "3-4 hours"
    },
    {
      title: "Ground Plane Restoration",
      steps: [
        "Check ground connections",
        "Repair ground plane breaks",
        "Reinforce connections",
        "Apply shielding",
        "Verify ground integrity"
      ],
      equipment: [
        "Ground tester",
        "Conductive adhesive",
        "Reinforcement tools",
        "EMI shielding",
        "Continuity meter"
      ],
      timeEstimate: "2-3 hours"
    }
  ],
  moderate: [
    {
      title: "Circuit Trace Repair",
      steps: [
        "Identify affected circuit traces",
        "Clean area with specialized solution",
        "Apply conductive repair compound",
        "Verify connections with oscilloscope",
        "Test under load conditions"
      ],
      equipment: [
        "Digital microscope",
        "Cleaning solution",
        "Conductive repair kit",
        "Oscilloscope",
        "Load tester"
      ],
      timeEstimate: "1-2 hours"
    }
  ],
  low: [
    {
      title: "Preventive Maintenance",
      steps: [
        "Clean affected area with isopropyl alcohol",
        "Apply protective coating",
        "Test connectivity with multimeter",
        "Monitor for 24 hours"
      ],
      equipment: [
        "Isopropyl alcohol",
        "Protective coating spray",
        "Digital multimeter",
        "Monitoring system"
      ],
      timeEstimate: "30-45 minutes"
    }
  ]
};

export const surfaceContaminationCorrections = {
  high: [
    {
      title: "Deep Cleaning Protocol",
      steps: [
        "Remove power and isolate board",
        "Apply specialized cleaning solution",
        "Use ultrasonic cleaner",
        "Dry in controlled environment",
        "Apply protective coating"
      ],
      equipment: [
        "Ultrasonic cleaner",
        "Industrial cleaning solution",
        "Dehumidifier",
        "Protective coating",
        "ESD-safe brushes"
      ],
      timeEstimate: "4-5 hours"
    }
  ],
  moderate: [
    {
      title: "Surface Treatment",
      steps: [
        "Clean with isopropyl alcohol",
        "Use compressed air to remove particles",
        "Apply contact cleaner",
        "Inspect under microscope",
        "Apply conformal coating"
      ],
      equipment: [
        "Isopropyl alcohol",
        "Compressed air system",
        "Contact cleaner",
        "Digital microscope",
        "Conformal coating"
      ],
      timeEstimate: "2-3 hours"
    }
  ],
  low: [
    {
      title: "Light Cleaning",
      steps: [
        "Dust removal with compressed air",
        "Gentle cleaning with IPA",
        "Visual inspection",
        "Apply protective spray"
      ],
      equipment: [
        "Compressed air can",
        "IPA wipes",
        "Inspection light",
        "Protective spray"
      ],
      timeEstimate: "30 minutes"
    }
  ]
};

export const layerMisalignmentCorrections = {
  high: [
    {
      title: "Complete Layer Realignment",
      steps: [
        "Remove affected components",
        "Apply heat treatment",
        "Realign using precision tools",
        "Verify alignment with X-ray",
        "Reflow solder connections"
      ],
      equipment: [
        "Reflow station",
        "X-ray inspection system",
        "Precision alignment tools",
        "Temperature controller",
        "Microscope"
      ],
      timeEstimate: "6-8 hours"
    }
  ],
  moderate: [
    {
      title: "Partial Realignment",
      steps: [
        "Identify misaligned areas",
        "Local heat application",
        "Adjust using alignment tools",
        "Verify with digital imaging",
        "Test connections"
      ],
      equipment: [
        "Heat gun",
        "Alignment toolkit",
        "Digital microscope",
        "Testing equipment",
        "Precision tools"
      ],
      timeEstimate: "3-4 hours"
    }
  ],
  low: [
    {
      title: "Minor Adjustment",
      steps: [
        "Inspect misalignment degree",
        "Apply minimal heat",
        "Make fine adjustments",
        "Test functionality"
      ],
      equipment: [
        "Inspection camera",
        "Fine adjustment tools",
        "Temperature probe",
        "Multimeter"
      ],
      timeEstimate: "1-2 hours"
    }
  ]
};