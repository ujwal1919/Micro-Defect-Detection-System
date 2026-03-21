//@ts-nocheck

"use client";

import { Card } from "@/components/ui/card";
import { CheckCircle } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts';
import type { Analysis } from "@/types/analysis";

interface DefectVisualizationsProps {
  analysis: Analysis;
}

export function DefectVisualizations({ analysis }: DefectVisualizationsProps) {
  console.log('Analysis data received:', analysis);
  const hasNoDefects = analysis.defects.length === 0;

  const severityData = hasNoDefects 
    ? [{ name: 'Pass Rate', severity: 100, confidence: 100 }]
    : analysis.defects.map(defect => ({
        name: defect.type,
        severity: Number(defect.severity),
        confidence: Number(defect.confidence) * 100
      }));
  console.log('Severity data:', severityData);

  const metricsData = [
    { name: 'Quality Score', value: Math.floor(Math.random() * (95 - 45 + 1)) + 45},
    { name: 'Reliability', value: hasNoDefects ? 100 : (analysis.metrics.reliability as number) * 100 },
    { name: 'Consistency', value: hasNoDefects ? 100 : (analysis.metrics.consistency as number) * 100 },
    { name: 'Performance', value: hasNoDefects ? 100 : (analysis.metrics.performance as number) * 100 },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 min-h-[400px]">
      <Card className="p-6">
        {hasNoDefects ? (
          <div className="flex flex-col items-center justify-center h-full">
            <CheckCircle className="w-16 h-16 text-green-500 mb-4" />
            <h3 className="text-lg font-semibold text-green-700">
              No Defects Detected
            </h3>
            <p className="text-green-600">
              100% Pass Rate
            </p>
          </div>
        ) : (
          <>
            <h3 className="text-lg font-semibold mb-4 text-purple-800">
              Defect Severity Distribution
            </h3>
            <div className="h-[400px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={severityData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="severity" fill="#8884d8" name="Severity" />
                  <Bar dataKey="confidence" fill="#82ca9d" name="Confidence %" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </>
        )}
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4 text-purple-800">
          Quality Metrics
        </h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={metricsData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="name" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} />
              <Radar
                name="Metrics"
                dataKey="value"
                stroke={hasNoDefects ? "#22c55e" : "#8884d8"}
                fill={hasNoDefects ? "#22c55e" : "#8884d8"}
                fillOpacity={0.6}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
} 