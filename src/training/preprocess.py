"""
Preprocessing module.
Run via: python -m training preprocess
"""
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Preprocess data")
    parser.add_argument("--input", default="data/raw/train.csv", help="Input data path")
    parser.add_argument("--output", default="data/processed/train.csv", help="Output data path")
    args = parser.parse_args()

    print(f"Preprocessing {args.input} -> {args.output}")
    # TODO: Implement actual preprocessing
    # df = pd.read_csv(args.input)
    # df.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()