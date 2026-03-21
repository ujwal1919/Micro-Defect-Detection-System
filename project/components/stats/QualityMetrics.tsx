//@ts-nocheck

"use client";

import { MetricCard } from "./MetricCard";
import { MetricStatus } from "./metrics/MetricStatus";
import { MetricIcons } from "./metrics/MetricIcons";
import { metricConfigurations } from "./metrics/MetricConfig";
import type { DetailedMetrics } from "@/types/analysis";

interface QualityMetricsProps {
  metrics: DetailedMetrics;
}

export function QualityMetrics({ metrics }: QualityMetricsProps) {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {(Object.keys(metrics) as Array<keyof DetailedMetrics>).map((key) => {
          const config = metricConfigurations[key];
          const iconClassName = `h-5 w-5 text-${config.color}-500`;
          const IconComponent = MetricIcons[key.split('_')[0] as keyof typeof MetricIcons];

          return (
            <MetricCard
              key={key}
              label={config.label}
              value={metrics[key]}
              description={config.description}
              icon={IconComponent(iconClassName)}
              footer={
                <MetricStatus
                  value={metrics[key].replace('%', '')}
                  thresholds={config.thresholds}
                />
              }
            />
          );
        })}
      </div>
    </div>
  );
}