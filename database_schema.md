Documento autogenerado usando el comando `python manage.py generate_markdown`

## Resúmenes

Modelo que representa un resumen.

| Campo | Tipo | Permite NULL | Descripción |
|-------|------|-------------|-------------|
| id | BigAutoField | ❌ |  |
| created_at | DateTimeField | ❌ | Fecha de creación del registro. |
| updated_at | DateTimeField | ❌ | Fecha de última modificación del registro. |
| full_name | CharField | ✅ | Nombre completo del usuario. |
| email | CharField | ✅ | Correo electrónico asociado al resumen. |
| summary | TextField | ✅ | Resumen o descripción general del usuario. |
| template_selected | ForeignKey | ✅ | Plantilla seleccionada para la visualización del resumen. |
| user | ForeignKey | ❌ | Usuario dueño del resumen. |

## Habilidades

Representa una habilidad dentro del resumen.

| Campo | Tipo | Permite NULL | Descripción |
|-------|------|-------------|-------------|
| id | BigAutoField | ❌ |  |
| created_at | DateTimeField | ❌ | Fecha de creación del registro. |
| updated_at | DateTimeField | ❌ | Fecha de última modificación del registro. |
| name | CharField | ❌ | Nombre de la habilidad. |
| resume | ForeignKey | ❌ | Resumen al que pertenece la habilidad. |
| orden | PositiveIntegerField | ❌ | Orden en el que se mostrarán las habilidades en el resumen. |
| keywords | JSONField | ✅ | Palabras clave asociadas a la habilidad. |
| level | CharField | ✅ | Nivel de la habilidad (Ej: Básico, Avanzado, Experto). |

## Experiencias

Representa una experiencia laboral dentro del resumen.

| Campo | Tipo | Permite NULL | Descripción |
|-------|------|-------------|-------------|
| id | BigAutoField | ❌ |  |
| created_at | DateTimeField | ❌ | Fecha de creación del registro. |
| updated_at | DateTimeField | ❌ | Fecha de última modificación del registro. |
| name | CharField | ❌ | Nombre de la empresa u organización. |
| position | CharField | ❌ | Puesto desempeñado en la empresa. |
| start_date | DateField | ❌ | Fecha de inicio del empleo. |
| resume | ForeignKey | ❌ | Resumen al que pertenece la experiencia. |
| orden | PositiveIntegerField | ❌ | Orden en el que se mostrarán las experiencias en el resumen. |
| url | CharField | ✅ | Enlace a la empresa o descripción del trabajo. |
| summary | TextField | ✅ | Descripción general de la experiencia laboral. |
| highlights | JSONField | ✅ | Aspectos destacados del trabajo. |
| end_date | DateField | ✅ | Fecha de finalización del empleo. NULL si aún está en curso. |

## Plantillas

Representa una plantilla de diseño para los resúmenes.

| Campo | Tipo | Permite NULL | Descripción |
|-------|------|-------------|-------------|
| id | BigAutoField | ❌ |  |
| created_at | DateTimeField | ❌ | Fecha de creación del registro. |
| updated_at | DateTimeField | ❌ | Fecha de última modificación del registro. |
| name | CharField | ❌ | Nombre de la plantilla. |
| componet_name | CharField | ❌ | Nombre del componente web asociado a la plantilla. |
| customazation_rules | JSONField | ❌ | Reglas de personalización de la plantilla. |
| descripcion | TextField | ✅ | Descripción de la plantilla. |

## Personalización de Resúmenes

Representa una personalización aplicada a un resumen con una plantilla específica.

| Campo | Tipo | Permite NULL | Descripción |
|-------|------|-------------|-------------|
| id | BigAutoField | ❌ |  |
| created_at | DateTimeField | ❌ | Fecha de creación del registro. |
| updated_at | DateTimeField | ❌ | Fecha de última modificación del registro. |
| resume | ForeignKey | ❌ | Resumen al que se aplica la personalización. |
| template | ForeignKey | ❌ | Plantilla seleccionada para la personalización. |
| custom_styles | JSONField | ❌ | Estilos personalizados aplicados al resumen. |

