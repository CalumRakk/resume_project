## Un punto de partida para interactuar con la API

**Consideraciones generales antes de empezar:**

- **Autenticación:** La mayoría de los endpoints requieren autenticación mediante JWT. Después de iniciar sesión (`/v1/login/`) recibirás un token de acceso y un token de refresco. Incluye el token de acceso en la cabecera `Authorization` de tus peticiones, así: `Authorization: Bearer <tu_token_de_acceso>`.
- **Tokens de refresco:** Los tokens de acceso tienen una duración limitada. Utiliza el endpoint `/v1/refresh-token/` con el token de refresco para obtener un nuevo token de acceso cuando el actual expire.
- **Verbos HTTP:** La API sigue los principios REST. Usa los verbos HTTP (GET, POST, PUT, DELETE) de manera semántica para realizar operaciones en los recursos.
- **Formato de datos:** La API espera y responde con datos en formato JSON.

## **Endpoints principales:**

A continuación, verás las URLs disponibles, recuerda que todas están dentro del scope `/v1/`

| Método | Endpoint             | Descripción                                                                                                                                                |
| :----- | :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| POST   | `/v1/login/`         | Obtiene un token de acceso y un token de refresco para un usuario autenticado.                                                                             |
| POST   | `/v1/refresh-token/` | Refresca un token de acceso utilizando un token de refresco.                                                                                               |
| GET    | `/v1/resumes/`       | Lista todos los resumes del usuario autenticado.                                                                                                           |
| POST   | `/v1/resumes/`       | Crea un nuevo resume para el usuario autenticado.                                                                                                          |
| GET    | `/v1/resumes/<id>/`  | Obtiene los detalles de un resume específico (identificado por `id`) del usuario autenticado.                                                              |
| PUT    | `/v1/resumes/<id>/`  | **Reemplaza** completamente un resume existente (identificado por `id`) con los datos proporcionados. ¡Es importante enviar _todos_ los campos del resume! |
| DELETE | `/v1/resumes/<id>/`  | Elimina un resume específico (identificado por `id`) del usuario autenticado.                                                                              |
| GET    | `/v1/templates/`     | Lista todos los templates disponibles.                                                                                                                     |
| PATCH  | `/v1/templates/`     | Actualiza el template seleccionado para un resumen específico. Envia un JSON con los campos `resume_id` y `template_selected`.                             |

**Ejemplo de interacción (Crear un resume):**

1.  **Obtener un token:**

    ```http
    POST /v1/login/
    Content-Type: application/json

    {
      "username": "usuario",
      "password": "contraseña"
    }
    ```

    Respuesta:

    ```json
    {
      "access": "token_de_acceso",
      "refresh": "token_de_refresco"
    }
    ```

2.  **Crear un resume:**

    ```http
    POST /v1/resumes/
    Content-Type: application/json
    Authorization: Bearer <token_de_acceso>

    {
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "summary": "Desarrollador web con experiencia...",
      "template_selected": 1,
      "skills": [
        {"name": "JavaScript", "level": "Experto", "orden": 0},
        {"name": "React", "level": "Avanzado", "orden": 1}
      ],
      "experiences": [
        {
          "name": "Empresa XYZ",
          "position": "Desarrollador Frontend",
          "url": "https://www.empresa.com",
          "summary": "Desarrollé interfaces de usuario...",
          "start_date": "2023-01-01",
          "end_date": "2024-01-01",
          "orden": 0
        }
      ]
    }
    ```

    Respuesta:

    ```json
    {
      "id": 123,
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "summary": "Desarrollador web con experiencia...",
      "template_selected": {
        "id": 1,
        "name": "Modern",
        "descripcion": "Plantilla moderna...",
        "componet_name": "modern-resume",
        "customization_rules": []
      },
      "skills": [...],
      "experiences": [...],
       "user": 1,
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    }
    ```

## **Panel de Administración de Django:**

El proyecto incluye un panel de administración de Django (`/admin/`) que permite:

- Gestionar usuarios y permisos.
- Crear, editar y eliminar resumes, plantillas, habilidades y experiencias directamente en la base de datos.
- Tener una visión general de todos los datos del sistema.

## **Vista de Logs:**

Para facilitar la depuración y el monitoreo del sistema, está disponible la vista de logs accesible en el endpoint **`/logs/`**. En `/logs/` puedes ver el registro de gran parte de las acciones realizadas y también te permite:

- Visualizar los últimos registros del sistema directamente desde el navegador.
- Descargar el archivo de logs completo para un análisis más detallado.

## **Documentación Swagger**

El proyecto incluye la documentación con Swagger. Puedes acceder a ella visitando el endpoint `/v1/swagger/`.

Swagger te proporciona:

- Una interfaz interactiva para explorar todos los endpoints de la API.
- Detalles de los parámetros que cada endpoint espera.
- Ejemplos de solicitudes y respuestas JSON.
- La posibilidad de probar los endpoints directamente desde el navegador.
