import React from "react";

const DynamicComponent = ({ componentName, resume, setResume, setDynamicComponentName }) => {
  const handleChangeComponent = () => {
    setDynamicComponentName("ClassicResume");
  };

  const ComponentToRender = React.lazy(() => import(`./${componentName}`));

  return (
    <div>
      <React.Suspense fallback={<div>Cargando componente...</div>}>
        <ComponentToRender resume={resume} setResume={setResume} />
      </React.Suspense>

      <button onClick={handleChangeComponent}>Cambiar Componente</button>
    </div>
  );
};

export default DynamicComponent;