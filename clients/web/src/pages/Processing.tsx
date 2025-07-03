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

  console.log("[Processing] persona:", persona);          // should log id
console.log("[Processing] blob size:", blob?.size);  
console.log("mutate is", analyze.mutate?.name || "undefined");


/* 1. Run when you have BOTH persona and blob */
const handleSubmit = () => {
  console.log(">>>>>>>> about to call mutate", {blob, persona})
  analyze.mutate(
    { blob, persona },                 // matches TVariables
    {
      onSuccess: (data) => {
        setResponse(data);             // store JSON in context
        nav("/results", { replace: true });
      },
      onError: (err) => alert(err.message),
    }
  );
};

/* 2. Render states */
if (analyze.isPending) return <Loader />;
if (analyze.isError)   return <p>Error: {analyze.error.message}</p>;



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
