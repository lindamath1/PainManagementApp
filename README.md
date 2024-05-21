# PainManagementApp

PainManagementApp is a simplistic application for managing and tracking pain entries. This project serves as a learning experience for building a web application using FastAPI, SQLAlchemy, and other Python technologies.

## Features

- **CRUD Operations**: create, read, update, and delete pain entries.
- **Data Visualization**: visualize pain levels over time using Plotly.
- **Web Interface**: simple web interface for interacting with the pain entries.

## Project Structure

- `crud.py`: contains CRUD operations for managing pain entries.
- `database.py`: database connection and session management.
- `models.py`: database models.
- `schemas.py`: pydantic schemas for data validation.
- `plots.py`: functions for creating data visualizations using Plotly.
- `routes.py`: FastAPI routes for handling web requests.
- `main.py`: entry point for the FastAPI application.
- `templates/`: Jinja2 templates for rendering HTML pages.
- `utils/parameters.py`: configuration parameters, such as the database URL.


### Running the Application

1. **Start the FastAPI server:**

    ```bash
    uvicorn main:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`.

2. **Access the web interface:**

    - Go to `http://127.0.0.1:8000/pain/form` to add new pain entries.
    - Go to `http://127.0.0.1:8000/pain/read` to view all pain entries.
    - Go to `http://127.0.0.1:8000/pain/plot` to view the pain levels over time.



