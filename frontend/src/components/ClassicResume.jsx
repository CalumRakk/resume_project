import React from "react";
import styles from "./ModernResume.module.css";

function ClassicResume( {  resume, setResume }) {
return (
    <div className={styles.container}>
      <div className={styles.resume}>
        <header style={{color: "red"}}>
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

export default ClassicResume;