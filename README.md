#### FarmGuard

**On-Device Crop Disease Detection with PyTorch Mobile \& Flutter**

FarmGuard is an end-to-end machine learning and mobile systems project that explores how computer vision models can be trained, optimized, and deployed directly on smartphones to support smallholder farmers in resource-constrained environments. 

This project emphasizes real-world deployment challenges, including offline inference, mobile constraints, and system integration across multiple technologies.


##### **Motivation**

In many rural communities, especially in developing regions, crop disease can severely affect food security and income. While machine learning models for plant disease detection exist, most rely on cloud-based inference and stable internet access.

FarmGuard was built to explore a key question:

**Can practical machine learning tools run entirely on-device, offline, and on low-cost smartphones?**

This question connects my interests in machine learning, systems engineering, edge AI, and technology for real-world impact.


##### **What This Project Demonstrates**

* End-to-end ML workflow: EDA → Training → Optimization → Mobile Deployment
* On-device inference using PyTorch Mobile
* Cross-platform mobile development with Flutter
* System-level thinking beyond model accuracy
* Real-world constraints: memory limits, build size, tooling issues


##### **System Overview**

FarmGuard consists of two major components:

###### **1. Machine Learning Pipeline (Python / PyTorch)**
* Dataset exploration and preprocessing
* CNN-based image classification
* Model evaluation and validation
* Export to TorchScript for mobile compatibility

###### **2. Mobile Application (Flutter + Android)**
* Image capture and selection
* Model lifecycle management
* On-device inference using PyTorch Mobile
* Offline-first design (no server dependency)

A detailed architecture breakdown is available in **docs/system\_architecture.md**


##### Data Flow

Leaf Image

   ↓

Image Preprocessing (Mobile)

   ↓

TorchScript Model (PyTorch Mobile)

   ↓

Prediction Scores

   ↓

Disease Label Display


##### Demo

The demo showcases real inference performed directly on a smartphone.
Demo details: **docs/demo\_description.md**
Screenshots of successful predictions are included in the repository.

**Note**
Trained model files are not included due to GitHub file size limits.The full training and export pipeline is provided so results can be reproduced.


##### **Repository Structure**

FarmGuard/

├── ml/                     # EDA, training, optimization, export

│   ├── notebooks/

│   ├── training/

│   ├── requirements.txt

│   └── export/

│

├── mobile/

│   └── farmguard\_app/       # Flutter application (unmodified structure)

│

├── docs/                   # Documentation

│   ├── demo\_description.md

│   ├── system\_architecture.md

│   └── reflection.md

│

├── screenshots/            # Demo evidence

│

└── README.md


##### **Technologies Used**

###### **Machine Learning**
* Python
* PyTorch
* TorchScript
* NumPy
* OpenCV

###### **Mobile \& Systems**
* Flutter (Dart)
* Android SDK
* PyTorch Mobile
* Gradle


##### **Challenges \& Engineering Lessons**

This project revealed that deployment is often harder than training.

Key challenges included:
* TorchScript compatibility constraints
* Asset and file system management on Android
* Debugging across Flutter, Android, and native libraries
* Managing build size and memory limits
* Handling GitHub restrictions on large binaries

Rather than hiding these challenges, they are documented and reflected upon as part of the learning process.


##### **Reflection**

A full project reflection is available here: **docs/reflection.md**

It discusses:
* Technical setbacks and recoveries
* System-level debugging
* Trade-offs and architectural decisions
* Personal growth as an engineer


##### **Impact \& Future Work**

FarmGuard is a prototype, but it points toward future possibilities:

* Edge AI for agriculture
* Offline-first ML tools
* Accessible technology for underserved communities

Future improvements could include:

* Model quantization
* Expanded crop coverage
* Integration with agronomic guidance


##### **Author**

Hamed Moustapha Nsangou
Aspiring Computer Scientist & Engineer
Interested in machine learning systems, embedded AI, Edge deployment, and real-world impact


##### **License**
This project is shared for educational and portfolio purposes.

