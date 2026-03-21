import { Card } from "@/components/ui/card";
import { Clock, CheckSquare, Wrench } from "lucide-react";
import { useState } from "react";
import { motion } from "framer-motion";

interface CorrectionStep {
  title: string;
  steps: string[];
  equipment: string[];
  timeEstimate: string;
}

interface CorrectionMethodProps {
  correction: CorrectionStep;
}

export function CorrectionMethod({ correction }: CorrectionMethodProps) {
  return (
    <Card className="p-6 bg-[#2d1159]/30 border-[#8659ff]/20">
      <h4 className="text-lg font-semibold bg-gradient-to-r from-[#a587ff] to-[#6c3aed] bg-clip-text text-transparent">
        {correction.title}
      </h4>
      
      <div className="space-y-4 mt-4">
        <div className="flex items-center gap-2 text-sm text-[#c4b1ff]">
          <Clock className="h-4 w-4 text-[#8659ff]" />
          <span>Estimated time: {correction.timeEstimate}</span>
        </div>
        
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <CheckSquare className="h-4 w-4 text-[#8659ff]" />
            <span className="font-medium text-[#a587ff]">Required Steps:</span>
          </div>
          <ul className="list-disc pl-6 space-y-2">
            {correction.steps.map((step, index) => (
              <li key={index} className="text-sm text-[#c4b1ff]">{step}</li>
            ))}
          </ul>
        </div>
        
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Wrench className="h-4 w-4 text-[#8659ff]" />
            <span className="font-medium text-[#a587ff]">Required Equipment:</span>
          </div>
          <ul className="list-disc pl-6 space-y-2">
            {correction.equipment.map((item, index) => (
              <li key={index} className="text-sm text-[#c4b1ff]">{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </Card>
  );
}