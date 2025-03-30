import cv2
import numpy as np

# Open the video file
input_video_path = '/home/stavros/Documents/certh/projects/TREEADS/codes/treeads_v8.2/video_input/goats_2.mp4'
output_video_path = '/home/stavros/Documents/certh/projects/TREEADS/codes/treeads_v8.2/video_input/output_video_aaa.mp4'
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

# Duration of black intervals (in seconds) and the number of frames for those intervals
interval_duration = 2
interval_frames = fps * interval_duration

# Calculate the frame index where the last 10 seconds start
last_10_sec_start_frame = total_frames - (20 * fps)

# Process each frame
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print(f"Finished processing video. Total frames processed: {frame_count}")
        break

    # Check if we are in the last 10 seconds of the video
    if frame_count >= last_10_sec_start_frame:
        # Make the frame black if we are in the last 10 seconds
        black_frame = np.zeros_like(frame)
        out.write(black_frame)
    else:
        # Apply black frames every other 2 seconds
        if (frame_count // interval_frames) % 2 == 0:  # Check if we are in the black frame interval
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
