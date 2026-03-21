"use client";

interface MetricStatusProps {
  value: string;
  thresholds: {
    warning: number;
    critical: number;
  };
}

export function MetricStatus({ value, thresholds }: MetricStatusProps) {
  const numericValue = parseInt(value);
  
  const getStatusColor = () => {
    if (numericValue >= thresholds.warning) return "text-green-500";
    if (numericValue >= thresholds.critical) return "text-yellow-500";
    return "text-red-500";
  };

  return (
    <span className={`text-sm font-medium ${getStatusColor()}`}>
      {numericValue >= thresholds.warning ? "Optimal" : 
       numericValue >= thresholds.critical ? "Warning" : "Critical"}
    </span>
  );
}