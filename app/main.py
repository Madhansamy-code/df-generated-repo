`

```python
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing import Dict

# Pydantic Models for API responses
class HealthStatus(BaseModel):
    """
    Represents the health status of the service.
    """
    status: str

class Employee(BaseModel):
    """
    Represents an employee with an ID and a name.
    """
    id: int
    name: str

# In-memory database for employees
# In a real application, this would be a database connection.
_employees_db: Dict[int, Dict[str, any]] = {
    1: {"id": 1, "name": "Alice"},
    2: {"id": 2, "name": "Bob"},
    3: {"id": 3, "name": "Charlie"},
}

# Initialize FastAPI application
app = FastAPI(
    title="Employee API",
    description="A simple API for managing employee information.",
    version="1.0.0",
)

@app.get("/health", response_model=HealthStatus, summary="Health Check")
async def health_check():
    """
    Responds with a health status to indicate the service is running.
    """
    return {"status": "ok"}

@app.get("/employees/{employee_id}", response_model=Employee, summary="Get Employee by ID")
async def get_employee(employee_id: int):
    """
    Retrieves an employee by their ID.
    If the employee is not found, returns a placeholder with 'Unknown' name.
    """
    employee_data = _employees_db.get(employee_id)
    if employee_data:
        return Employee(**employee_data)
    else:
        # As per requirement: return placeholder for unknown employees
        return Employee(id=employee_id, name="Unknown")

# Entry point for running the Uvicorn server directly
# This block is essential for Cloud Run to pick up the server binding.
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False) # reload=False for production
```

---

### `