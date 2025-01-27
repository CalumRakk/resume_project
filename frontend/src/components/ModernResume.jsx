import React, { useState } from "react";
import axios from "axios";
import styles from "./ModernResume.module.css";

const ModernResume = ({  resume, setResume }) => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleUpdate = async () => {
    try {
      setLoading(true);
      setMessage("");

      const copyResume= {...resume, template_selected: resume.template_selected.id};
      const response = await axios.put(
        "http://127.0.0.1:8000/v1/resumes/1/",
        copyResume
      );

      setMessage("Datos actualizados con éxito.");
      console.log("Respuesta de la API:", response.data);

    } catch (error) {
      console.error("Error al actualizar los datos:", error);
      setMessage("Ocurrió un error al actualizar los datos.");
    } finally {
      setLoading(false);
    }
  };

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
};

export default ModernResume;