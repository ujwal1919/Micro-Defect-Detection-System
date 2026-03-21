//@ts-nocheck

import { Analysis, Defect } from "@/types/analysis";
import { Card } from "../ui/card";
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

interface DefectVisualizerProps {
  analysis: Analysis;
}

export function DefectVisualizer({ analysis }: DefectVisualizerProps) {
  console.log('Analysis in DefectVisualizer:', analysis); // Debug log

  // Ensure analysis.defects exists and is an array
  if (!analysis?.defects || !Array.isArray(analysis.defects)) {
    console.log('No defects data available');
    return (
      <Card className="p-6 bg-[#2d1159]/50 backdrop-blur-sm border border-[#8659ff]/20">
        <h2 className="text-xl font-bold text-white mb-6">Defect Distribution</h2>
        <p className="text-[#c4b1ff]">No defect data available</p>
      </Card>
    );
  }

  // Prepare data for visualization
  const defectTypes = analysis.defects.reduce((acc: Record<string, number>, defect: Defect) => {
    acc[defect.type] = (acc[defect.type] || 0) + 1;
    return acc;
  }, {});

  const pieData = Object.entries(defectTypes).map(([name, value]) => ({
    name: name.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
    value
  }));

  console.log('Pie chart data:', pieData); // Debug log

  // If no data after processing, show message
  if (pieData.length === 0) {
    return (
      <Card className="p-6 bg-[#2d1159]/50 backdrop-blur-sm border border-[#8659ff]/20">
        <h2 className="text-xl font-bold text-white mb-6">Defect Distribution</h2>
        <p className="text-[#c4b1ff]">No defects detected</p>
      </Card>
    );
  }

  const COLORS = ['#8659ff', '#60a5fa', '#4ade80', '#f97316', '#ef4444'];

  return (
    <Card className="p-6 bg-[#2d1159]/50 backdrop-blur-sm border border-[#8659ff]/20">
      <h2 className="text-xl font-bold text-white mb-6">Defect Distribution</h2>
      <div className="h-[300px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={pieData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              fill="#8659ff"
              paddingAngle={5}
              dataKey="value"
            >
              {pieData.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#2d1159', 
                borderColor: '#8659ff',
                borderRadius: '8px',
                color: '#c4b1ff'
              }}
            />
            <Legend 
              formatter={(value) => <span style={{ color: '#c4b1ff' }}>{value}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
} 