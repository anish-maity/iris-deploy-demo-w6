# 1. Use an official Python base image - slim is recommended for smaller size
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the dependencies file and install them
# This step is done separately and first to leverage Docker's build cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application files (iris_fastapi.py and model.joblib)
COPY . /app

# 5. Expose the port the FastAPI application will run on (default for Uvicorn is 8000)
EXPOSE 8000

# 6. Command to run the Uvicorn server, binding it to 0.0.0.0 for external access
# We use the app:app format (module:FastAPI_instance_name)
CMD ["uvicorn", "iris_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
