import { Metrics } from "@/types/analysis";
import { Card } from "@/components/ui/card";



export function DefectMetrics({ metrics }: any) {
  return (
    <div className="grid gap-4">
      {/* Classification Performance */}
      <Card className="p-4">
        <h3 className="font-semibold mb-3">Classification Performance</h3>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <span className="text-sm text-muted-foreground">Accuracy</span>
            <p className="text-lg font-medium">{(metrics.accuracy * 100).toFixed(1)}%</p>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">F1 Score</span>
            <p className="text-lg font-medium">{(metrics.f1_score * 100).toFixed(1)}%</p>
          </div>
        </div>
      </Card>

      {/* Quality Metrics */}
      <Card className="p-4">
        <h3 className="font-semibold mb-3">Quality Assessment</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-sm text-muted-foreground">Quality Score</span>
            <p className="text-lg font-medium">{metrics.quality_score.toFixed(1)}%</p>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">Reliability</span>
            <p className="text-lg font-medium">{metrics.reliability.toFixed(1)}%</p>
          </div>
        </div>
      </Card>

      {/* Detailed Performance */}
      <Card className="p-4">
        <h3 className="font-semibold mb-3">Detailed Performance</h3>
        <div className="space-y-2">
          <div>
            <span className="text-sm text-muted-foreground">Soldering Quality</span>
            <p className="text-lg font-medium">
              {metrics.detailed_performance.soldering_quality.toFixed(1)}%
            </p>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">Alignment Accuracy</span>
            <p className="text-lg font-medium">
              {metrics.detailed_performance.alignment_accuracy.toFixed(1)}%
            </p>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">Surface Finish</span>
            <p className="text-lg font-medium">
              {metrics.detailed_performance.surface_finish.toFixed(1)}%
            </p>
          </div>
        </div>
      </Card>

      {/* Severity Levels */}
      <Card className="p-4">
        <h3 className="font-semibold mb-3">Defect Severity</h3>
        <div className="grid grid-cols-3 gap-2">
          <div>
            <span className="text-sm text-muted-foreground">Critical</span>
            <p className="text-lg font-medium text-red-500">
              {metrics.severity_levels.critical}
            </p>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">Moderate</span>
            <p className="text-lg font-medium text-yellow-500">
              {metrics.severity_levels.moderate}
            </p>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">Minor</span>
            <p className="text-lg font-medium text-blue-500">
              {metrics.severity_levels.minor}
            </p>
          </div>
        </div>
      </Card>

      {/* Confidence Metrics */}
      <Card className="p-4">
        <h3 className="font-semibold mb-3">Confidence Metrics</h3>
        <div className="space-y-2">
          <div>
            <span className="text-sm text-muted-foreground">Mean Confidence</span>
            <p className="text-lg font-medium">
              {metrics.confidence_intervals.mean_confidence.toFixed(1)}%
            </p>
          </div>
          <div>
            <span className="text-sm text-muted-foreground">95% Confidence</span>
            <p className="text-lg font-medium">
              {metrics.confidence_intervals.confidence_95.toFixed(1)}%
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
} 