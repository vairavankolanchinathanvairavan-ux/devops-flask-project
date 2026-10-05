.PHONY: install test run docker-build docker-run compose-up compose-down k8s-apply k8s-delete

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements-dev.txt

test:
	. .venv/bin/activate && pytest -v

run:
	. .venv/bin/activate && python -m app.main

docker-build:
	docker build -t devops-demo:local .

docker-run:
	docker run --rm -p 5000:5000 devops-demo:local

compose-up:
	docker compose up --build

compose-down:
	docker compose down

k8s-apply:
	kubectl apply -f k8s/deployment.yaml

k8s-delete:
	kubectl delete -f k8s/deployment.yaml
