### **FarmGuard – Demo Description**

FarmGuard is a mobile application designed to demonstrate how machine learning can be deployed directly on low-cost smartphones to support smallholder farmers.

The demo focuses on **on-device crop disease inference** using images captured with a phone camera. The goal is to show that useful AI tools can run **offline**, without internet access, which is critical in rural and resource-constrained environments.


##### **Demo Flow**

* The user opens the FarmGuard mobile application.
* The user selects a crop type (e.g., cassava or maize).
* The user captures or uploads a photo of a leaf.
* The image is preprocessed on the device.
* A PyTorch model runs inference locally on the phone.
* The app displays the predicted disease class.


##### **What the Demo Proves**

* End-to-end ML deployment from training to mobile inference
* Offline inference using PyTorch Mobile
* Practical constraints such as model size, latency, and memory usage
* Real-world applicability for agricultural decision support


##### **Limitations**

Due to GitHub file size constraints, the trained model files used in the demo are not included in this repository. However, the full training, optimization, and export pipeline is provided, and inference results are documented with screenshots.


##### **Target Audience**

* Students and educators interested in applied machine learning
* Researchers exploring edge AI deployment
* Institutions evaluating technical depth and real-world impact



