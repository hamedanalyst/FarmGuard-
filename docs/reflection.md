### **Project Reflection – FarmGuard**

FarmGuard began as a technical curiosity and evolved into a deep learning
experience that challenged both my engineering skills and my problem-solving mindset.


##### **What I Set Out to Build**

My initial goal was to train a machine learning model and deploy it on a mobile device. However, as the project progressed, I realized that true deployment meant far more than achieving high accuracy in a notebook.

I wanted to understand what it actually takes to move a model from research code to a real user-facing application.


##### **Technical Challenges**

###### **1. Model Deployment on Mobile**

Exporting a PyTorch model to TorchScript and running it on a mobile device introduced constraints I had never encountered during training, including file size limits, strict input formats, and runtime compatibility issues. These constraints forced me to think beyond model performance and consider how architectural decisions affect real-world usability.

###### **2. Debugging Across Systems**

Debugging failures required understanding interactions between multiple layers of the system:

* Flutter (Dart)
* Android build tools
* PyTorch Mobile
* File system and asset management

Errors were often indirect, forcing me to reason carefully about system boundaries rather than relying on trial-and-error. This pushed me to read documentation, inspect logs, and form hypotheses about failure points.

###### **3. Debug vs Release Deployment Challenges**

At an earlier stage of development, FarmGuard successfully performed on-device inference when run in debug mode on a physical Android device. Multiple real predictions were observed and documented, confirming that the trained model and preprocessing pipeline were functional.

However, while attempting to generate a release APK, I made several low-level configuration changes to Android native files to address build and packaging requirements. These changes introduced a critical failure in the native library loading process.

As a result:
* The release build failed to load the model correctly
* Subsequent debug builds also failed with native runtime errors
* Inference errors originated from the Android–PyTorch Mobile integration layer rather than the model itself

This experience highlighted an important lesson: a working model does not guarantee a working deployment.

The machine learning model did not cause the failure, but the complexity of integrating Flutter, Android native tooling, and PyTorch Mobile’s runtime requirements did. This was my first exposure to real-world ML systems engineering challenges, where deployment often becomes more difficult than training.

###### **4. Resource Constraints**

Memory limits, build sizes, and GitHub file size restrictions influenced architectural decisions, prompting me to document results rather than rely on distributable binaries. These constraints influenced how I structured the project and reinforced the importance of reproducibility and clear documentation.


##### **What I Learned**

* Deployment is as important as model accuracy
* Clean architecture matters when systems grow complex
* Engineering is about trade-offs, not perfection
* Clear documentation can preserve work even when demos fail


##### **Personal Growth**

This project taught me persistence more than anything else. There were moments when inference worked, moments when it broke, and moments when rebuilding was no longer practical. Instead of discarding the project, I learned how to salvage, document, and present it honestly. That process reflects how real engineering work happens and strengthened my confidence in tackling complex, open-ended problems.


##### **Looking Forward**

FarmGuard has shaped my interest in:

* Edge AI and embedded systems
* Machine learning systems engineering
* Technology for resource-constrained communities



I now approach projects with a stronger emphasis on robustness, documentation, and real-world constraints.

