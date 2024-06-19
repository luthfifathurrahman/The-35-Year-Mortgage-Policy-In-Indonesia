# Evaluating the 35-Year Mortgage Policy in Indonesia

## Business Understanding
1. What is the comparison between the number of households that own homes and those that do not?
2. What is the relationship between the number of houses sold in each Indonesian province and the provincial minimum wage?
3. What is the relationship between the number of houses sold in each Indonesian province and the population size?
4. What is the relationship between the number of houses sold in each Indonesian province and the number of households?
5. What is the relationship between the number of houses sold in each Indonesian province and the number of households without homes?
6. How significant is the disparity in the ability to purchase homes across different regions in Indonesia?
7. What is the regional impact on mortgage loan duration?
8. Is the 35-year mortgage policy appropriate?

## Data Understanding
### Data Source:
  - Real Estate Marketplace in Indonesia
  - Badan Pusat Statistik Indonesia
  - Otoritas Jasa Keuangan Indonesia
  - Kementerian Ketenagakerjaan Indonesia
  - Goodstats
    
### There are four datasets, which are:
  - House data: 7 columns and 141,721 rows
    - judul: Title of the house listing in the marketplace.
    - lokasi: Information about the location of the house.
    - kamar_tidur: Number of bedrooms in the house.
    - kamar_mandi: Number of bathrooms in the house.
    - luas_tanah: Land area of the house.
    - luas_bangunan: Building area of the house.
    - harga: Selling price of the house.
      
  - Population Data: 2 columns and 38 rows
    - provinsi:the names of the provinces in Indonesia.
    - jumlah_penduduk: the population of each respective province.
      
  - Household Data:
    - Total household data: 2 columns and 34 rows
      - provinsi: the names of the provinces in Indonesia.
      - total: the total number of households in each province.
    - Homeownership status data: 5 columns and 34 rows
      - provinsi: the names of the provinces in Indonesia.
      - kontrak_sewa: the number of households renting their homes in each province.
      - bebas_sewa: the number of households living rent-free in each province.
      - lainnya: the number of households with other homeownership statuses in each province.
      - total: the total number of households.
        
  - Provincial Minimum Wage Data: 3 columns and 37 rows
    - provinsi: the names of the provinces.
    - upah minimum provinsi: the minimum wage of each respective province.

## Data Preparation
-	Python Programming Language
-	Packages: selenium, pandas, streamlit, altair, numpy, scipy.stats, regex, pathlib, sklearn.cluster

## Data Cleansing
### House Data:
  - Rearrange column names
  - Eliminate duplicated data entries
  - Remove missing values
  - Exclude rows with '0' in columns "bedrooms", "bathrooms", "building_area", and "land_area"
  - Remove rows with "Contact agent for price" in the "price" column
  - Remove "Rp" and "." from the "price" column
  - Convert data type of "price" column to numeric
  - Create two new columns "district" and "city", populated from the "location" column
  - Modify values in "district" and "city" columns at row index 90975
  - Remove empty rows in "city" and "district" columns
  - Create a "province" column by mapping values from "city" and "district" columns
  - Delete "title" and "Location" columns
  - Sort columns in the order of 'district', 'city', 'province', 'bedrooms', 'bathrooms', 'land_area', 'building_area', 'price'
  - Save the modified dataframe as "cleaned_listing_data.csv"

### Population Data:
  - Convert data type of "population_amount" column to numeric
  - Save the modified dataframe as "cleaned_population_data.csv"

### Household Data:
  - Rename "total" column in total household data to "total_rt"
  - Rename "total" column in house ownership status data to "total_rt_no_house"
  - Remove numbers, dots, and spaces from the beginning of strings and capitalize the first letter, except for "DKI Jakarta" and "DI Yogyakarta" in the "province" column
  - Merge two tables: total household data and house ownership status data
  - Create "total_rt_have_house" column by subtracting "total_rt_no_house" from "total_rt"
  - Sort columns in the table as 'province', 'rental_contract', 'rent_free', 'other', 'total_rt_no_house', 'total_rt_have_house', 'total_rt'
  - Save the modified dataframe as "cleaned_rumah_tangga_data.csv"

### Provincial Minimum Wage Data:
  - Rename "provincial minimum wage" column to "ump"
  - Remove commas from values in the "ump" column
  - Rename "DI. Yogyakarta" to "DI Yogyakarta" in the "province" column
  - Add a new column "average_installment_payment" with a value of 1620000
  - Save the modified dataframe as "cleaned_ump_data.csv"

## Exploratory Data Analysis
#### 1. Perbandingan Jumlah Rumah Tangga Yang Memiliki Rumah Dan Tidak Memiliki Rumah

![Amount of Household](https://raw.githubusercontent.com/luthfifathurrahman/The-35-Year-Mortgage-Policy-In-Indonesia/main/image/amount_household.png)

#### 2. Korelasi Antara Rumah Tangga Yang Tidak Memiliki Rumah Dan Jumlah Rumah Yang Dijual Berdasarkan Provinsi

![Correlation Image](https://raw.githubusercontent.com/luthfifathurrahman/The-35-Year-Mortgage-Policy-In-Indonesia/main/image/correlation.png)

#### 3. Analisis Kesenjangan Kemampuan Membeli Rumah di Berbagai Wilayah Indonesia

![Correlation Image](https://raw.githubusercontent.com/luthfifathurrahman/The-35-Year-Mortgage-Policy-In-Indonesia/main/image/Analisis%20Kesenjangan%20Kemampuan%20Membeli%20Rumah%20di%20Berbagai%20Wilayah%20Indonesia.png)

#### 4. Clustering Upah Minimum Provinsi Menjadi 5 Kelompok

![Correlation Image](https://raw.githubusercontent.com/luthfifathurrahman/The-35-Year-Mortgage-Policy-In-Indonesia/main/image/clustering.png)

#### 3. Dampak Regional terhadap Durasi Pinjaman KPR

![Correlation Image](https://raw.githubusercontent.com/luthfifathurrahman/The-35-Year-Mortgage-Policy-In-Indonesia/main/image/Dampak%20Regional%20terhadap%20Durasi%20Pinjaman%20KPR.png)
