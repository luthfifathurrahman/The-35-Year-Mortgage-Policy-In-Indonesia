# Evaluating the 35-Year Mortgage Policy in Indonesia

## Web Scraping

### Overview

This directory contains Python scripts for web scraping various websites using the Selenium library. The purpose of these scripts is to extract specific data from external websites. The focus is on retrieving information such as the number of bedrooms, bathrooms, land area, built-up area, location, and price.

### Prerequisites

- Python programming language
- Selenium library

### Setup

1. Install Python: Make sure you have Python installed on your machine. If not, you can download it from [python.org](https://www.python.org/).

2. Install Selenium: You can install the Selenium library using the following command:
   ```bash
   pip install selenium
   ```

3. Download WebDriver Manager: Selenium requires a WebDriver to interact with the web browser. Download the appropriate WebDriver for your browser (e.g., ChromeDriver for Google Chrome) and ensure it is in your system's PATH.
   ```bash
   pip install webdriver-manager
   ```

### Code Details

The code in the script performs the following tasks:

- Logs the process during data extraction.
- Utilizes the Selenium library for web automation.
- Extracts data such as the number of bedrooms, bathrooms, land size, built-up area, location, and price from the target website.
- Stores the extracted data in a CSV file for further analysis.

### Confidentiality

Kindly be advised that the authentic scraped data and logs have been omitted from this repository to uphold confidentiality.

Should you have any queries or encounter any issues, do not hesitate to reach out to the proprietor of this repository.

Wishing you contented web scraping endeavors!

---

## Data Cleaning

### Overview
This repository contains scripts for cleaning three different datasets related to house listings, population data, and minimum provincial income per capita. Each cleaning process is detailed below.

### Prerequisites
- Python programming language
- Pandas and re library

### Setup
1. Install Python: Make sure you have Python installed on your machine. If not, you can download it from [python.org](https://www.python.org/).
2. Required libraries: pandas, re
   - Install Pandas: You can install the pandas library using the following command:
     ```bash
     pip install pandas
     ```
   - Installing re (regular expression library) - re is actually part of Python's standard library, so you don't need to install it separately.

### Code Details

#### 1. Cleaning House Listing Data (`cleaning_listing_data.py`)
```python
# Initialize library
import pandas as pd
import re

# ... (code for reading and basic information display)

# Tidying up the column names in the dataframe.
df.columns = [col.strip() for col in df.columns]

# Remove duplicate data
df_no_duplicate = df.drop_duplicates()

# Showing missing values
missing_value = df_no_duplicate[df_no_duplicate.isnull().any(axis=1)]

# ... (code for various cleaning steps)

# Saving to CSV file as 'cleaned_listing_data.csv'
df_clean.to_csv('cleaned_listing_data.csv', index=False)
```

#### 2. Cleaning Population Data (`cleaning_population_data.py`)
```python
# Initialize library
import pandas as pd

# ... (code for reading and basic information display)

# Remove "jiwa" and "." from each value in the "jumlah_penduduk" column
jumlah_penduduk['jumlah_penduduk'] = jumlah_penduduk['jumlah_penduduk'].str.replace('jiwa', '').str.replace('.', '')

# Convert the data type of the "jumlah_penduduk" column to numeric
jumlah_penduduk['jumlah_penduduk'] = pd.to_numeric(jumlah_penduduk['jumlah_penduduk'])

# Saving to CSV file as 'cleaned_population_data.csv'
jumlah_penduduk.to_csv('cleaned_population_data.csv', index=False)
```

#### 3. Cleaning Provincial Income Data (`cleaning_income_data.py`)
```python
# Initialize library
import pandas as pd

# ... (code for reading and basic information display)

# Altering column names using the rename method.
df = df.rename(columns={'upah minimum provinsi': 'ump'})

# Adding a new column with identical values (value=1620000)
df['rata_rata_angsuran'] = 1620000

# Saving to CSV file as 'cleaned_income_province.csv'
df.to_csv('cleaned_income_province.csv', index=False)
```

### Confidentiality
Kindly be advised that the authentic data has not been disclosed within this repository to preserve confidentiality. I will only distribute the data post the cleansing process.

Should you have inquiries or encounter any challenges, do not hesitate to reach out to the proprietor of the repository.

Wishing you a delightful experience in your data cleaning endeavors!

---

## Datasets Directory

### Overview
This directory contains a set of cleaned datasets to ensure the confidentiality and privacy of the data. The datasets have undergone a cleaning process to remove any sensitive information and to comply with data protection standards.

### Dataset Files
1. **cleaned_income_province.csv**
   - Description: This dataset provides cleaned minimum income data at the provincial level in 2024.
   - Columns:
     - provinsi
     - ump
     - rata_rata_angsuran

2. **cleaned_listing_data.csv**
   - Description: The cleaned version of the listing data, with sensitive information removed.
   - Columns:
     - kecamatan
     - kota
     - provinsi
     - kamar_tidur
     - kamar_mandi
     - luas_tanah
     - luas_bangunan
     - harga

3. **cleaned_population_data.csv**
   - Description: Cleaned population data.
   - Columns:
     - provinsi
     - jumlah_penduduk

### Usage
These datasets are ready for analysis and can be used for research, statistical analysis, and other purposes. Please note that the data has been processed to protect the privacy of individuals and comply with data protection regulations.

### Data Cleaning Process
The cleaning process involved removing or anonymizing any information that could potentially identify individuals. Steps taken include:
- Removal of personally identifiable information (PII).
- Aggregation or anonymization of specific data fields.
- Ensuring compliance with relevant privacy regulations.

### Disclaimer
While efforts have been made to thoroughly clean and protect the data, users are encouraged to exercise caution and adhere to ethical guidelines when using this dataset. It is the responsibility of the user to ensure compliance with any applicable data protection laws and regulations.

### License
Please refer to the license file in this directory for information regarding the usage and distribution of these cleaned datasets.

---

## Image Directory

This directory contains several images that can be used in your project. Here is the list of images along with their sources:

1. **Bank.png**
   - Source: [Flaticon - Bank](https://www.flaticon.com/free-icon/bank_2830284?term=bank&page=1&position=1&origin=search&related_id=2830284)
   - File Name: bank.png

2. **Team.png**
   - Source: [Flaticon - Team](https://www.flaticon.com/free-icon/team_476761?related_id=476863&origin=search)
   - File Name: team.png

3. **Rumah.jpg**
   - Source: [Pexels - Aerial Photography of a House](https://www.pexels.com/id-id/foto/fotografi-udara-rumah-3392324/)
   - File Name: rumah.jpg

Feel free to use these images according to the needs of your project. Don't forget to check and comply with the licensing rules from the image sources.

## Machine Learning

### Overview
This repository contains a machine learning project focused on predicting housing prices using the Random Forest Regressor algorithm. The dataset used for this project is sourced from [cleaned_listing_data.csv](https://raw.githubusercontent.com/luthfifathurrahman/Evaluating-the-Effectiveness-of-the-35-Year-Mortgage-Policy-and-Predicting-Housing-Prices/main/datasets/cleaned_listing_data.csv).

### Directory Structure
- `machine_learning.py`: Python script containing the machine learning model implementation.

### Libraries Used
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import pickle
import time
```

### Installation
Before running the script, make sure to install the required libraries using:
```bash
pip install pandas numpy scikit-learn pickle5
```

### Data Cleaning
Before model creation, the dataset undergoes a cleaning process, including:
-

 Removal of specific values.
- Dropping the "kecamatan" column.

### Data Encoding
Encoding is performed on the "provinsi" and "kota" columns to prepare categorical data for model training.

### Feature and Label Separation
The dataset is split into features and labels for model training.

### Model Creation
The Random Forest Regressor algorithm is utilized to create the predictive model.

### Model Evaluation Metrics
The model is evaluated using the following metrics:
- Mean Squared Error (MSE)
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Percentage Error (MAPE)
- R-squared (R2)

### Model Saving
The trained model is saved using the Pickle library and named `rf_regressor_model.pkl`.

### Model Storage
Due to GitHub's size limitations, the model file is stored on Dropbox. You can download it [here](https://www.dropbox.com/scl/fi/g6wfirgh9ix4uvbovt6ms/rf_regressor_model.pkl?rlkey=rr6zrln6jk9tsu8m4qtk5wu5r&dl=1).

Feel free to explore the code and dataset to understand the machine learning process used in predicting housing prices. If you have any questions or suggestions, please reach out!

---

## Streamlit App

### Overview

This directory contains the Streamlit app (`app.py`) for visualizing and analyzing the results of the machine learning model.

### Analysis Sections

#### 1. Korelasi Antara Populasi Dan Jumlah Rumah Yang Dijual Berdasarkan Provinsi

![Correlation Image](https://raw.githubusercontent.com/luthfifathurrahman/Evaluating-the-35-Year-Mortgage-Policy-in-Indonesia/main/image/correlation.svg)

#### 2. Analisis Kesenjangan Kemampuan Membeli Rumah di Berbagai Wilayah Indonesia

![Correlation Image](https://raw.githubusercontent.com/luthfifathurrahman/Evaluating-the-35-Year-Mortgage-Policy-in-Indonesia/main/image/minimum_wage.svg)


#### 3. Dampak Regional terhadap Durasi Pinjaman KPR

![Correlation Image](https://raw.githubusercontent.com/luthfifathurrahman/Evaluating-the-35-Year-Mortgage-Policy-in-Indonesia/main/image/mortgage.svg)

### Requirements

The necessary dependencies for running the app are listed in the `requirements.txt` file.

```
streamlit==1.31.1
pandas==2.2.0
altair==5.2.0
numpy==1.26.4
dill==0.3.8
scikit-learn==1.4.1.post1
requests==2.31.0
```

Feel free to explore the app and reach out for any questions or feedback!
