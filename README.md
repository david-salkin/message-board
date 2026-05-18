# Message Board Application

An asynchronous message board application. This repository was developed as a take-home assessment for recruitment evaluation.

---

## Tech Stack

* **Framework:** FastAPI (Asynchronous ASGI)
* **ORM and Database:** SQLModel (SQLAlchemy 2.0 Core) + `aiosqlite` (asynchronouse driver)
* **Configuration and Validation:** Pydantic V2 + `pydantic-settings`
* **Security:** `python-jose` (JWT Tokens) + `passlib[bcrypt]` (password hashing configuration)
* **Testing:** `pytest` 
* **Infrastructure:** Docker, VS Code DevContainers

---

## Prerequisites

Before running the application, ensure your environment meets the following requirements:

### Windows
* **Docker Desktop**
* **WSL 2 (Windows Subsystem for Linux)** backend enabled within Docker Desktop settings
* Git bash terminal or WSL2 to execute shell scripts

### Linux (Ubuntu/Debian-based)
* **Docker Engine** installed.
* Your user added to the `docker` group to execute commands without `sudo`:
    ```bash
    sudo usermod -aG docker $USER && newgrp docker
    ```

### macOS
* **Docker Desktop for Mac** 

## Execution Workflows

You can run, test, and develop using three strategies depending on your toolchain:

### Strategy A: Automated Docker Scripts
The repository includes three production-grade utility scripts that handle image builds, container lifecycles, and cryptographic security initialization automatically.

1.  **Build the Image:**
    ```bash
    ./docker_build.sh
    ```
2.  **Run server:**
    
    ```bash
    ./docker_run.sh
    ```
    *The API is at `http://localhost:8000`. You can access the interactive documentation at `http://localhost:8000/docs`.*
3.  **Run the Test Suite:**
    ```bash
    ./docker_test.sh
    ```
    *This runs the test suite inside an isolated container using an in-memory SQLite instance.*

### Strategy B: Swagger UI Manual Testing Workflow

Follow this sequence to test endpoints (because the Swagger application enforces strict token-based authentication):

### Step 1: Initialize the Session
1. Boot the application using `./docker_run.sh` and navigate to `http://localhost:8000/docs`
2. Locate the green **Authorize** button at the top right of the page

### Step 2: Acquire the Bearer Token
1. Click the **Authorize** button to open the login modal.
2. Enter a valid user's credentials (or create one first using the `POST /users` registration endpoint).
3. Click **Authorize**. 

### Step 3: Execute Protected Actions
1. Scroll down to the `POST /messages` route.
2. Click **Try it out**, fill in the message payload, and click **Execute**.
3. Verify the server returns a `201 Created` status code, showing that your `current_user.id` was successfully extracted from the payload signature and linked to the message model.

### Strategy C: Developing inside VS Code DevContainers

To access the complete development environment:

1. Open the project directory in **Visual Studio Code**.
2. Ensure the vscode extension **Dev Containers** is active.
3. execute from the command line:
   ```python3.11 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))" > .env```
4. Click the button in the bottom-left corner of VS Code ('Open a Remote Window') and select **"Reopen in Container"**.
5. The devcontainer will automatically spin up, map your workspace, and initialize your local SQLite instance.
6. Open a terminal within the devcontainer and type:
   ```bash
   uvicorn app.main:app --port 8000 --reload --host 0.0.0.0
   ```

   

### Strategy D: Running Locally (Without Containers)
If you prefer to execute the application directly on your host machine's command line, follow this python setup pattern:

1.  **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
    ```
2.  **Install System Dependencies:**
    
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set Required Environment Variables & Launch:**
    Because the application protects against structural key leakage, you must export your runtime variables directly to your shell session before starting the engine:
    ```bash
    # Linux / macOS / Git Bash
    export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    # Or
    python3.11 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))" > .env
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
4.  **Run Tests Locally:**
    
    ```bash
    python3 -m pytest tests/test_messageboard.py
    ```
