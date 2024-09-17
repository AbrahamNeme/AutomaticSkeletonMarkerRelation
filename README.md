# Evaluation of Real-Time SMPL Model Representation and Integration

### Luke Mikat, Abraham Neme Alvarez, Valdone Zabutkaite

## Poster

TODO

## Problem Description

In marker-based motion capturing (MoCap), markers are placed on the body. However, it is not always possible to place all markers exactly where they ideally belong. As a result, the relationship between the markers and the skeleton is missing, which means that the skeletal structure can no longer be accurately reconstructed from the markers.

## Proposed Solution

To improve the relationship between MoCap markers and the skeleton, it is proposed to test existing research that utilizes parametric human models such as [SMPL (Skinned Multi-Person Linear Model)](https://smpl.is.tue.mpg.de/). These models can be embedded in depth images captured by RGBD cameras, such as the Azure Kinect.

The main idea is to first fit the SMPL model to the depth images and then recognize the MoCap markers to establish their relationship with the SMPL model. By using the SMPL model, more accurate marker positioning could be achieved, because the model provides detailed information about the human body shape and structure.

To ensure the quality and functionality of the existing approach for fitting the SMPL model onto a human in real time, a comprehensive evaluation will be conducted. The created setup will evaluate on the method's ability to accurately and consistently represent a person as an SMPL model in real-time and fit it to the depth images. This includes evaluating the accuracy of the model fitting, particularly regarding the alignment and coverage between the estimated body parameters and the real recordings. Potential sources of error will also be identified and analyzed to ensure that the approach is robust against different body shapes, movements, camera perspectives and lighting conditions. The results of this evaluation will serve as the basis for making improvements and optimizing the method for use in conjunction with the markers.

## Approach

1. **Review of Existing Methods:**
- Review current solutions based on the SMPL model, such as the [Avatar Project](https://github.com/sxyu/avatar). This repository written in C++ enables the mapping of 3D-SMPL models onto human bodies in real time. It will be evaluated for its suitability for the task.
   
2. **Avatar Project Setup:**
- The Avatar Project will be configured to work in real time with depth images from the Azure Kinect. The goal is to integrate the SMPL model into the captured depth data and create an accurate representation of the person shown in the recordings.

3. **Utilizing and Testing the SMPL Demo and Live-Demo:**
- In the provided repository there are 2 executables, which can be used for creating the SMPL Model. The Demo, which is utilizing a prerecorded dataset for displaying the SMPL Model frame by frame, and the Live-Demo, which is displaying the SMPL Model for the human in the Kinect cameras live stream. Both these will be used to test the functionality of the SMPL model. Suitable datasets must also be created or collected to serve as the basis for the testing of the demo.


4. **Evaluation of the SMPL-Model Fitting:**
- A comprehensive evaluation of the performance of the SMPL model representation will be conducted to assess the quality of fitting to Kinect recordings. Particular attention will be given to the accuracy of the movement of the model and body shape representation. Weaknesses in the fitting process will be documented to identify potential improvements.

5. **(Optional): Marker Detection and Assignment**
- The markers positions will be mapped to the SMPL model to allow for more precise determination of their location relative to the body structure. This aims to improve the accuracy and functionality of the entire tracking system.

## Avatar Project

### Dependencies

The following configuration of the repository requires you to have Windows or Linux as your OS, as the Azure Kinect SDK is not available for macOS. The setup has only been thoroughly tested on Windows.

First you'll need to install [cmake](https://cmake.org/download/) to build the project.

We have used vcpkg to manage the projects dependencies. With the following commands you can install it:

```bash
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
./bootstrap-vcpkg.bat # For Windows
./bootstrap-vcpkg.sh  # For Linux
./vcpkg integrate install
```

Make sure you're inside your vcpkg directory. Install the projects dependencies via vcpkg:

```bash
./vcpkg install azure-kinect-sensor-sdk
./vcpkg install opencv3
./vcpkg install opencv3[openexr]
./vcpkg install eigen3
./vcpkg install zlib
./vcpkg install boost
./vcpkg install ceres
./vcpkg install glfw3
```

### Test Data

The model data and OpenARK datasets from the [original repository](https://github.com/sxyu/avatar/releases/) were no longer available, so [this guide](https://github.com/augcog/OpenARK/tree/master/data/avatar-model) had to be followed to obtain and create the necessary files for testing.

#### Model

The `data/avatar-model` directory has to include the following files for running the `live-demo.exe` and `demo.exe`:

- model.pcd
- skeleton.txt
- joint_regressor.txt
- pose_prior.txt
- tree.150k.refine.srtr
- tree.150k.refine.srtr.partmap

#### OpenARK Datasets

The `demo.exe` is utilizing datasets in form of the OpenARK Datasets.

Download and extract the [OpenARK-Dataset](https://github.com/sxyu/OpenARK-Deps/releases/download/0.0.1/avatar-dataset.zip) to the directory `data/avatar-dataset`


### Build

Make sure you are inside the root directory of you project. Replace the path to vcpkg in the following command:

```bash
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=C:\path\to\vcpkg\scripts\buildsystems\vcpkg.cmake
```

```bash
cd build
cmake --build build --config Release
cd Release
```

Make sure the files `live-demo.exe` and `demo.exe` have been created.

### Live-Demo 

The live demo displays a real-time representation from a Azure Kinect camera, visualizing a 3D avatar onto the person in the image.

Inside the `Release` directory:

```bash
./live-demo.exe --rtree ./tree.150k.refine.srtr
```

#### Options

TODO

### Demo

The demo showcases the processing and animation of the SMPL-Model (`data/avatar-model`) based on a pre-recorded OpenARK Dataset (`data/avatar-dataset`), which includes RGB images, depth images and the joints. This demo is designed to illustrate the results of the pipeline without requiring real-time data from the Azure Kinect.

```bash
cd build/Release
./demo --rtree tree.150k.refine.srtr --dataset_path ../../data/avatar-dataset/human-dance-random --image 351 --background 351
```

#### Options
  - `dataset_path`: Root directory containing the input dataset.
  - `rtree`: Path to the RTree model used for segmentation.
  - `--background` (`-b`): Background image ID (default: 9999).
  - `--image` (`-i`): Current image ID (default: 1).
  - `--pad` (`-p`): Padding width for image names (default: 4).
  - `--rtree-only` (`-R`): Flag to skip optimization and only show RTree segmentation.
  - `--no-occlusion`: Disable occlusion detection in the avatar optimizer.
  - `--betapose`: Weight for the pose prior term in optimization (default: 0.05).
  - `--betashape`: Weight for the shape prior term in optimization (default: 0.12).
  - `--data-interval`: Pixel computation interval. Lower values increase RTree segmentation accuracy but increase computational load. (default: 12). 
  - `--nnstep`: Step size for nearest-neighbor search during optimization (default: 20). Reducing it improves accuracy but may slow processing.
  - `--frame-icp-iters` (`-t`): ICP iterations per frame (default: 3). Higher values improve accuracy but slow down the process.
  - `--reinit-icp-iters` (`-T`): ICP iterations during reinitialization (default: 6). Higher values improve accuracy but slow down the process.
  - `--inner-iters`:Maximum inner iterations per ICP step (default: 10).
  - `--min-points` (`-M`): Minimum number of detected body points required for tracking (default: 1000). Lower values increase the risk of tracking failure due to insufficient points.

#### Data Recording

The executable for recording necessary parts of an OpenARK dataset. However, due to missing generation of critical files, such as joint data, the datasets created with this tool could not be used for the demo.

### Evaluation

#### Approach

#### Metrics

#### Implementation

### Results

#### Live-Demo 

TODO 
Images from the Live-Demo evaluation

![Avatar Project Evaluation](./images/avatar-project-evaluation.png) -

#### Demo

TODO 
Images from the DEMO

### Project Retrospective

Reproducing the repository proved to be a challenging task due to outdated C++ libraries and dependency conflicts. Additionally, both the datasets and models were missing, and the links provided in the repository were no longer available. As a result, we had to assemble the datasets ourselves, which was time-consuming and prone to errors, due to the lack of documentation. We managed to get both the live demo and the demo to work and could evaluate them. Due to the sheer lack of documentation and necessary files from the model and OpenARK datasets we had to put more time into understanding the repositories workflows instead of concentrating on the evaluation itself. 

### Future Research

The optional marker detection and assignment task would be the next step to investigate in our future work. We deem this approach to be promising, however the repository seems to be outdated and should be revised or adapted for our requirements. Additionally there are very promising new apporaches in the creation of SMPL-Model representataions of human bodies from normal RGB cameras without the need of depth images from a Kinect, which is way more intuitive. For example [Meshcapade](https://meshcapade.com/SMPL). 

## Task Division

TODO

### Abraham (@)

### Valdone (@)

### Luke (@s82765)
- Setup and integration of the project
- Resolved dependency conflicts
- Assembled OpenARK datasets
- Built the project
- Tested demo, live demo, and data recording executables
- Modified live-demo code to export multiple outputs for the evaluation dataset
- Recorded evaluation datasets
- Created illustrations for the poster
- Wrote documentation


## Personal Reflexion

TODO

### Abraham (@)

### Valdone (@)

### Luke (@s82765)
