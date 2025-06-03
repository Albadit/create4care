import cv2
import math
import time
import mediapipe as mp
import logging
import numpy as np  # New import for handling image arrays

# Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

class PoseDetector:
    def __init__(self):
        logging.debug("Initializing PoseDetector.")
        # Dictionary for all toggles.
        self.toggles = {
            "draw_alignment_lines": True,
            "draw_pose_landmarks": True,
            "neck_alignment": True,  # This toggle now handles shoulder-ear alignment.
            "torso_alignment": True,
            "knee_alignment": True,
            "feet_flat": True
        }
        
        # Lambda functions to toggle each flag.
        self.toggle_draw_alignment_lines = lambda: self.toggles.update({
            "draw_alignment_lines": not self.toggles["draw_alignment_lines"]
        })
        self.toggle_draw_pose_landmarks = lambda: self.toggles.update({
            "draw_pose_landmarks": not self.toggles["draw_pose_landmarks"]
        })
        self.toggle_neck_alignment = lambda: self.toggles.update({
            "neck_alignment": not self.toggles["neck_alignment"]
        })
        self.toggle_torso_alignment = lambda: self.toggles.update({
            "torso_alignment": not self.toggles["torso_alignment"]
        })
        self.toggle_knee_alignment = lambda: self.toggles.update({
            "knee_alignment": not self.toggles["knee_alignment"]
        })
        self.toggle_feet_flat = lambda: self.toggles.update({
            "feet_flat": not self.toggles["feet_flat"]
        })
        
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        try:
            self.pose = self.mp_pose.Pose(min_detection_confidence=0.5,
                                          min_tracking_confidence=0.5)
            logging.debug("Mediapipe Pose model loaded successfully.")
        except Exception as e:
            logging.error("Error initializing Mediapipe Pose model: %s", e)
            raise e
        
        # To avoid saving multiple screenshots
        self.image_saved = False
        self.landmark_image_saved = False  # New flag for landmark-only screenshot.
        self.correct_start_time = None  # To track when correct posture started

    # ----------------------------
    # Individual Check Functions
    # ----------------------------
    
    def evaluate_neck_alignment(self, landmarks, image, draw=True, ear_shoulder_angle_threshold=10):
        """
        Evaluates the alignment between the shoulder center and the average ear center.
        """
        logging.debug("Evaluating shoulder-ear alignment.")
        if not self.toggles["neck_alignment"]:
            logging.debug("Shoulder-ear alignment check is toggled off.")
            return True

        try:
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

            if draw:
                h, w, _ = image.shape
                ear_center_px = (int(ear_center_x * w), int(ear_center_y * h))
                shoulder_center_px = (int(shoulder_center_x * w), int(shoulder_center_y * h))
                cv2.line(image, ear_center_px, shoulder_center_px, (0, 165, 255), 2)  # Orange line.
                cv2.putText(image, f"Shoulder-Ear angle: {theta:.1f} deg", 
                            (shoulder_center_px[0] + 10, shoulder_center_px[1] + 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
            logging.debug("Shoulder-ear alignment: %.1f deg, OK: %s", theta, alignment_ok)
            return alignment_ok
        except Exception as e:
            logging.error("Error in evaluate_neck_alignment: %s", e)
            return False

    def evaluate_torso_alignment(self, landmarks, image, draw=True, alignment_factor=0.1):
        logging.debug("Evaluating torso alignment.")
        if not self.toggles["torso_alignment"]:
            logging.debug("Torso alignment check is toggled off.")
            return True

        try:
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

            if draw:
                h, w, _ = image.shape
                # Convert normalized coordinates to pixels.
                left_shoulder_px = (int(left_shoulder.x * w), int(left_shoulder.y * h))
                right_shoulder_px = (int(right_shoulder.x * w), int(right_shoulder.y * h))
                left_hip_px = (int(left_hip.x * w), int(left_hip.y * h))
                right_hip_px = (int(right_hip.x * w), int(right_hip.y * h))
                left_knee_px = (int(left_knee.x * w), int(left_knee.y * h))
                right_knee_px = (int(right_knee.x * w), int(right_knee.y * h))
                # Compute midpoints.
                shoulder_center_px = ((left_shoulder_px[0] + right_shoulder_px[0]) // 2,
                                      (left_shoulder_px[1] + right_shoulder_px[1]) // 2)
                hip_center_px = ((left_hip_px[0] + right_hip_px[0]) // 2,
                                 (left_hip_px[1] + right_hip_px[1]) // 2)
                knee_center_px = ((left_knee_px[0] + right_knee_px[0]) // 2,
                                  (left_knee_px[1] + right_knee_px[1]) // 2)
                # Draw lines connecting the midpoints.
                cv2.line(image, shoulder_center_px, hip_center_px, (0, 255, 0), 2)
                cv2.line(image, hip_center_px, knee_center_px, (0, 255, 0), 2)
            logging.debug("Torso alignment OK: %s", alignment_ok)
            return alignment_ok
        except Exception as e:
            logging.error("Error in evaluate_torso_alignment: %s", e)
            return False

    def evaluate_knee_alignment(self, landmarks, image, draw=True, knee_angle_threshold=160):
        logging.debug("Evaluating knee alignment.")
        if not self.toggles["knee_alignment"]:
            logging.debug("Knee alignment check is toggled off.")
            return True

        try:
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

            if draw:
                h, w, _ = image.shape
                left_knee_px = (int(left_knee.x * w), int(left_knee.y * h))
                right_knee_px = (int(right_knee.x * w), int(right_knee.y * h))
                cv2.putText(image, f"L Knee: {left_angle:.1f} deg", (left_knee_px[0] - 50, left_knee_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                cv2.putText(image, f"R Knee: {right_angle:.1f} deg", (right_knee_px[0] - 50, right_knee_px[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            logging.debug("Knee angles: L=%.1f, R=%.1f; OK: %s", left_angle, right_angle, knees_ok)
            return knees_ok
        except Exception as e:
            logging.error("Error in evaluate_knee_alignment: %s", e)
            return False

    def evaluate_feet_flat(self, landmarks, image, draw=True, foot_y_diff_threshold=0.02):
        logging.debug("Evaluating feet flatness.")
        if not self.toggles["feet_flat"]:
            logging.debug("Feet flat check is toggled off.")
            return True

        try:
            left_heel = landmarks[self.mp_pose.PoseLandmark.LEFT_HEEL.value]
            right_heel = landmarks[self.mp_pose.PoseLandmark.RIGHT_HEEL.value]
            left_toe = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
            right_toe = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]

            left_flat = abs(left_heel.y - left_toe.y) < foot_y_diff_threshold
            right_flat = abs(right_heel.y - right_toe.y) < foot_y_diff_threshold
            feet_flat_ok = left_flat and right_flat

            if draw:
                h, w, _ = image.shape
                left_heel_px = (int(left_heel.x * w), int(left_heel.y * h))
                left_toe_px = (int(left_toe.x * w), int(left_toe.y * h))
                right_heel_px = (int(right_heel.x * w), int(right_heel.y * h))
                right_toe_px = (int(right_toe.x * w), int(right_toe.y * h))
                cv2.line(image, left_heel_px, left_toe_px, (0, 255, 255), 2)
                cv2.line(image, right_heel_px, right_toe_px, (0, 255, 255), 2)
            logging.debug("Feet flat check: OK: %s", feet_flat_ok)
            return feet_flat_ok
        except Exception as e:
            logging.error("Error in evaluate_feet_flat: %s", e)
            return False

    def evaluate_posture(self, landmarks, image, draw=True,
                         alignment_factor=0.1, foot_y_diff_threshold=0.02,
                         neck_angle_threshold=10, knee_angle_threshold=160):
        logging.debug("Evaluating overall posture.")
        torso_ok = self.evaluate_torso_alignment(landmarks, image, draw, alignment_factor)
        feet_ok = self.evaluate_feet_flat(landmarks, image, draw, foot_y_diff_threshold)
        # Note: evaluate_neck_alignment now uses ear and shoulder positions.
        neck_ok = self.evaluate_neck_alignment(landmarks, image, draw, neck_angle_threshold)
        knee_ok = self.evaluate_knee_alignment(landmarks, image, draw, knee_angle_threshold)
        overall_ok = torso_ok and feet_ok and neck_ok and knee_ok
        logging.debug("Posture evaluation: torso=%s, feet=%s, shoulder-ear=%s, knees=%s => Overall OK=%s",
                      torso_ok, feet_ok, neck_ok, knee_ok, overall_ok)
        return overall_ok

    # ----------------------------
    # Main Processing Functions
    # ----------------------------

    def process_frame(self, frame):
        logging.debug("Processing a new frame.")
        try:
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except Exception as e:
            logging.error("Error converting frame to RGB: %s", e)
            return frame

        image_rgb.flags.writeable = False
        try:
            results = self.pose.process(image_rgb)
        except Exception as e:
            logging.error("Error processing frame with Mediapipe: %s", e)
            return frame
        image_rgb.flags.writeable = True
        try:
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        except Exception as e:
            logging.error("Error converting image_rgb back to BGR: %s", e)
            return frame

        if results.pose_landmarks:
            logging.debug("Pose landmarks detected.")
            if self.toggles["draw_pose_landmarks"]:
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            posture_ok = self.evaluate_posture(results.pose_landmarks.landmark, image, draw=self.toggles["draw_alignment_lines"])
            current_time = time.time()
            # If posture is correct, start or continue the timer.
            if posture_ok:
                if self.correct_start_time is None:
                    self.correct_start_time = current_time
                    logging.info("Correct posture detected; starting timer.")
                # Calculate how long the posture has been correct.
                elapsed = current_time - self.correct_start_time
                cv2.putText(image, f"Good posture: {elapsed:.1f}s", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                logging.debug("Posture has been correct for %.1f seconds.", elapsed)
                # Once correct for 5 seconds, take screenshots if not already saved.
                if elapsed >= 5:
                    if not self.image_saved:
                        filename = f"standing_straight_{int(time.time())}.png"
                        try:
                            cv2.imwrite(filename, image)
                            self.image_saved = True
                            logging.info("Screenshot saved as %s", filename)
                        except Exception as e:
                            logging.error("Error saving screenshot: %s", e)
                    
                    if not self.landmark_image_saved:
                        # Create a blank (black) image of the same shape.
                        blank = np.zeros_like(image)
                        # Draw only the pose landmarks on the blank image.
                        self.mp_drawing.draw_landmarks(blank, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                        landmark_filename = f"landmarks_only_{int(time.time())}.png"
                        try:
                            cv2.imwrite(landmark_filename, blank)
                            self.landmark_image_saved = True
                            logging.info("Landmark screenshot saved as %s", landmark_filename)
                        except Exception as e:
                            logging.error("Error saving landmark screenshot: %s", e)
            else:
                logging.info("Posture not correct; timer reset.")
                # Reset timer if posture is not correct.
                self.correct_start_time = None
                cv2.putText(image, "Please stand straight", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            logging.debug("No pose landmarks detected in this frame.")

        return image

    def run(self):
        logging.info("Starting video capture.")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logging.error("Error: Could not open webcam.")
            return

        # Setting up resolution and FPS.
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 60)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                logging.error("Error: Failed to capture frame.")
                break

            annotated_image = self.process_frame(frame)
            cv2.imshow('Pose Detection', annotated_image)

            # Key controls:
            # 'o' toggles custom alignment lines drawing.
            # 'p' toggles built-in pose landmarks.
            # 'n' toggles shoulder-ear alignment check (formerly neck alignment).
            # 'r' toggles torso alignment check.
            # 'e' toggles feet flat check.
            # 'k' toggles knee alignment check.
            # 'q' quits.
            key = cv2.waitKey(10) & 0xFF
            if key == ord('o'):
                self.toggle_draw_alignment_lines()
                logging.debug("Toggled draw_alignment_lines: %s", self.toggles["draw_alignment_lines"])
            elif key == ord('p'):
                self.toggle_draw_pose_landmarks()
                logging.debug("Toggled draw_pose_landmarks: %s", self.toggles["draw_pose_landmarks"])
            elif key == ord('n'):
                self.toggle_neck_alignment()
                logging.debug("Toggled neck_alignment: %s", self.toggles["neck_alignment"])
            elif key == ord('r'):
                self.toggle_torso_alignment()
                logging.debug("Toggled torso_alignment: %s", self.toggles["torso_alignment"])
            elif key == ord('e'):
                self.toggle_feet_flat()
                logging.debug("Toggled feet_flat: %s", self.toggles["feet_flat"])
            elif key == ord('k'):
                self.toggle_knee_alignment()
                logging.debug("Toggled knee_alignment: %s", self.toggles["knee_alignment"])
            elif key == ord('q'):
                logging.info("Quit key pressed. Exiting.")
                break

        cap.release()
        cv2.destroyAllWindows()
        logging.info("Video capture ended.")

if __name__ == "__main__":
    # try:
        detector = PoseDetector()
        detector.run()
    # except Exception as e:
    #     logging.critical("Fatal error in main execution: %s", e)
