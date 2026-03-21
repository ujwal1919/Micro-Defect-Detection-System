//@ts-nocheck

"use client";

import { Card } from "@/components/ui/card";
import type { Metrics } from "@/types/analysis";
import { motion } from "framer-motion";

interface MetricsGridProps {
  metrics: Metrics;
}

export function MetricsGrid({ metrics }: MetricsGridProps) {
  const formatValue = (value: string | number) => {
    // If it's a percentage, ensure it's formatted properly
    if (typeof value === 'number') {
      return `${Math.round(value * 100)}%`;
    }
    return value;
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {Object.entries(metrics).map(([key, value], index) => (
        <div
          key={key}
          className="relative group"
        >
          {/* Background glow effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-[#8659ff]/10 via-[#a587ff]/10 to-[#6c3aed]/10 
                         rounded-xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          
          <div className="relative p-6 rounded-xl bg-[#2d1159]/50 border border-[#8659ff]/20 backdrop-blur-sm
                         hover:bg-[#2d1159]/70 hover:border-[#8659ff]/40 transition-all duration-300">
            <div className="flex flex-col gap-3">
              {/* Metric Label */}
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-gradient-to-r from-[#8659ff] to-[#6c3aed]" />
                <h4 className="text-sm font-medium text-[#c4b1ff] group-hover:text-white/90 transition-colors">
                  {key.replace(/_/g, ' ').toUpperCase()}
                </h4>
              </div>
              
              {/* Metric Value */}
              <div className="flex items-baseline gap-2">
                <p className="text-4xl font-bold text-[#a587ff] group-hover:text-white/90 transition-colors">
                  {formatValue(value)}
                </p>
              </div>
            </div>

            {/* Decorative corner accent */}
            <div className="absolute top-0 right-0 w-16 h-16 overflow-hidden">
              <div className="absolute top-0 right-0 w-[2px] h-8 bg-gradient-to-b from-white/0 via-white/20 to-white/0 
                             transform rotate-45 translate-x-4" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}