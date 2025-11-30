# Change Detection Algorithm

This project implements a computer vision algorithm to detect and highlight differences between paired "before" and "after" images of the same scene. It is designed to identify missing objects or changes and mark them with a bounding box.

## Features

-   **Automatic Pair Detection**: Automatically identifies pairs of images based on a naming convention (`X.jpg` and `X~2.jpg`).
-   **Change Detection**: Uses image subtraction and thresholding to detect changes.
-   **Visualization**: Draws red bounding boxes around detected changes on the "after" image.
-   **Output Management**: Saves the result image (`X~3.jpg`) and a copy of the original "before" image to a dedicated output folder.

## Prerequisites

-   Python 3.x
-   OpenCV (`cv2`)
-   NumPy

## Installation

1.  Clone this repository or download the script.
2.  Install the required Python packages:

    ```bash
    pip install opencv-python numpy
    ```

## Usage

1.  **Prepare Input Images**:
    -   Place your image pairs in a folder named `input-images` in the same directory as the script.
    -   Ensure the images follow the naming convention:
        -   Before image: `Filename.jpg`
        -   After image: `Filename~2.jpg`
    -   Images must be perfectly aligned.

2.  **Run the Script**:

    ```bash
    python change_detection.py
    ```

3.  **Check Results**:
    -   The script will create a folder named `output-images`.
    -   Inside, you will find:
        -   `Filename.jpg`: The original "before" image.
        -   `Filename~3.jpg`: The processed image with detected changes highlighted.

## Algorithm Overview

1.  **Load Images**: Reads the "before" and "after" images.
2.  **Grayscale Conversion**: Converts images to grayscale to simplify processing.
3.  **Absolute Difference**: Computes the absolute difference between the two grayscale images.
4.  **Thresholding**: Applies a binary threshold to the difference map to highlight significant changes.
5.  **Morphological Operations**: Uses dilation to close gaps and remove small noise.
6.  **Contour Detection**: Finds contours in the thresholded image.
7.  **Bounding Box**: Draws a bounding box around contours that exceed a minimum area threshold.
