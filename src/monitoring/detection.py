"""
Drift Detection module.
Run via: python -m monitoring.detection
Or with custom config: python -m monitoring.detection drift.threshold=0.3
"""
import logging
from pathlib import Path

import hydra
import pandas as pd
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.report import Report
from omegaconf import DictConfig, OmegaConf

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="configs", config_name="drift")
def detect_drift(cfg: DictConfig):
    """Detect data drift using Hydra configuration."""
    # Log the configuration
    log.info(f"Drift detection configuration:\n{OmegaConf.to_yaml(cfg)}")

    # Load reference and current data
    reference_path = Path(cfg.data.reference_path)
    current_path = Path(cfg.data.current_path)

    if not reference_path.exists():
        log.error(f"Reference data not found: {reference_path}")
        return

    if not current_path.exists():
        log.error(f"Current data not found: {current_path}")
        return

    log.info(f"Loading reference data from: {reference_path}")
    reference = pd.read_csv(reference_path)

    log.info(f"Loading current data from: {current_path}")
    current = pd.read_csv(current_path)

    log.info(f"Reference shape: {reference.shape}, Current shape: {current.shape}")

    # Build Evidently report
    metrics = []
    if "data_drift" in cfg.evidently.metrics or "data_dift" in cfg.evidently.metrics:
        metrics.append(DataDriftPreset())
    if "target_drift" in cfg.evidently.metrics:
        metrics.append(TargetDriftPreset())

    if not metrics:
        metrics.append(DataDriftPreset())

    report = Report(metrics=metrics)

    # Run drift detection
    log.info("Running drift detection...")
    report.run(reference_data=reference, current_data=current)

    # Save report
    output_path = Path(cfg.drift.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report.save_html(output_path)
    log.info(f"Drift report saved to: {output_path}")

    # Get drift summary
    drift_result = report.as_dict()
    if "metrics" in drift_result:
        for metric in drift_result["metrics"]:
            if "data_drift" in metric:
                drift_score = metric["data_drift"].get("drift_share", 0)
                log.info(f"Data drift score: {drift_score:.2%}")
                if drift_score > cfg.drift.threshold:
                    log.warning(f"DRIFT DETECTED! Drift score {drift_score:.2%} exceeds threshold {cfg.drift.threshold:.2%}")
                else:
                    log.info("No significant drift detected.")

    log.info("Drift detection completed successfully!")


if __name__ == "__main__":
    detect_drift()