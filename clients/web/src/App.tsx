import { Routes, Route, Navigate } from "react-router-dom";

import Home    from "./pages/Home";      // ✅ import the page
import Record  from "./pages/Record";    // stubs can return <div>TODO</div>
// import Processing from "./pages/Processing";
// import Results from "./pages/Results";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />          {/* Home route */}
      <Route path="/record" element={<Record />} />
      {/* <Route path="/processing" element={<Processing />} />
      <Route path="/results" element={<Results />} /> */}
      {/* fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
