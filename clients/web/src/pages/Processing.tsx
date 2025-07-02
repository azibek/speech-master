import { useLocation, useNavigate } from "react-router-dom";
import { useContext, useEffect } from "react";
import { useAnalyze } from "../hooks/useAnalyze";
import Loader from "../components/Loader";
import { SessionContext } from "../context/SessionContext";

export default function Processing() {
  const nav = useNavigate();
  const loc = useLocation();
  const { persona, setResponse } = useContext(SessionContext);

  // Redirect if no persona or blob in state
  const blob = (loc.state as { blob?: Blob })?.blob;
  if (!persona || !blob) {
    nav("/", { replace: true });
    return null;
  }

  const analyze = useAnalyze();

  useEffect(() => {
    analyze.mutate(
      { blob, persona },
      {
        onSuccess: (data) => {
          setResponse(data);
          nav("/results", { replace: true });
        },
      }
    );
  }, [analyze, blob, persona, nav, setResponse]);

  if (analyze.isError)
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4">
        <p className="text-red-600">❌ {String(analyze.error)}</p>
        <button
          onClick={() => nav("/record")}
          className="px-4 py-2 rounded-full bg-primary text-white"
        >
          Try again
        </button>
      </div>
    );

  return (
    <div className="min-h-screen flex items-center justify-center">
      <Loader />
    </div>
  );
}
