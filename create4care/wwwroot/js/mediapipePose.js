// Default modelComplexity = 1
// Lightweight (0)
// Standard (1)
// Heavy (2)

window.startMediapipePose = function () {
    const videoElement = document.getElementById("videoInput");
    const canvasElement = document.getElementById("output");
    const canvasCtx = canvasElement.getContext("2d");
    const counterElem = document.getElementById("counter");
    const notificationElem = document.getElementById("notification");
    const container = document.getElementById("container");

    // New elements for loading and error states.
    const loadingElem = document.getElementById("loading");
    const errorElem = document.getElementById("error");

    // Flags and timer for screenshots and posture timer.
    // let imageSaved = false;
    let landmarkImageSaved = false;
    let correctStartTime = null;
    let correctEndTime = 3;

    // Define landmark indices (based on MediaPipe Pose's 33-landmark model).
    const LANDMARKS = {
        LEFT_EAR: 7,
        RIGHT_EAR: 8,
        LEFT_SHOULDER: 11,
        RIGHT_SHOULDER: 12,
        LEFT_HIP: 23,
        RIGHT_HIP: 24,
        LEFT_KNEE: 25,
        RIGHT_KNEE: 26,
        LEFT_ANKLE: 27,
        RIGHT_ANKLE: 28,
        LEFT_HEEL: 29,
        RIGHT_HEEL: 30,
        LEFT_FOOT_INDEX: 31,
        RIGHT_FOOT_INDEX: 32,
    };

    // --- Posture Evaluation Functions ---

    // Check neck alignment between ear center and shoulder center.
    function evaluateNeckAlignment(landmarks, angleThreshold = 10) {
        const leftEar = landmarks[LANDMARKS.LEFT_EAR];
        const rightEar = landmarks[LANDMARKS.RIGHT_EAR];
        const leftShoulder = landmarks[LANDMARKS.LEFT_SHOULDER];
        const rightShoulder = landmarks[LANDMARKS.RIGHT_SHOULDER];

        if (!leftEar || !rightEar || !leftShoulder || !rightShoulder) {
            return false;
        }
    
        const shoulderCenterX = (leftShoulder.x + rightShoulder.x) / 2;
        const shoulderCenterY = (leftShoulder.y + rightShoulder.y) / 2;
        const earCenterX = (leftEar.x + rightEar.x) / 2;
        const earCenterY = (leftEar.y + rightEar.y) / 2;
    
        const deltaX = shoulderCenterX - earCenterX;
        const deltaY = shoulderCenterY - earCenterY;
        const theta = Math.atan2(deltaX, deltaY) * (180 / Math.PI);
        return Math.abs(theta) < angleThreshold;
    }

    // Check torso alignment by comparing horizontal centers of shoulders, hips, and knees.
    function evaluateTorsoAlignment(landmarks, alignmentFactor = 0.1) {
        const leftShoulder = landmarks[LANDMARKS.LEFT_SHOULDER];
        const rightShoulder = landmarks[LANDMARKS.RIGHT_SHOULDER];
        const leftHip = landmarks[LANDMARKS.LEFT_HIP];
        const rightHip = landmarks[LANDMARKS.RIGHT_HIP];
        const leftKnee = landmarks[LANDMARKS.LEFT_KNEE];
        const rightKnee = landmarks[LANDMARKS.RIGHT_KNEE];

        if (!leftShoulder || !rightShoulder || !leftHip || !rightHip || !leftKnee || !rightKnee) {
            return false;
        }
    
        const shoulderCenterY = (leftShoulder.y + rightShoulder.y) / 2;
        const hipCenterY = (leftHip.y + rightHip.y) / 2;
        const torsoLength = Math.abs(shoulderCenterY - hipCenterY);
        const threshold = torsoLength * alignmentFactor;
    
        const shoulderCenterX = (leftShoulder.x + rightShoulder.x) / 2;
        const hipCenterX = (leftHip.x + rightHip.x) / 2;
        const kneeCenterX = (leftKnee.x + rightKnee.x) / 2;
    
        return (
            Math.abs(shoulderCenterX - hipCenterX) < threshold &&
            Math.abs(hipCenterX - kneeCenterX) < threshold
        );
    }

    // Utility to calculate the angle between three points (in degrees) at point b.
    function calculateAngle(a, b, c) {
        const baX = a.x - b.x;
        const baY = a.y - b.y;
        const bcX = c.x - b.x;
        const bcY = c.y - b.y;
        const dotProduct = baX * bcX + baY * bcY;
        const normBA = Math.sqrt(baX * baX + baY * baY);
        const normBC = Math.sqrt(bcX * bcX + bcY * bcY);
        if (normBA * normBC === 0) return 0;
        const angleRad = Math.acos(dotProduct / (normBA * normBC));
        return angleRad * (180 / Math.PI);
    }

    // Ensure both knees are bent at an acceptable angle.
    function evaluateKneeAlignment(landmarks, kneeAngleThreshold = 160) {
        const leftHip = landmarks[LANDMARKS.LEFT_HIP];
        const leftKnee = landmarks[LANDMARKS.LEFT_KNEE];
        const leftAnkle = landmarks[LANDMARKS.LEFT_ANKLE];
    
        const rightHip = landmarks[LANDMARKS.RIGHT_HIP];
        const rightKnee = landmarks[LANDMARKS.RIGHT_KNEE];
        const rightAnkle = landmarks[LANDMARKS.RIGHT_ANKLE];
    
        if (!leftHip || !leftKnee || !leftAnkle || !rightHip || !rightKnee || !rightAnkle) {
            return false;
        }

        const leftAngle = calculateAngle(leftHip, leftKnee, leftAnkle);
        const rightAngle = calculateAngle(rightHip, rightKnee, rightAnkle);
    
        return leftAngle >= kneeAngleThreshold && rightAngle >= kneeAngleThreshold;
    }

    // Check that both feet are flat by comparing heel and toe vertical positions.
    function evaluateFeetFlat(landmarks, footYDiffThreshold = 0.02) {
        const leftHeel = landmarks[LANDMARKS.LEFT_HEEL];
        const rightHeel = landmarks[LANDMARKS.RIGHT_HEEL];
        const leftToe = landmarks[LANDMARKS.LEFT_FOOT_INDEX];
        const rightToe = landmarks[LANDMARKS.RIGHT_FOOT_INDEX];

        if (!leftHeel || !rightHeel || !leftToe || !rightToe) {
            return false;
        }
    
        const leftFlat = Math.abs(leftHeel.y - leftToe.y) < footYDiffThreshold;
        const rightFlat = Math.abs(rightHeel.y - rightToe.y) < footYDiffThreshold;
        return leftFlat && rightFlat;
    }

    // Combine the checks to decide if the overall posture is correct.
    function evaluatePosture(
        landmarks,
        alignmentFactor = 0.1,
        footYDiffThreshold = 0.02,
        neckAngleThreshold = 10,
        kneeAngleThreshold = 160
    ) {
        const torsoOk = evaluateTorsoAlignment(landmarks, alignmentFactor);
        const neckOk = evaluateNeckAlignment(landmarks, neckAngleThreshold);
        const kneeOk = evaluateKneeAlignment(landmarks, kneeAngleThreshold);
        const feetOk = evaluateFeetFlat(landmarks, footYDiffThreshold);
        return torsoOk && neckOk && kneeOk && feetOk;
    }

    // --- Setup MediaPipe Pose ---
    const pose = new Pose({
        locateFile: (file) =>
            `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
    });

    pose.setOptions({
        modelComplexity: 0,
        smoothLandmarks: true,
        enableSegmentation: false,
        smoothSegmentation: false,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5,
    });

    pose.onResults((results) => {
        if (!results.poseLandmarks) { return; }
        canvasCtx.save();

        // Clear the canvas and draw the video frame.
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

        const currentTime = performance.now() / 1000; // current time in seconds
        postureOk = evaluatePosture(results.poseLandmarks);

        if (postureOk) {
            if (!correctStartTime) {
                correctStartTime = currentTime;
            }
            const elapsed = currentTime - correctStartTime;
    
            // Update the counter element with the elapsed time.
            if (counterElem) {
                counterElem.style.visibility = "visible";
                counterElem.innerText = `${elapsed.toFixed(1)}s`;
            }
    
            // If the correct posture has been maintained for 5 seconds, trigger screenshots.
            if (elapsed >= correctEndTime) {
                // if (!imageSaved) {
                //     const link = document.createElement("a");
                //     link.download = `standing_straight_${Date.now()}.png`;
                //     link.href = canvasElement.toDataURL();
                //     link.click();
                //     imageSaved = true;
                // }
                if (!landmarkImageSaved) {
                    // Create a temporary canvas for landmark-only image.
                    const blankCanvas = document.createElement("canvas");
                    blankCanvas.width = canvasElement.width;
                    blankCanvas.height = canvasElement.height;
                    const blankCtx = blankCanvas.getContext("2d");
        
                    // The drawing functions are provided by the MediaPipe drawing_utils.
                    drawConnectors(blankCtx, results.poseLandmarks, POSE_CONNECTIONS, { color: "#FFFFFF", lineWidth: 4 });
                    drawLandmarks(blankCtx, results.poseLandmarks, { color: "#FF0000", lineWidth: 2 });

                    const link2 = document.createElement("a");
                    link2.download = `landmarks_only_${Date.now()}.png`;
                    link2.href = blankCanvas.toDataURL();
                    link2.click();
                    landmarkImageSaved = true;

                    if (counterElem) { counterElem.style.display = "none"; }
                    if (notificationElem) {
                        notificationElem.style.display = "block";
                        notificationElem.innerText = "Image is saved";
                    }
                }
            }
        } else {
            correctStartTime = null;
            if (counterElem) {
                counterElem.style.visibility = "hidden";
                counterElem.innerText = "0.0s";
            }
        }

        canvasCtx.globalAlpha = 0.1;
        canvasCtx.fillStyle = postureOk ? "green" : "none";
        canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);
        canvasCtx.globalAlpha = 1.0;
    
        canvasCtx.restore();
    });

    // --- Function to Adjust Canvas Based on Container Width and Height ---
    function adjustCanvas() {
        const dpr = window.devicePixelRatio || 1;
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;
    
        const videoWidth = videoElement.videoWidth;
        const videoHeight = videoElement.videoHeight;
        if (!videoWidth || !videoHeight) return;
    
        const videoAspectRatio = videoWidth / videoHeight;
        const containerAspectRatio = containerWidth / containerHeight;
    
        let displayWidth, displayHeight;
    
        if (containerAspectRatio > videoAspectRatio) {
            // Container is wider than video: fit width, crop height
            displayWidth = containerWidth;
            displayHeight = containerWidth / videoAspectRatio;
        } else {
            // Container is taller than video: fit height, crop width
            displayHeight = containerHeight;
            displayWidth = containerHeight * videoAspectRatio;
        }
    
        canvasElement.width = displayWidth * dpr;
        canvasElement.height = displayHeight * dpr;
    
        canvasElement.style.width = displayWidth + "px";
        canvasElement.style.height = displayHeight + "px";
    
        canvasCtx.setTransform(1, 0, 0, 1, 0, 0);
        canvasCtx.scale(dpr, dpr);
    }

    // Show the loading indicator.
    if (loadingElem) {
        loadingElem.style.display = "block";
    }

    // --- Start Camera and Processing Loop ---
    // navigator.mediaDevices
    //     .getUserMedia({
    //         video: {
    //             facingMode: "environment",
    //             width: { ideal: 1920 },
    //             height: { ideal: 1080 },
    //         },
    //     })
    //     .then((stream) => {
    //         videoElement.srcObject = stream;
    //         videoElement.play();
    
    //         videoElement.onloadedmetadata = () => {
    //             adjustCanvas();
        
    //             async function processFrame() {
    //                 await pose.send({ image: videoElement });
    //                 requestAnimationFrame(processFrame);
    //             }
    //             processFrame();
    //         };
    //     })
    //     .catch((error) => {
    //         console.error("Error accessing the camera:", error);
    //     });
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({
            // video: {
            //     facingMode: "environment",
            //     width: { ideal: 1920 },
            //     height: { ideal: 1080 },
            // },
            video: true,
        })
        .then((stream) => {
            // Hide any previous error messages.
            if (errorElem) {
                errorElem.style.display = "none";
            }
            videoElement.srcObject = stream;
            videoElement.play();
    
            videoElement.onloadedmetadata = () => {
                // Hide the loading indicator when the video metadata has loaded.
                if (loadingElem) {
                    loadingElem.style.display = "none";
                }
                adjustCanvas();
        
                async function processFrame() {
                    await pose.send({ image: videoElement });
                    requestAnimationFrame(processFrame);
                }
                processFrame();
            };
        })
        .catch((error) => {
            // Hide the loading indicator and display an error message.
            if (loadingElem) {
                loadingElem.style.display = "none";
            }
            if (errorElem) {
                errorElem.style.display = "block";
                errorElem.innerText = "Error accessing the camera: " + error.message;
            }
            console.error("Error accessing the camera:", error);
        });
    } else {
        errorElem.style.display = "block";
        errorElem.innerText = "getUserMedia is not supported in this browser.";
        console.error("getUserMedia is not supported in this browser.");
    }

    window.addEventListener("resize", () => {
        adjustCanvas();
        // startMediapipePose();
    });
};
