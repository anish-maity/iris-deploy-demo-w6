# 🌸 Iris Classifier API: Continuous Deployment (CD) Pipeline

This repository contains all the necessary components for an Iris classification FastAPI service, containerized with Docker, and deployed automatically to **Google Kubernetes Engine (GKE)** using **GitHub Actions**.

The Continuous Deployment (**CD**) pipeline ensures that every commit pushed to the `main` branch results in a new, secure, and production-ready deployment on the GKE cluster.

---

## 1. Project Architecture

The application follows a standard cloud-native pattern:

| Component       | Technology                  | Purpose                                                    |
|-----------------|----------------------------|------------------------------------------------------------|
| Application     | Python / FastAPI           | Serves the machine learning model.                        |
| Container       | Docker                     | Packages the application and dependencies into an immutable image. |
| Image Registry  | Google Artifact Registry (GAR) | Securely stores the built Docker image.                  |
| Orchestration   | Google Kubernetes Engine (GKE) | Manages scaling, healing, and external access to the containerized service. |
| Automation      | GitHub Actions             | Defines the automated Build, Push, and Deploy pipeline.   |

---

## 2. File Utility Breakdown

The files in this repository are divided into three core categories: **Application**, **Containerization**, and **CI/CD Infrastructure**.

### A. Application Files

| File Name        | Utility         | Objective |
|-----------------|----------------|-----------|
| `iris_fastapi.py` | API Logic      | Defines the FastAPI application. It loads `model.joblib`, establishes the data schema using `pydantic.BaseModel` (`IrisInput`), and creates the `/predict/` endpoint for classification. |
| `model.joblib`   | Application Data | Serialized (trained) machine learning model (e.g., Decision Tree) used by `iris_fastapi.py` to make predictions. |
| `requirements.txt` | Dependency Management | Lists all Python packages required to run the application (FastAPI, uvicorn, scikit-learn, etc.). Used by Dockerfile during the build process. |

### B. Containerization Files

| File Name | Utility          | Objective |
|-----------|-----------------|-----------|
| `Dockerfile` | Container Blueprint | Contains instructions for building the application's Docker image. Specifies base OS, sets up working directory, installs dependencies from `requirements.txt`, copies application files, and defines the final command (`CMD ["uvicorn", ...]`) to run the API server. |

### C. CI/CD Infrastructure Files

| File Name                  | Utility                   | Objective |
|----------------------------|--------------------------|-----------|
| `.github/workflows/cd.yml` | Continuous Deployment Pipeline | Main automation script defining actions executed on every push to the `main` branch: <br>1. Authenticate to GCP using Workload Identity Federation (WIF). <br>2. Build the Docker image. <br>3. Push the image to Google Artifact Registry. <br>4. Deploy the new image to GKE via `kubectl`. <br>5. Post a status comment to the Git commit. |
| `k8s/deployment.yaml`      | Kubernetes Manifest       | Defines the desired state of the application in the GKE cluster: <br>- **Deployment**: Specifies app name (`iris-demo-workload`), replicas, and container definition (`iris-api-sha256-1`). <br>- **Service (LoadBalancer)**: Exposes the deployment externally on port 80 with a public IP. |

---

## 3. GitHub Actions Workflow Summary

The `cd.yml` workflow is a 6-step automation chain powered by the Google GitHub Actions library:

1. **Checkout Repository**: Fetches the code.
2. **Google Auth**: Securely authenticates to GCP using Workload Identity Federation (**WIF**).
3. **Build and Push Docker Image to GAR**: Creates the Docker image and tags it with the unique Git **SHA**, pushing the artifact to Artifact Registry.
4. **Get GKE Credentials**: Configures the `kubectl` tool to communicate with the target GKE cluster.
5. **Deploy to GKE and Rollout Update**: Executes `kubectl set image` to trigger a zero-downtime rolling update on the `iris-demo-workload` Deployment.
6. **Post Deployment Status Comment**: Provides instant feedback directly on the GitHub commit, confirming success/failure and providing the new image tag and external IP address.

---

This setup ensures a fully automated **CI/CD pipeline**, from code push to production-ready deployment on GKE.
