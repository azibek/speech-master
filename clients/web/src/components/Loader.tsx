export default function Loader() {
  return (
    <div className="flex flex-col items-center gap-4">
      <div className="animate-spin h-12 w-12 border-4 border-primary border-t-transparent rounded-full" />
      <p className="text-lg">Analyzing your speech…</p>
    </div>
  );
}
