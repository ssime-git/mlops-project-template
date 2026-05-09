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

### Hydra Configuration

This template uses **Hydra** for composition-based config management.

**Basic usage:**
```bash
# Run with default config
python -m ml_project train

# Override parameters via command line
python -m ml_project train model.n_estimators=200 training.cv_folds=3

# Use a different model config
python -m ml_project train model=LightGBM
```

**Config structure:**
- `configs/default.yaml` — base defaults
- `configs/model/*.yaml` — model-specific configs  
- `configs/train.yaml` — training settings

**Composition example:**
```yaml
# configs/train.yaml
defaults:
  - _self_
  - model: default  # loads configs/model/default.yaml

data:
  raw_path: data/raw/train.csv
  test_size: 0.2
```

**Multirun (sweep hyperparams):**
```bash
python -m ml_project train model.n_estimators=100,200,300
```

```bash
# Run training with explicit config
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