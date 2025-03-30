import cv2
import numpy as np

# Open the video file
input_video_path = '/home/stavros/Documents/certh/projects/TREEADS/codes/treeads_v8.2/video_input/goats_2.mp4'
output_video_path = '/home/stavros/Documents/certh/projects/TREEADS/codes/treeads_v8.2/video_input/output_video_3sec.mp4'


cap = cv2.VideoCapture(input_video_path)

# Check if the video file is successfully opened
if not cap.isOpened():
    print("Error: Could not open the video file.")
    exit()

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Video properties - FPS: {fps}, Width: {frame_width}, Height: {frame_height}, Total Frames: {total_frames}")

# Create a VideoWriter object to save the modified video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Check if the VideoWriter object was created successfully
if not out.isOpened():
    print("Error: Could not create the output video file.")
    exit()

# Duration of black intervals and normal intervals (in seconds)
interval_duration = 3
interval_frames = fps * interval_duration

# Process each frame
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print(f"Finished processing video. Total frames processed: {frame_count}")
        break

    # Apply black frames every other 2 seconds
    if (frame_count // interval_frames) % 3 == 0:  # Check if we are in the black frame interval
        black_frame = np.zeros_like(frame)
        out.write(black_frame)
    else:
        out.write(frame)

    frame_count += 1

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

print('Video processing complete. Output saved as', output_video_path)