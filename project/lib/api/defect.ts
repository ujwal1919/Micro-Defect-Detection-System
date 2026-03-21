import type { Analysis } from "@/types/analysis";
import { handleApiError } from "@/lib/utils/error";

export async function analyzeImage(file: File): Promise<Analysis> {
  try {
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch("/api/analyze", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Failed to analyze image");
    }

    const data = await response.json();
    return validateAnalysisResponse(data);
  } catch (error) {
    throw handleApiError(error, "Failed to analyze image");
  }
}

function validateAnalysisResponse(data: any): Analysis {
  if (!data || typeof data !== "object") {
    throw new Error("Invalid response format");
  }

  const requiredFields = [
    "criticalDefects",
    "minorDefects",
    "passRate",
    "defects",
    "metrics",
    "recommendations",
  ];

  for (const field of requiredFields) {
    if (!(field in data)) {
      throw new Error(`Missing required field: ${field}`);
    }
  }

  return data as Analysis;
}