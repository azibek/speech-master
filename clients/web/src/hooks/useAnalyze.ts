import { useMutation } from "@tanstack/react-query";

export type ApiResponse = { /* … */ };

export function useAnalyze() {
  return useMutation<ApiResponse, Error, { blob: Blob; persona: string }>(
    // mutationFn ───────────────────────────────────────────────
    async ({ blob, persona }) => {
      const form = new FormData();
      form.append("persona_id", persona);
      form.append("audio", blob, "recording.webm");

      const res = await fetch("http://localhost:8000/analyze_and_clone", {
        method: "POST",
        body: form,
      });
      if (!res.ok) throw new Error(await res.text());
      return (await res.json()) as ApiResponse;
    }
    // options?  ←  omit or add a second argument here
  );
}
