import React, { useEffect, useState } from "react";
const apiUrl = process.env.REACT_APP_API_URL;


function ResumeList() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${apiUrl}/v1/resumes/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setResumes(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Resumes</h1>
      <ul>
        {resumes.map((resume) => (
          <li key={resume.id}>
            <a href={`/resumes/${resume.id}`}>{resume.full_name}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ResumeList;