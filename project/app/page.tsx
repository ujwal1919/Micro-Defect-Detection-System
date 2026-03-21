//@ts-nocheck
"use client"

import React from 'react';
import { motion } from 'framer-motion';
import { Cpu, Activity, AlertCircle, CircuitBoard } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import DefectAnalysis from "@/components/DefectAnalysis";
import ImageUploader from "@/components/ImageUploader";
import DefectStats from "@/components/DefectStats";
import { useDefectAnalysis } from "@/hooks/use-defect-analysis";
import type { Analysis } from "@/types/analysis";

const sampleData = {
  defects: [
    { type: "Crack", severity: "0.8", confidence: "0.9" },
    { type: "Scratch", severity: "0.6", confidence: "0.85" }
  ],
  metrics: {
    qualityScore: "0.75",
    reliability: "0.8",
    consistency: "0.85",
    performance: "0.9"
  },
  selectedDefect: null,
  criticalDefects: 1,
  minorDefects: 1,
  passRate: 80,
  recommendations: ["Improve process control", "Regular maintenance"]
};

export default function Home() {
  const { analyzing, analysis, analyze } = useDefectAnalysis();
  
  console.log('Home page analysis:', analysis);

  const defaultAnalysis: Analysis = {
    defects: [
      { 
        type: "Sample Defect",
        severity: "0.8",
        confidence: "0.9",
        //@ts-ignore
        location: "center",
        recommendation: "Sample recommendation"
      }
    ],
    metrics: {
      qualityScore: "0.75",
      reliability: "0.8",
      consistency: "0.85",
      performance: "0.9",
      defect_density: "0.2",
      edge_quality: "0.7",
      component_integrity: "0.8"
    },
    selectedDefect: null,
    criticalDefects: 1,
    minorDefects: 1,
    passRate: 80,
    recommendations: ["Sample recommendation"]
  };

  return (
    <div className="min-h-screen bg-[#1a1a1a]">
      {/* Background Effects */}
      <div className="fixed inset-0">
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-[#8659ff]/20 rounded-full blur-[100px]" />
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-[#6c3aed]/20 rounded-full blur-[100px]" />
      </div>

      <main className="relative container mx-auto px-4 py-8">
        <motion.div 
          className="mb-12 text-center"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-[#a587ff] to-[#6c3aed] bg-clip-text text-transparent glow-text">
            Micro Defect Detection
          </h1>
          <p className="text-xl text-[#c4b1ff]">
            Neural Network Chip Production Analysis System
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card className="p-8 bg-[#2d1159]/50 backdrop-blur-sm border border-[#8659ff]/20 shadow-lg hover:shadow-[#8659ff]/10 transition-all duration-300">
              <motion.div 
                className="flex items-center gap-3 mb-6"
                whileHover={{ scale: 1.02 }}
              >
                <div className="p-3 rounded-full bg-[#8659ff]/20">
                  <CircuitBoard className="h-6 w-6 text-[#a587ff]" />
                </div>
                <h2 className="text-2xl font-semibold text-white">Upload Chip Image</h2>
              </motion.div>
              <ImageUploader onUpload={analyze} />
              {analyzing && (
                <motion.div 
                  className="mt-6"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <Progress value={66} className="h-2 mb-3 bg-[#8659ff]/20" />
                  <p className="text-sm text-[#c4b1ff] flex items-center gap-2">
                    <Activity className="h-4 w-4 animate-pulse" />
                    Analyzing chip image...
                  </p>
                </motion.div>
              )}
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card className="p-8 bg-[#2d1159]/50 backdrop-blur-sm border border-[#8659ff]/20 shadow-lg hover:shadow-[#8659ff]/10 transition-all duration-300">
              <motion.div 
                className="flex items-center gap-3 mb-6"
                whileHover={{ scale: 1.02 }}
              >
                <div className="p-3 rounded-full bg-[#8659ff]/20">
                  <AlertCircle className="h-6 w-6 text-[#a587ff]" />
                </div>
                <h2 className="text-2xl font-semibold text-white">Defect Statistics</h2>
              </motion.div>
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.5 }}
              >
                <DefectStats analysis={analysis} />
              </motion.div>
            </Card>
          </motion.div>
        </div>

        {(analysis || defaultAnalysis) && (
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <DefectAnalysis analysis={analysis || defaultAnalysis} />
          </motion.div>
        )}
      </main>
    </div>
  );
}