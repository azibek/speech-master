import { useMutation } from "@tanstack/react-query";

export type ApiResponse = {
  transcript: string;
  similarity: number;
  metrics: Record<string, number>;
  advice: string[];
  reference_audio_url: string;
};

export function useAnalyze() {
  return useMutation<ApiResponse, Error, { blob: Blob; persona: string }>(
    // 1️⃣ THIS is the mutationFn
    async ({ blob, persona }) => {
        console.log("---------------> Inside useMutation hook")
      const form = new FormData();
      form.append("persona_id", persona);
      form.append("audio", blob, "recording.webm");
      

      console.log(import.meta.env.VITE_API_URL);
      const res = await fetch(
        import.meta.env.VITE_API_URL + "/analyze_and_clone",
        { method: "POST", body: form }
      );
      if (!res.ok) throw new Error(await res.text());
      return (await res.json()) as ApiResponse;
    }
    // 2️⃣ (options object goes here — optional)
  );
}
