import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ResumeList from "./components/ResumeList";
import ResumeDetail from "./components/ResumeDetail";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ResumeList />} />
        <Route path="/resumes/:id" element={<ResumeDetail />} />
      </Routes>
    </Router>
  );
}

export default App;