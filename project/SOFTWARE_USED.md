# COMPLETE LIST OF SOFTWARE USED IN PCB DEFECT DETECTION PROJECT

## 📋 PROJECT OVERVIEW
**Project Name**: Micro Defect Detection For Pure Performance Production In Neural Network Chip  
**Type**: Full-Stack AI/ML Web Application  
**Architecture**: Frontend (Next.js) + Backend (FastAPI) + AI/ML (PyTorch)

---

## 🖥️ PROGRAMMING LANGUAGES

### 1. **Python 3.13**
- **Purpose**: Backend API, AI/ML model training, image processing
- **Used for**: Server-side logic, defect detection algorithms, deep learning

### 2. **TypeScript/JavaScript**
- **Purpose**: Frontend development
- **TypeScript**: Type-safe frontend code
- **JavaScript**: Runtime execution

### 3. **JSON**
- **Purpose**: Configuration files, API responses

---

## 🤖 DEEP LEARNING & AI FRAMEWORKS

### 1. **PyTorch (torch) - Version 1.9.0**
- **Purpose**: Deep learning framework
- **Usage**: 
  - Creating neural network models
  - Training CNN models for defect detection
  - Model inference and predictions
- **Key Features Used**:
  - Neural network layers (nn.Module)
  - Optimization (Adam optimizer)
  - Loss functions (CrossEntropyLoss)
  - GPU/CPU computation

### 2. **TorchVision - Version 0.10.0**
- **Purpose**: Pre-trained models and image transforms
- **Usage**:
  - ResNet18, ResNet50 architectures
  - Image preprocessing transforms
  - Transfer learning (ImageNet weights)
- **Key Models Used**:
  - ResNet18 (for quick training)
  - ResNet50 (for accuracy)

### 3. **Transfer Learning**
- **Purpose**: Using pre-trained ImageNet models
- **Benefit**: Faster training, better accuracy

---

## 🖼️ COMPUTER VISION LIBRARIES

### 1. **OpenCV (opencv-python) - Version 4.5.3.56**
- **Purpose**: Image processing and defect detection
- **Usage**:
  - Image thresholding (OTSU, Binary)
  - Edge detection (Canny)
  - Contour analysis
  - Hough transforms (circles, lines)
  - Connected components analysis
  - Image filtering and preprocessing
- **Algorithms Used**:
  - **Canny Edge Detection**: For detecting circuit traces
  - **Hough Circle Transform**: For detecting missing holes
  - **Hough Line Transform**: For detecting spurs and open circuits
  - **Connected Components**: For short circuit detection
  - **Contour Analysis**: For shape analysis (mouse bites, spurious copper)

### 2. **Pillow (PIL) - Version 8.3.2**
- **Purpose**: Image manipulation and processing
- **Usage**:
  - Opening image files (JPG, PNG)
  - Converting image formats
  - Resizing images
  - Image color space conversion (RGB)

---

## 🔢 SCIENTIFIC COMPUTING

### 1. **NumPy - Version 1.21.2**
- **Purpose**: Numerical computations
- **Usage**:
  - Array operations
  - Mathematical calculations
  - Image data manipulation
  - Statistical analysis (mean, std, diff)

---

## 🌐 BACKEND FRAMEWORK

### 1. **FastAPI - Version 0.68.1**
- **Purpose**: Modern Python web framework for building APIs
- **Usage**:
  - RESTful API endpoints
  - File upload handling
  - JSON response formatting
  - Request validation
- **Key Features**:
  - Async/await support
  - Automatic API documentation
  - Type hints and validation

### 2. **Uvicorn - Version 0.15.0**
- **Purpose**: ASGI web server
- **Usage**: Running FastAPI application
- **Server**: HTTP server for backend API

### 3. **Python-multipart - Version 0.0.5**
- **Purpose**: File upload support
- **Usage**: Handling image file uploads from frontend

---

## 🎨 FRONTEND FRAMEWORK & LIBRARIES

### 1. **Next.js - Version 13.5.1**
- **Purpose**: React framework for production
- **Usage**: 
  - Server-side rendering
  - API routes
  - Page routing
  - Build optimization
- **Features Used**:
  - App Router
  - Server Components
  - Static generation

### 2. **React - Version 18.2.0**
- **Purpose**: UI library for building user interfaces
- **Usage**: Component-based UI development

### 3. **React DOM - Version 18.2.0**
- **Purpose**: React rendering for web browsers

---

## 🎨 UI COMPONENTS & STYLING

### 1. **Tailwind CSS - Version 3.3.3**
- **Purpose**: Utility-first CSS framework
- **Usage**: Styling and responsive design

### 2. **tailwindcss-animate - Version 1.0.7**
- **Purpose**: Animation utilities for Tailwind

### 3. **Radix UI Components**
- **Purpose**: Unstyled, accessible UI components
- **Components Used**:
  - Accordion, Alert Dialog, Avatar
  - Checkbox, Dialog, Dropdown Menu
  - Progress, Select, Slider, Tabs
  - Toast, Tooltip, and many more

### 4. **shadcn/ui**
- **Purpose**: Component library built on Radix UI
- **Usage**: Pre-built, customizable UI components

### 5. **Framer Motion - Version 11.15.0**
- **Purpose**: Animation library for React
- **Usage**: Smooth animations and transitions

### 6. **Lucide React - Version 0.446.0**
- **Purpose**: Icon library
- **Usage**: UI icons throughout the application

---

## 📊 DATA VISUALIZATION

### 1. **Chart.js - Version 4.4.7**
- **Purpose**: JavaScript charting library
- **Usage**: Creating charts and graphs

### 2. **react-chartjs-2 - Version 5.2.0**
- **Purpose**: React wrapper for Chart.js
- **Usage**: React components for charts

### 3. **Recharts - Version 2.15.0**
- **Purpose**: Composable charting library
- **Usage**: Defect statistics and trends visualization

### 4. **react-circular-progressbar - Version 2.1.0**
- **Purpose**: Circular progress indicators
- **Usage**: Displaying confidence scores, metrics

---

## 📝 FORM HANDLING & VALIDATION

### 1. **React Hook Form - Version 7.53.0**
- **Purpose**: Form state management
- **Usage**: Handling user inputs

### 2. **@hookform/resolvers - Version 3.9.0**
- **Purpose**: Form validation resolvers

### 3. **Zod - Version 3.23.8**
- **Purpose**: TypeScript-first schema validation
- **Usage**: Form validation and type checking

---

## 🔔 NOTIFICATIONS & UI FEEDBACK

### 1. **Sonner - Version 1.5.0**
- **Purpose**: Toast notification library
- **Usage**: User feedback messages

---

## 🎯 UTILITY LIBRARIES

### 1. **clsx - Version 2.1.1**
- **Purpose**: Conditional className utility

### 2. **tailwind-merge - Version 2.5.2**
- **Purpose**: Merge Tailwind CSS classes

### 3. **class-variance-authority - Version 0.7.0**
- **Purpose**: Component variant management

### 4. **date-fns - Version 3.6.0**
- **Purpose**: Date utility library
- **Usage**: Date formatting and manipulation

---

## 🛠️ DEVELOPMENT TOOLS

### 1. **TypeScript - Version 5.2.2**
- **Purpose**: Type-safe JavaScript
- **Usage**: Frontend type checking

### 2. **ESLint - Version 8.49.0**
- **Purpose**: JavaScript/TypeScript linting
- **Usage**: Code quality checking

### 3. **PostCSS - Version 8.4.30**
- **Purpose**: CSS transformation tool
- **Usage**: Processing Tailwind CSS

### 4. **Autoprefixer - Version 10.4.15**
- **Purpose**: CSS vendor prefixing

---

## 🚀 BUILD & PROCESS MANAGEMENT

### 1. **Concurrently - Version 8.2.2**
- **Purpose**: Run multiple commands concurrently
- **Usage**: Running frontend and backend together

---

## 📦 PACKAGE MANAGERS

### 1. **npm (Node Package Manager)**
- **Purpose**: Managing JavaScript dependencies
- **Usage**: Installing and managing Node.js packages

### 2. **pip (Python Package Installer)**
- **Purpose**: Managing Python dependencies
- **Usage**: Installing Python packages

---

## 🔄 RUNTIME ENVIRONMENTS

### 1. **Node.js**
- **Purpose**: JavaScript runtime
- **Usage**: Running Next.js application

### 2. **Python Runtime**
- **Purpose**: Python execution environment
- **Usage**: Running FastAPI backend

---

## 💾 MODEL STORAGE

### 1. **PyTorch Model Files (.pth)**
- **Files Used**:
  - `quick_trained_model.pth` - Quick trained model
  - `new_trained_model.pth` - New dataset trained model
  - `fast_model_final.pth` - Fast training model
- **Purpose**: Storing trained neural network weights

---

## 🌍 NETWORK & COMMUNICATION

### 1. **CORS (Cross-Origin Resource Sharing)**
- **Purpose**: Allowing frontend-backend communication
- **Implementation**: FastAPI CORS middleware

### 2. **HTTP/HTTPS Protocol**
- **Purpose**: Client-server communication

### 3. **RESTful API**
- **Purpose**: API architecture pattern
- **Endpoints**:
  - POST `/api/analyze` - Image defect analysis

---

## 🔧 SYSTEM & ENVIRONMENT

### 1. **Windows 10/11**
- **Operating System**: Development environment

### 2. **PowerShell**
- **Purpose**: Command-line shell
- **Usage**: Running scripts and commands

---

## 📚 ALGORITHMS & TECHNIQUES USED

### Machine Learning Algorithms:
1. **Convolutional Neural Network (CNN)**
   - ResNet18, ResNet50 architectures
   - Transfer learning
   - Binary classification (Normal vs Defective)

### Computer Vision Algorithms:
1. **Edge Detection** - Canny algorithm
2. **Thresholding** - OTSU, Binary
3. **Hough Transform** - Circle and line detection
4. **Connected Components** - Component analysis
5. **Contour Analysis** - Shape detection
6. **Moment Calculation** - Feature extraction
7. **Pattern Analysis** - Statistical analysis (mean, std)

### Image Processing Techniques:
1. **Image Normalization** - Standardization
2. **Data Augmentation** - Training enhancement
3. **Resizing** - Dimension standardization
4. **Color Space Conversion** - RGB, Grayscale

---

## 📊 SUMMARY BY CATEGORY

### **Backend Technologies:**
- Python, FastAPI, Uvicorn, PyTorch, TorchVision

### **AI/ML Technologies:**
- PyTorch, TorchVision, ResNet, CNN, Transfer Learning

### **Computer Vision:**
- OpenCV, PIL/Pillow, NumPy

### **Frontend Technologies:**
- Next.js, React, TypeScript, Tailwind CSS

### **UI Components:**
- Radix UI, shadcn/ui, Framer Motion

### **Visualization:**
- Chart.js, Recharts, React ChartJS-2

### **Development Tools:**
- TypeScript, ESLint, PostCSS

---

## 🎓 TECHNICAL STACK SUMMARY

**Frontend**: Next.js 13 + React 18 + TypeScript + Tailwind CSS  
**Backend**: FastAPI + Python 3.13  
**AI/ML**: PyTorch + ResNet + OpenCV  
**Styling**: Tailwind CSS + Radix UI  
**Visualization**: Chart.js + Recharts  
**Forms**: React Hook Form + Zod  
**Notifications**: Sonner  

---

*This document lists all software, libraries, frameworks, and tools used in the PCB Defect Detection project.*


