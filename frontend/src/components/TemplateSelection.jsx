import { useEffect, useState } from "react";
const apiUrl = process.env.REACT_APP_API_URL;

const TemplateSelection = ({ resumeId }) => {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);

  useEffect(() => {
    fetch(`${apiUrl}/v1/templates/`)
      .then((response) => response.json())
      .then((data) => setTemplates(data))
      .catch((error) => console.error("Error fetching templates:", error));
  }, []);

  const handleTemplateSelect = (resumeId, templateId) => {
    setSelectedTemplate(templateId);

    // Enviar la selección al backend (actualizar el Resume con el Template elegido)
    fetch(`${apiUrl}/v1/templates/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ resume_id: resumeId, template_selected: templateId }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Resume actualizado:", data);     
        document.location.href = `/resumes/${resumeId}`;
      })
      .catch((error) => console.error("Error al actualizar el resume:", error));
  };

  return (
    <div>
      <h2>Selecciona un Template</h2>
      <div style={{ display: "flex", gap: "10px" }}>
        {templates.map((template) => (
          <div
            key={template.id}
            style={{
              border: selectedTemplate === template.id ? "3px solid blue" : "1px solid gray",
              padding: "10px",
              cursor: "pointer",
            }}
            onClick={() => handleTemplateSelect(resumeId, template.id )}
          >
            <img src="https://picsum.photos/200" alt={template.componet_name} width="125" />
            <p>{template.componet_name}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TemplateSelection;
