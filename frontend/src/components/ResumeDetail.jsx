import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import styles from "./ResumeDetail.module.css";
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
    <div className={styles.container}>
      <div className={styles.resume}>
        <header className={styles.header}>
          <h1>{resume.full_name}</h1>
          <p>{resume.email}</p>
        </header>
        <section className={styles.section}>
          <h2>Resumen</h2>
          <p>{resume.summary}</p>
        </section>

        <section className={styles.experiences}>
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
        </section>
        
        <section className={styles.skills}>
          <h2>Habilidades</h2>
          <ul className={styles.skills}>
            {resume.skills.map((skill) => (
              <li key={skill.id}>{skill.name}</li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}

export default ResumeDetail;