# 10-Finger Gesture Controlled LED System

A real-time hand gesture recognition system that uses Python, OpenCV, MediaPipe, and an Arduino to control 10 LEDs based on the number of detected fingers.

## Overview

The system uses a webcam to detect and track up to two hands using MediaPipe's Hand Landmarker. Each detected hand provides 21 landmarks, which are processed to determine how many fingers are extended.

The total number of detected fingers is then sent from Python to an Arduino through serial communication. The Arduino uses this value to control 10 LEDs, with the number of illuminated LEDs corresponding to the number of detected fingers.

## Features

- Real-time hand gesture recognition using a webcam
- Detection and tracking of up to two hands
- 21 hand landmarks per detected hand using MediaPipe Hand Landmarker
- Custom finger-counting logic based on landmark positions
- Geometric distance calculations for thumb detection
- Detection of up to 10 fingers simultaneously
- Python-to-Arduino serial communication
- Control of 10 LEDs based on the detected finger count
- Visual display of detected hand landmarks and finger count
- Integration of computer vision, serial communication, and embedded hardware

## How It Works

```text
                    Webcam
                       │
                       ▼
                    OpenCV
                       │
                       ▼
            MediaPipe Hand Landmarker
                       │
                       ▼
               Hand Landmarks
                       │
                       ▼
          Custom Finger-Counting Logic
                       │
                       ▼
              Total Finger Count
                       │
                       ▼
             Serial Communication
                       │
                       ▼
                    Arduino
                       │
                       ▼
                    10 LEDs
```

The number of detected fingers determines how many LEDs are illuminated:

```text
0 fingers  → 0 LEDs ON
1 finger   → 1 LED ON
2 fingers  → 2 LEDs ON
3 fingers  → 3 LEDs ON
4 fingers  → 4 LEDs ON
5 fingers  → 5 LEDs ON
6 fingers  → 6 LEDs ON
7 fingers  → 7 LEDs ON
8 fingers  → 8 LEDs ON
9 fingers  → 9 LEDs ON
10 fingers → 10 LEDs ON
```

## Finger Detection

The project uses MediaPipe Hand Landmarker to obtain 21 landmarks for each detected hand.

The four fingers other than the thumb are detected by comparing the vertical positions of their fingertip and PIP joint landmarks.

The thumb uses a geometric distance calculation. The distance between the thumb tip and index finger MCP is compared against the palm size to determine whether the thumb is extended.

The finger counts from both detected hands are then combined to obtain the total finger count.

## Python Program

`handtest.py` handles the computer-vision side of the project.

It:

1. Captures frames from the webcam using OpenCV.
2. Mirrors the webcam feed.
3. Converts the frame from BGR to RGB.
4. Creates a MediaPipe image.
5. Detects up to two hands using the Hand Landmarker.
6. Extracts the 21 landmarks from each detected hand.
7. Applies the custom finger-counting logic.
8. Calculates the total number of detected fingers.
9. Sends the finger count to the Arduino through serial communication.
10. Displays the finger count and detected hand landmarks on the webcam feed.

## Arduino Program

`handgestures.ino` handles the hardware side of the project.

The Arduino receives the finger count through serial communication and constrains the value between 0 and 10.

It then controls 10 LEDs so that the first `n` LEDs are turned on, where `n` is the detected finger count.

### LED Pin Configuration

```text
LED 1  → D3
LED 2  → D4
LED 3  → D5
LED 4  → D6
LED 5  → D7
LED 6  → D8
LED 7  → D9
LED 8  → D10
LED 9  → D11
LED 10 → D12
```

## Hardware

- Arduino
- 10 LEDs
- Current-limiting resistors
- Breadboard
- Jumper wires
- Webcam

## Software & Technologies

- Python
- OpenCV
- MediaPipe
- PySerial
- Arduino
- Serial Communication
- Computer Vision
- Embedded Systems

## Project Structure

```text
gesture-controlled-leds/
├── README.md
├── hand_landmarker.task
├── handgestures.ino
└── handtest.py
```

### `handtest.py`

Python program responsible for webcam capture, hand landmark detection, finger counting, visualization, and serial communication.

### `handgestures.ino`

Arduino program responsible for receiving the detected finger count and controlling the 10 LEDs.

### `hand_landmarker.task`

MediaPipe Hand Landmarker model used for detecting and tracking hand landmarks.

## Setup

### 1. Install Python Dependencies

```bash
pip install opencv-python mediapipe pyserial
```

### 2. Connect the Arduino

Connect the 10 LEDs to the Arduino according to the pin configuration above.

### 3. Upload the Arduino Code

Open `handgestures.ino` in the Arduino IDE and upload it to the Arduino.

### 4. Configure the Serial Port

In `handtest.py`, update the serial port if necessary:

```python
arduino = serial.Serial("COM9", 9600)
```

Replace `COM9` with the port assigned to your Arduino.

### 5. Run the Python Program

From the project directory:

```bash
python handtest.py
```

The webcam window will open and display the detected hand landmarks and current finger count.

Press `Q` to exit the program.

## Demo

[Watch the demo](media/demo.mp4)

## What I Learned

- Real-time hand tracking using MediaPipe
- Computer vision with OpenCV
- Working with MediaPipe's 21-point hand landmark system
- Implementing custom finger-counting logic
- Using geometric distance calculations for gesture detection
- Python-to-Arduino serial communication
- Controlling multiple LEDs using an Arduino
- Integrating computer vision with embedded hardware

## Future Improvements

- Improve finger detection across different hand orientations
- Add recognition of specific hand gestures
- Use gestures to control different hardware functions
- Improve the stability of finger detection
- Expand the system beyond LED control
- Develop a gesture-controlled virtual piano that uses hand movements to trigger musical notes.

## Technologies

`Python` `OpenCV` `MediaPipe` `PySerial` `Arduino` `Serial Communication` `Embedded Systems` `Computer Vision`
