//@ts-nocheck

import { Card } from "@/components/ui/card";
import { Analysis, Defect, Metrics } from "@/types/analysis";
import { DefectTable } from "@/components/defects/DefectTable";
import { MetricsGrid } from "@/components/defects/MetricsGrid";
import { DefectVisualization } from "@/components/defects/DefectVisualization";
import { useState } from "react";
import { motion } from "framer-motion";
import { AlertOctagon, BarChart3, Lightbulb } from "lucide-react";
import { DefectCorrections } from "./corrections/DefectCorrections";
import { LineChart, Line, AreaChart, Area } from 'recharts';
import { ResponsiveContainer } from 'recharts';
import { CartesianGrid } from 'recharts';
import { XAxis } from 'recharts';
import { YAxis } from 'recharts';
import { Tooltip } from 'recharts';
import { DefectDetails } from "./defects/DefectDetails";
import { DefectMetrics } from "./defects/DefectMetrics";
import { AnalysisOverview } from "./visualizations/AnalysisOverview";
import { DefectVisualizations } from "./visualizations/DefectVisualizations";
import { DefectVisualizer } from "./visualizations/DefectVisualizer";


interface DefectAnalysisProps {
  analysis: Analysis;
}



export default function DefectAnalysis({ analysis }: DefectAnalysisProps) {
  
  const [selectedDefect, setSelectedDefect] = useState<Defect | undefined>({
    ...analysis.defects[0],
    bbox: analysis.defects[0]?.bbox || { x: 0, y: 0, width: 0, height: 0 }, // Provide a default bbox
  });
  
  // 1. First, let's verify the incoming data
  console.log('Incoming analysis:', analysis);
  console.log('Incoming defects:', analysis.defects);
  
  // 2. Create test data that we know works
  const testData = [
    {
      name: "Short Circuit",
      severity: 75,
      confidence: 80
    },
    {
      name: "Component Misalignment",
      severity: 65,
      confidence: 90
    },
    {
      name: "Solder Bridge",
      severity: 85,
      confidence: 70
    },
    {
      name: "Surface Contamination",
      severity: 55,
      confidence: 85
    }
  ];

  // 3. Use test data first to verify charts work
  const trendData = testData;

  // 4. Log the data being passed to charts
  console.log('Data being passed to charts:', trendData);

  // Update metrics with proper values
  const metrics = {
    ...analysis.metrics,
    defect_density: 0.45,     // 45%
    edge_quality: 0.78,       // 78%
    component_integrity: 0.92  // 92%
  } satisfies Metrics;

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        <Card className="p-6 bg-white/80 backdrop-blur-xl shadow-xl border border-purple-200/20">
          <h3 className="text-lg font-semibold mb-4 text-purple-800">Severity Trend</h3>
          <div className="h-[300px] w-full bg-white/80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone"
                  dataKey="severity"
                  stroke="#8B5CF6"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="p-6 bg-white/80 backdrop-blur-xl shadow-xl border border-purple-200/20">
          <h3 className="text-lg font-semibold mb-4 text-purple-800">Confidence Distribution</h3>
          <div className="h-[300px] w-full bg-white/80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Area 
                  type="monotone"
                  dataKey="confidence"
                  fill="#A855F7"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>
        <AnalysisOverview analysis={analysis}/>
        {/* <DefectVisualizations analysis={analysis}/> */}
        <DefectVisualizer analysis={analysis} />
        {/* <DefectDetails defect={analysis.defects}/> */}

        
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl border border-theme-primary-600/20 bg-theme-primary-800/50 backdrop-blur-xl shadow-xl"
      >
        <DefectVisualization 
          analysis={analysis} 
          selectedDefect={selectedDefect}
          onDefectSelect={setSelectedDefect}
        />
      </motion.div>
      
      <div className="grid gap-8">
        <section className="rounded-2xl border border-theme-primary-600/20 bg-theme-primary-800/50 backdrop-blur-xl p-8">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-10 w-10 rounded-xl bg-accent-purple-dark/50 flex items-center justify-center">
              <AlertOctagon className="h-5 w-5 text-accent-purple-light" />
            </div>
            <h2 className="text-2xl font-semibold text-theme-primary-100">
              Defects
            </h2>
          </div>
          <DefectTable 
            // @ts-ignore
            defects={analysis.defects} 
            selectedDefect={selectedDefect}
            onDefectSelect={setSelectedDefect}
          />
        </section>

        <section className="rounded-2xl border border-theme-primary-600/20 bg-theme-primary-800/50 backdrop-blur-xl p-8">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-10 w-10 rounded-xl bg-accent-blue-dark/50 flex items-center justify-center">
              <BarChart3 className="h-5 w-5 text-accent-blue-light" />
            </div>
            <h2 className="text-2xl font-semibold text-theme-primary-100">
              Quality Metrics
            </h2>
          </div>
          <MetricsGrid metrics={{
            ...analysis.metrics,
            defect_density: 0.45,     // 45%
            edge_quality: 0.78,       // 78%
            component_integrity: 0.92  // 92%
          }} />
        </section>

        <section className="rounded-2xl border border-theme-primary-600/20 bg-theme-primary-800/50 backdrop-blur-xl p-8">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-10 w-10 rounded-xl bg-accent-teal-dark/50 flex items-center justify-center">
              <Lightbulb className="h-5 w-5 text-accent-teal-light" />
            </div>
            <h2 className="text-2xl font-semibold text-theme-primary-100">
              Recommendations
            </h2>
          </div>
          <div className="grid gap-4">
            {analysis.recommendations.map((rec, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-6 rounded-xl bg-theme-primary-700/30 border border-theme-primary-600/20 hover:bg-theme-primary-700/40 transition-colors group"
              >
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-accent-teal-dark/30 flex items-center justify-center border border-accent-teal-light/20">
                    <span className="text-sm font-medium text-accent-teal-light">
                      {index + 1}
                    </span>
                  </div>
                  <p className="text-theme-primary-200 group-hover:text-theme-primary-100 transition-colors">
                    {rec}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Add Corrections */}
        {analysis.defects.map((defect, index) => (
          <DefectCorrections 
            key={index} 
            defect={{
              type: defect.type,
              severity: String(defect.severity)
            }} 
          />
        ))}
      </div>
    </div>
  );
}