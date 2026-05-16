"""
Training module.
Run via: python -m training train
Or with custom config: python -m training train model=lightgbm training.cv_folds=10
"""
import logging
from pathlib import Path

import hydra
import joblib
import mlflow
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from sklearn.ensemble import RandomForestClassifier

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="configs", config_name="train")
def train(cfg: DictConfig):
    """Train a model using Hydra configuration."""
    # Log the full configuration
    log.info(f"Training configuration:\n{OmegaConf.to_yaml(cfg)}")

    # Start MLflow run
    mlflow.set_experiment(cfg.mlflow.experiment_name)
    with mlflow.start_run(run_name="training"):
        # Log configuration
        mlflow.log_params(OmegaConf.to_container(cfg, resolve=True))

        # Load data
        train_path = Path(cfg.data.processed_path)
        if not train_path.exists():
            log.error(f"Training data not found: {train_path}")
            return

        df = pd.read_csv(train_path)
        log.info(f"Loaded training data: {df.shape}")

        # Separate features and target (assumes 'target' column exists)
        if "target" not in df.columns:
            log.warning("No 'target' column found. Using last column as target.")
            X = df.iloc[:, :-1]
            y = df.iloc[:, -1]
        else:
            X = df.drop(columns=["target"])
            y = df["target"]

        # Initialize model based on config
        model_name = cfg.model.name
        if model_name == "RandomForestClassifier":
            model = RandomForestClassifier(
                n_estimators=cfg.model.n_estimators,
                max_depth=cfg.model.max_depth,
                random_state=cfg.model.random_state,
            )
        else:
            log.warning(f"Unknown model: {model_name}, using RandomForestClassifier")
            model = RandomForestClassifier(
                n_estimators=cfg.model.n_estimators,
                max_depth=cfg.model.max_depth,
                random_state=cfg.model.random_state,
            )

        # Train model
        log.info("Training model...")
        model.fit(X, y)

        # Make output directory
        output_path = Path("models")
        output_path.mkdir(parents=True, exist_ok=True)

        # Save model
        model_path = output_path / "model.joblib"
        joblib.dump(model, model_path)
        log.info(f"Model saved to: {model_path}")

        # Log model to MLflow
        mlflow.sklearn.log_model(model, "model")

        # Log metrics (placeholder - calculate actual metrics in production)
        mlflow.log_metric("train_completed", 1)

        log.info("Training completed successfully!")


if __name__ == "__main__":
    train()