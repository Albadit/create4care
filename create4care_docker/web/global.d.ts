// global.d.ts
// Place next to your tsconfig.json

declare global {
    interface Window {
        FilesetResolver: typeof import('@mediapipe/tasks-vision').FilesetResolver;
        PoseLandmarker: typeof import('@mediapipe/tasks-vision').PoseLandmarker;
        DrawingUtils: typeof import('@mediapipe/tasks-vision').DrawingUtils;
    }
}

export {};
