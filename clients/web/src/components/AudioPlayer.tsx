import { useEffect, useRef } from "react";
import WaveSurfer from "wavesurfer.js";

type Props = { src: string };

export default function AudioPlayer({ src }: Props) {
  const container = useRef<HTMLDivElement | null>(null);
  const waveRef = useRef<WaveSurfer | null>(null);

  useEffect(() => {
    if (!container.current) return;

    waveRef.current?.destroy();
    waveRef.current = WaveSurfer.create({
      container: container.current,
      waveColor: "#A0C2F7",
      progressColor: "#4285F4",
      height: 80,
      barWidth: 2,
      cursorWidth: 1,
    });

    waveRef.current.load(src);

    return () => waveRef.current?.destroy();
  }, [src]);

  return (
    <div className="space-y-2">
      <div ref={container} className="rounded-md overflow-hidden" />
      <div className="flex gap-2">
        <button
          onClick={() => waveRef.current?.playPause()}
          className="bg-primary text-white px-4 py-1 rounded-full"
        >
          Play / Pause
        </button>
      </div>
    </div>
  );
}
