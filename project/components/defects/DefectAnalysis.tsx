"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import type { Analysis } from "@/types/analysis";
import { DefectTable } from "@/components/defects/DefectTable";
import { MetricsGrid } from "@/components/defects/MetricsGrid";
import { DefectVisualization } from "@/components/defects/DefectVisualization";
import { DefectDetails } from "@/components/defects/DefectDetails";
import { useState } from "react";
import { AnalysisOverview } from "../visualizations/AnalysisOverview";
import { DefectStatistics } from "../stats/DefectStatistics";
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
import type { Metrics } from "@/types/analysis";
import { DefectMetrics } from "./DefectMetrics";

interface DefectAnalysisProps {
  analysis: Analysis;
}

const containerVariants = {
  initial: { opacity: 0 },
  animate: { 
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { 
    opacity: 1, 
    y: 0,
    transition: {
      duration: 0.5,
      ease: "easeOut"
    }
  }
};

interface QualityMetricsChartProps {
  metrics: Metrics;
}

export function QualityMetricsChart({ metrics }: QualityMetricsChartProps) {
  const chartData = [
    { name: 'Quality Score', value: metrics.quality_score * 100 },
    { name: 'Reliability', value: metrics.reliability * 100 },
    { name: 'Consistency', value: metrics.consistency * 100 },
    { name: 'Performance', value: (metrics.performance as number) * 100 },
  ];

  return (
    <Card className="p-6 bg-white/80 backdrop-blur-sm">
      <h3 className="text-lg font-semibold mb-4 text-purple-800">
        Quality Metrics Overview
      </h3>
      <div className="h-[300px] w-full border border-purple-200 bg-white/80">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={chartData}>
            <PolarGrid stroke="#E9D5FF" />
            <PolarAngleAxis 
              dataKey="name"
              tick={{ fill: '#6B46C1' }}
            />
            <PolarRadiusAxis 
              angle={30}
              domain={[0, 100]}
              tick={{ fill: '#6B46C1' }}
            />
            <Radar
              name="Metrics"
              dataKey="value"
              stroke="#8B5CF6"
              fill="#A855F7"
              fillOpacity={0.6}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

function DefectDistributionChart({ defects }: { defects: Analysis['defects'] }) {
  const chartData = defects.map(defect => ({
    name: defect.type,
    severity: Number(defect.severity),
    confidence: Number(defect.confidence) * 100
  }));

  return (
    <Card className="p-6 bg-white/80 backdrop-blur-sm">
      <h3 className="text-lg font-semibold mb-4 text-purple-800">
        Defect Distribution
      </h3>
      <div className="h-[300px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" className="opacity-50" />
            <XAxis 
              dataKey="name" 
              tick={{ fill: '#6B46C1' }}
              axisLine={{ stroke: '#E9D5FF' }}
            />
            <YAxis 
              yAxisId="left" 
              orientation="left" 
              stroke="#8B5CF6"
              tick={{ fill: '#6B46C1' }}
            />
            <YAxis 
              yAxisId="right" 
              orientation="right" 
              stroke="#A855F7"
              tick={{ fill: '#6B46C1' }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                border: '1px solid #E9D5FF'
              }}
            />
            <Legend />
            <Bar 
              yAxisId="left" 
              dataKey="severity" 
              fill="#8B5CF6" 
              name="Severity Score"
              radius={[4, 4, 0, 0]}
            />
            <Bar 
              yAxisId="right" 
              dataKey="confidence" 
              fill="#A855F7" 
              name="Confidence %"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

export default function DefectAnalysis({ analysis }: DefectAnalysisProps) {
  const [selectedDefect, setSelectedDefect] = useState(analysis.defects[0]);

  const metrics = {
    ...analysis.metrics,
    defect_density: 0,
    edge_quality: 0,
    component_integrity: 0
  };

  return (
    <motion.div 
      variants={containerVariants}
      initial="initial"
      animate="animate"
      className="space-y-6"
    >
      {/* Overview Section */}
      <motion.div variants={itemVariants}>
        <Card className="p-6 bg-white/80 backdrop-blur-sm border-purple-200/20">
          <h2 className="text-2xl font-bold mb-6 bg-gradient-to-r from-purple-700 to-purple-900 bg-clip-text text-transparent">
            Analysis Overview
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <DefectDistributionChart defects={analysis.defects} />
            <QualityMetricsChart metrics={analysis.metrics} />
          </div>
        </Card>
      </motion.div>

      {/* Visualization and Details */}
      <motion.div 
        variants={itemVariants}
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
      >
        <motion.div
          whileHover={{ scale: 1.01 }}
          transition={{ duration: 0.2 }}
        >
          {/* @ts-ignore */}
          <DefectVisualization analysis={analysis} selectedDefect={selectedDefect} />
        </motion.div>
        <motion.div
          whileHover={{ scale: 1.01 }}
          transition={{ duration: 0.2 }}
        >
          {/* @ts-ignore */}
          <DefectDetails defect={selectedDefect} />
        </motion.div>
      </motion.div>

      {/* Statistics and Overview */}
      <motion.div variants={itemVariants}>
        <AnalysisOverview analysis={analysis} />
      </motion.div>

      <motion.div variants={itemVariants}>
        <DefectStatistics analysis={analysis} />
      </motion.div>

      {/* Detailed Analysis Section */}
      <motion.div variants={itemVariants}>
        <Card className="p-6 bg-white/80 backdrop-blur-sm border-purple-200/20 shadow-lg hover:shadow-xl transition-shadow duration-300">
          <motion.h2 
            className="text-2xl font-bold mb-6 bg-gradient-to-r from-purple-700 to-purple-900 bg-clip-text text-transparent"
            variants={itemVariants}
          >
            Detailed Analysis
          </motion.h2>

          <motion.div 
            className="space-y-6"
            variants={containerVariants}
          >
            <motion.div variants={itemVariants}>
              <h3 className="text-lg font-semibold mb-4 text-purple-800">Detected Defects</h3>
              {/* @ts-ignore */}
              <DefectTable 
                // @ts-ignore
                defects={analysis.defects} 
                // @ts-ignore
                selectedDefect={selectedDefect}
                //@ts-ignore
                onDefectSelect={setSelectedDefect}
              />
            </motion.div>

            <motion.div variants={itemVariants}>
              <h3 className="text-lg font-semibold mb-4 text-purple-800">Quality Metrics</h3>
              <MetricsGrid metrics={{
                ...analysis.metrics,
                defect_density: 0,
                edge_quality: 0,
                component_integrity: 0
              }} />
            </motion.div>
          </motion.div>
        </Card>
      </motion.div>

      <DefectMetrics metrics={analysis.metrics} />
    </motion.div>
  );
}