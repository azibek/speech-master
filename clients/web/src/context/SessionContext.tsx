import { createContext, useState } from "react";
import type { ReactNode } from "react";   // 👈 type-only import

/* ------------------------------------------------------------------ */
/* Types                                                              */
/* ------------------------------------------------------------------ */
export type ApiResponse = {
  transcript: string;
  similarity: number;
  metrics: Record<string, number>;
  advice: string[];
  reference_audio_url: string;
};

/* ------------------------------------------------------------------ */
/* Context object                                                     */
/* ------------------------------------------------------------------ */
export const SessionContext = createContext<{
  persona: string | null;
  setPersona: (p: string | null) => void;
  response: ApiResponse | null;
  setResponse: (r: ApiResponse | null) => void;
}>({
  persona: null,
  setPersona: () => {},
  response: null,
  setResponse: () => {},
});

/* ------------------------------------------------------------------ */
/* Provider component                                                 */
/* ------------------------------------------------------------------ */
export const SessionProvider = ({ children }: { children: ReactNode }) => {
  const [persona, setPersona] = useState<string | null>(null);
  const [response, setResponse] = useState<ApiResponse | null>(null);

  return (
    <SessionContext.Provider value={{ persona, setPersona, response, setResponse }}>
      {children}
    </SessionContext.Provider>
  );
};
