# Quick Start

## Local
```bash
cd devops-flask-project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
python -m app.main
```

Open http://localhost:5000

## Docker
```bash
docker build -t devops-demo:local .
docker run --rm -p 5000:5000 devops-demo:local
```

## Monitoring
```bash
docker compose up --build
```

App: http://localhost:5000  
Prometheus: http://localhost:9090

## Kubernetes
1. Push your Docker image to Docker Hub.
2. Replace `YOUR_DOCKERHUB_USERNAME` in `k8s/deployment.yaml`.
3. Run:

```bash
minikube start
kubectl apply -f k8s/deployment.yaml
kubectl get pods
minikube service devops-demo-service
```
