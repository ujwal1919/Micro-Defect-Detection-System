import { NextResponse } from "next/server";
import type { Analysis } from "@/types/analysis";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function POST(req: Request) {
  try {
    const formData = await req.formData();
    const file = formData.get("image") as File;

    if (!file) {
      return NextResponse.json(
        { error: "No image file provided" },
        { status: 400 }
      );
    }

    // Validate file type
    if (!file.type.startsWith("image/")) {
      return NextResponse.json(
        { error: "Invalid file type. Please upload an image file." },
        { status: 400 }
      );
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      return NextResponse.json(
        { error: "File size exceeds 10MB limit." },
        { status: 400 }
      );
    }

    const backendFormData = new FormData();
    backendFormData.append("file", file);

    const response = await fetch(`${API_URL}/api/analyze`, {
      method: "POST",
      body: backendFormData,
    });

    if (!response.ok) {
      const error = await response.json();
      return NextResponse.json(
        { error: error.detail || "Analysis failed" },
        { status: response.status }
      );
    }

    const analysis: Analysis = await response.json();
    return NextResponse.json(analysis);
  } catch (error) {
    console.error("Error in analyze route:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}