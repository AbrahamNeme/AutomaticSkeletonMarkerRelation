import cv2
import numpy as np


def get_image_and_mask(path):
    # Load the image
    img = cv2.imread(path)

    # Preprocess: Apply GaussianBlur to reduce noise
    blurred_image = cv2.GaussianBlur(img, (5, 5), 0)

    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

    # Define color ranges for red, yellow and pink
    lower_red = np.array([0, 30, 30])
    upper_red = np.array([15, 255, 255])

    lower_yellow = np.array([15, 50, 50])
    upper_yellow = np.array([35, 255, 255])

    lower_pink = np.array([150, 50, 50])
    upper_pink = np.array([200, 255, 255])

    # Create masks for red, yellow and pink
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    pink_mask = cv2.inRange(hsv_image, lower_pink, upper_pink)

    # Combine the three masks
    mask = cv2.bitwise_or(cv2.bitwise_or(red_mask, yellow_mask), pink_mask)

    return img, mask


# Function to process image and extract human body with multiple contours
def extract_body_with_multiple_contours(original_image, mask, area_threshold=500):
    # Apply morphological operations with a small kernel
    kernel = np.ones((3, 3), np.uint8)
    cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_OPEN, kernel)
    cleaned_mask = cv2.erode(cleaned_mask, kernel, iterations=1)  # Add erosion

    # Remove pixels in the region from (0, 0) to (width, 50)
    cleaned_mask[0:48, :] = 0  # Set the region from y=0 to y=50 to 0

    # Find contours on the cleaned mask
    contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a new mask to store the combined large contours
    human_mask = np.zeros_like(cleaned_mask)

    # Filter and keep multiple contours based on area
    for contour in contours:
        if cv2.contourArea(contour) > area_threshold:
            cv2.drawContours(human_mask, [contour], -1, 255, thickness=cv2.FILLED)

    # Extract the human shape using the final mask
    human_shape = cv2.bitwise_and(original_image, original_image, mask=human_mask)

    return human_shape


# Function to combine the depth and model shapes using a weighted blend
def combine_shapes(depth, model, alpha=0.5):
    # Blend the images with the given alpha for transparency
    combined = cv2.addWeighted(depth, alpha, model, 1 - alpha, 0)
    return combined


# Function to convert an image to a binary array (1 for non-black, 0 for black pixels)
def image_to_binary_array(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create a binary mask: 1 for non-black pixels, 0 for black pixels
    binary_array = np.where(gray_image > 7, 1, 0)

    return binary_array


# Function to compare two binary arrays and calculate the similarity percentage
def calculate_similarity(binary_array1, binary_array2):
    # Ensure both arrays have the same shape
    if binary_array1.shape != binary_array2.shape:
        raise ValueError("Arrays must have the same size for comparison")

    # Find indexes where at least one of the arrays has a value of 1
    # Discard all indexes where both arrays have a value of 0 (black background)
    relevant_indexes = (binary_array1 + binary_array2) > 0

    # Compare only the relevant indices
    matching_pixels = np.sum(binary_array1[relevant_indexes] == binary_array2[relevant_indexes])

    # Calculate similarity based on the relevant indices
    total_relevant_pixels = np.sum(relevant_indexes)
    accuracy_percentage = (matching_pixels / total_relevant_pixels) * 100

    return accuracy_percentage


# ------------------------------- #
accuracies = 0

# Create arrays for the specified ranges
arr1 = np.arange(10, 39)
arr2 = np.arange(49, 95)
arr3 = np.arange(99, 102)
arr4 = np.arange(103, 115)
arr5 = np.arange(121, 147)
arr6 = np.arange(149, 180)
arr7 = np.arange(188, 213)
arr8 = np.arange(222, 243)
arr9 = np.arange(271, 285)
arr10 = np.arange(287, 292)
arr11 = np.arange(302, 328)
arr12 = np.arange(335, 370)
arr13 = [410, 413, 415, 418, 419]

# Combine the arrays into a single array
final_array = np.concatenate([arr1, arr2, arr3, arr4, arr5, arr6, arr7, arr8, arr9, arr10, arr11, arr12, arr13])

for i in final_array:
    # Get depth image and shape
    depth_image_path = f'frames/depth/frame_{i:04d}.png'
    depth_image, depth_mask = get_image_and_mask(depth_image_path)
    depth_shape = extract_body_with_multiple_contours(depth_image, depth_mask, area_threshold=3000)

    # Get model image and shape
    model_image_path = f'frames/model/frame_{i:04d}.png'
    model_image = cv2.imread(model_image_path)

    #Get binary arrays containing only 1's and 0's
    depth_binary = image_to_binary_array(depth_shape)
    model_binary = image_to_binary_array(model_image)

    # Calculate the similarity between the two images
    accuracy = calculate_similarity(depth_binary, model_binary)
    accuracies += accuracy
    print(f"Similarity between the depth and model images for frame_{i:04d}: {accuracy:.2f}%")

    # Combine depth_shape + model_shape and store the new image
    combined_shape = combine_shapes(depth_shape, model_image, alpha=0.5)
    cv2.imwrite(f'results/frame_{i:04d}.png', combined_shape)

avg_accuracy = accuracies / len(final_array)
print(f"Average accuracy of the model: {avg_accuracy}")
