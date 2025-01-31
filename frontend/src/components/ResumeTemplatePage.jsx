import TemplateSelection from "../components/TemplateSelection";
import { useParams } from "react-router-dom";

const ResumeTemplatePage = () => {
  const { resumeId } = useParams(); // Obtiene el ID del resume de la URL

  return (
    <div>
      <h1>Seleccionar Template para el Resume #{resumeId}</h1>
      <TemplateSelection resumeId={resumeId} />
    </div>
  );
};

export default ResumeTemplatePage;
