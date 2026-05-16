"""
Evaluation module.
Run via: python -m training evaluate
Or with custom config: python -m training evaluate model.path=models/custom_model.joblib
"""
import json
import logging
from pathlib import Path

import hydra
import joblib
import mlflow
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from sklearn.metrics import accuracy_score, precision_score, recall_score

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="configs", config_name="evaluate")
def evaluate(cfg: DictConfig):
    """Evaluate a model using Hydra configuration."""
    # Log the configuration
    log.info(f"Evaluation configuration:\n{OmegaConf.to_yaml(cfg)}")

    # Start MLflow run
    mlflow.set_experiment(cfg.mlflow.experiment_name)
    with mlflow.start_run(run_name="evaluation"):
        # Load model
        model_path = Path(cfg.model.path)
        if not model_path.exists():
            log.error(f"Model not found: {model_path}")
            return

        log.info(f"Loading model from: {model_path}")
        model = joblib.load(model_path)

        # Load test data
        test_path = Path(cfg.data.test_path)
        if not test_path.exists():
            log.warning(f"Test data not found: {test_path}, using train data instead")
            test_path = Path(cfg.data.train_path)

        df = pd.read_csv(test_path)
        log.info(f"Loaded test data: {df.shape}")

        # Separate features and target
        if "target" not in df.columns:
            log.warning("No 'target' column found. Using last column as target.")
            X = df.iloc[:, :-1]
            y = df.iloc[:, -1]
        else:
            X = df.drop(columns=["target"])
            y = df["target"]

        # Make predictions
        y_pred = model.predict(X)

        # Calculate metrics (placeholder - adapt to your problem type)
        metrics = {}
        try:
            metrics["accuracy"] = accuracy_score(y, y_pred)
        except Exception as e:
            log.warning(f"Could not calculate accuracy: {e}")

        try:
            metrics["precision"] = precision_score(y, y_pred, average="weighted", zero_division=0)
        except Exception as e:
            log.warning(f"Could not calculate precision: {e}")

        try:
            metrics["recall"] = recall_score(y, y_pred, average="weighted", zero_division=0)
        except Exception as e:
            log.warning(f"Could not calculate recall: {e}")

        # Log metrics
        log.info(f"Evaluation metrics: {metrics}")
        for metric_name, value in metrics.items():
            mlflow.log_metric(metric_name, value)

        # Save metrics to file
        output_path = Path(cfg.metrics.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(metrics, f, indent=2)

        log.info(f"Metrics saved to: {output_path}")
        log.info("Evaluation completed successfully!")


if __name__ == "__main__":
    evaluate()