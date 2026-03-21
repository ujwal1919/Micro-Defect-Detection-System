# HARDWARE REQUIREMENTS FOR PCB DEFECT DETECTION PROJECT

## MINIMUM HARDWARE REQUIREMENTS

### **Processor (CPU)**
- **Minimum**: Intel Core i5 (7th Generation) or AMD Ryzen 5 (Equivalent)
- **Clock Speed**: 2.5 GHz or higher
- **Cores**: Quad-core (4 cores) or better
- **Purpose**: Running backend server, image processing, and model inference

### **Memory (RAM)**
- **Minimum**: 8 GB
- **Recommended**: 16 GB or higher
- **Purpose**: 
  - Storing image data in memory
  - Running Python backend with PyTorch models
  - Running Next.js frontend server
  - Loading pre-trained models (ResNet18/ResNet50)

### **Storage**
- **Minimum**: 20 GB free space
- **Recommended**: 50 GB or higher (SSD preferred)
- **Purpose**:
  - Installing Python packages and dependencies (~5 GB)
  - Installing Node.js and npm packages (~2 GB)
  - Storing trained models (~1-2 GB per model)
  - Storing dataset images (varies, can be 10+ GB)
  - Operating system and other software

### **Graphics Card (GPU) - Optional but Recommended**
- **For Training**: NVIDIA GPU with CUDA support
  - Minimum: NVIDIA GTX 1050 Ti or better
  - Recommended: NVIDIA RTX 3060 or better
  - VRAM: 4 GB minimum, 8 GB recommended
- **For Inference Only**: CPU is sufficient (GPU not required)
- **Purpose**: 
  - Accelerating model training (10-100x faster with GPU)
  - Faster image processing during training
  - Optional for deployment (CPU works fine)

### **Display**
- **Minimum**: 1366 x 768 resolution
- **Recommended**: 1920 x 1080 (Full HD) or higher
- **Purpose**: Viewing the web interface and defect visualization

### **Input/Output**
- **Mouse and Keyboard**: Standard input devices
- **Network**: 
  - Internet connection for downloading dependencies
  - Local network for accessing the web application

---

## RECOMMENDED HARDWARE REQUIREMENTS (For Best Performance)

### **Processor (CPU)**
- **Recommended**: Intel Core i7 (10th Generation+) or AMD Ryzen 7 (Equivalent)
- **Clock Speed**: 3.0 GHz or higher
- **Cores**: 6-8 cores or better
- **Benefits**: Faster image processing and model inference

### **Memory (RAM)**
- **Recommended**: 16 GB or 32 GB
- **Benefits**: 
  - Can process larger images
  - Faster model loading
  - Smooth multitasking

### **Storage**
- **Recommended**: 256 GB SSD or higher
- **Benefits**: 
  - Faster application startup
  - Quicker model loading
  - Better overall performance

### **Graphics Card (GPU) - Highly Recommended**
- **Recommended**: NVIDIA RTX 3060, RTX 3070, or better
- **VRAM**: 8 GB or higher
- **CUDA**: Version 11.0 or higher
- **Benefits**: 
  - Model training 50-100x faster
  - Real-time defect detection
  - Can train larger models

### **Display**
- **Recommended**: 1920 x 1080 (Full HD) or 2560 x 1440 (2K)
- **Benefits**: Better visualization of defect details

---

## HARDWARE REQUIREMENTS EXPLAINED (SIMPLE WAY)

### 1. **PROCESSOR (CPU) - The Brain**
**What it is**: The main processing unit of your computer.

**Why we need it**: 
- Runs all the code (Python backend, frontend server)
- Processes images (OpenCV operations)
- Executes AI model predictions
- Handles multiple operations simultaneously

**Simple Analogy**: Like the engine of a car - more powerful = faster performance.

**For our project**: 
- **Minimum**: Can run the application but slower
- **Recommended**: Faster image processing and defect detection

---

### 2. **MEMORY (RAM) - The Workspace**
**What it is**: Temporary storage that holds data while programs are running.

**Why we need it**: 
- Stores uploaded images in memory
- Loads AI models (ResNet models are large - 50-100 MB each)
- Keeps multiple programs running (backend + frontend)
- Holds image processing data (arrays, calculations)

**Simple Analogy**: Like a desk - bigger desk = more papers you can work with at once.

**For our project**:
- **8 GB**: Works but might be slow when processing large images
- **16 GB**: Comfortable for most operations
- **32 GB**: Best for training models and processing multiple images

---

### 3. **STORAGE (Hard Drive/SSD) - The Filing Cabinet**
**What it is**: Permanent storage for files, programs, and data.

**Why we need it**: 
- Stores all software installations
- Saves trained AI models
- Stores dataset images
- Keeps project files and code

**Simple Analogy**: Like a filing cabinet - stores everything permanently.

**For our project**:
- **HDD**: Works but slower
- **SSD (Recommended)**: Much faster - programs start quickly, models load faster

---

### 4. **GRAPHICS CARD (GPU) - The Accelerator (Optional)**
**What it is**: Specialized processor designed for graphics and parallel computing.

**Why we need it**: 
- **Training Models**: Makes training 50-100x faster (instead of hours, takes minutes)
- **Real-time Processing**: Can process images very quickly
- **Parallel Processing**: Can do many calculations at once

**Simple Analogy**: Like a turbocharger - not necessary, but makes everything much faster.

**For our project**:
- **Not Required**: CPU can do everything, just slower
- **Highly Recommended**: If you want to train models or process images quickly
- **NVIDIA GPU**: Required for PyTorch CUDA support

**Note**: GPU is only useful if you have CUDA-compatible NVIDIA GPU. AMD GPUs don't work with PyTorch CUDA.

---

### 5. **DISPLAY - The Monitor**
**What it is**: Your computer screen.

**Why we need it**: 
- View the web application interface
- See defect detection results
- Visualize graphs and charts
- View defect annotations on images

**Simple Analogy**: Like a TV screen - you need it to see what's happening.

**For our project**: Any standard monitor works. Higher resolution = better visualization.

---

### 6. **NETWORK CONNECTION**
**What it is**: Internet or local network connection.

**Why we need it**: 
- **During Setup**: Download Python packages, Node.js packages, model weights
- **During Development**: Access online resources, documentation
- **During Deployment**: Users access the web application
- **Optional**: Can work offline once everything is installed

**Simple Analogy**: Like a phone line - needed to call (download), but not needed after installation.

---

## HARDWARE REQUIREMENTS BY USE CASE

### **For Development Only (Writing Code)**
- **CPU**: Intel Core i5 or equivalent
- **RAM**: 8 GB
- **Storage**: 20 GB
- **GPU**: Not required
- **Suitable for**: Writing code, testing with small images

### **For Testing & Demo (Running Application)**
- **CPU**: Intel Core i5 or better
- **RAM**: 8-16 GB
- **Storage**: 30 GB
- **GPU**: Not required
- **Suitable for**: Running the application, detecting defects in uploaded images

### **For Model Training**
- **CPU**: Intel Core i7 or better
- **RAM**: 16 GB or higher
- **Storage**: 50 GB or higher
- **GPU**: NVIDIA RTX 3060 or better (Highly Recommended)
- **Suitable for**: Training new models, processing large datasets

### **For Production Deployment (Server)**
- **CPU**: Intel Xeon or AMD EPYC (Multiple cores)
- **RAM**: 32 GB or higher
- **Storage**: 100 GB+ SSD
- **GPU**: Optional (can use CPU for inference)
- **Suitable for**: Handling multiple users, high availability

---

## PERFORMANCE COMPARISON

### **Training Time Examples (with different hardware)**

| Hardware Configuration | Training Time (10 epochs) |
|------------------------|---------------------------|
| CPU Only (Intel i5) | 2-4 hours |
| CPU Only (Intel i7) | 1-2 hours |
| GPU (GTX 1050 Ti) | 20-30 minutes |
| GPU (RTX 3060) | 5-10 minutes |
| GPU (RTX 3090) | 3-5 minutes |

**Note**: GPU training is 50-100x faster than CPU!

### **Inference Time (Detecting Defects)**
- **CPU**: 1-3 seconds per image
- **GPU**: 0.1-0.5 seconds per image

---

## MINIMUM SYSTEM SPECIFICATIONS (SUMMARY)

```
┌─────────────────────────────────────────┐
│  MINIMUM REQUIREMENTS                   │
├─────────────────────────────────────────┤
│  CPU:      Intel i5 / AMD Ryzen 5       │
│  RAM:      8 GB                         │
│  Storage:  20 GB (HDD okay)             │
│  GPU:      Not required                 │
│  OS:       Windows 10/11, Linux, macOS  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  RECOMMENDED REQUIREMENTS               │
├─────────────────────────────────────────┤
│  CPU:      Intel i7 / AMD Ryzen 7       │
│  RAM:      16 GB                        │
│  Storage:  50 GB SSD                    │
│  GPU:      NVIDIA RTX 3060+ (Optional)  │
│  OS:       Windows 10/11, Linux, macOS  │
└─────────────────────────────────────────┘
```

---

## OPERATING SYSTEM REQUIREMENTS

### **Supported Operating Systems**
- **Windows**: Windows 10 (64-bit) or Windows 11
- **Linux**: Ubuntu 20.04+, Debian 11+, CentOS 8+
- **macOS**: macOS 10.15 (Catalina) or later

### **System Requirements**
- **Architecture**: 64-bit (x64) required
- **Administrator Rights**: Required for software installation
- **Internet**: Required for initial setup (downloading dependencies)

---

## NETWORK REQUIREMENTS

### **For Development**
- **Internet Connection**: Required for downloading packages and dependencies
- **Bandwidth**: Minimum 5 Mbps (for downloading large packages)
- **Ports**: 
  - Port 3000: Frontend server (Next.js)
  - Port 8000: Backend API (FastAPI)
  - These ports should be available

### **For Deployment**
- **Local Network**: For local deployment
- **Public IP**: For remote access (if needed)
- **Firewall**: Configure to allow traffic on ports 3000 and 8000

---

## ADDITIONAL HARDWARE (OPTIONAL)

### **For Enhanced Experience**
- **Webcam**: For real-time image capture (optional feature)
- **Printer**: For printing defect reports (optional)
- **Multiple Monitors**: For better development experience (optional)

---

## HARDWARE CHECKLIST

### **Essential Components** ✅
- [ ] CPU (Processor)
- [ ] RAM (Memory)
- [ ] Storage (Hard Drive/SSD)
- [ ] Display (Monitor)
- [ ] Mouse and Keyboard
- [ ] Internet Connection (for setup)

### **Optional but Recommended** ⭐
- [ ] NVIDIA GPU with CUDA support (for training)
- [ ] SSD instead of HDD (for faster performance)
- [ ] Extra RAM (16 GB+) (for better multitasking)
- [ ] High-resolution monitor (for better visualization)

---

## ESTIMATED COST (REFERENCE)

### **Minimum Setup**
- **Used/Entry-Level PC**: $300-500
- **Suitable for**: Basic development and testing

### **Recommended Setup**
- **Mid-Range PC**: $800-1200
- **Suitable for**: Development, testing, and moderate training

### **High-Performance Setup**
- **Gaming/Workstation PC**: $1500-3000
- **Suitable for**: Fast training, production deployment

---

*This document lists all hardware requirements for the PCB Defect Detection project.*

