"use client";

import { useState, useCallback } from "react";
import { Upload } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

interface ImageUploaderProps {
  onUpload: (file: File) => void;
}

export default function ImageUploader({ onUpload }: ImageUploaderProps) {
  const [dragActive, setDragActive] = useState(false);
  const { toast } = useToast();

  const validateFile = (file: File): boolean => {
    // Check file type
    if (!file.type.startsWith("image/")) {
      toast({
        title: "Invalid file type",
        description: "Please upload an image file (JPG, PNG)",
        variant: "destructive",
      });
      return false;
    }

    // Check file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast({
        title: "File too large",
        description: "Please upload an image smaller than 10MB",
        variant: "destructive",
      });
      return false;
    }

    return true;
  };

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setDragActive(false);

      const files = e.dataTransfer.files;
      if (files?.[0] && validateFile(files[0])) {
        onUpload(files[0]);
      }
    },
    [onUpload]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      e.preventDefault();
      const files = e.target.files;
      if (files?.[0] && validateFile(files[0])) {
        onUpload(files[0]);
      }
    },
    [onUpload]
  );

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-6 text-center ${
        dragActive ? "border-primary bg-secondary/50" : "border-border"
      }`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        id="image-upload"
        className="hidden"
        accept="image/*"
        onChange={handleChange}
      />
      <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
      <label
        htmlFor="image-upload"
        className="block text-sm font-medium mb-2 cursor-pointer"
      >
        Drop your chip image here or click to upload
      </label>
      <p className="text-xs text-muted-foreground">
        Supports: JPG, PNG (max 10MB)
      </p>
    </div>
  );
}