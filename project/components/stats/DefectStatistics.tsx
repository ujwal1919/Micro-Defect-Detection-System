"use client";

import { Card } from "@/components/ui/card";
import { CheckCircle, AlertCircle } from "lucide-react";
import type { Analysis } from "@/types/analysis";

interface DefectStatisticsProps {
  analysis: Analysis;
}

export function DefectStatistics({ analysis }: DefectStatisticsProps) {
  const hasNoDefects = analysis.defects.length === 0;
  
  const stats = {
    totalDefects: hasNoDefects ? 0 : analysis.defects.length,
    passRate: hasNoDefects ? 100 : 100 - (analysis.defects.length * 10),
    averageSeverity: hasNoDefects ? 0 : analysis.defects.reduce((acc, d) => acc + Number(d.severity), 0) / analysis.defects.length,
    criticalDefects: hasNoDefects ? 0 : analysis.defects.filter(d => Number(d.severity) > 0.8).length
  };

  return (
    <Card className="p-6 bg-white/80 backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-4">
        {hasNoDefects ? (
          <CheckCircle className="w-6 h-6 text-green-500" />
        ) : (
          <AlertCircle className="w-6 h-6 text-amber-500" />
        )}
        <h2 className="text-xl font-semibold">
          {hasNoDefects ? "Perfect Quality Score" : "Defect Statistics"}
        </h2>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          label="Pass Rate"
          value={`${stats.passRate}%`}
          trend={hasNoDefects ? "positive" : stats.passRate > 80 ? "positive" : "negative"}
        />
        <StatCard
          label="Total Defects"
          value={stats.totalDefects}
          trend={hasNoDefects ? "positive" : "negative"}
        />
        <StatCard
          label="Avg Severity"
          value={stats.averageSeverity.toFixed(2)}
          trend={hasNoDefects ? "positive" : stats.averageSeverity < 0.5 ? "positive" : "negative"}
        />
        <StatCard
          label="Critical Defects"
          value={stats.criticalDefects}
          trend={hasNoDefects ? "positive" : "negative"}
        />
      </div>
    </Card>
  );
}

interface StatCardProps {
  label: string;
  value: string | number;
  trend: "positive" | "negative" | "neutral";
}

function StatCard({ label, value, trend }: StatCardProps) {
  return (
    <div className="p-4 rounded-lg bg-white/50 backdrop-blur-sm">
      <p className="text-sm text-gray-600">{label}</p>
      <p className={`text-2xl font-bold ${
        trend === "positive" ? "text-green-600" : 
        trend === "negative" ? "text-red-600" : 
        "text-gray-800"
      }`}>
        {value}
      </p>
    </div>
  );
} 