import { useCallback, useEffect, useRef, useState } from "react";

type UseRecorderReturn = {
  isRecording: boolean;
  elapsed: number;                 // seconds
  blob: Blob | null;
  url: string | null;              // object URL of blob
  start: () => Promise<void>;
  stop: () => void;
  reset: () => void;
};

export function useRecorder(maxSeconds = 15): UseRecorderReturn {
  const [isRecording, setRec] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [blob, setBlob] = useState<Blob | null>(null);
  const [url, setUrl] = useState<string | null>(null);

  const mediaRec = useRef<MediaRecorder | null>(null);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);



  const chunks = useRef<BlobPart[]>([]);

  // ------------ helpers --------------------------- //
  const clearTimer = () => {
    if (timer.current) clearInterval(timer.current);
    timer.current = null;
  };

  const reset = () => {
    clearTimer();
    setRec(false);
    setElapsed(0);
    setBlob(null);
    if (url) {
      URL.revokeObjectURL(url);
      setUrl(null);
    }
  };

  const stopAndFinalize = () => {
    clearTimer();
    setRec(false);
  }; 

  const stop = useCallback(() => {
    mediaRec.current?.stop();
  }, []);

  const start = useCallback(async () => {
    if (isRecording) return;

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const rec = new MediaRecorder(stream, { mimeType: "audio/webm" });
    mediaRec.current = rec;
    chunks.current = [];

    rec.ondataavailable = (e) => chunks.current.push(e.data);
    rec.onstop = () => {
        const blob = new Blob(chunks.current, { type: "audio/webm" });
        setBlob(blob);
        console.log("✅ recording done", blob?.size);
        setUrl(URL.createObjectURL(blob));
        stopAndFinalize();          // DON'T wipe blob/url
    };

    rec.start();
    setRec(true);

    // timer
    timer.current = setInterval(() => {
      setElapsed((sec) => {
        if (sec + 1 >= maxSeconds) stop();
        return sec + 1;
      });
    }, 1000);
  }, [isRecording, maxSeconds, stop]);

  // cleanup
  useEffect(() => () => reset(), []);

  return { isRecording, elapsed, blob, url, start, stop, reset };
}
