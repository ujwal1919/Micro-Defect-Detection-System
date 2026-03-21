import { useState } from "react";
import { Card } from "@/components/ui/card";
import { motion } from "framer-motion";
import { CorrectionMethod } from "./CorrectionMethod";
import { shortCircuitCorrections } from "../../lib/corrections/shortCircuit";
import { surfaceContaminationCorrections } from "../../lib/corrections/surfaceContamination";
import { layerMisalignmentCorrections } from "../../lib/corrections/layerMisalignment";
import { traceWidthVariationCorrections } from "../../lib/corrections/traceWidthVariation";

interface DefectCorrectionsProps {
  defect: {
    type: string;
    severity: string;
  };
}

interface CorrectionStep {
  title: string;
  steps: string[];
  equipment: string[];
  timeEstimate: string;
}

interface CorrectionsBySeverity {
  high: CorrectionStep[];
  moderate: CorrectionStep[];
  low: CorrectionStep[];
}

export function DefectCorrections({ defect }: DefectCorrectionsProps) {
  const [selectedMethod, setSelectedMethod] = useState(0);

  const getCorrectionMethods = () => {
    console.log('Defect:', defect);
    console.log('Type:', defect.type);
    console.log('Severity:', defect.severity);

    const severity = defect.severity.toLowerCase() as keyof CorrectionsBySeverity;
    const defectType = defect.type.toLowerCase().replace(/[-\s]/g, '_');
    
    console.log('Normalized type:', defectType);
    console.log('Normalized severity:', severity);

    let methods: CorrectionStep[] = [];
    switch (defectType) {
      case 'short_circuit':
        methods = shortCircuitCorrections[severity] || [];
        break;
      case 'surface_contamination':
        methods = surfaceContaminationCorrections[severity] || [];
        break;
      case 'layer_misalignment':
        methods = layerMisalignmentCorrections[severity] || [];
        break;
      case 'trace_width_variation':
        methods = traceWidthVariationCorrections[severity] || [];
        break;
      default:
        methods = [];
    }

    console.log('Selected methods:', methods);
    return methods;
  };

  const corrections = getCorrectionMethods();

  console.log('Final corrections:', corrections);

  return (
    <Card className="p-6 bg-[#2d1159]/50 backdrop-blur-sm border border-[#8659ff]/20">
      <h3 className="text-xl font-bold mb-6 bg-gradient-to-r from-[#a587ff] to-[#6c3aed] bg-clip-text text-transparent">
        Correction Methods for {defect.type.replace(/_/g, ' ')}
      </h3>
      
      {corrections && corrections.length > 0 ? (
        <div className="space-y-6">
          <div className="flex gap-2 overflow-x-auto pb-2">
            {corrections.map((correction, index) => (
              <button
                key={index}
                onClick={() => setSelectedMethod(index)}
                className={`px-4 py-2 rounded-lg transition-all ${
                  selectedMethod === index
                    ? 'bg-[#8659ff] text-white'
                    : 'bg-[#2d1159]/30 text-[#a587ff] hover:bg-[#2d1159]/50'
                }`}
              >
                Method {index + 1}
              </button>
            ))}
          </div>

          <motion.div
            key={selectedMethod}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <CorrectionMethod correction={corrections[selectedMethod]} />
          </motion.div>
        </div>
      ) : (
        <div className="text-[#c4b1ff]">
          <p>Debug Info:</p>
          <p>Type: {defect.type}</p>
          <p>Severity: {defect.severity}</p>
          <p>Normalized Type: {defect.type.toLowerCase().replace(/[-\s]/g, '_')}</p>
        </div>
      )}
    </Card>
  );
}