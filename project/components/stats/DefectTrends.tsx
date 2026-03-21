"use client";

import { AlertTriangle, AlertCircle, CheckCircle } from "lucide-react";
import { MetricCard } from "./MetricCard";
import type { Analysis } from "@/types/analysis";

interface DefectTrendsProps {
  analysis: Analysis;
}

export function DefectTrends({ analysis }: DefectTrendsProps) {
  const trends = [
    {
      label: "Critical Defects",
      value: analysis.criticalDefects,
      icon: <AlertTriangle className="h-5 w-5 text-red-500" />,
      description: "High-priority defects requiring immediate attention"
    },
    {
      label: "Minor Defects",
      value: analysis.minorDefects,
      icon: <AlertCircle className="h-5 w-5 text-yellow-500" />,
      description: "Low-priority defects for monitoring"
    },
    {
      label: "Pass Rate",
      value: `${analysis.passRate}%`,
      icon: <CheckCircle className="h-5 w-5 text-green-500" />,
      description: "Overall quality pass rate"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {trends.map((trend) => (
        <MetricCard
          key={trend.label}
          label={trend.label}
          value={trend.value}
          icon={trend.icon}
          description={trend.description}
        />
      ))}
    </div>
  );
}