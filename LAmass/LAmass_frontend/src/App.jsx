import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Homepage from "./pages/Homepage/index";
import MSDial from "./pages/MSDial/index";
import MSFinder from "./pages/MSFinder/index";
import MRMprobs from "./pages/MRMprobs/index";

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        <div className="flex-1 flex flex-col overflow-hidden">
          <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100">
            <div className="mx-auto">
              <Routes>
                <Route path="/" element={<Homepage />} />
                <Route path="/ms-dial" element={<MSDial />} />
                <Route path="/ms-finder" element={<MSFinder />} />
                <Route path="/mrm-probs" element={<MRMprobs />} />
              </Routes>
            </div>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
