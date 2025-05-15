import cv2
import math
import mediapipe as mp
import numpy as np

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            model_complexity=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def evaluate_neck_alignment(self, landmarks, ear_shoulder_angle_threshold=50):
        left_ear = landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value]
        right_ear = landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
        shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
        ear_center_x = (left_ear.x + right_ear.x) / 2
        ear_center_y = (left_ear.y + right_ear.y) / 2

        delta_x = shoulder_center_x - ear_center_x
        delta_y = shoulder_center_y - ear_center_y
        theta = math.degrees(math.atan2(delta_x, delta_y))
        return abs(theta) < ear_shoulder_angle_threshold

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

        return (abs(shoulder_center_x - hip_center_x) < threshold and
                abs(hip_center_x - knee_center_x) < threshold)

    def evaluate_knee_alignment(self, landmarks, knee_angle_threshold=160):
        def calculate_angle(a, b, c):
            ba = (a[0] - b[0], a[1] - b[1])
            bc = (c[0] - b[0], c[1] - b[1])
            dot = ba[0]*bc[0] + ba[1]*bc[1]
            norm_ba = math.hypot(*ba)
            norm_bc = math.hypot(*bc)
            if norm_ba * norm_bc == 0:
                return 0
            angle = math.degrees(math.acos(dot / (norm_ba * norm_bc)))
            return angle

        left = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value],
                landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]]
        right = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                 landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],
                 landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]]

        left_angle = calculate_angle((left[0].x, left[0].y),
                                     (left[1].x, left[1].y),
                                     (left[2].x, left[2].y))
        right_angle = calculate_angle((right[0].x, right[0].y),
                                      (right[1].x, right[1].y),
                                      (right[2].x, right[2].y))

        return left_angle >= knee_angle_threshold and right_angle >= knee_angle_threshold

    def evaluate_feet_flat(self, landmarks, foot_y_diff_threshold=0.02):
        left_heel = landmarks[self.mp_pose.PoseLandmark.LEFT_HEEL.value]
        right_heel = landmarks[self.mp_pose.PoseLandmark.RIGHT_HEEL.value]
        left_toe = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
        right_toe = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]

        left_flat = abs(left_heel.y - left_toe.y) < foot_y_diff_threshold
        right_flat = abs(right_heel.y - right_toe.y) < foot_y_diff_threshold
        return left_flat and right_flat

    # ----------------------------
    # Main Processing Functions
    # ----------------------------

    def evaluate_image(self, image_path):
        """
        Evaluate a single image for posture correctness.
        Returns:
            - {'issues': [...]} if posture is incorrect
            - {'landmark_image': np.ndarray} if posture is correct (image with landmarks only)
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Cannot load image from {image_path}")

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)

        if not results.pose_landmarks:
            return {'issues': ['No pose detected in the image']}

        landmarks = results.pose_landmarks.landmark
        issues = []

        if not self.evaluate_neck_alignment(landmarks):
            issues.append('Adjust neck alignment: keep ears over shoulders')
        if not self.evaluate_torso_alignment(landmarks):
            issues.append('Straighten torso: align shoulders, hips, and knees vertically')
        if not self.evaluate_knee_alignment(landmarks):
            issues.append('Extend knees: keep legs straight')
        if not self.evaluate_feet_flat(landmarks):
            issues.append('Place feet flat on the ground')

        if issues:
            return {'issues': issues}
        else:
            # Create a transparent background image (4-channel)
            h, w = image.shape[:2]
            transparent = np.zeros((h, w, 4), dtype=np.uint8)
            # Draw landmarks onto a separate BGR canvas
            canvas = np.zeros((h, w, 3), dtype=np.uint8)
            self.mp_drawing.draw_landmarks(
                canvas,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )
            # Convert canvas to BGRA and set alpha where landmarks exist
            canvas_bgra = cv2.cvtColor(canvas, cv2.COLOR_BGR2BGRA)
            # Alpha channel: non-black pixels become opaque
            alpha = np.any(canvas != 0, axis=2).astype(np.uint8) * 255
            canvas_bgra[:, :, 3] = alpha
            return {'landmark_image': canvas_bgra}

if __name__ == "__main__":
    detector = PoseDetector()
    # Replace with your image path (use raw string, double backslashes, or forward slashes)
    img_path = r'C:/Users/ardit/Documents/GitHub/School/year_3/sem6/pose_decection/dummy_correct.jpg'
    result = detector.evaluate_image(img_path)
    if 'issues' in result:
        print("Posture improvements needed:")
        for issue in result['issues']:
            print("-", issue)
    else:
        landmark_img = result['landmark_image']
        # Save landmark-only image to current working directory
        save_filename = 'landmarks_only.png'
        cv2.imwrite(save_filename, landmark_img)
        print(f"Landmark image saved as {save_filename} in the current folder.")