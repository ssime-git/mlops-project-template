# MLOps Project Template

⚠️ **This repository is a TEMPLATE** — adapt it to your real ML project. It provides a basic structure and examples for each phase of the MLOps lifecycle.


## MLOps Methodology

This methodology describes a structured path to industrialize an ML project through 4 main phases. The goal is to reach a robust, monitored, and maintainable production system.

### Framing (Preliminary Step)

Before any technical implementation, it is imperative to frame the project:

| Task | Description |
|-------|-------------|
| **Define the business problem** | What decision does the model influence? |
| **Identify metrics** | ML Metrics (accuracy, recall, etc.) + Business Metrics (revenue, savings, etc.) |
| **Establish a baseline** | Simple model or heuristic to beat |
| **Assess feasibility** | Data available? Sufficient? Labeled? |
| **Identify constraints** | Latency, (CPU/GPU/edge), regulations |

**File to complete :** `configs/problem.yaml`

```bash
# First reflex: fill in the framing
code configs/problem.yaml
```


### Project Phases

#### Phase 1: Foundations & Containerization (The Unit)
**Objective :** Make the model accessible via a containerized API.

| Main Task | Technical Detail |
|------------------|-------------------|
| Environment & Baseline | Setup `uv`, train the first simple model. |
| API Implementation | Create the FastAPI server. |
| Containerization | Write `Dockerfile.api` and the first `docker-compose.yml` (api service only). |

**Technical Deliverable :** A functional API service launched via `docker-compose up api`.

#### Phase 2: Microservices & Data Management (The Ecosystem)
**Objective :** Manage the lifecycle of data and models.

| Main Task | Technical Detail |
|------------------|-------------------|
| Experiment Tracking | Add MLflow to `docker-compose.yml` (or configure Dagshub). |
| Data Versioning | Add MinIO (S3) to `docker-compose.yml` $\rightarrow$ Config DVC. |
| Training Pipeline | Create `Dockerfile.train` to isolate the training process. |

**Technical Deliverable :** Orchestrated stack `api` + `mlflow` + `minio`, with active experiment tracking.

#### Phase 3: Orchestration & Security (The Pipeline)
**Objective :** Automate the data flow and secure access.

| Main Task | Technical Detail |
|------------------|-------------------|
| Workflow Automation | Add Prefect or Airflow to `docker-compose.yml`. |
| CI/CD Pipeline | Automate the build and push of Docker images. |
| API Gateway & Security | Implement JWT and access management on the API. |

**Technical Deliverable : la** Automated pipeline (Data $\rightarrow$ Train $\rightarrow$ Deploy) and secured API.

#### Phase 4: Monitoring & Observability (Production)
**Objective :** Ensure stability and detect model degradation.

| Main Task | Technical Detail |
|------------------|-------------------|
| Infra Metrics | Add Prometheus and Grafana to `docker-compose.yml`. |
| Model Drift | Integrate Evidently to monitor data drift. |
| Feedback Loop | Implement alerts and automatic retraining strategy. |

**Technical Deliverable :** Complete monitoring dashboard and operational alerting system.

#### 📅 Presentation : date to be defined


## 🔄 Transitions between Phases

Each phase ends with a **review** before moving to the next:

```sh
Phase 1 ──► Review (model + API validated) ──► Phase 2 ──► Review ──► Phase 3 ──► Review ──► Phase 4
   │                                                    │                              │
   ▼                                                    ▼                              ▼
Technical Validation                              Infra Validation                  Prod Validation
```

### Passage Criteria :

- **Phase 1 → Phase 2 :** Tests OK, API functional, Dockerfile validated
- **Phase 2 → Phase 3 :** Experiments tracked, versioning operational, artifacts versioned
- **Phase 3 → Phase 4 :** CI/CD operational, rollback possible, setup in place


## Teamwork (Parallel Tasks)

To optimize time, some tasks can be carried out in **parallel**:

| Task A | Task B | Team |
|---------|---------|--------|
| Model Training | API Development | ML Eng + MLE |
| Feature engineering | Data contracts definition | Data Eng |
| MLflow Setup | Docker Infrastructure | MLE + DevOps |
| Unit Tests | Documentation | QA + Tech Writer |
| Monitoring | CI/CD | SRE + DevOps |


## MLOps Technologies

This template uses some default technologies, but other options are possible depending on your needs:

### Pipeline Orchestration

| Techno | When to use | Installation |
|--------|------------------|--------------|
| **Prefect** (default) | Small to medium project, simplicity, cloud monitoring | `uv pip install prefect` |
| **Airflow** | Large project, robust ecosystem, many integrations | `pip install apache-airflow` |
| **Dagster** | Modern project, software engineering best practices | `pip install dagster` |

**Prefect (example) :**
```python
# Prefect pipeline example
from prefect import flow, task

@task
def preprocess_data():
    # your code
    pass

@flow
def train_pipeline():
    data = preprocess_data()
    model = train_model(data)
    return model
```

**Airflow (alternative) :**

```bash
# Launch Airflow
airflow standalone
```

```python
# Airflow DAG example
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG('ml_pipeline', start_date=datetime(2024,1,1)) as dag:
    preprocess = PythonOperator(task_id='preprocess', python_callable=preprocess)
    train = PythonOperator(task_id='train', python_callable=train)
    preprocess >> train
```

### Data Versioning

| Techno | When to use | Installation |
|--------|------------------|--------------|
| **DVC** (default) | File versioning, declarative pipeline | `pip install dvc` |
| **lakeFS** | Data lake with versioning, dev/prod environment | Docker Compose |
| **Delta Lake** | Parquet format with transactions (Spark) | Spark dependency |

**DVC :**
```bash
# Initialize DVC
dvc init

# Add data
dvc add data/raw/

# Version
git add data/raw.dvc
git commit -m \"Add raw data v1\"

# Retrieve a version
dvc checkout
```

**Useful DVC Commands :**
```bash
dvc repro          # Relaunch the pipeline
dvc metrics show   # Show metrics
dvc diff           # See changes
dvc queue start    # Retraining queue
```

### Experiment Tracking

| Techno | When to use | Installation |
|--------|------------------|--------------|
| **MLflow** (default) | Open tracking, multi-language | `pip install mlflow` |
| **Weights & Biases** | Elegant user interface, collaboration | `pip install wandb` |
| **Neptune.ai** | Comprehensive platform, metadata richness | `pip install neptune` |

**MLflow :**
```bash
# Start the server
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts
```

```python
import mlflow

mlflow.set_experiment(\"mon_experience\")
with mlflow.start_run():
    mlflow.log_metric(\"accuracy\", 0.95)
    mlflow.log_params({\"n_estimators\": 100})
    mlflow.sklearn.log_model(model, \"model\")
```

### Inference API

| Techno | When to use | Installation |
|--------|------------------|--------------|
| **FastAPI** (default) | Performance, Pydantic validation, native async | `pip install fastapi uvicorn` |
| **Flask** | Simplicity, small project | `pip install flask` |
| **BentoML** | Specialized inference framework, simple packaging | `pip install bentoml` |

**FastAPI (default) :**
```bash
# Launch the server
uvicorn api.main:app --reload

# Test
curl http://localhost:8000/health
```

### Monitoring & Drift Detection

| Techno | When to use | Installation |
|--------|------------------|--------------|
| **Prometheus + Grafana** (default) | Custom metrics, powerful visualizations | docker-compose |
| **Evidently** (default) | Data/model drift detection | `pip install evidently` |
| **Arize** | Comprehensive ML monitoring platform | pip install arize-ai |

**Evidently :**
```python
from evidently.dashboard import Dashboard
from evidently.tabs import DataDriftTab

dashboard = Dashboard(tabs=[DataDriftTab()])
dashboard.calculate(reference_data=df_ref, current_data=df_current)
dashboard.save(\"reports/drift.html\")
```

---

## Installation and Quick Start

### Prerequisites
```bash
# Install UV (package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Docker and Docker Compose
# See https://docs.docker.com/
```

### Project Setup
```bash
# Clone the template
git clone <your-repo-url>
cd mlops-project

# Install dependencies
uv sync

# Install dev dependencies
uv sync --extra dev
```

### Step 1 : Framing
```bash
# Fill the problem file
code configs/problem.yaml
```

### Launch services
```bash
# API only (Phase 1)
docker-compose up api -d

# All services (Phase 2-4)
docker-compose up -d
```

### Available Services
| Service | URL | Description |
|---------|-----|-------------|
| API | http://localhost:8000 | Inference endpoint |
| API Doc | http://localhost:8000/docs | Swagger UI |
| MLflow | http://localhost:5000 | Tracking |
| Prometheus | http://localhost:9090 | Metrics |
| Grafana | http://localhost:3000 | Dashboards (admin/admin) |
| MinIO | http://localhost:9000 | Object Storage |L


## Project Structure

```sh
mlops_project/
├── .github/workflows/     # CI/CD
├── api/                   # API FastAPI
├── configs/               # Configurations Hydra
│   └── problem.yaml      # Project framing
├── data/                  # Data
│   ├── raw/              # Raw data
│   └── features/         # Feature engineering
├── models/                # Trained models
├── notebooks/             # Jupyter exploration
├── pipelines/            # Prefect pipelines
├── reports/               # Drift reports
├── src/                   # Source code
│   └── ml_project/       # Main package
├── tests/                 # Tests
├── deployment/           # Infra configs (Prometheus, Grafana)
├── docker/               # Dockerfiles
├── docker-compose.yml     # Orchestration
├── pyproject.toml        # Dependencies
└── dvc.yaml              # DVC pipeline
```

## ✅ Checklist by Phase

### Phase 1 : Foundations
- [ ] `configs/problem.yaml` filled
- [ ] Reproducible environment (uv sync)
- [ ] Functional inference API
- [ ] Initial containerization (`docker-compose up api`)

### Phase 2 : Microservices & Data Management
- [ ] MLflow operational (experiment tracking)
- [ ] la Data versioned via MinIO (S3/DVC)
- [ ] Isolated training container (`Dockerfile.train`)
- [ ] Orchestrated stack (`api` + `mlflow` + `minio`)

### Phase la 3 : Orchestration & Security
- [ ] Orchestrator launched via Docker (Prefect/Airflow)
- [ ] la Pipeline CI/CD functional (Build $\rightarrow$ Push)
- [ ] Secured API (JWT)
- [ ] la Docker Compose updated with the orchestrator

### Phase 4 : Monitoring & Observability
- [ ] Prometheus & Grafana launched via Docker Compose
- [ ] Model drift monitoring (Evidently)
- [ ] Operational alerting
- [ ] Documentation final and runbooks

## Customization of the Template

To adapt this template to your project:

1. **Replace `problem.yaml`** with your use case
2. **Modify Hydra configs** in `configs/`
3. **Implement your model** in `src/ml_project/`
4. **Adapt the API** in `api/main.py`
5. **Configure metrics** in `prometheus/prometheus.yml`
6. **Add your tests** in `tests/`

## 📚 Complementary Resources

- [Awesome MLOps](https://github.com/visenger/awesome-mlops)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [DVC Documentation](https://dvc.org/doc)