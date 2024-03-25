# Initialize library
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import pickle
import time
from pathlib import Path


# --- CONFIG ---
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.02f' % x)

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
previous_dir = current_dir.parent

# --- CREATE A DATAFRAME ---
cleaned_listing_data = previous_dir / "datasets" / "cleaned_listing_data.csv"
df_house = pd.read_csv(cleaned_listing_data)

# --- MACHINE LEARNING
df_house_baru = df_house.copy()

# Removing houses that have a price under 50 million
df_house_baru = df_house_baru[df_house_baru['harga'] >= 50000000]

# Drop columns
df_house_baru = df_house_baru.drop(['kecamatan'], axis=1)

# Performing one-hot encoding
df_house_baru = pd.get_dummies(df_house_baru, columns=['provinsi', 'kota'])

# Performing scaler
scaler = StandardScaler()
df_house_baru[['kamar_tidur', 'kamar_mandi', 'luas_tanah', 'luas_bangunan']] = scaler.fit_transform(df_house_baru[['kamar_tidur', 'kamar_mandi', 'luas_tanah', 'luas_bangunan']])

# Separating Features and Labels
df_machine_learning = df_house_baru.copy()
X = df_machine_learning.drop('harga', axis=1)
y = df_machine_learning['harga']

# Record the start time
start_time = time.time()

# Create the model
rf_regressor_model = RandomForestRegressor(random_state=28)

# Preparing Training, Testing, And Validating Dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the model on training data
rf_regressor_model.fit(X_train, y_train)

# Make predictions
y_train_pred = rf_regressor_model.predict(X_train)
y_test_pred = rf_regressor_model.predict(X_test)

# Evaluate the model
train_mse = mean_squared_error(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_rmse = np.sqrt(train_mse)
train_mape = mean_absolute_percentage_error(y_train, y_train_pred)
train_r2 = r2_score(y_train, y_train_pred)

test_mse = mean_squared_error(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_rmse = np.sqrt(test_mse)
test_mape = mean_absolute_percentage_error(y_test, y_test_pred)
test_r2 = r2_score(y_test, y_test_pred)

# Display evaluation results
print("\nTrain Mean Squared Error (MSE): {:.2f}".format(train_mse))
print("Test Mean Squared Error (MSE): {:.2f}".format(test_mse))
print("Train Mean Absolute Error (MAE): {:.2f}".format(train_mae))
print("Test Mean Absolute Error (MAE): {:.2f}".format(test_mae))
print("Train Root Mean Squared Error (RMSE): {:.2f}".format(train_rmse))
print("Test Root Mean Squared Error (RMSE): {:.2f}".format(test_rmse))
print("Train Mean Absolute Percentage Error (MAPE): {:.2f}".format(train_mape))
print("Test Mean Absolute Percentage Error (MAPE): {:.2f}".format(test_mape))
print("Train R-squared (R2): {:.2f}".format(train_r2))
print("Test R-squared (R2): {:.2f} \n".format(test_r2))

# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the runtime
print("Execution time: {:.2f} seconds".format(end_time - start_time))

# Save the trained model using pickle
model_filename = 'rf_regressor_model.pkl'
with open(model_filename, 'wb') as file:
    pickle.dump(rf_regressor_model, file)

print(f"Model saved as {model_filename}")
