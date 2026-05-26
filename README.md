# AI-Based Forest Tree Detection System

## Overview

This project is an AI-based forestry analysis and decision support system developed for a Computer Science bachelor thesis.

The system processes forest walkthrough videos and performs:

- automatic frame extraction
- AI-based tree detection using YOLOv8
- tree tracking
- forest visualization
- CUT / KEEP decision support
- 3D forest mapping
- statistics and report generation

The system is designed as a prototype intelligent forestry automation pipeline for future autonomous forest thinning applications.

---

# Features

- Forest video processing
- Automatic frame extraction
- YOLOv8 tree detection
- Tree tracking with persistent IDs
- CUT / KEEP decision overlay
- Processed output video generation
- Static 3D forest map
- Interactive 3D forest map
- Statistics and report generation
- GUI desktop application

---

# Technologies Used

- Python
- YOLOv8 (Ultralytics)
- OpenCV
- Tkinter
- Plotly
- NumPy
- Matplotlib
- Roboflow

---

# Project Structure

```text
forest/
│
├── forest_gui.py
├── frame_extractor.py
├── tree_detector.py
├── tracker.py
├── map_generator.py
├── interactive_map_generator.py
├── video_generator.py
├── stats_generator.py
│
├── dataset/
├── runs/
├── gui_output/
└── requirements.txt
```

---

# Installation

## 1. Install Python

Recommended version:

```text
Python 3.11
```

---

## 2. Install Required Libraries

Open terminal inside the project folder and run:

```bash
pip install ultralytics opencv-python plotly matplotlib numpy
```

---

# Dataset Structure

The dataset should follow YOLOv8 format:

```text
dataset/
│
├── train/
│   ├── images/
│   └── labels/
│
├── valid/
│   ├── images/
│   └── labels/
│
├── test/
│   ├── images/
│   └── labels/
│
└── data.yaml
```

---

# Model Training

Train the YOLOv8 model using:

```bash
yolo task=detect mode=train model=yolov8n.pt data="dataset/data.yaml" epochs=50 imgsz=640
```

After training, the best model will be saved in:

```text
runs/detect/train/weights/best.pt
```

---

# Running the System

Run the GUI application:

```bash
python forest_gui.py
```

---

# System Workflow

```text
Video Input
→ Frame Extraction
→ Tree Detection
→ Tree Tracking
→ Spatial Analysis
→ CUT / KEEP Decision
→ 3D Mapping
→ Report Generation
```

---

# Output Files

After processing, outputs are saved in:

```text
gui_output/
```

Generated outputs include:

- extracted frames
- detected frames
- processed output video
- 3D map
- interactive 3D map
- statistics report

---

# Detection Logic

The YOLOv8 model detects:

```text
tree
```

The system then performs post-processing analysis to determine:

- tree size
- forest density
- nearby tree spacing
- CUT / KEEP decision

---

# Current Limitations

- Relative distances are estimated from image coordinates
- No real GPS integration yet
- No LiDAR integration yet
- Dataset size is limited
- Forest environments contain heavy object overlap

---

# Future Improvements

- GPS integration
- LiDAR sensor integration
- Real-world distance estimation
- Advanced forest health analysis
- Real-time processing optimization
- Improved tracking algorithms

---

# Thesis Information

Bachelor Thesis Project  
Computer Science  
Riga Technical University (RTU)

Project Type:

```text
AI-Based Intelligent Forestry Decision Support System
```
