# Rock vs Mine Prediction

This mini machine learning project predicts whether a sonar signal is reflected from a **Rock (R)** or a **Mine (M)**.

## Project Structure

- `bookss.csv` - Dataset used for training and evaluation
- `src/train.py` - Train and evaluate a Logistic Regression model
- `src/predict.py` - Predict class for one custom sonar sample
- `requirements.txt` - Python dependencies

## Setup

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
```

2. Activate it:

- Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Train and Evaluate

Run:

```bash
python src/train.py
```

This prints:
- train/test split shape
- training accuracy
- test accuracy

## Run a Custom Prediction

Run:

```bash
python src/predict.py
```

By default, it uses one sample from the dataset format and prints:
- predicted class
- human-readable label (Rock or Mine)

## Notes

- The dataset target column is expected as `Result` with values `R` and `M`.
- Random seed is fixed for reproducible split.

