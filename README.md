## A starting point for interacting with the API

**General considerations before starting:**

- **Authentication:** Most endpoints require authentication via JWT. After logging in (`/v1/login/`) you will receive an access token and a refresh token. Include the access token in the `Authorization` header of your requests, like this: `Authorization: Bearer <your_access_token>`.
- **Refresh Tokens:** Access tokens have a limited lifespan. Use the `/v1/refresh-token/` endpoint with the refresh token to obtain a new access token when the current one expires.
- **HTTP Verbs:** The API follows REST principles. Use HTTP verbs (GET, POST, PUT, DELETE) semantically to perform operations on resources.
- **Data Format:** The API expects and responds with data in JSON format.

## **Main Endpoints:**

Below you will see the available URLs, remember that they are all within the `/v1/` scope.

| Method | Endpoint             | Description                                                                                                                         |
| :----- | :------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| POST   | `/v1/login/`         | Obtains an access token and a refresh token for an authenticated user.                                                              |
| POST   | `/v1/refresh-token/` | Refreshes an access token using a refresh token.                                                                                    |
| GET    | `/v1/resumes/`       | Lists all resumes of the authenticated user.                                                                                        |
| POST   | `/v1/resumes/`       | Creates a new resume for the authenticated user.                                                                                    |
| GET    | `/v1/resumes/<id>/`  | Gets the details of a specific resume (identified by `id`) of the authenticated user.                                               |
| PUT    | `/v1/resumes/<id>/`  | **Completely replaces** an existing resume (identified by `id`) with the provided data. It's important to send _all_ resume fields! |
| DELETE | `/v1/resumes/<id>/`  | Deletes a specific resume (identified by `id`) of the authenticated user.                                                           |
| GET    | `/v1/templates/`     | Lists all available templates.                                                                                                      |
| PATCH  | `/v1/templates/`     | Updates the selected template for a specific resume. Send a JSON with the `resume_id` and `template_selected` fields.               |

**Interaction Example (Creating a resume):**

1.  **Obtain a token:**

    ```http
    POST /v1/login/
    Content-Type: application/json

    {
      "username": "username",
      "password": "password"
    }
    ```

    Response:

    ```json
    {
      "access": "access_token",
      "refresh": "refresh_token"
    }
    ```

2.  **Create a resume:**

    ```http
    POST /v1/resumes/
    Content-Type: application/json
    Authorization: Bearer <access_token>

    {
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "summary": "Web developer with experience...",
      "template_selected": 1,
      "skills": [
        {"name": "JavaScript", "level": "Expert", "orden": 0},
        {"name": "React", "level": "Advanced", "orden": 1}
      ],
      "experiences": [
        {
          "name": "Company XYZ",
          "position": "Frontend Developer",
          "url": "https://www.company.com",
          "summary": "I developed user interfaces...",
          "start_date": "2023-01-01",
          "end_date": "2024-01-01",
          "orden": 0
        }
      ]
    }
    ```

    Response:

    ```json
    {
      "id": 123,
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "summary": "Web developer with experience...",
      "template_selected": {
        "id": 1,
        "name": "Modern",
        "descripcion": "Modern template...",
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

## **Django Administration Panel:**

The project includes a Django administration panel (`/admin/`) that allows:

- Manage users and permissions.
- Create, edit, and delete resumes, templates, skills, and experiences directly in the database.
- Get an overview of all the system's data.

## **Logs View:**

To facilitate debugging and monitoring of the system, the logs view is available at the endpoint **`/logs/`**. In `/logs/` you can see the recording of most of the actions performed and it also allows you to:

- Visualize the latest system logs directly from the browser.
- Download the complete logs file for more detailed analysis.

## **Swagger Documentation**

The project includes documentation with Swagger. You can access it by visiting the endpoint `/v1/swagger/`.

Swagger provides you with:

- An interactive interface to explore all API endpoints.
- Details of the parameters that each endpoint expects.
- Examples of JSON requests and responses.
- The ability to test endpoints directly from the browser.
