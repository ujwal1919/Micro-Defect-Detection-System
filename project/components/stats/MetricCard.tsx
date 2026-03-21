//@ts-nocheck

"use client";

import { Card } from "@/components/ui/card";
import { Tooltip } from "@/components/ui/tooltip";
import { Info } from "lucide-react";

interface MetricCardProps {
  label: string;
  value: string | number;
  description?: string;
  trend?: number;
  icon?: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
}

export function MetricCard({ 
  label, 
  value, 
  description, 
  trend, 
  icon, 
  footer,
  className 
}: MetricCardProps) {
  return (
    <Card className={`p-4 relative ${className}`}>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {icon}
          <h4 className="text-sm font-medium text-muted-foreground">{label}</h4>
          {description && (
            <Tooltip content={description}>
              <Info className="h-4 w-4 text-muted-foreground cursor-help" />
            </Tooltip>
          )}
        </div>
      </div>
      <div className="flex items-baseline gap-2 mb-2">
        <p className="text-2xl font-bold">{value}</p>
        {trend !== undefined && (
          <span className={`text-sm ${trend >= 0 ? 'text-green-500' : 'text-red-500'}`}>
            {trend > 0 ? '+' : ''}{trend}%
          </span>
        )}
      </div>
      {footer && <div className="mt-2">{footer}</div>}
    </Card>
  );
}