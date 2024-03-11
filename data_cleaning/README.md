# Data Cleaning

## Overview
This repository contains scripts for cleaning three different datasets related to house listings, population data, and minimum provincial income per capita. Each cleaning process is detailed below.

## Prerequisites

- Python programming language
- Pandas and re library

## Setup
1. Install Python: Make sure you have Python installed on your machine. If not, you can download it from [python.org](https://www.python.org/).
2. Required libraries: pandas, re
   - Install Pandas: You can install the pandas library using the following command:
     
     ```bash
     pip install pandas
     ```
     
   - Installing re (regular expression library) - re is actually part of Python's standard library, so you don't need to install it separately.

## Code Details

### 1. Cleaning House Listing Data (`cleaning_listing_data.py`)
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

### 2. Cleaning Population Data (`cleaning_population_data.py`)
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

### 3. Cleaning Provincial Income Data (`cleaning_income_data.py`)
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

## Confidentiality
Kindly be advised that the authentic data has not been disclosed within this repository to preserve confidentiality.
I will only distribute the data post the cleansing process. 

Should you have inquiries or encounter any challenges, do not hesitate to reach out to the proprietor of the repository.

Wishing you a delightful experience in your data cleaning endeavors!
