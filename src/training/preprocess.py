"""
Preprocessing module.
Run via: python -m training preprocess
Or with custom config: python -m training preprocess preprocessing.test_size=0.3
"""

import logging
from pathlib import Path

import hydra
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="configs", config_name="preprocess")
def preprocess(cfg: DictConfig):
    """Preprocess data using Hydra configuration."""
    # Log the configuration
    log.info(f"Preprocessing configuration:\n{OmegaConf.to_yaml(cfg)}")

    # Load raw data
    raw_path = Path(cfg.data.raw_path)
    if not raw_path.exists():
        log.error(f"Raw data not found: {raw_path}")
        return

    log.info(f"Loading raw data from: {raw_path}")
    df = pd.read_csv(raw_path)
    log.info(f"Loaded data: {df.shape}")

    # Handle missing values based on config
    handle_method = cfg.preprocessing.handle_missing
    if handle_method == "drop":
        df = df.dropna()
        log.info("Dropped rows with missing values")
    elif handle_method == "mean":
        df = df.fillna(df.mean(numeric_only=True))
        log.info("Filled missing values with mean")
    elif handle_method == "median":
        df = df.fillna(df.median(numeric_only=True))
        log.info("Filled missing values with median")

    # Scale features if enabled
    if cfg.preprocessing.scale_features:
        numeric_cols = df.select_dtypes(include=["number"]).columns
        if len(numeric_cols) > 0:
            scaler = StandardScaler()
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
            log.info(f"Scaled {len(numeric_cols)} numeric columns")

    # Split data
    test_size = cfg.preprocessing.test_size
    random_state = cfg.preprocessing.random_state

    if "target" in df.columns:
        x = df.drop(columns=["target"])
        y = df["target"]
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=test_size, random_state=random_state
        )

        # Create processed directory
        processed_path = Path(cfg.data.processed_path)
        processed_path.parent.mkdir(parents=True, exist_ok=True)

        # Save train and test sets
        train_df = pd.concat([x_train, y_train], axis=1)
        test_df = pd.concat([x_test, y_test], axis=1)

        # For simplicity, save as single file (in production, save separately)
        train_df.to_csv(processed_path, index=False)

        # Also create test file
        test_path = processed_path.parent / "test.csv"
        test_df.to_csv(test_path, index=False)

        log.info(f"Saved processed data to: {processed_path}")
        log.info(f"Saved test data to: {test_path}")
        log.info(f"Train size: {len(train_df)}, Test size: {len(test_df)}")
    else:
        log.warning("No 'target' column found. Saving processed data without split.")
        processed_path = Path(cfg.data.processed_path)
        processed_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(processed_path, index=False)
        log.info(f"Saved processed data to: {processed_path}")

    log.info("Preprocessing completed successfully!")


if __name__ == "__main__":
    preprocess()
