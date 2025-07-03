import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { SessionContext } from "../context/SessionContext";
import { useRecorder } from "../hooks/useRecorder";
import AudioPlayer from "../components/AudioPlayer";

export default function Record() {
  const nav = useNavigate();
  const { persona, setResponse } = useContext(SessionContext);

  // redirect if user refreshed without picking persona
  useEffect(()=> {
    if (!persona) nav("/", { replace: true });

  }, [ persona, nav ])

  const { isRecording, elapsed, url, blob, start, stop, reset } = useRecorder();

  const handleNext = () => {
    if (!blob) {
        console.log()
        return;
    }
    // store blob in context or go straight to /processing
    nav("/processing", { state: { blob } });
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-8">
      <h1 className="text-2xl font-semibold">Speak up to 15&nbsp;seconds</h1>

      <button
        onClick={isRecording ? stop : start}
        className={`w-24 h-24 rounded-full flex items-center justify-center shadow-lg transition
          ${isRecording ? "bg-red-500 animate-pulse" : "bg-primary hover:shadow-xl"}`}
      >
        {isRecording ? "Stop" : "Record"}
      </button>

      <p className="text-lg">{elapsed.toString().padStart(2, "0")} s</p>

      {url && (
        <>
          <AudioPlayer src={url} />
          <div className="flex gap-4">
            <button onClick={reset} className="px-4 py-2 rounded-full bg-gray-300">
              Re-record
            </button>
            <button
              onClick={handleNext}
              className="px-4 py-2 rounded-full bg-success text-white"
            >
              Continue
            </button>
          </div>
        </>
      )}
    </div>
  );
}
