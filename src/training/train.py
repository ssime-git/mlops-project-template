"""
Training module.
Run via: python -m training train
"""
import argparse
import joblib


def main():
    parser = argparse.ArgumentParser(description="Train model")
    parser.add_argument("--data", default="data/processed/train.csv", help="Training data path")
    parser.add_argument("--output", default="models/model.joblib", help="Model output path")
    args = parser.parse_args()

    print(f"Training model from {args.data}")
    # TODO: Implement actual training
    # model = RandomForestClassifier()
    # model.fit(X, y)
    # joblib.dump(model, args.output)


if __name__ == "__main__":
    main()