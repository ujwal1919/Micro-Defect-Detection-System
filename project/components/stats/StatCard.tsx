"use client";

import { Card } from "@/components/ui/card";
import { LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value: number | string;
  icon: LucideIcon;
  color: string;
}

export function StatCard({ label, value, icon: Icon, color }: StatCardProps) {
  return (
    <Card className="p-4 flex flex-col items-center justify-center">
      <Icon className={`h-8 w-8 ${color} mb-2`} />
      <p className="text-sm font-medium text-muted-foreground">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
    </Card>
  );
}