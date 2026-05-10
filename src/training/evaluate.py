"""
Evaluation module.
Run via: python -m training evaluate
"""
import argparse
import json
import joblib


def main():
    parser = argparse.ArgumentParser(description="Evaluate model")
    parser.add_argument("--model", default="models/model.joblib", help="Model path")
    parser.add_argument("--data", default="data/processed/train.csv", help="Test data path")
    parser.add_argument("--metrics", default="metrics/eval_metrics.json", help="Metrics output path")
    args = parser.parse_args()

    print(f"Evaluating model {args.model} on {args.data}")
    # TODO: Implement actual evaluation
    # model = joblib.load(args.model)
    # metrics = {"accuracy": 0.95, "precision": 0.93, "recall": 0.91}
    # with open(args.metrics, "w") as f:
    #     json.dump(metrics, f)


if __name__ == "__main__":
    main()