import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { SessionContext } from "../context/SessionContext";
import AudioPlayer from "../components/AudioPlayer";
import RadarChart from "../components/RadarChart";

export default function Results() {
  const nav = useNavigate();
  const { response } = useContext(SessionContext);

  if (!response) {
    nav("/", { replace: true });
    return null;
  }

  return (
    <div className="min-h-screen flex flex-col items-center gap-8 py-10">
      <h1 className="text-3xl font-bold">{response.similarity.toFixed(1)}% match</h1>

      <RadarChart metrics={response.metrics} />

      <div className="flex flex-col md:flex-row gap-6">
        <div>
          <h2 className="text-lg font-medium mb-2">Your original</h2>
          <AudioPlayer src={response.reference_audio_url.replace("styled", "original")} />
        </div>
        <div>
          <h2 className="text-lg font-medium mb-2">Styled clone</h2>
          <AudioPlayer src={response.reference_audio_url} />
        </div>
      </div>

      <div className="max-w-md">
        <h2 className="text-lg font-medium mb-2">Improvement tips</h2>
        <ul className="list-disc list-inside space-y-1">
          {response.advice.map((tip, i) => (
            <li key={i}>{tip}</li>
          ))}
        </ul>
      </div>

      <button
        onClick={() => nav("/record")}
        className="bg-primary text-white px-6 py-2 rounded-2xl shadow-md hover:shadow-lg transition"
      >
        Try another take
      </button>
    </div>
  );
}
