# MLOps Project Template

Production-ready machine learning project template following the **MLOps 4-Phase Roadmap**.

## 🚀 First Step: Define Your Problem

**Before writing any code, fill out `configs/problem.yaml`** — this forces you to:

1. Articulate the business problem
2. Define success metrics (ML + business)
3. Establish a baseline to beat
4. Identify constraints (latency, hardware)

```bash
# Edit your problem definition first
code configs/problem.yaml
```

---

## 📋 MLOps Roadmap (4 Phases)

### Phase 1: Fondations & Containerisation
**Deadline: 30 janvier**

- [ ] Define project objectives and key metrics (`configs/problem.yaml`)
- [ ] Set up reproducible dev environment
- [ ] Collect and preprocess data
- [ ] Build and evaluate baseline ML model
- [ ] Implement unit tests
- [ ] Implement basic inference API

### Phase 2: Microservices, Suivi & Versioning
**Deadline: 6 février**

- [ ] Set up experiment tracking with MLflow
- [ ] Implement data and model versioning
- [ ] Decompose into microservices with orchestration

### Phase 3: Orchestration & Déploiement
**Deadline: 13 febrero**

- [ ] Finalize end-to-end orchestration
- [ ] Create CI pipeline
- [ ] Optimize and secure API
- [ ] Implement scalability with Docker/Kubernetes

### Phase 4: Monitoring & Maintenance
**Deadline: 20 février**

- [ ] Set up performance monitoring (Prometheus/Grafana)
- [ ] Implement drift detection (Evidently)
- [ ] Develop automated model/component updates
- [ ] Finalize technical documentation

### 📅 Soutenance: 23/24 février

---

## Project Structure

```
mlops_project_template/
├── .github/workflows/     # CI/CD pipelines
├── api/                  # FastAPI inference service
├── configs/              # Hydra configuration (problem.yaml, etc.)
├── data/                 # Data directory
│   ├── raw/              # Raw data
│   ├── processed/        # Processed data
│   └── features/         # Engineered features
├── models/               # Saved models
├── notebooks/            # Jupyter notebooks
├── src/                  # Source code
│   └── ml_project/       # Main package
├── tests/                # Test suite
├── docker-compose.yml    # Local orchestration
├── Dockerfile.api        # API container
├── Dockerfile.train      # Training container
├── pyproject.toml        # UV project config
└── dvc.yaml              # Data pipeline
```

---

## Setup

```bash
# Install all dependencies
uv sync

# Install dev dependencies
uv sync --extra dev
```

---

## Phase 1: Quick Start

### Define your problem first
```bash
# Edit configs/problem.yaml before anything else
code configs/problem.yaml
```

### Run training
```bash
# With Hydra defaults
python -m ml_project train

# Override parameters
python -m ml_project train model.n_estimators=200 training.cv_folds=3
```

### Run tests
```bash
pytest tests/
```

### Run inference API (Phase 1 deliverable)
```bash
# Start FastAPI service
uvicorn api.main:app --reload

# Test inference
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"features": [1.0, 2.0, 3.0]}'
```

---

## Phase 2: MLflow & Versioning

### Start MLflow tracking server
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts
```

### Use in code
```python
import mlflow

mlflow.set_experiment("my_experiment")
with mlflow.start_run():
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")
```

### Data versioning with DVC
```bash
dvc init
dvc add data/raw/
git add data/raw.dvc
git commit -m "Version data"
```

---

## Phase 3: Docker & Orchestration

### Build containers
```bash
docker build -f Dockerfile.train -t ml_project:train .
docker build -f Dockerfile.api -t ml_project:api .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

### Access services
- API: http://localhost:8000
- MLflow: http://localhost:5000

---

## Phase 4: Monitoring

### Prometheus metrics (in API)
```python
from prometheus_client import Counter

requests = Counter('inference_requests', 'Total inference requests')
```

### Drift detection with Evidently
```bash
evidently dashboard --reference reference.csv --current current.csv
```

### Run Grafana for visualization
```bash
docker-compose up grafana
```

---

## Features Included

| Tool | Purpose |
|------|---------|
| **UV** | Fast package management |
| **Hydra** | Composition-based config |
| **MLflow** | Experiment tracking |
| **FastAPI** | Inference API |
| **DVC** | Data versioning |
| **Great Expectations** | Data validation |
| **Docker Compose** | Local orchestration |
| **Evidently** | Drift detection |
| **Prometheus/Grafana** | Monitoring |

---

## CI/CD

GitHub Actions workflow included in `.github/workflows/`:

- Lint (ruff, black)
- Type check (mypy)
- Unit tests
- Build Docker images

---

## Next Steps

1. **Start with Phase 1**: Fill `configs/problem.yaml`
2. **Build baseline model**: Add code to `src/ml_project/`
3. **Add tests**: Expand `tests/`
4. **Deploy API**: Configure `api/main.py`
5. **Progress through phases**: Each phase builds on the previous