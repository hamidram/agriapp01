# Capstone Project: Deployment & Monitoring Architecture

## 1. Executive Summary
This document outlines the end-to-end production architecture for the **Agricultural Yield Intelligence** capstone application. The system is containerized using Docker, orchestrated via Docker Compose on a Google Cloud Platform (GCP) Virtual Machine, governed by automated Continuous Integration (CI) via GitHub Actions, and fully instrumented for real-time observability using Prometheus and Grafana.

---

## 2. System Architecture & Tech Stack
The production stack consists of four core microservices running within an isolated Docker bridge network:
* **FastAPI Backend (`agri-api-service`):** Serves machine learning inference endpoints, instrumented with `prometheus-fastapi-instrumentator` to expose live HTTP and performance metrics on port `8000`.
* **Streamlit UI (`agri-ui-service`):** Provides an interactive web frontend for users to input agricultural telemetry and view yield predictions on port `8501`.
* **Prometheus (`prometheus`):** Scrapes metrics from the FastAPI backend at configured intervals and stores time-series data on port `9090`.
* **Grafana (`grafana`):** Connects to Prometheus as a data source to render custom operational dashboards and visualize system health on port `3000`.

---

## 3. CI/CD & Automation Workflow
To ensure software reliability and prevent regressions, code changes are governed by an automated CI pipeline:
* **Version Control & Trigger:** Code pushes and pull requests to the `main` branch automatically trigger a GitHub Actions workflow (`ci.yml`).
* **Automated Testing:** The cloud runner provisions a clean Ubuntu environment, installs project dependencies from `requirements.txt` in editable mode (`pip install -e .`), and executes unit and integration tests using `pytest` and `httpx`.
* **Deployment Gate:** Only code passing all automated test suites is approved for deployment to the production environment.

---

## 4. Production Deployment & Observability (GCP VM)
The production environment is hosted on a GCP Compute Engine instance:
* **Orchestration:** Managed via a single declarative `docker-compose.yml` manifest, ensuring environment parity between local development and cloud production.
* **Network & Firewall:** Ingress traffic is managed via GCP VPC firewall rules permitting secure external access to application ports (`8000`, `8501`, `3000`, `9090`).
* **Monitoring & Alerting:** Prometheus tracks API availability, request latencies, and error rates (`http_requests_total`), while Grafana visualizes these metrics in real-time dashboards to ensure high availability.