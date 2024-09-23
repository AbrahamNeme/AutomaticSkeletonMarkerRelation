
import json
import numpy as np

file_path = './evaluation/pose_comparison/mean_distances.json'

with open(file_path, 'r') as json_file:
    data = json.load(json_file)

small_distance = 0
big_distance = 0
no_detection = 0
mean_distances = []
for mean_distance in data:
    if mean_distance['mean_distance'] < 0.05:
        small_distance +=1
        mean_distances.append(mean_distance['mean_distance'])

    if mean_distance['mean_distance'] >= 0.05 and mean_distance['mean_distance'] < 1:
        big_distance +=1
        mean_distances.append(mean_distance['mean_distance'])

    if mean_distance['mean_distance'] == 1:
        no_detection +=1


overall_mean = np.mean(mean_distances)

print("Number of images with a difference < 0.5: ", small_distance)
print("Number of images with a difference > 0.5: ", big_distance)
print("Number of images where pose landmarks where not detected", no_detection)
print("Mean distance overall: ", round(overall_mean,3))
print("Smallest difference: ", min(mean_distances), "Biggest difference: ", max(mean_distances))

