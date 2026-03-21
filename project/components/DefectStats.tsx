//@ts-nocheck

"use client";

import { Card } from "@/components/ui/card";
import type { Analysis } from "@/types/analysis";
import { DefectTrends } from "@/components/stats/DefectTrends";
import { QualityMetrics } from "@/components/stats/QualityMetrics";

interface DefectStatsProps {
  analysis: Analysis | null;
}

export default function DefectStats({ analysis }: DefectStatsProps) {
  if (!analysis) {
    return (
      <div className="text-center text-muted-foreground">
        Upload an image to see defect statistics
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Defect Trends</h3>
        <DefectTrends analysis={analysis} />
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Quality Metrics</h3>
        <QualityMetrics metrics={analysis.metrics} />
      </Card>
    </div>
  );
}