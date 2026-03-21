from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
import io
import uvicorn
import logging
from defect_detection import DefectDetector
from image_processor import ImageProcessor
from analysis_engine import AnalysisEngine
from visualization import DefectVisualizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
defect_detector = DefectDetector()
image_processor = ImageProcessor()
analysis_engine = AnalysisEngine()
visualizer = DefectVisualizer()

@app.post("/api/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload an image file."
            )
        
        # Read image file
        contents = await file.read()
        try:
            image = Image.open(io.BytesIO(contents))
        except UnidentifiedImageError:
            raise HTTPException(
                status_code=400,
                detail="Could not process image file. Please ensure it's a valid image."
            )
        
        # Convert to RGB if needed
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Process image
        logger.info("Preprocessing image...")
        processed_image = image_processor.preprocess(image)
        
        # Detect defects
        logger.info("Detecting defects...")
        defects = defect_detector.detect(processed_image)
        
        # Create visualizations
        logger.info("Creating visualizations...")
        visualizations = visualizer.create_visualization(processed_image, defects)
        
        # Analyze defects
        logger.info("Analyzing defects...")
        analysis = analysis_engine.analyze(defects)
        
        # Add visualizations to analysis
        analysis["annotatedImage"] = visualizations["annotated"]
        analysis["heatmap"] = visualizations["heatmap"]
        
        return JSONResponse(content=analysis)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

if __name__ == "__main__":
    logger.info("Starting API server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)