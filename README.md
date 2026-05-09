# MLOps Project Template

Production-ready machine learning project with UV package management.

## 🚀 First Step: Define Your Problem

**Before writing any code, fill out `configs/problem.yaml`** — this forces you to:

1. Articulate the business problem
2. Define success metrics (ML + business)
3. Establish a baseline to beat
4. Identify constraints (latency, hardware)

```bash
# Edit your problem definition
code configs/problem.yaml
```

## Project Structure

```
ml-project/
├── .github/workflows/     # CI/CD pipelines
├── configs/              # Hydra configuration files
├── data/                 # Data directory
│   ├── raw/              # Raw data
│   ├── processed/        # Processed data
│   └── features/         # Engineered features
├── models/               # Saved models
├── notebooks/            # Jupyter notebooks
├── pipelines/            # Prefect/MLFlow pipelines
├── src/                  # Source code
│   └── ml_project/       # Main package
├── tests/                # Test suite
└── pyproject.toml        # UV project configuration
```

## Setup

```bash
# Install dependencies
uv sync

# Install dev dependencies
uv sync --extra dev
```

## Usage

```bash
# Run training
python -m ml_project train --config configs/train.yaml

# Run tests
pytest tests/
```

## Features

- **UV** for fast package management
- **Hydra** for configuration management
- **MLflow** for experiment tracking
- **Prefect** for pipeline orchestration
- **Great Expectations** for data validation
- **DVC** for data versioning (optional)