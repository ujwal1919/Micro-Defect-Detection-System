//@ts-nocheck

import { Card } from "@/components/ui/card";
import { AlertTriangle, AlertCircle, Info } from "lucide-react";
import type { Defect } from "@/types/analysis";
import { DefectCorrections } from "../corrections/DefectCorrections";

interface DefectDetailsProps {
  defect: Defect;
}

export function DefectDetails({ defect }: DefectDetailsProps) {
  const getSeverityIcon = () => {
    switch (typeof defect.severity === "string" ? defect.severity.toLowerCase() : defect.severity) {
      case "critical":
        return <AlertTriangle className="h-5 w-5 text-[#ff5c5c]" />;
      case "moderate":
        return <AlertCircle className="h-5 w-5 text-[#ffd15c]" />;
      default:
        return <Info className="h-5 w-5 text-[#5c9fff]" />;
    }
  };

  return (
    <Card className="p-6 bg-[#2d1159]/50 backdrop-blur-sm border border-[#8659ff]/20">
      <div className="flex items-center gap-3 mb-4">
        {getSeverityIcon()}
        <h3 className="text-xl font-bold bg-gradient-to-r from-[#a587ff] to-[#6c3aed] bg-clip-text text-transparent">
          {defect.type}
        </h3>
      </div>

      <div className="space-y-6 text-[#c4b1ff]">
        <div>
          <h4 className="font-medium mb-2 text-[#a587ff]">Location Details</h4>
          
          <p>{defect.location}</p>
        </div>

        <div>
          <h4 className="font-medium mb-2 text-[#a587ff]">Severity Assessment</h4>
          <p>
            {defect.severity} - Confidence: {Math.round(defect.confidence * 100)}%
          </p>
        </div>

        <div>
          <h4 className="font-medium mb-2 text-[#a587ff]">Immediate Recommendation</h4>
          <p>{defect.recommendation}</p>
        </div>

      </div>
    </Card>
  );
}