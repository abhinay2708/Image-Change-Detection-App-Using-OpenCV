import cv2
import os
import shutil
import numpy as np

def detect_changes(input_dir, output_dir):
    """
    Detects changes between paired images in the input directory and saves results to the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get all files in the input directory
    files = os.listdir(input_dir)
    
    # Filter for "before" images (X.jpg)
    # We assume "after" images are named X~2.jpg
    before_images = [f for f in files if f.endswith('.jpg') and '~' not in f]

    for before_img_name in before_images:
        base_name = os.path.splitext(before_img_name)[0]
        after_img_name = f"{base_name}~2.jpg"
        
        before_path = os.path.join(input_dir, before_img_name)
        after_path = os.path.join(input_dir, after_img_name)

        if not os.path.exists(after_path):
            print(f"Warning: Paired image for {before_img_name} not found. Skipping.")
            continue

        print(f"Processing pair: {before_img_name} and {after_img_name}")

        # Load images
        img1 = cv2.imread(before_path)
        img2 = cv2.imread(after_path)

        if img1 is None or img2 is None:
            print(f"Error loading images for {base_name}. Skipping.")
            continue
            
        if img1.shape != img2.shape:
             print(f"Error: Images {before_img_name} and {after_img_name} have different dimensions. Skipping.")
             continue

        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Compute absolute difference
        diff = cv2.absdiff(gray1, gray2)

        # Apply thresholding to create a binary mask
        # Using a simple threshold, can be adjusted or switched to adaptive
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Morphological operations to remove noise and close gaps
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw bounding boxes on the "after" image (or a copy of it)
        result_img = img2.copy()
        
        min_area = 500 # Minimum area to be considered a valid change
        
        for contour in contours:
            if cv2.contourArea(contour) < min_area:
                continue
            
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 0, 255), 2) # Red bounding box

        # Save output
        output_result_name = f"{base_name}~3.jpg"
        output_result_path = os.path.join(output_dir, output_result_name)
        cv2.imwrite(output_result_path, result_img)
        
        # Copy original "before" image
        output_before_path = os.path.join(output_dir, before_img_name)
        shutil.copy2(before_path, output_before_path)
        
        print(f"Saved result to {output_result_path}")

if __name__ == "__main__":
    input_directory = "input-images"
    output_directory = "output-images"
    
    # Ensure paths are absolute or correct relative to execution
    current_dir = os.getcwd()
    abs_input_dir = os.path.join(current_dir, input_directory)
    abs_output_dir = os.path.join(current_dir, output_directory)

    detect_changes(abs_input_dir, abs_output_dir)
