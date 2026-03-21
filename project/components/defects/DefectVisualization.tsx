"use client";

import { useState, useEffect, useRef } from 'react';
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Analysis, Defect } from "@/types/analysis";
import { DEFECT_TYPES } from "@/lib/constants/defectTypes";
import { Badge } from "@/components/ui/badge";
import Image from "next/image";
import { motion } from 'framer-motion';

interface DefectVisualizationProps {
  analysis: Analysis;
  selectedDefect?: Defect;
  onDefectSelect?: (defect: Defect) => void;
}

interface LabelPosition {
  x: number;
  y: number;
  width: number;
  height: number;
  position: 'top' | 'bottom' | 'left' | 'right';
}

export function DefectVisualization({ analysis, selectedDefect, onDefectSelect }: DefectVisualizationProps) {
  const [activeTab, setActiveTab] = useState("annotated");
  const [hoveredDefect, setHoveredDefect] = useState<Defect | null>(null);
  const [labelPositions, setLabelPositions] = useState<Map<number, LabelPosition>>(new Map());
  const containerRef = useRef<HTMLDivElement>(null);

  const getDefectLabel = (defect: Defect) => {
    const normalizedType = defect.type.toUpperCase().replace(/ /g, "_") as keyof typeof DEFECT_TYPES;
    const defectInfo = DEFECT_TYPES[normalizedType];
    return defectInfo?.label || defect.type;
  };

  // Check if two rectangles overlap
  const doRectsOverlap = (rect1: LabelPosition, rect2: LabelPosition) => {
    return !(rect1.x + rect1.width < rect2.x ||
           rect2.x + rect2.width < rect1.x ||
           rect1.y + rect1.height < rect2.y ||
           rect2.y + rect2.height < rect1.y);
  };

  // Find a non-overlapping position for the label
  const findNonOverlappingPosition = (
    bbox: { x: number; y: number; width: number; height: number },
    defectIndex: number,
    existingPositions: Map<number, LabelPosition>,
    containerWidth: number,
    containerHeight: number
  ): LabelPosition => {
    const LABEL_WIDTH = 160;  // Estimated label width in pixels
    const LABEL_HEIGHT = 80;  // Estimated label height in pixels
    const MARGIN = 20;
    
    // Convert bbox percentages to pixels
    const bboxPixels = {
      x: (bbox.x * containerWidth) / 100,
      y: (bbox.y * containerHeight) / 100,
      width: (bbox.width * containerWidth) / 100,
      height: (bbox.height * containerHeight) / 100
    };

    // Possible positions to try
    const positions: Array<'top' | 'bottom' | 'left' | 'right'> = ['top', 'right', 'bottom', 'left'];
    
    for (const pos of positions) {
      let candidatePos: LabelPosition;
      
      switch (pos) {
        case 'top':
          candidatePos = {
            x: bboxPixels.x + (bboxPixels.width / 2) - (LABEL_WIDTH / 2),
            y: bboxPixels.y - LABEL_HEIGHT - MARGIN,
            width: LABEL_WIDTH,
            height: LABEL_HEIGHT,
            position: 'top'
          };
          break;
        case 'bottom':
          candidatePos = {
            x: bboxPixels.x + (bboxPixels.width / 2) - (LABEL_WIDTH / 2),
            y: bboxPixels.y + bboxPixels.height + MARGIN,
            width: LABEL_WIDTH,
            height: LABEL_HEIGHT,
            position: 'bottom'
          };
          break;
        case 'left':
          candidatePos = {
            x: bboxPixels.x - LABEL_WIDTH - MARGIN,
            y: bboxPixels.y + (bboxPixels.height / 2) - (LABEL_HEIGHT / 2),
            width: LABEL_WIDTH,
            height: LABEL_HEIGHT,
            position: 'left'
          };
          break;
        case 'right':
          candidatePos = {
            x: bboxPixels.x + bboxPixels.width + MARGIN,
            y: bboxPixels.y + (bboxPixels.height / 2) - (LABEL_HEIGHT / 2),
            width: LABEL_WIDTH,
            height: LABEL_HEIGHT,
            position: 'right'
          };
          break;
      }

      // Keep label within container bounds
      candidatePos.x = Math.max(MARGIN, Math.min(containerWidth - LABEL_WIDTH - MARGIN, candidatePos.x));
      candidatePos.y = Math.max(MARGIN, Math.min(containerHeight - LABEL_HEIGHT - MARGIN, candidatePos.y));

      // Check if this position overlaps with any existing labels
      let hasOverlap = false;
      for (const [otherIndex, otherPos] of existingPositions.entries()) {
        if (otherIndex !== defectIndex && doRectsOverlap(candidatePos, otherPos)) {
          hasOverlap = true;
          break;
        }
      }

      if (!hasOverlap) {
        // Convert back to percentages
        return {
          x: (candidatePos.x / containerWidth) * 100,
          y: (candidatePos.y / containerHeight) * 100,
          width: (LABEL_WIDTH / containerWidth) * 100,
          height: (LABEL_HEIGHT / containerHeight) * 100,
          position: candidatePos.position
        };
      }
    }

    // If all positions overlap, return the top position as fallback
    return {
      x: (bbox.x + bbox.width / 2),
      y: bbox.y - 10,
      width: (LABEL_WIDTH / containerWidth) * 100,
      height: (LABEL_HEIGHT / containerHeight) * 100,
      position: 'top'
    };
  };

  // Update label positions when hovering or selecting defects
  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const { width, height } = container.getBoundingClientRect();
    const newPositions = new Map<number, LabelPosition>();

    analysis.defects.forEach((defect, index) => {
      // @ts-ignore
      if (!defect.bbox) return;
      if (defect === selectedDefect || defect === hoveredDefect) {
        const position = findNonOverlappingPosition(
          // @ts-ignore
          defect.bbox,
          index,
          newPositions,
          width,
          height
        );
        newPositions.set(index, position);
      }
    });

    setLabelPositions(newPositions);
  }, [selectedDefect, hoveredDefect, analysis.defects]);

  const DefectOverlay = ({ defect, isSelected, index }: { defect: Defect; isSelected: boolean; index: number }) => {
    if (!defect.bbox) return null;
  
    const isHighlighted = isSelected || hoveredDefect === defect;
    const labelPosition = labelPositions.get(index);
  
    return (
      <>
        {/* Bounding box */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: index * 0.1 }}
          className="absolute cursor-pointer"
          style={{
            left: `${defect.bbox.x}%`,
            top: `${defect.bbox.y}%`,
            width: `${defect.bbox.width}%`,
            height: `${defect.bbox.height}%`,
          }}
          onMouseEnter={() => setHoveredDefect(defect)}
          onMouseLeave={() => setHoveredDefect(null)}
        >
          <div
            className={`
              absolute 
              inset-0 
              ${isHighlighted ? 'border-[6px]' : 'border-4'} 
              border-[#8659ff] 
              shadow-lg
              shadow-[#8659ff]/20
              transition-all
              duration-200
              rounded-md
              ${isHighlighted ? 'bg-[#8659ff]/20' : 'bg-transparent'}
            `}
          />
        </motion.div>

        {/* Label */}
        {isHighlighted && labelPosition && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="absolute z-50 pointer-events-none"
            style={{
              left: `${labelPosition.x}%`,
              top: `${labelPosition.y}%`,
              width: `${labelPosition.width}%`,
            }}
          >
            <div className="p-[6px] bg-[#2d1159]/95 rounded-xl backdrop-blur-md border border-[#8659ff]/20">
              <div className="relative bg-[#2d1159]/80 text-[#c4b1ff] px-4 py-3 rounded-lg shadow-2xl border-2 border-[#8659ff]">
                {/* Connector line */}
                <div
                  className={`
                    absolute
                    ${labelPosition.position === 'top' ? 'bottom-0 left-1/2 -mb-8 w-2 h-8' :
                      labelPosition.position === 'bottom' ? 'top-0 left-1/2 -mt-8 w-2 h-8' :
                      labelPosition.position === 'left' ? 'right-0 top-1/2 -mr-8 w-8 h-2' :
                      'left-0 top-1/2 -ml-8 w-8 h-2'}
                    bg-blue-400
                    transform
                    ${labelPosition.position === 'top' || labelPosition.position === 'bottom' ? '-translate-x-1/2' : '-translate-y-1/2'}
                  `}
                />
                
                <div className="flex flex-col gap-2">
                  <span className="font-semibold text-base whitespace-nowrap">
                    {getDefectLabel(defect)}
                  </span>
                  <Badge
                    variant="outline"
                    className={`
                      w-fit
                      text-sm
                      font-medium
                      px-2.5
                      py-1
                      ${String(defect.severity).toLowerCase() === 'critical' 
                        ? 'bg-red-500/30 border-2 border-red-400 text-red-200' 
                        : String(defect.severity).toLowerCase() === 'moderate'
                        ? 'bg-yellow-500/30 border-2 border-yellow-400 text-yellow-200'
                        : 'bg-blue-500/30 border-2 border-blue-400 text-blue-200'
                      }
                    `}
                  >
                    {defect.severity}
                  </Badge>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </>
    );
  };

  // Rest of the component remains the same
  return (
    <div className="flex gap-4">
      <Card className="flex-1 p-6 bg-[#2d1159]/50 backdrop-blur-sm border border-[#8659ff]/20">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold bg-gradient-to-r from-[#a587ff] to-[#6c3aed] bg-clip-text text-transparent">
            PCB Defect Analysis
          </h3>
          <Badge variant="outline" className="text-[#c4b1ff] border-[#8659ff]/40">
            {analysis.defects.length} Defects Found
          </Badge>
        </div>
        
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="mb-4 bg-[#2d1159]/30">
            <TabsTrigger 
              value="annotated"
              className="data-[state=active]:bg-[#8659ff] data-[state=active]:text-white text-[#a587ff]"
            >
              Annotated Image
            </TabsTrigger>
            <TabsTrigger 
              value="heatmap"
              className="data-[state=active]:bg-[#8659ff] data-[state=active]:text-white text-[#a587ff]"
            >
              Defect Heatmap
            </TabsTrigger>
          </TabsList>

          <TabsContent value="annotated" className="mt-4">
            {analysis.annotatedImage ? (
              <div className="relative w-full h-[600px] overflow-hidden rounded-lg bg-black">
                <Image
                  src={`data:image/jpeg;base64,${analysis.annotatedImage}`}
                  alt="PCB defect analysis"
                  width={800} 
                  height={600} 
                  className="w-full h-full object-contain"
                  />
                <div className="absolute inset-0">
                  {analysis.defects.map((defect, index) => (
                    <DefectOverlay
                      key={index}
                      // @ts-ignore
                      defect={defect}
                      isSelected={defect === selectedDefect}
                      index={index}
                    />
                  ))}
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-[600px] bg-muted/20 rounded-lg">
                <span className="text-muted-foreground">No annotated image available</span>
              </div>
            )}
          </TabsContent>

          <TabsContent value="heatmap" className="mt-4">
            {analysis.heatmap ? (
              <div className="w-full h-[600px] overflow-hidden rounded-lg bg-black">
                <Image
                  src={`data:image/jpeg;base64,${analysis.heatmap}`}
                  alt="PCB defect heatmap"
                  className="w-full h-full object-contain"
                  width={500}                
                  height={300}                     
                />
              </div>
            ) : (
              <div className="flex items-center justify-center h-[600px] bg-muted/20 rounded-lg">
                <span className="text-muted-foreground">No heatmap available</span>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </Card>

      
    </div>
  );
}

export default DefectVisualization;