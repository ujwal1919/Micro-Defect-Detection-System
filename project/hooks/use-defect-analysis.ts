import { useState } from "react";
import { useToast } from "@/components/ui/use-toast";
import { analyzeImage } from "@/lib/api/defect";
import type { Analysis } from "@/types/analysis";

export function useDefectAnalysis() {
  const [analyzing, setAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const { toast } = useToast();

  const analyze = async (image: File) => {
    setAnalyzing(true);
    try {
      const response = await analyzeImage(image);
      setAnalysis(response);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  return { analyzing, analysis, analyze };
}