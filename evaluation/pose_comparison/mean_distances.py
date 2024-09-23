import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import json

def extract_keypoints(landmarks):
   keypoints = []
   if len(landmarks) == 0 :
      return []
   print(len(landmarks[0]))
   for landmark in landmarks[0]:
    keypoints.append((landmark.x, landmark.y))
   return keypoints

def calculate_distances(keypoints1, keypoints2):
  distances = []
  for (x1, y1), (x2, y2) in zip(keypoints1, keypoints2):
        distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        distances.append(distance)
  return distances

def compare_keypoints(keypoints1, keypoints2):
    if len(keypoints1) == 0 or len(keypoints2) == 0:
       return 1
    distances = calculate_distances(keypoints1, keypoints2)
    mean_distance = np.mean(distances)
    return mean_distance

def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]

    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      pose_landmarks_proto,
      solutions.pose.POSE_CONNECTIONS,
      solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image


# Create an PoseLandmarker object.
base_options = python.BaseOptions(model_asset_path='pose_landmarker.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=True)
detector = vision.PoseLandmarker.create_from_options(options)

mean_distances = []

for i in range(433):
  # Load the input image and transform them into the right format.
  image = cv2.imread(f"./dataset/frames-cropped/rgb/frame_{i:04d}.png")
  image_model = cv2.imread(f"./dataset/frames-cropped/model/frame_{i:04d}.png")
  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  image_model_rgb = cv2.cvtColor(image_model, cv2.COLOR_BGR2RGB)

  mp_image_rgb = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
  mp_image_model = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_model_rgb)
  # Detect pose landmarks from the input image.
  detection_result_rgb = detector.detect(mp_image_rgb)
  detection_result_model = detector.detect(mp_image_model)

  landmarks = detection_result_rgb.pose_landmarks
  landmarks_model = detection_result_model.pose_landmarks

  # Get normalized x,y coordinates for all pose landmarks.
  keypoints = extract_keypoints(landmarks)
  keypoints_model = extract_keypoints(landmarks_model)

  # Calculate the mean Euclidean distance for all pose landmarks/keypoints.
  mean_distance = round(compare_keypoints(keypoints,keypoints_model),2)
  print("Mean distance of all Keypoints: ",mean_distance)

  mean_distances.append({"frame": i, "mean_distance": mean_distance })

  # Visualize the results.
  annotated_image = draw_landmarks_on_image(image, detection_result_rgb)
  cv2.imwrite(f"./dataset/pose_landmarks/rgb/frame_{i:04d}.png",cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

  annotated_image_model = draw_landmarks_on_image(image_model, detection_result_model)
  cv2.imwrite(f"./dataset/pose_landmarks/model/frame_{i:04d}.png",cv2.cvtColor(annotated_image_model, cv2.COLOR_RGB2BGR))

# Write the mean distances into a json file for the evaluation.
file_path = "mean_distances.json"

with open(file_path, 'w') as json_file:
   json.dump(mean_distances, json_file)
    