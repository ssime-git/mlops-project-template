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

**File to complete:** `configs/problem.yaml`

```bash
# First reflex: fill in the framing
code configs/problem.yaml
```


### Project Phases

#### Phase 1: Foundations & Containerization (The Unit)
**Objective:** Make the model accessible via a containerized, tested API.

| Main Task | Technical Detail |
|------------------|-------------------|
| Environment & Baseline | Setup `uv`, train the first simple model. |
| API Implementation | Create the FastAPI server in `src/api/`. |
| Unit Tests | Write tests for `/health`, `/predict`, and preprocessing functions. |
| Data Validation | Add basic schema checks on input data (column names, types, ranges). |
| Containerization | Write `docker/api.Dockerfile` and the first `docker-compose.yml` (api service only). |

**Technical Deliverable:** A functional, tested API service launched via `docker-compose up api`.

#### Phase 2: Microservices & Data Management (The Ecosystem)
**Objective:** Manage the lifecycle of data, experiments, and models — and automate their delivery.

| Main Task | Technical Detail |
|------------------|-------------------|
| Experiment Tracking | Add MLflow to `docker-compose.yml` (or configure Dagshub). |
| Model Registry | Register trained models in MLflow Model Registry; use `Staging` and `Production` stages. |
| Data Versioning | Add MinIO (S3) to `docker-compose.yml` -> Config DVC. |
| Training Pipeline | Create `docker/train.Dockerfile` to isolate the training process. |
| CI/CD Pipeline | Automate Docker image build and push on each commit (GitHub Actions). |

**Technical Deliverable:** Orchestrated stack `api` + `mlflow` + `minio`, with active experiment tracking, versioned artifacts, model registry, and an automated build pipeline.

#### Phase 3: Orchestration & Security (The Pipeline)
**Objective:** Automate the data flow and secure API access.

| Main Task | Technical Detail |
|------------------|-------------------|
| Workflow Automation | Add Prefect or Airflow to `docker-compose.yml`. |
| API Gateway & Security | Implement JWT and access management on the API. |

**Technical Deliverable:** Automated pipeline (Data -> Train -> Deploy) and secured API.

#### Phase 4: Monitoring & Observability (Production)
**Objective:** Ensure stability and detect model degradation early.

| Main Task | Technical Detail |
|------------------|-------------------|
| Infra Metrics | Add Prometheus and Grafana to `docker-compose.yml`. |
| Model Drift | Integrate Evidently to monitor data drift (`src/monitoring/detection.py`). |
| Feedback Loop | Define alert thresholds on drift metrics; trigger retraining when exceeded; validate and promote the new model via the MLflow registry. |

**Technical Deliverable:** Complete monitoring dashboard, operational alerting, and a documented retraining decision process.

#### 📅 Presentation: date to be defined


## 🔄 Transitions between Phases

Each phase ends with a **review** before moving to the next:

```sh
Phase 1 ──► Review (model + API validated) ──► Phase 2 ──► Review ──► Phase 3 ──► Review ──► Phase 4
   │                                                    │                              │
   ▼                                                    ▼                              ▼
Technical Validation                              Infra Validation                  Prod Validation
```

### Passage Criteria:

- **Phase 1 → Phase 2:** Tests passing, API functional, Dockerfile validated, data validation in place
- **Phase 2 → Phase 3:** Experiments tracked, versioning operational, artifacts versioned, model in registry, CI/CD running
- **Phase 3 → Phase 4:** Orchestrated pipeline operational, rollback possible, API secured


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

**Prefect (example):**
```python
from prefect import flow, task

@task
def preprocess_data():
    pass

@flow
def train_pipeline():
    data = preprocess_data()
    model = train_model(data)
    return model
```

**Airflow (alternative):**

```bash
airflow standalone
```

```python
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

**DVC:**
```bash
dvc init
dvc add data/raw/
git add data/raw.dvc
git commit -m "Add raw data v1"
dvc checkout
```

**Useful DVC commands:**
```bash
dvc repro          # Re-run the pipeline
dvc metrics show   # Show metrics
dvc diff           # See changes
```

### Experiment Tracking

| Techno | When to use | Installation |
|--------|------------------|--------------|
| **MLflow** (default) | Open tracking, multi-language | `pip install mlflow` |
| **Weights & Biases** | Elegant user interface, collaboration | `pip install wandb` |
| **Neptune.ai** | Comprehensive platform, metadata richness | `pip install neptune` |

**MLflow:**
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts
```

```python
import mlflow

mlflow.set_experiment("my_experiment")
with mlflow.start_run():
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_params({"n_estimators": 100})
    mlflow.sklearn.log_model(model, "model")
```

### Inference API

| Techno | When to use | Installation |
|--------|------------------|--------------|
| **FastAPI** (default) | Performance, Pydantic validation, native async | `pip install fastapi uvicorn` |
| **Flask** | Simplicity, small project | `pip install flask` |
| **BentoML** | Specialized inference framework, simple packaging | `pip install bentoml` |

**FastAPI (default):**
```bash
# Launch the server
uvicorn src.api.main:app --reload

# Test
curl http://localhost:8000/health
```

### Monitoring & Drift Detection

| Techno | When to use | Installation |
|--------|------------------|--------------|
| **Prometheus + Grafana** (default) | Custom metrics, powerful visualizations | docker-compose |
| **Evidently** (default) | Data/model drift detection | `pip install evidently` |
| **Arize** | Comprehensive ML monitoring platform | `pip install arize-ai` |

**Evidently (v0.4+):**
```python
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.report import Report

report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
report.run(reference_data=df_ref, current_data=df_current)
report.save_html("reports/drift/drift_report.html")
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

# Install dependencies (dev deps included automatically)
uv sync
```

### Step 1: Framing
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
| API Docs | http://localhost:8000/docs | Swagger UI |
| MLflow | http://localhost:5000 | Tracking |
| Prometheus | http://localhost:9090 | Metrics |
| Grafana | http://localhost:3000 | Dashboards (admin/admin) |
| MinIO | http://localhost:9001 | Object Storage console |


## Project Structure

```sh
mlops_project/
├── .github/workflows/     # CI/CD
├── configs/               # Hydra configurations
│   ├── model/            # Model hyperparameters
│   ├── problem.yaml      # Project framing
│   └── train.yaml        # Training config
├── data/                  # Data (managed by DVC)
│   ├── raw/              # Raw data
│   └── processed/        # Processed data
├── deployment/           # Infra configs (Prometheus, Grafana)
├── docker/               # Dockerfiles
├── docs/                 # Methodology documentation
├── models/               # Trained models
├── reports/              # Generated drift reports (HTML)
├── src/                  # UV workspace packages
│   ├── api/             # FastAPI inference service
│   ├── common/          # Shared utilities
│   ├── monitoring/      # Drift detection
│   └── training/        # Train / preprocess / evaluate
├── tests/                # Tests
├── docker-compose.yml    # Local orchestration
├── dvc.yaml              # DVC pipeline
└── pyproject.toml        # Root workspace config
```

## ✅ Checklist by Phase

### Phase 1: Foundations
- [ ] `configs/problem.yaml` filled
- [ ] Reproducible environment (`uv sync`)
- [ ] Functional inference API (`src/api/main.py`)
- [ ] Unit tests passing (`pytest tests/`)
- [ ] Basic data validation in place
- [ ] Initial containerization (`docker-compose up api`)

### Phase 2: Microservices & Data Management
- [ ] MLflow operational (experiment tracking)
- [ ] Model registered in MLflow Model Registry
- [ ] Data versioned via MinIO (S3/DVC)
- [ ] Isolated training container (`docker/train.Dockerfile`)
- [ ] Orchestrated stack (`api` + `mlflow` + `minio`)
- [ ] CI/CD pipeline operational (build + push)

### Phase 3: Orchestration & Security
- [ ] Orchestrator launched via Docker (Prefect/Airflow)
- [ ] Automated pipeline (Data -> Train -> Deploy)
- [ ] API secured (JWT)
- [ ] `docker-compose.yml` updated with the orchestrator

### Phase 4: Monitoring & Observability
- [ ] Prometheus & Grafana launched via Docker Compose
- [ ] Model drift monitoring operational (Evidently)
- [ ] Alert thresholds defined and tested
- [ ] Retraining trigger documented
- [ ] Final documentation and runbooks

## Customization of the Template

To adapt this template to your project:

1. **Replace `problem.yaml`** with your use case
2. **Modify Hydra configs** in `configs/`
3. **Implement your model** in `src/training/`
4. **Adapt the API** in `src/api/main.py`
5. **Configure metrics** in `deployment/prometheus/prometheus.yml`
6. **Add your tests** in `tests/`

## 📚 Complementary Resources

- [Awesome MLOps](https://github.com/visenger/awesome-mlops)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [DVC Documentation](https://dvc.org/doc)
