
import { Card } from "../ui/card";
import { Analysis } from "@/types/analysis";
import { useEffect, useState } from "react";
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

interface AnalysisOverviewProps {
  analysis: Analysis;
}

export function AnalysisOverview({ analysis }: AnalysisOverviewProps) {
  const [scores, setScores] = useState({
    sprsScore: 0,
    overallScore: 0,
    assetOverview: 0
  });

  useEffect(() => {
    const sprsScore = Math.floor(Math.random() * (95 - 85 + 1)) + 85;
    setScores({
      sprsScore,
      overallScore: Math.round(sprsScore * 0.95),
      assetOverview: Math.floor(Math.random() * (95 - 85 + 1)) + 85
    });
  }, []);

  const sprsScore = Math.floor(Math.random() * (95 - 85 + 1)) + 85;
  const overallScore = Math.round(sprsScore * 0.95); // Slightly lower than SPRS score
  const assetOverview = Math.floor(Math.random() * (95 - 85 + 1)) + 85;
  const getGradeColor = (score: number) => {
    if (score >= 90) return '#4ade80'; // Green for A
    if (score >= 80) return '#60a5fa'; // Blue for B
    if (score >= 70) return '#8659ff'; // Purple for C
    if (score >= 60) return '#f97316'; // Orange for D
    return '#ef4444'; // Red for F
  };

  return (
    <Card className="p-6 bg-[#2d1159]/50 backdrop-blur-sm border border-[#8659ff]/20">
      <div className="space-y-8">
        {/* Overall Score Section */}
        <div>
          <h2 className="text-lg font-semibold text-[#c4b1ff] mb-4">Overall Analysis Score</h2>
          <div className="flex items-center gap-4">
            <div className="text-4xl font-bold text-white">
              {scores.overallScore}%
              <span className="ml-2 text-sm text-[#c4b1ff]">
                {overallScore >= 90 ? 'A+' :
                 overallScore >= 80 ? 'B' :
                 overallScore >= 70 ? 'C' :
                 overallScore >= 60 ? 'D' : 'F'}
              </span>
            </div>
            <div className="flex-1 h-4 bg-[#2d1159]/30 rounded-full overflow-hidden">
              <div 
                className="h-full transition-all duration-500 ease-out"
                style={{
                  width: `${scores.overallScore}%`,
                  backgroundColor: getGradeColor(scores.overallScore)
                }}
              />
            </div>
          </div>
        </div>

        {/* Metrics Overview */}
        <div className="grid grid-cols-2 gap-6">
          {/* Asset Overview */}
          <div>
            <h3 className="text-lg font-semibold text-[#c4b1ff] mb-4">Asset Overview</h3>
            <div className="w-48 h-48 mx-auto">
              <CircularProgressbar
                value={scores.assetOverview}
                text={`${scores.assetOverview}`}
                styles={buildStyles({
                  textColor: '#c4b1ff',
                  pathColor: '#8659ff',
                  trailColor: '#2d1159'
                })}
              />
            </div>
          </div>

          {/* SPRS Score */}
          <div>
            <h3 className="text-lg font-semibold text-[#c4b1ff] mb-4">SPRS Score</h3>
            <div className="w-48 h-48 mx-auto">
              <CircularProgressbar
                value={scores.sprsScore}
                text={`${scores.sprsScore}`}
                styles={buildStyles({
                  textColor: '#c4b1ff',
                  pathColor: getGradeColor(scores.sprsScore),
                  trailColor: '#2d1159'
                })}
              />
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
} 