from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "bookss.csv"

    df = pd.read_csv(data_path)

    if "Result" not in df.columns:
        raise ValueError("Expected target column 'Result' in dataset.")

    x = df.drop(columns=["Result"], axis=1)
    y = df["Result"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.1, stratify=y, random_state=1
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(x_train, y_train)

    x_train_pred = model.predict(x_train)
    train_accuracy = accuracy_score(y_train, x_train_pred)

    x_test_pred = model.predict(x_test)
    test_accuracy = accuracy_score(y_test, x_test_pred)

    print(f"Dataset shape: {df.shape}")
    print(f"Train shape: {x_train.shape}, Test shape: {x_test.shape}")
    print(f"Training accuracy: {train_accuracy:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")


if __name__ == "__main__":
    main()

