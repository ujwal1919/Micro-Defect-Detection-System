//@ts-nocheck
"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { DefectBadge } from "./DefectBadge";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Info } from "lucide-react";
import type { Defect } from "@/types/analysis";
import { DEFECT_TYPES } from "@/lib/constants/defectTypes";
import { motion } from "framer-motion";

interface DefectTableProps {
  defects: Defect[];
  selectedDefect?: Defect;
  onDefectSelect?: (defect: Defect) => void;
}

const getSeverityColor = (severity: string) => {
  switch (severity.toLowerCase()) {
    case 'high':
      return 'bg-[#2d1159]/80 text-[#c4b1ff] border-[#8659ff]/30 hover:bg-[#2d1159]/60';
    case 'moderate':
      return 'bg-[#2d1159]/60 text-[#c4b1ff] border-[#8659ff]/30 hover:bg-[#2d1159]/40';
    case 'low':
      return 'bg-[#2d1159]/40 text-[#c4b1ff] border-[#8659ff]/30 hover:bg-[#2d1159]/20';
    default:
      return 'bg-gray-900/80 text-gray-300 border-gray-500/30';
  }
};

const getSeverityDot = (severity: string) => {
  switch (severity.toLowerCase()) {
    case 'high':
      return 'bg-[#8659ff] shadow-[#8659ff]/50 animate-pulse';
    case 'moderate':
      return 'bg-[#a587ff] shadow-[#a587ff]/50';
    case 'low':
      return 'bg-[#c4b1ff] shadow-[#c4b1ff]/50';
    default:
      return 'bg-gray-400 shadow-gray-400/50';
  }
};

export function DefectTable({ defects, selectedDefect, onDefectSelect }: DefectTableProps) {
  const getDefectInfo = (type: string) => {
    const normalizedType = type.toUpperCase().replace(/ /g, "_") as keyof typeof DEFECT_TYPES;
    return DEFECT_TYPES[normalizedType];
  };

  const getDefectTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'missing_component':
        return 'bg-purple-950/50 text-purple-200 border-purple-500/30';
      case 'misalignment':
        return 'bg-purple-950/50 text-purple-200 border-purple-500/30';
      case 'solder_bridge':
        return 'bg-purple-800/50 text-purple-200 border-purple-500/30';
      case 'insufficient_solder':
        return 'bg-purple-700/50 text-purple-200 border-purple-500/30';
      case 'excess_solder':
        return 'bg-purple-600/50 text-purple-200 border-purple-500/30';
      default:
        return 'bg-gray-950/50 text-gray-200 border-gray-500/30';
    }
  };

  return (
    <div className="overflow-hidden rounded-2xl border border-[#8659ff]/20 bg-[#2d1159]/50 backdrop-blur-sm">
      <table className="w-full">
        <thead className="bg-[#2d1159]/80">
          <tr>
            <th className="p-5 text-left font-semibold text-[#c4b1ff]">Type</th>
            <th className="p-5 text-left font-semibold text-[#c4b1ff]">Severity</th>
            <th className="p-5 text-left font-semibold text-[#c4b1ff]">Location</th>
          </tr>
        </thead>
        <tbody>
          {defects.map((defect, index) => (
            <motion.tr
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              onClick={() => onDefectSelect?.(defect)}
              className={`
                border-t border-[#8659ff]/10 cursor-pointer
                ${selectedDefect === defect 
                  ? 'bg-[#8659ff]/20' 
                  : 'hover:bg-[#8659ff]/10'
                }
                transition-all duration-200 ease-in-out
              `}
            >
              <td className="p-5">
                <div className="flex items-center gap-3">
                  <span className={`
                    px-3 py-1.5 rounded-lg text-sm font-medium
                    bg-[#2d1159]/60 text-[#c4b1ff] border-[#8659ff]/30
                    border shadow-lg
                    transition-all duration-200
                    hover:scale-105
                  `}>
                    {defect.type.replace(/_/g, ' ')}
                  </span>
                  {getDefectInfo(defect.type) && (
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger>
                          <Info className="h-5 w-5 text-[#8659ff] hover:text-[#a587ff] transition-colors" />
                        </TooltipTrigger>
                        <TooltipContent 
                          className="bg-[#2d1159]/95 border border-[#8659ff]/20 px-4 py-3 rounded-lg shadow-xl max-w-xs"
                        >
                          <p className="text-sm leading-relaxed text-[#c4b1ff]">
                            {getDefectInfo(defect.type).description}
                          </p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  )}
                </div>
              </td>
              <td className="p-5">
                <motion.span 
                  whileHover={{ scale: 1.05 }}
                  className={`
                    px-4 py-2 rounded-lg text-sm font-medium
                    ${getSeverityColor(defect.severity)}
                    shadow-lg
                    inline-flex items-center gap-2
                  `}
                >
                  <span className={`h-2 w-2 rounded-full shadow-lg ${getSeverityDot(defect.severity)}`} />
                  {defect.severity}
                </motion.span>
              </td>
              <td className="p-5">
                <span className="text-[#c4b1ff] hover:text-white transition-colors font-medium">
                  {defect.location}
                </span>
              </td>
            </motion.tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
