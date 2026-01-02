##### **System Architecture – FarmGuard**

This document describes the end-to-end architecture of the FarmGuard project, from data preparation to mobile deployment.


##### **High-Level Overview**

FarmGuard consists of two main subsystems:
* Machine Learning Pipeline (Python / PyTorch)
* Mobile Application (Flutter + PyTorch Mobile)

These subsystems are developed independently, but are tightly integrated through a shared model interface.


##### **Machine Learning Pipeline**

###### **1. Data Handling**
* Image datasets organized by crop and disease class
* Data augmentation is applied during training to improve robustness

###### **2. Model Training**
* Convolutional Neural Network trained using PyTorch
* Transferred learning using EFFICIENTNET-B0 architecture 
* Supervised classification objective
* Evaluation using validation accuracy and loss

###### **3. Model Export \& Optimization**
* Trained model converted to TorchScript
* Model optimized for mobile inference (size and speed)
* Compatibility verified with PyTorch Mobile


##### **Mobile Application Architecture**

###### **UI Layer (Flutter)**
* Image capture and selection
* Crop selection interface
* Result visualization

###### **Service Layer**
* Model loading and lifecycle management
* Image preprocessing (resize, normalization)
* Inference execution

###### **Inference Engine**
* PyTorch Mobile runtime
* On-device execution (no server calls)
* Outputs raw logits mapped to labels

##### **Data Flow**

User Image

↓

Image Preprocessing (Flutter)

↓

TorchScript Model (PyTorch Mobile)

↓

Prediction Output

↓

User Interface


##### **Design Principles**

* Offline-first: No dependency on internet connectivity
* Resource-aware: Designed for low-memory mobile devices
* Modular: ML pipeline and mobile app can evolve independently


##### **Future Extensions**

* Model quantization for faster inference
* Support for additional crops
* Integration with agronomic guidance systems







