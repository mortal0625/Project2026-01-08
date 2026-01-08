# API Documentation

This document provides details on the API for the Task and Schedule management application.

## Base URL

`http://127.0.0.1:5000`

---

## Endpoints

### 1. Get All Tasks

- **HTTP Method:** `GET`
- **Path:** `/api/tasks`
- **Description:** Retrieves a list of all currently stored tasks and schedules.
- **Success Response:**
  - **Code:** `200 OK`
  - **Content Example:**
    ```json
    [
        {
            "id": 1,
            "description": "Finish the project report",
            "completed": false
        },
        {
            "id": 2,
            "description": "Team meeting at 2 PM",
            "completed": false
        }
    ]
    ```

### 2. Add a New Task

- **HTTP Method:** `POST`
- **Path:** `/api/tasks`
- **Description:** Adds a new task or schedule to the list. The task description must be provided in the request body.
- **Request Body:**
  - **Type:** `application/json`
  - **Content:**
    ```json
    {
        "description": "Your new task description"
    }
    ```
- **Success Response:**
  - **Code:** `201 Created`
  - **Content Example:** The newly created task object is returned.
    ```json
    {
        "id": 3,
        "description": "Your new task description",
        "completed": false
    }
    ```
- **Error Response:**
  - **Code:** `400 Bad Request`
  - **Description:** Returned if the `description` field is missing from the request body.
  - **Content:**
    ```json
    {
        "error": "Missing description"
    }
    ```
