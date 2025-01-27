import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import styles from "./ResumeDetail.module.css";
import DynamicComponent  from "./DynamicComponent";
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
      <DynamicComponent componentName="ModernResume" resume={ resume } />
    </div>
  );
}

export default ResumeDetail;