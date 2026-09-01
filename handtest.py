import cv2
import mediapipe as mp
import math
import serial
import time


# ==========================================
# MediaPipe setup
# ==========================================

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2
)


# ==========================================
# Distance between two landmarks
# ==========================================

def distance(a, b):
    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2
    )


# ==========================================
# Count fingers on ONE hand
# ==========================================

def count_fingers(hand):

    fingers = 0

    # -----------------------------
    # Index, middle, ring, little
    # -----------------------------

    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]

    for tip, pip in zip(finger_tips, finger_pips):

        if hand[tip].y < hand[pip].y:
            fingers += 1

    # -----------------------------
    # Thumb
    # -----------------------------

    thumb_tip = hand[4]
    index_mcp = hand[5]

    palm_size = distance(hand[0], hand[9])
    thumb_distance = distance(thumb_tip, index_mcp)

    # Natural thumb extension threshold
    if thumb_distance > palm_size * 0.55:
        fingers += 1

    return fingers


# ==========================================
# Connect to Arduino
# ==========================================

arduino = serial.Serial("COM9", 9600)

# Arduino resets when Serial connection opens
time.sleep(2)


# ==========================================
# Webcam
# ==========================================

cap = cv2.VideoCapture(0)


# ==========================================
# Start MediaPipe
# ==========================================

with HandLandmarker.create_from_options(options) as landmarker:

    while True:

        success, frame = cap.read()

        if not success:
            print("Could not access webcam")
            break

        # Mirror webcam
        frame = cv2.flip(frame, 1)

        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Create MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hands
        result = landmarker.detect(mp_image)


        # ==================================
        # Count fingers from both hands
        # ==================================

        total_fingers = 0

        if result.hand_landmarks:

            for hand in result.hand_landmarks:

                fingers = count_fingers(hand)

                total_fingers += fingers


        # ==================================
        # Keep value between 0 and 10
        # ==================================

        total_fingers = max(0, min(total_fingers, 10))


        # ==================================
        # Send number to Arduino
        # ==================================

        arduino.write(
            f"{total_fingers}\n".encode()
        )


        # ==================================
        # Display finger count
        # ==================================

        cv2.putText(
            frame,
            f"Fingers: {total_fingers}",
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            3
        )


        # ==================================
        # Draw hand landmarks
        # ==================================

        if result.hand_landmarks:

            h, w, _ = frame.shape

            for hand in result.hand_landmarks:

                # Draw points
                for landmark in hand:

                    x = int(landmark.x * w)
                    y = int(landmark.y * h)

                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 255, 0),
                        -1
                    )

                # Hand connections
                connections = [
                    (0, 1), (1, 2), (2, 3), (3, 4),
                    (0, 5), (5, 6), (6, 7), (7, 8),
                    (5, 9), (9, 10), (10, 11), (11, 12),
                    (9, 13), (13, 14), (14, 15), (15, 16),
                    (13, 17), (17, 18), (18, 19), (19, 20),
                    (0, 17)
                ]

                for start, end in connections:

                    x1 = int(hand[start].x * w)
                    y1 = int(hand[start].y * h)

                    x2 = int(hand[end].x * w)
                    y2 = int(hand[end].y * h)

                    cv2.line(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )


        # ==================================
        # Show webcam
        # ==================================

        cv2.imshow(
            "10 Finger LED Controller",
            frame
        )


        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


# ==========================================
# Cleanup
# ==========================================

cap.release()
cv2.destroyAllWindows()
arduino.close()