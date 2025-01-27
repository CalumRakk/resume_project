import React, { Suspense, lazy } from "react";

const DynamicComponent = ({ componentName, resume  }) => {
  const Component = React.useMemo(() => {
    try {
      return lazy(() => import(`./${componentName}`));
    } catch (error) {
      console.error("Error al cargar el componente:", error);
      return null;
    }
  }, [componentName]);

  return (
    <Suspense fallback={<div>Cargando componente...</div>}>
      {Component ? <Component resume={resume} /> : <div>No se pudo cargar el componente.</div>}
    </Suspense>
  );
};

export default DynamicComponent;
