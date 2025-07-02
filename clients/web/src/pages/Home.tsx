import PersonaCard from "../components/PersonaCard";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { SessionContext } from "../context/SessionContext";

const PERSONAS = [
  { id: "mrbeast", label: "MrBeast" },
  { id: "aliabdaal", label: "Ali Abdaal" },
  { id: "emma", label: "Emma Chamberlain" },
];

export default function Home() {
  const { persona, setPersona } = useContext(SessionContext);
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-10">
      <h1 className="text-3xl font-bold">Who do you want to sound like?</h1>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        {PERSONAS.map(p => (
          <PersonaCard
            key={p.id}
            id={p.id}
            label={p.label}
            active={persona === p.id}
            onClick={() => setPersona(p.id)}
          />
        ))}
      </div>

      <button
        disabled={!persona}
        onClick={() => navigate("/record")}
        className="bg-primary disabled:bg-gray-400 text-white px-6 py-2 rounded-2xl shadow-md hover:shadow-lg transition"
      >
        Next
      </button>
    </div>
  );
}
