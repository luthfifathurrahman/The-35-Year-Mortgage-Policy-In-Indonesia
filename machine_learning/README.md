# Machine Learning Directory

This directory contains Python scripts for machine learning tasks.

## Files

### 1. `clustering.py`

This script performs clustering using KMeans algorithm on income data.

#### Usage

```bash
python clustering.py
```

#### Description

- Reads income data from `datasets/cleaned_ump_data.csv`.
- Performs one-hot encoding on categorical feature 'provinsi'.
- Performs KMeans clustering with the specified number of clusters.
- Saves the clustering results to `datasets/cluster.csv`.

### 2. `machine_learning.py`

This script implements a Random Forest Regressor model for predicting house prices.

#### Usage

```bash
python machine_learning.py
```

#### Description

- Reads house listing data from `datasets/cleaned_listing_data.csv`.
- Cleans the data, removes houses with prices under 50 million, and performs one-hot encoding on categorical features.
- Splits the data into training and testing sets.
- Trains a Random Forest Regressor model on the training data.
- Evaluates the model's performance on both training and testing sets.
- Saves the trained model as `rf_regressor_model.pkl`.

## Trained Model

You can download the trained Random Forest Regressor model from [here](https://www.dropbox.com/scl/fi/g6wfirgh9ix4uvbovt6ms/rf_regressor_model.pkl?rlkey=rr6zrln6jk9tsu8m4qtk5wu5r&dl=0).
