import cv2
import numpy as np

# Load the image
image_path_corrected = 'image.png'
image = cv2.imread(image_path_corrected)

# Convert to HSV color space for better color segmentation
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the red color range for detecting the cones
lower_red_1 = np.array([0, 170, 150])  # Lower bound for red
upper_red_1 = np.array([10, 255, 255])  # Upper bound for red
mask1 = cv2.inRange(hsv_image, lower_red_1, upper_red_1)

# Define the second red color range (to account for wrapping around hue)
lower_red_2 = np.array([170, 150, 130])  # Second range lower bound for red
upper_red_2 = np.array([180, 255, 255])  # Second range upper bound for red
mask2 = cv2.inRange(hsv_image, lower_red_2, upper_red_2)

# Combine both masks for red color detection
mask = mask1 | mask2

# Find contours in the red mask
mask = cv2.GaussianBlur(mask, (5,5), 0)
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Initialize lists for left and right cone centroids
left_cone_centroids = []
right_cone_centroids = []

# Loop over contours to detect and classify cones
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 100:  # Filter small areas
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # Separate left and right cones based on x-coordinate
            if cX < image.shape[1] // 2:
                left_cone_centroids.append((cX, cY))
            else:
                right_cone_centroids.append((cX, cY))

# Sort centroids by Y coordinate to ensure proper line drawing
left_cone_centroids = sorted(left_cone_centroids, key=lambda x: x[1])
right_cone_centroids = sorted(right_cone_centroids, key=lambda x: x[1])

# Draw the left red line over the left cones
for i in range(len(left_cone_centroids) - 1):
    cv2.line(image, left_cone_centroids[i], left_cone_centroids[i + 1], (0, 0, 255), 5)

# Draw the right red line over the right cones
for i in range(len(right_cone_centroids) - 1):
    cv2.line(image, right_cone_centroids[i], right_cone_centroids[i + 1], (0, 0, 255), 5)

# Save the output image with corrected parallel lines
output_image_parallel_lines_path = 'answer_clustering.png'
cv2.imwrite(output_image_parallel_lines_path, image)

print("Processing complete. The output image has been saved.")