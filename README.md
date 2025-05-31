
# 💤 Sleep Detection System using MediaPipe & OpenCV

### 📌 **Author**: Adithya  
### 📅 **Last Updated**: May 2025  
### 🎯 **Purpose**: Detect if a person is drowsy or falling asleep by monitoring Eye Aspect Ratio (EAR) and triggering an alarm if eyes remain closed for a certain number of frames.

---

## 🔧 Dependencies
- **OpenCV**: `cv2` – Used for video processing and drawing.
- **MediaPipe**: `mediapipe` – For detecting face mesh and extracting eye landmarks.
- **NumPy**: `numpy` – For mathematical calculations.
- **Threading**: For playing alarm sound without freezing the UI.
- **Pygame**: For alarm sound playback.

---

## 🧠 Key Concepts

### 1. **Eye Aspect Ratio (EAR)**
A method to determine if eyes are closed by comparing the vertical and horizontal distances between landmarks around the eye.

### 2. **Drowsiness Detection**
If EAR falls below a threshold for `N` consecutive frames, the system considers the user to be sleeping and triggers an alarm.

---

## ⚙️ Configuration

| Variable | Purpose |
|---------|---------|
| `EAR_THRESHOLD = 0.18` | Threshold to detect if eyes are closed |
| `SLEEP_CONSEC_FRAMES = 20` | Minimum number of consecutive frames for sleep detection |
| `ALARM_PATH` | Local path to the alarm sound file |

---

## 📦 Code Structure

### 1. **Alarm Function**
Plays the alarm sound using `pygame` in a separate thread to avoid freezing the camera feed.

### 2. **MediaPipe Face Mesh Initialization**
Initializes MediaPipe face mesh for detecting 468 facial landmarks.

### 3. **Video Capture**
Starts the webcam and continuously reads frames.

### 4. **EAR Calculation**
Computes the eye aspect ratio using 6 landmarks around each eye.

### 5. **Sleep Detection Logic**
- Checks if `avg_ear` is below threshold.
- Increments a counter.
- If counter exceeds `SLEEP_CONSEC_FRAMES`, it triggers the alarm.
- Resets the counter when eyes open again.

### 6. **Drawing and Display**
- Displays EAR value on the screen.
- Draws eye and facial landmarks.
- Shows a **"SLEEPING"** warning.
- Adds a watermark: `"Made by Adithya"`.

### 7. **Exit Mechanism**
Press `q` to exit the loop and close the webcam.

---

## 📌 How to Use

1. Make sure the webcam is connected.
2. Place your face in front of the camera.
3. If you close your eyes for too long, the alarm will play.
4. Press `q` to quit the application.

---

## 🔊 Notes

- Make sure the `ALARM_PATH` points to a valid `.wav` sound file.
- You can adjust `EAR_THRESHOLD` and `SLEEP_CONSEC_FRAMES` based on testing.
- Works best in well-lit environments.
