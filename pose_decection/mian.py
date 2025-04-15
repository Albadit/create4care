import cv2
import math
import time
import mediapipe as mp
import numpy as np

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # To avoid saving multiple screenshots
        self.image_saved = False
        self.landmark_image_saved = False  # New flag for landmark-only screenshot.
        self.correct_start_time = None  # To track when correct posture started

    # ----------------------------
    # Individual Check Functions
    # ----------------------------
    
    def evaluate_neck_alignment(self, landmarks, ear_shoulder_angle_threshold=10):
        # Get ear landmarks.
        left_ear = landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value]
        right_ear = landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value]
        # Get shoulder landmarks.
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # Compute centers: average of shoulders and average of ears.
        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
        shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
        ear_center_x = (left_ear.x + right_ear.x) / 2
        ear_center_y = (left_ear.y + right_ear.y) / 2

        # Compute the angle between the line connecting ear center and shoulder center relative to the vertical.
        delta_x = shoulder_center_x - ear_center_x
        delta_y = shoulder_center_y - ear_center_y
        theta = math.degrees(math.atan2(delta_x, delta_y))
        alignment_ok = abs(theta) < ear_shoulder_angle_threshold

        return alignment_ok

    def evaluate_torso_alignment(self, landmarks, alignment_factor=0.1):
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]

        torso_length = abs(((left_shoulder.y + right_shoulder.y) / 2) - ((left_hip.y + right_hip.y) / 2))
        threshold = torso_length * alignment_factor

        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
        hip_center_x = (left_hip.x + right_hip.x) / 2
        knee_center_x = (left_knee.x + right_knee.x) / 2

        alignment_ok = (abs(shoulder_center_x - hip_center_x) < threshold and
                        abs(hip_center_x - knee_center_x) < threshold)

        return alignment_ok

    def evaluate_knee_alignment(self, landmarks, knee_angle_threshold=160):
        # Left knee angle.
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
        # Right knee angle.
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]
        right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        def calculate_angle(a, b, c):
            # a, b, c are (x, y) tuples; angle at b.
            ba = (a[0] - b[0], a[1] - b[1])
            bc = (c[0] - b[0], c[1] - b[1])
            dot_product = ba[0]*bc[0] + ba[1]*bc[1]
            norm_ba = math.sqrt(ba[0]**2 + ba[1]**2)
            norm_bc = math.sqrt(bc[0]**2 + bc[1]**2)
            if norm_ba * norm_bc == 0:
                return 0
            angle_rad = math.acos(dot_product / (norm_ba * norm_bc))
            return math.degrees(angle_rad)

        left_hip_coord = (left_hip.x, left_hip.y)
        left_knee_coord = (left_knee.x, left_knee.y)
        left_ankle_coord = (left_ankle.x, left_ankle.y)

        right_hip_coord = (right_hip.x, right_hip.y)
        right_knee_coord = (right_knee.x, right_knee.y)
        right_ankle_coord = (right_ankle.x, right_ankle.y)

        left_angle = calculate_angle(left_hip_coord, left_knee_coord, left_ankle_coord)
        right_angle = calculate_angle(right_hip_coord, right_knee_coord, right_ankle_coord)

        knees_ok = (left_angle >= knee_angle_threshold and right_angle >= knee_angle_threshold)

        return knees_ok

    def evaluate_feet_flat(self, landmarks, foot_y_diff_threshold=0.02):
        left_heel = landmarks[self.mp_pose.PoseLandmark.LEFT_HEEL.value]
        right_heel = landmarks[self.mp_pose.PoseLandmark.RIGHT_HEEL.value]
        left_toe = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
        right_toe = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]

        left_flat = abs(left_heel.y - left_toe.y) < foot_y_diff_threshold
        right_flat = abs(right_heel.y - right_toe.y) < foot_y_diff_threshold
        feet_flat_ok = left_flat and right_flat

        return feet_flat_ok

    def evaluate_posture(self, landmarks, alignment_factor=0.1, foot_y_diff_threshold=0.02, neck_angle_threshold=10, knee_angle_threshold=160):
        torso_ok = self.evaluate_torso_alignment(landmarks, alignment_factor)
        feet_ok = self.evaluate_feet_flat(landmarks, foot_y_diff_threshold)
        neck_ok = self.evaluate_neck_alignment(landmarks, neck_angle_threshold)
        knee_ok = self.evaluate_knee_alignment(landmarks, knee_angle_threshold)
        overall_ok = torso_ok and feet_ok and neck_ok and knee_ok

        return overall_ok

    # ----------------------------
    # Main Processing Functions
    # ----------------------------

    def process_frame(self, frame):
        posture_ok = False
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image_rgb.flags.writeable = False
        try:
            results = self.pose.process(image_rgb)
        except:
            return frame
        
        image_rgb.flags.writeable = True
        try:
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        except:
            return frame

        if results.pose_landmarks:
            posture_ok = self.evaluate_posture(results.pose_landmarks.landmark)
            current_time = time.time()
            
            # If posture is correct, start or continue the timer.
            if posture_ok:
                if self.correct_start_time is None:
                    self.correct_start_time = current_time

                # Calculate how long the posture has been correct.
                elapsed = current_time - self.correct_start_time
                # Only display the timer text when posture is correct (green).
                cv2.putText(image, f"{elapsed:.1f}s", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Once correct for 5 seconds, take screenshots if not already saved.
                if elapsed >= 5:
                    if not self.image_saved:
                        filename = f"standing_straight_{int(time.time())}.png"
                        try:
                            cv2.imwrite(filename, image)
                            self.image_saved = True
                        except Exception as e:
                            print("Error saving screenshot: %s", e)
                    
                    if not self.landmark_image_saved:
                        # Create a blank (black) image of the same shape.
                        blank = np.zeros_like(image)
                        # Draw only the pose landmarks on the blank image.
                        self.mp_drawing.draw_landmarks(blank, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                        landmark_filename = f"landmarks_only_{int(time.time())}.png"
                        try:
                            cv2.imwrite(landmark_filename, blank)
                            self.landmark_image_saved = True
                        except Exception as e:
                            print("Error saving landmark screenshot: %s", e)
            else:
                # Reset timer if posture is not correct.
                self.correct_start_time = None

        if posture_ok:
            overlay_color = (0, 255, 0)  # Green in BGR
        else:
            overlay_color = (0, 0, 255)  # Red in BGR

        height, width = image.shape[:2]
        overlay = np.full((height, width, 3), overlay_color, dtype=np.uint8)
        # Blend the overlay with the original image with an opacity of 0.1.
        image = cv2.addWeighted(overlay, 0.1, image, 0.9, 0)

        return image

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return

        # Setting up resolution and FPS.
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 60)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            annotated_image = self.process_frame(frame)
            cv2.imshow('Pose Detection', annotated_image)

            key = cv2.waitKey(10) & 0xFF

            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = PoseDetector()
    detector.run()
