"use client";

import { Badge } from "@/components/ui/badge";
import { DEFECT_TYPES } from "@/lib/constants/defectTypes";

interface DefectBadgeProps {
  type: string;
  severity: string;
}

export function DefectBadge({ type, severity }: DefectBadgeProps) {
  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case "critical":
        return "bg-red-500 hover:bg-red-600";
      case "moderate":
        return "bg-yellow-500 hover:bg-yellow-600";
      case "minor":
        return "bg-blue-500 hover:bg-blue-600";
      default:
        return "bg-gray-500 hover:bg-gray-600";
    }
  };

  const normalizedType = type.toUpperCase().replace(/ /g, "_") as keyof typeof DEFECT_TYPES;
  const defectInfo = DEFECT_TYPES[normalizedType];

  return (
    <Badge className={`${getSeverityColor(severity)} text-white font-medium`}>
      {defectInfo?.label || type}
    </Badge>
  );
}