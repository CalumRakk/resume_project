import React from "react";
const DynamicComponent = ({ componentName, resume}) => {

  const ComponentToRender = React.lazy(() => import(`./${componentName}`));

  return (
    <div>     
      <React.Suspense fallback={<div>Cargando componente...</div>}>
        <ComponentToRender resume={resume} />
      </React.Suspense>
    </div>
  );
};

export default DynamicComponent;