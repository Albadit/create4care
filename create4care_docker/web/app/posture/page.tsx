'use client';

import { useEffect, useRef, useState, useCallback, useLayoutEffect } from 'react';
import {
  FilesetResolver,
  PoseLandmarker,
  DrawingUtils
} from '@mediapipe/tasks-vision';
import { Button } from "@heroui/react";

export default function PosturePage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const landmarkerRef = useRef<PoseLandmarker|null>(null);
  const modeRef = useRef<'IMAGE'|'VIDEO'>('IMAGE');

  const [showLandmarks, setShowLandmarks] = useState(false);
  const showLandmarksRef = useRef(showLandmarks);
  useEffect(() => { showLandmarksRef.current = showLandmarks; }, [showLandmarks]);

  const [cameraReady, setCameraReady] = useState(false);
  const [modelReady, setModelReady]   = useState(false);

  const [initialSettings, setInitialSettings] = useState<MediaTrackSettings|null>(null);
  // const [capabilities, setCapabilities] = useState<MediaTrackSettings|null>(null);
  const capabilities = useRef<MediaTrackCapabilities|null>(null);

  let lastVideoTime = -1;

  // --- Adjust the Canvas and Video Display ---
  const adjustCanvas = useCallback((videoWidth: number, videoHeight: number) => {
    const container = containerRef.current!;
    const canvasEl  = canvasRef.current!;
    const videoEl   = videoRef.current!;

    if (!container || !canvasEl || !videoEl) return;

    const containerWidth  = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    let scale: number;
    if (containerWidth >= containerHeight) {
      scale = Math.min(containerWidth / videoWidth, containerHeight / videoHeight);
    } else {
      scale = Math.max(containerWidth / videoWidth, containerHeight / videoHeight);
    }

    const displayWidth  = videoWidth  * scale;
    const displayHeight = videoHeight * scale;

    // set actual drawing buffer size
    canvasEl.width  = videoWidth;
    canvasEl.height = videoHeight;
    // set CSS size
    canvasEl.style.width  = `${displayWidth}px`;
    canvasEl.style.height = `${displayHeight}px`;

    videoEl.width  = videoWidth;
    videoEl.height = videoHeight;
    videoEl.style.width  = `${displayWidth}px`;
    videoEl.style.height = `${displayHeight}px`;
  }, []);

  // model setup
  const setupModel = useCallback(async () => {
    const vision = await FilesetResolver.forVisionTasks(
      'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm'
    );
    landmarkerRef.current = await PoseLandmarker.createFromOptions(vision, {
      baseOptions: {
        modelAssetPath:
          'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task',
        delegate: 'GPU'
      },
      runningMode: modeRef.current,
      numPoses: 2
    });
    setModelReady(true);
  }, []);

  // camera setup
  const setupCamera = useCallback(async () => {
    const vid = videoRef.current!;
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: {
        facingMode: "environment",
        width: { ideal: 1280 },
        height: { ideal: 720 }
      } 
    });

    for (const track of stream.getVideoTracks()) {
      const caps = track.getCapabilities?.() ?? {};
      capabilities.current = caps
      // setCapabilities(caps);
      setInitialSettings(track.getSettings());
      if (caps.width?.max && caps.height?.max) {
        try {
          await track.applyConstraints({
            width: caps.width.max,
            height: caps.height.max
          });
          adjustCanvas(caps.width.max, caps.height.max);
          console.log('Applied max-resolution constraints.');
        } catch (e) {
          console.error('Error applying resolution constraints:', e);
        }
      } else {
        console.warn('Max width/height not available.');
      }
    }

    vid.srcObject = stream;
    // console.log(capabilities.current)
    
    setCameraReady(true);
  }, [adjustCanvas]);

  // SINGLE effect to set up both model & camera
  useEffect(() => {
    (async () => {
      await Promise.all([ setupModel(), setupCamera() ]);
    })();
  }, [setupModel, setupCamera]);

  useLayoutEffect(() => {
    if (!containerRef.current) return;
    
    // initial draw
    const width = capabilities.current?.width?.max;
    const height = capabilities.current?.height?.max;
    if (typeof width === 'number' && typeof height === 'number') {
      adjustCanvas(width, height);
    }
    
    const ro = new ResizeObserver(() => {
      const width = capabilities.current?.width?.max;
      const height = capabilities.current?.height?.max;
      if (typeof width === 'number' && typeof height === 'number') {
        adjustCanvas(width, height);
      }
    });
    ro.observe(containerRef.current);
    
    return () => {
      ro.disconnect();
    };
  }, [adjustCanvas, capabilities.current?.width!.max, capabilities.current?.height!.max]);
  

  // prediction loop
  const predictWebcam = useCallback(() => {
    const videoEl = videoRef.current!;
    const canvasEl = canvasRef.current!;
    const poseLandmarker = landmarkerRef.current!;
    if (!showLandmarksRef.current) {
      canvasEl.getContext('2d')!.clearRect(0, 0, videoEl.width, videoEl.height);
      return;
    }
    if (modeRef.current === 'IMAGE') {
      modeRef.current = 'VIDEO';
      poseLandmarker.setOptions({ runningMode: 'VIDEO' });
    }
    const now = performance.now();
    if (videoEl.currentTime !== lastVideoTime) {
      lastVideoTime = videoEl.currentTime;
      poseLandmarker.detectForVideo(videoEl, now, (result) => {
        const ctx = canvasEl.getContext('2d')!;
        ctx.save();
        ctx.clearRect(0, 0, videoEl.width, videoEl.height);
        const du = new DrawingUtils(ctx);
        for (const lm of result.landmarks) {
          du.drawLandmarks(lm, {
            radius: d => DrawingUtils.lerp(d.from!.z, -0.15, 0.1, 5, 1)
          });
          du.drawConnectors(lm, PoseLandmarker.POSE_CONNECTIONS);
        }
        ctx.restore();
      });
    }
    requestAnimationFrame(predictWebcam);
  }, []);

  // toggle overlay
  const onToggle = () => {
    setShowLandmarks(on => {
      const next = !on;
      if (next) requestAnimationFrame(predictWebcam);
      return next;
    });
  };

  return (
    <main className="flex flex-grow p-2.5 ">
      {(!modelReady || !cameraReady) && (
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-white text-lg font-medium">
            Loading
            {!modelReady && ' model'}
            {(!modelReady && !cameraReady) && ' &'}
            {!cameraReady && ' camera'}…
          </span>
        </div>
      )}
      <div 
        ref={containerRef}
        className="relative w-full h-full flex-grow overflow-hidden rounded-lg">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          className="absolute left-1/2 transform -translate-x-1/2 rounded-lg"
        />
        <canvas
          ref={canvasRef}
          className="absolute left-1/2 transform -translate-x-1/2 rounded-lg"
        />
        {(modelReady && cameraReady) && (
          <Button
            color="primary"
            onPress={onToggle}
            className="absolute bottom-0 left-0 w-full"
          >
            {showLandmarks ? 'Hide Landmarks' : 'Show Landmarks'}
          </Button>
        )}
      </div>
    </main>
  );
}
