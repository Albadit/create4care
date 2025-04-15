// Default modelComplexity = 1
// Lightweight (0)
// Standard (1)
// Heavy (2)

window.startMediapipePose = function () {
    const videoElement = document.getElementById("videoInput");
    const canvasElement = document.getElementById("output");
    const canvasCtx = canvasElement.getContext("2d");
    const notificationElem = document.getElementById("notification");
    const loadingElem = document.getElementById("loading");
    const errorElem = document.getElementById("error");
    const snapshotButton = document.getElementById("snapshotButton");
    let initialSettings = null;
    let capabilities = null;

    // Define landmark indices (based on MediaPipe Pose's 33-landmark model)
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

    // --- API Call Function ---
    async function postMeasurement(measurementData) {
        try {
            const response = await fetch("https://api.blokk.mooo.com/measurements", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(measurementData)
            });
            if (!response.ok) {
                throw new Error("Network response was not ok: " + response.status);
            }
            const responseData = await response.json();
            console.log("Measurement saved successfully:", responseData);
            return responseData;
        } catch (error) {
            console.error("Error posting measurement:", error);
            return null;
        }
    }

    // --- Pose Evaluation Functions ---
    function evaluateNeckAlignment(landmarks, angleThreshold = 20) {
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

    function evaluatePosture(landmarks) {
        const torsoOk = evaluateTorsoAlignment(landmarks);
        const neckOk = evaluateNeckAlignment(landmarks);
        const kneeOk = evaluateKneeAlignment(landmarks);
        const feetOk = evaluateFeetFlat(landmarks);
        return { postureOk: torsoOk && neckOk && kneeOk && feetOk, torsoOk, neckOk, kneeOk, feetOk };
    }

    // --- Setup MediaPipe Pose ---
    const pose = new Pose({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
    });

    pose.setOptions({
        modelComplexity: 0,
        smoothLandmarks: true,
        enableSegmentation: false,
        smoothSegmentation: false,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5,
    });

    // Process results from the snapshot
    pose.onResults(async (results) => {
        canvasCtx.save();
        // Clear the canvas and draw the snapshot (results.image)
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

        // Hide any previous notifications
        notificationElem.style.display = "none";

        if (!results.poseLandmarks) {
            // When no pose is detected.
            canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
            canvasCtx.fillStyle = "rgba(255,0,0,0.3)";
            canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);
            notificationElem.style.display = "block";
            notificationElem.innerText = "No pose detected. Please try again.";
            snapshotButton.innerText = "Try Again";
            // Update display: show canvas, hide video.
            canvasElement.style.display = "block";
            videoElement.style.display = "none";
            canvasCtx.restore();
            return;
        }

        // Evaluate overall posture and get individual check results.
        const { postureOk, torsoOk, neckOk, kneeOk, feetOk } = evaluatePosture(results.poseLandmarks);

        // (Optional) Uncomment to visualize the pose landmarks:
        // drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, { color: "#FFFFFF", lineWidth: 4 });
        // drawLandmarks(canvasCtx, results.poseLandmarks, { color: "#FF0000", lineWidth: 2 });
        
        if (postureOk) {
            // const savedImageDataUrl = canvasElement.toDataURL("image/png");
            // const apiResult = await postMeasurement({
            //     patient_id: 1,
            //     measured_by_user_id: 1,
            //     height_mm: 1,
            //     weight_kg: 1,
            //     sleep_hours: 1,
            //     exercise_hours: 1,
            //     image_base64: savedImageDataUrl
            // });
            // console.log("API call result:", apiResult);

            canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
            canvasCtx.fillStyle = "rgba(0,255,0,0.2)";
            canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);
            notificationElem.style.display = "block";
            notificationElem.innerText = "The posture is correct.";
            snapshotButton.innerText = "Next";
        } else {
            canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
            canvasCtx.fillStyle = "rgba(255,0,0,0.2)";
            canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);
            let feedbackMessages = [];
            if (!neckOk) { feedbackMessages.push("improve neck alignment"); }
            if (!torsoOk) { feedbackMessages.push("straighten your torso"); }
            if (!kneeOk) { feedbackMessages.push("adjust your knee angle"); }
            if (!feetOk) { feedbackMessages.push("adjust your foot placement"); }
            let feedback = "You need to stand better: " + feedbackMessages.join("; ") + ".";
    
            notificationElem.style.display = "block";
            notificationElem.innerText = feedback;
            snapshotButton.innerText = "Try Again";
        }
        // Update display: show canvas and hide the live video.
        canvasElement.style.display = "block";
        videoElement.style.display = "none";
        canvasCtx.restore();
    });

    // --- Setup Camera ---
    async function setupCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: "environment",
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
            });
            for (const track of stream.getVideoTracks()) {
                initialSettings = track.getSettings();
                capabilities = track.getCapabilities ? track.getCapabilities() : {};
                if (capabilities.width && capabilities.height && capabilities.width.max && capabilities.height.max) {
                    try {
                        await track.applyConstraints({
                            width: capabilities.width.max,
                            height: capabilities.height.max
                        });
                    } catch (error) {
                        console.error('Error applying max resolution constraints:', error);
                    }
                } else {
                    console.warn('Max width/height not available in capabilities.');
                }
            }
            videoElement.srcObject = stream;
            await new Promise(resolve => videoElement.onloadedmetadata = resolve);
            loadingElem.style.display = "none";
            adjustCanvas(capabilities.width.max, capabilities.height.max);
            snapshotButton.style.display = "block";
        } catch (error) {
            console.error('Error accessing camera:', error);
            loadingElem.style.display = "none";
            errorElem.style.display = "block";
            errorElem.innerText = "Error accessing camera: " + error.message;
        }
    }

    // --- Adjust the Canvas Dimensions ---
    function adjustCanvas(videoWidth = 1280, videoHeight = 720) {
        const container = document.getElementById("container");
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;
        let scale;
        if (containerWidth >= containerHeight) {
            scale = Math.min(containerWidth / videoWidth, containerHeight / videoHeight);
        } else {
            scale = Math.max(containerWidth / videoWidth, containerHeight / videoHeight);
        }
        const displayWidth = videoWidth * scale;
        const displayHeight = videoHeight * scale;

        canvasElement.width = videoWidth;
        canvasElement.height = videoHeight;
        canvasElement.style.width = displayWidth + "px";
        canvasElement.style.height = displayHeight + "px";

        videoElement.width = videoWidth;
        videoElement.height = videoHeight;
        videoElement.style.width = displayWidth + "px";
        videoElement.style.height = displayHeight + "px";
    }

    // --- Button Event Listener: Take Snapshot / Reset ---
    snapshotButton.addEventListener("click", async () => {
        if (canvasElement.style.display === "block") {
            videoElement.play();
            canvasElement.style.display = "none";
            videoElement.style.display = "block";
            notificationElem.style.display = "none";
            snapshotButton.innerText = "Take Picture";
            return;
        }
        // Otherwise, capture the snapshot.
        videoElement.pause();
        notificationElem.style.display = "none";
        snapshotButton.innerText = "Processing...";
        await pose.send({ image: videoElement });
    });

    setupCamera();

    // document.addEventListener('DOMContentLoaded', setupCamera);

    // window.addEventListener("resize", () => {
    //     adjustCanvas(capabilities.width.max, capabilities.height.max);
    // });
}