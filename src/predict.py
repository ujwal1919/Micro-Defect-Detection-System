from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


def load_and_train() -> tuple[LogisticRegression, list[str]]:
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "bookss.csv"

    df = pd.read_csv(data_path)
    x = df.drop(columns=["Result"], axis=1)
    y = df["Result"]

    model = LogisticRegression(max_iter=1000)
    model.fit(x, y)
    return model, x.columns.tolist()


def main() -> None:
    model, feature_columns = load_and_train()

    input_data = (
        0.0307,
        0.0523,
        0.0653,
        0.0521,
        0.0612,
        0.1021,
        0.1134,
        0.1522,
        0.1983,
        0.2331,
        0.2714,
        0.2894,
        0.3312,
        0.4121,
        0.5142,
        0.6113,
        0.6899,
        0.7221,
        0.7114,
        0.6552,
        0.5124,
        0.4251,
        0.3822,
        0.3204,
        0.2921,
        0.2567,
        0.2213,
        0.1908,
        0.1775,
        0.1561,
        0.1342,
        0.1225,
        0.1106,
        0.0952,
        0.0834,
        0.0721,
        0.0618,
    )

    input_array = np.asarray(input_data, dtype=float).reshape(1, -1)
    input_df = pd.DataFrame(input_array, columns=feature_columns)
    prediction = model.predict(input_df)[0]

    label = "Rock" if prediction == "R" else "Mine"
    print(f"Predicted class: {prediction}")
    print(f"Prediction label: {label}")


if __name__ == "__main__":
    main()

