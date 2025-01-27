import React from "react";

function ModernResume( { resume } ) {
  return (
    <div>
      <h1>Modern Resume</h1>
      <p>{resume.full_name}</p>
    </div>
  );
}

export default ModernResume;