// wwwroot/js/camera-init.js

let _stream = null;
let dotnetHelper = null;

window.initializeCamera = (dotnetRef) => {
  dotnetHelper = dotnetRef;

  // ---- Cached DOM & State ----
  const $ = id => document.getElementById(id);
  const container  = $('container');
  const video      = $('videoInput');
  const canvas     = $('output');
  const loading    = $('loading');
  const errorMsg   = $('error');
  const notify     = $('notification');
  const btn        = $('snapshotButton');
  const popup      = $('issuePopup');
  const issueList  = $('issueList');
  const retryBtn   = $('retryButton');
  let videoDims    = { width: 1280, height: 720 };

  // ---- Generic POST helper ----
  async function postData(url, payload) {
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.error(`Error POST ${url}:`, err);
      return null;
    }
  }

  // ---- Camera Setup ----
  async function setupCamera() {
    loading.hidden = false;
    try {
      _stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: 1280, height: 720 }
      });
      const track = _stream.getVideoTracks()[0];
      const caps  = track.getCapabilities?.() || {};

      // Try max resolution
      if (caps.width?.max && caps.height?.max) {
        await track.applyConstraints({
          width: caps.width.max,
          height: caps.height.max
        });
        videoDims = { width: caps.width.max, height: caps.height.max };
      }

      video.srcObject = _stream;
      await new Promise(r => video.onloadedmetadata = r);

      loading.hidden = true;
      adjustCanvas();
      btn.hidden = false;
    } catch (err) {
      console.error('Camera error:', err);
      loading.hidden = true;
      errorMsg.hidden = false;
      errorMsg.textContent = `Error accessing camera: ${err.message}`;
    }
  }

  // ---- Canvas Sizing ----
  function adjustCanvas() {
    const { width: vw, height: vh } = videoDims;
    const CW = container.clientWidth;
    const CH = container.clientHeight;
    let scale;
    if (CW >= CH) {
      scale = Math.min(CW / vw, CH / vh);
    } else {
      scale = Math.max(CW / vw, CH / vh);
    }
    
    // set the actual pixel buffer size
    canvas.width  = vw;
    canvas.height = vh;
    video.width  = vw;
    video.height = vh;

    // then scale both elements via CSS to fit inside #container
    [video, canvas].forEach(el => {
      el.style.width  = `${vw * scale}px`;
      el.style.height = `${vh * scale}px`;
    });
  }

  // ---- Snapshot Flow ----
  btn.addEventListener('click', async () => {
    if (!video.paused) {
    // Capture
    video.pause();
    btn.textContent = 'Processing...';
    notify.hidden = true;

    // Draw & encode
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, videoDims.width, videoDims.height);
    const imageBase64 = canvas.toDataURL();
    await dotnetHelper.invokeMethodAsync("OnMeasurementSave");

    // 1) Pose detection
    const pose = await postData(
      'https://api.blokk.duckdns.org/pose_detection/',
      { image_base64: imageBase64 }
    );
    if (!pose) {
      notify.textContent = 'Pose detection failed.';
      notify.hidden = false;
      return btn.textContent = 'Retry';
    }

    // 2) Show issues
    if (pose.issues?.length) {
      issueList.innerHTML = pose.issues.map(i => `<span>- ${i}</span>`).join('');
      popup.hidden = false;
      retryBtn.onclick = reset;
      return;
    }

    // 3) Save measurement
    if (pose.landmark_image) {
      const measurement = {
        patient_id: 1,
        measured_by_user_id: 1,
        height_mm: 1,
        weight_kg: 1,
        sleep_hours: 1,
        exercise_hours: 1,
        image: pose.landmark_image
      };
      const result = await postData(
        'https://api.blokk.duckdns.org/measurements/',
        measurement
      );
      if (result) {
        if (dotnetHelper) {
          await dotnetHelper.invokeMethodAsync("OnMeasurementSuccess");
        }
      } else {
        notify.textContent = "Failed to save measurement.";
      }
    } else {
      notify.textContent = 'No landmark image returned.';
    }

    notify.hidden = false;
    btn.textContent = 'Retry';

    } else {
      reset();
    }
  });

  function reset() {
    popup.hidden = true;
    video.play();
    notify.hidden = true;
    btn.textContent = 'Take Picture';
  }

  // ---- (Optional) Handle resize ----
  let resizeTimeout;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(adjustCanvas, 200);
  });

  // ---- Init ----
  setupCamera();
};

window.stopCamera = () => {
  const video = document.getElementById('videoInput');
  if (video && video.srcObject) {
    // Stop every track
    video.srcObject.getTracks().forEach(track => track.stop());
    video.srcObject = null;
  }
  _stream = null;
}