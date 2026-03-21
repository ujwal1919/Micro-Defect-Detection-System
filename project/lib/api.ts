import type { Analysis } from "@/types/analysis";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function analyzeImage(file: File): Promise<Analysis> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/api/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to analyze image");
  }

  return response.json();
}