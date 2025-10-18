`

```python
from fastapi.testclient import TestClient
from app.main import app, HealthStatus, Employee # Import models for stronger type assertions

# Initialize the TestClient with your FastAPI app
client = TestClient(app)

def test_health_endpoint():
    """
    Test the /health endpoint to ensure it returns status 'ok'.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    # Optional: Validate with Pydantic model for stricter checks
    health_status = HealthStatus(**response.json())
    assert health_status.status == "ok"

def test_get_existing_employee():
    """
    Test retrieving an existing employee by ID.
    """
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Alice"}
    employee = Employee(**response.json())
    assert employee.id == 1
    assert employee.name == "Alice"

def test_get_unknown_employee_returns_placeholder():
    """
    Test retrieving an employee with an unknown ID, expecting a placeholder.
    """
    response = client.get("/employees/999")
    assert response.status_code == 200 # As per requirement, returns a placeholder, not 404
    assert response.json() == {"id": 999, "name": "Unknown"}
    employee = Employee(**response.json())
    assert employee.id == 999
    assert employee.name == "Unknown"

def test_get_employee_with_invalid_id_type():
    """
    Test retrieving an employee with a non-integer ID, expecting a 422 Unprocessable Entity.
    """
    response = client.get("/employees/not_an_id")
    assert response.status_code == 422 # FastAPI's automatic validation for type errors
    assert "detail" in response.json()
    assert response.json()["detail"][0]["msg"] == "value is not a valid integer"
```

---

### `requirements.txt`

```
fastapi
uvicorn
pytest
httpx
pydantic # Although a dependency of fastapi, good to explicitly list if used directly
```

---

### How to Run

1.  **Create the files and directory structure** as shown above.
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the service locally:**
    ```bash
    python app/main.py
    ```
    The service will be available at `http://0.0.0.0:8080`.
    You can test it with `curl http://localhost:8080/health` or `http://localhost:8080/employees/1`.
4.  **Run the tests:**
    ```bash
    pytest app/tests/
    ```

This setup provides a robust, minimal, and testable foundation for your FastAPI service, ready for deployment to environments like Google Cloud Run.