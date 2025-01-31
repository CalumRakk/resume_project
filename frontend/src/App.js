import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ResumeList from "./components/ResumeList";
import ResumeDetail from "./components/ResumeDetail";
import ResumeTemplatePage from "./components/ResumeTemplatePage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ResumeList />} />
        <Route path="/resumes/:resumeId" element={<ResumeDetail />} />
        <Route path="/resumes/:resumeId/template" element={<ResumeTemplatePage />} />
      </Routes>
    </Router>
  );
}

export default App;