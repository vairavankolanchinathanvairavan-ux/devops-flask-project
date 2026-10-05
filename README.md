# DevOps Project: Flask App → Docker → CI/CD → Kubernetes → Monitoring

This is a complete beginner-friendly DevOps project you can use for learning, college projects, interviews, or a portfolio.

## 1. Project Goal

The project demonstrates a real DevOps workflow:

**Developer writes code → Git stores code → automated tests run → Docker image is built → image is pushed to Docker Hub → Kubernetes deploys the image → Prometheus monitors the app.**

The application itself is intentionally small so you can focus on the DevOps process.

---

## 2. Architecture

```text
Developer
   |
   v
Git + GitHub
   |
   v
GitHub Actions CI/CD
   |
   +----> Run Pytest
   |
   +----> Build Docker Image
   |
   +----> Push Image to Docker Hub
                |
                v
          Kubernetes Cluster
                |
                v
          Flask Application
                |
                v
           /metrics endpoint
                |
                v
            Prometheus
```

---

## 3. Folder Structure

```text
devops-flask-project/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── k8s/
│   └── deployment.yaml
├── monitoring/
│   └── prometheus.yml
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── .dockerignore
└── README.md
```

---

## 4. What Each Part Does

### Flask Application
`app/main.py` creates a small web service.

Endpoints:

- `/` - main API response
- `/health` - health check used by Kubernetes
- `/metrics` - Prometheus metrics

### Tests
`tests/test_app.py` checks whether the main page and health endpoint work.

### Docker
`Dockerfile` packages the Python application and its dependencies into a portable container image.

### GitHub Actions
`.github/workflows/ci-cd.yml` runs automatically whenever code is pushed to `main`.

It performs:

1. Checkout source code
2. Install Python
3. Install dependencies
4. Run tests
5. Log in to Docker Hub
6. Build Docker image
7. Push Docker image to Docker Hub

### Kubernetes
`k8s/deployment.yaml` creates:

- 2 application replicas
- health checks
- a Service that exposes the application

### Prometheus
`monitoring/prometheus.yml` tells Prometheus to collect metrics from the application's `/metrics` endpoint.

---

# 5. Prerequisites

Install:

- Python 3.12 or newer
- Git
- Docker Desktop
- Docker Compose
- kubectl
- Minikube, Docker Desktop Kubernetes, or another Kubernetes cluster
- GitHub account
- Docker Hub account

Check installations:

```bash
python3 --version
git --version
docker --version
docker compose version
kubectl version --client
```

---

# 6. Run the Project Locally

Open Terminal and enter the project directory:

```bash
cd devops-flask-project
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Run tests:

```bash
pytest -v
```

Start the application:

```bash
python -m app.main
```

Open:

```text
http://localhost:5000
```

Health endpoint:

```text
http://localhost:5000/health
```

Metrics endpoint:

```text
http://localhost:5000/metrics
```

Stop the app with:

```text
Ctrl + C
```

---

# 7. Build the Docker Image

From the project directory:

```bash
docker build -t devops-demo:local .
```

Check the image:

```bash
docker images
```

Run the container:

```bash
docker run --rm -p 5000:5000 devops-demo:local
```

Open:

```text
http://localhost:5000
```

## Docker Workflow

```text
Source Code
   |
Dockerfile
   |
docker build
   |
Docker Image
   |
docker run
   |
Running Container
```

The Docker image contains your application and dependencies, so it behaves consistently on different computers.

---

# 8. Run App + Prometheus with Docker Compose

Run:

```bash
docker compose up --build
```

Application:

```text
http://localhost:5000
```

Prometheus:

```text
http://localhost:9090
```

In Prometheus, try this query:

```text
devops_demo_http_requests_total
```

Visit the Flask app a few times, then run the query again. The request counter should increase.

Stop everything:

```bash
docker compose down
```

---

# 9. Push the Project to GitHub

Create a new empty repository on GitHub, for example:

```text
devops-flask-project
```

Inside the project directory:

```bash
git init
git add .
git commit -m "Initial DevOps project"
git branch -M main
```

Connect your repository:

```bash
git remote add origin https://github.com/YOUR_USERNAME/devops-flask-project.git
```

Push:

```bash
git push -u origin main
```

If GitHub asks for authentication, use GitHub's supported authentication method such as a Personal Access Token or GitHub CLI. Do not use your normal GitHub password for Git operations.

---

# 10. Create a Docker Hub Repository

Log in to Docker Hub and create a repository named:

```text
devops-demo
```

Example image name:

```text
yourusername/devops-demo:latest
```

---

# 11. Configure GitHub Actions Secrets

Open your GitHub repository.

Go to:

```text
Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Create these secrets:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

`DOCKERHUB_USERNAME` is your Docker Hub username.

For `DOCKERHUB_TOKEN`, create a Docker Hub access token instead of storing your password.

---

# 12. CI/CD Workflow

After secrets are configured, edit a file and push it:

```bash
git add .
git commit -m "Test CI CD pipeline"
git push
```

GitHub Actions starts automatically.

The pipeline is:

```text
git push
   |
   v
GitHub Actions
   |
   v
Install Dependencies
   |
   v
Run Pytest
   |
   | success
   v
Docker Build
   |
   v
Docker Hub Login
   |
   v
Push Docker Image
```

If the tests fail, the Docker image will not be pushed.

That is an important DevOps principle: **do not deploy broken code**.

---

# 13. Deploy to Kubernetes

Before deployment, edit:

```text
k8s/deployment.yaml
```

Find:

```yaml
image: YOUR_DOCKERHUB_USERNAME/devops-demo:latest
```

Replace it with your Docker Hub username.

Example:

```yaml
image: myusername/devops-demo:latest
```

## Using Minikube

Start Minikube:

```bash
minikube start
```

Deploy:

```bash
kubectl apply -f k8s/deployment.yaml
```

Check deployment:

```bash
kubectl get deployments
```

Check pods:

```bash
kubectl get pods
```

Check services:

```bash
kubectl get services
```

For Minikube:

```bash
minikube service devops-demo-service
```

This opens the application.

## Kubernetes Workflow

```text
Docker Hub Image
      |
      v
Kubernetes Deployment
      |
      +---- Pod 1
      |
      +---- Pod 2
      |
      v
Kubernetes Service
      |
      v
Users
```

Kubernetes keeps the requested number of application replicas running.

If a pod crashes, Kubernetes can create a replacement.

---

# 14. Update the Application

Suppose you change:

```python
"version": "1.0.0"
```

to:

```python
"version": "1.1.0"
```

Commit and push:

```bash
git add .
git commit -m "Update application version"
git push
```

GitHub Actions runs tests and publishes a new Docker image.

To make Kubernetes pull the newest `latest` image:

```bash
kubectl rollout restart deployment devops-demo
```

Check rollout:

```bash
kubectl rollout status deployment devops-demo
```

---

# 15. Useful Kubernetes Commands

View pods:

```bash
kubectl get pods
```

View more details:

```bash
kubectl get pods -o wide
```

View deployment:

```bash
kubectl get deployment
```

View logs:

```bash
kubectl logs <pod-name>
```

Describe pod:

```bash
kubectl describe pod <pod-name>
```

Scale application:

```bash
kubectl scale deployment devops-demo --replicas=4
```

Delete project from Kubernetes:

```bash
kubectl delete -f k8s/deployment.yaml
```

---

# 16. Full DevOps Workflow Explained

## Step 1 — Development
A developer changes Python source code.

## Step 2 — Source Control
The code is committed to Git and pushed to GitHub.

## Step 3 — Continuous Integration
GitHub Actions automatically checks the project.

It installs dependencies and runs tests.

If tests fail, the pipeline stops.

## Step 4 — Containerization
If tests pass, GitHub Actions creates a Docker image.

## Step 5 — Container Registry
The image is pushed to Docker Hub.

Docker Hub stores versions of the application image.

## Step 6 — Deployment
Kubernetes pulls the Docker image and creates application pods.

## Step 7 — Health Checking
Kubernetes calls `/health`.

If the application is not healthy, Kubernetes can restart the container.

## Step 8 — Monitoring
Prometheus calls `/metrics` and collects application metrics.

## Step 9 — Continuous Improvement
The developer makes another code change and the cycle repeats.

```text
PLAN
  ↓
CODE
  ↓
GIT
  ↓
TEST
  ↓
BUILD
  ↓
DOCKER IMAGE
  ↓
REGISTRY
  ↓
DEPLOY
  ↓
MONITOR
  ↓
IMPROVE
  ↺
```

---

# 17. How to Explain This Project in an Interview

You can say:

> I built a Python Flask application and implemented a DevOps pipeline around it. I used Git and GitHub for version control, Pytest for automated testing, Docker for containerization, GitHub Actions for CI/CD, Docker Hub as the container registry, Kubernetes for deployment and scaling, and Prometheus for monitoring. The CI pipeline prevents the Docker image from being published if tests fail. Kubernetes uses health checks to verify the application is running correctly.

---

# 18. Common Problems

## Port 5000 is already used

Use another host port:

```bash
docker run --rm -p 8080:5000 devops-demo:local
```

Then open:

```text
http://localhost:8080
```

## Docker daemon is not running

Open Docker Desktop and wait until it is ready.

## GitHub Actions Docker login fails

Check:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

in GitHub repository secrets.

## Kubernetes ImagePullBackOff

Verify the image name in:

```text
k8s/deployment.yaml
```

and make sure the Docker Hub image is available to your cluster.

## Tests fail locally

Activate the virtual environment and reinstall dependencies:

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
```

---

# 19. Optional Improvements

After completing the basic project, you can add:

- Terraform for infrastructure provisioning
- Ansible for server configuration
- Helm charts for Kubernetes packaging
- Grafana dashboards
- Trivy image security scanning
- SonarQube code analysis
- AWS EKS, Azure AKS, or Google GKE
- Argo CD for GitOps deployment
- Nginx Ingress
- TLS/HTTPS
- PostgreSQL database
- Redis caching

---

# 20. Fast Demo Commands

Local:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
python -m app.main
```

Docker:

```bash
docker build -t devops-demo:local .
docker run --rm -p 5000:5000 devops-demo:local
```

Docker Compose + Prometheus:

```bash
docker compose up --build
```

Kubernetes:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl get pods
kubectl get services
```

---

## Final Result

After completing the project, you will understand:

- Git source control
- Automated testing
- Docker images and containers
- CI/CD
- Docker Hub
- Kubernetes deployments
- replicas and scaling
- health checks
- Prometheus monitoring
- the complete DevOps software delivery lifecycle
