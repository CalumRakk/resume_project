import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
const apiUrl = process.env.REACT_APP_API_URL;

function ResumeDetail() {
  const { id } = useParams();
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${apiUrl}/v1/resumes/${id}/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("La respuesta no fue exitosa");
        }
        return response.json();
      })
      .then((data) => {
        setResume(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <p>Cargando...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!resume) return <p>Resume no encontrado</p>;

  return (
    <div>
      <h1>{resume.full_name}</h1>
      <p>{resume.email}</p>
      <p>{resume.summary}</p>
      <h2>Experiencia</h2>
      <ul>
        {resume.experiences.map((exp) => (
          <li key={exp.id}>
            <h3>{exp.name}</h3>
            <p>{exp.position}</p>
            <p>{exp.url}</p>
            <p>{exp.start_date} - {exp.end_date}</p>
            <p>{exp.summary}</p>
          </li>
        ))}
      </ul>
      <h2>Habilidades</h2>
      <ul>
        {resume.skills.map((skill) => (
          <li key={skill.id}>{skill.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default ResumeDetail;