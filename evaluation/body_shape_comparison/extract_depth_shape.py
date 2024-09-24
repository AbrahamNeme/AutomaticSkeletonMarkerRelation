import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to process image and extract human body with multiple contours
def extract_body_with_multiple_contours(image_path, area_threshold=500):
    # Load the image
    image = cv2.imread(image_path)

    # Preprocess: Apply GaussianBlur to reduce noise
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

    # Define color ranges for red, yellow, and pink with wider pink range
    lower_red = np.array([0, 30, 30])
    upper_red = np.array([15, 255, 255])

    lower_yellow = np.array([15, 50, 50])
    upper_yellow = np.array([35, 255, 255])

    lower_pink = np.array([150, 50, 50])
    upper_pink = np.array([200, 255, 255])

    lower_light_purple = np.array([125, 30, 100])
    upper_light_purple = np.array([155, 255, 255])

    # Create masks for red, yellow, and pink
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    pink_mask = cv2.inRange(hsv_image, lower_pink, upper_pink)

    # Combine the three masks
    combined_mask = cv2.bitwise_or(cv2.bitwise_or(red_mask, yellow_mask), pink_mask)

    # Apply morphological operations with a larger kernel
    kernel = np.ones((3, 3), np.uint8)  # Increase kernel size
    cleaned_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
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
            cv2.drawContours(human_mask, [contour], -1, (255), thickness=cv2.FILLED)

    # Extract the human shape using the final mask
    human_shape = cv2.bitwise_and(image, image, mask=human_mask)

    return image, human_shape


# Paths for the two provided images
image_path1 = 'frames/depth/frame_0083.png'
image_path2 = 'frames/depth/frame_0056.png'

# Process both images
original1, human_shape1 = extract_body_with_multiple_contours(image_path1, area_threshold=2500)
original2, human_shape2 = extract_body_with_multiple_contours(image_path2, area_threshold=2500)

cv2.imwrite('depth_frame_0083.png', human_shape1)
cv2.imwrite('depth_frame_0354.png', human_shape2)

# Display results
plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
plt.title('Original Image 1')
plt.imshow(cv2.cvtColor(original1, cv2.COLOR_BGR2RGB))

plt.subplot(2, 2, 2)
plt.title('Extracted Human Shape 1')
plt.imshow(cv2.cvtColor(human_shape1, cv2.COLOR_BGR2RGB))

plt.subplot(2, 2, 3)
plt.title('Original Image 2')
plt.imshow(cv2.cvtColor(original2, cv2.COLOR_BGR2RGB))

plt.subplot(2, 2, 4)
plt.title('Extracted Human Shape 2')
plt.imshow(cv2.cvtColor(human_shape2, cv2.COLOR_BGR2RGB))

plt.tight_layout()
plt.savefig('extracted_human_shape.png', format='png', dpi=300)
plt.show()


