# Initialize library
import pandas as pd
import re
from pathlib import Path

# Set the maximum number of rows and columns to be displayed
pd.set_option('display.max_columns', None)

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
previous_dir = current_dir.parent

# Create a DataFrame
listing_data_path = current_dir / "listing_data.csv"
df = pd.read_csv(listing_data_path, delimiter=';')

# Viewing the number of columns, rows, missing values, and data types in each column.
print(df.info())

# Tidying up the column names in the dataframe.
df.columns = [col.strip() for col in df.columns]
print(df.info())

# Remove duplicate data
df_no_duplicate = df.drop_duplicates()
print(df_no_duplicate.info())

# Showing missing values
missing_value = df_no_duplicate[df_no_duplicate.isnull().any(axis=1)]
print(missing_value)

# Handling missing values by eliminating rows that contain them.
df_no_missing_value = df_no_duplicate.dropna()
print(df_no_missing_value.info())

# Remove rows with a value of 0 in any of the mentioned columns
df_no_zero = df_no_missing_value.loc[~((df_no_missing_value['kamar_tidur'] == 0)
                                       | (df_no_missing_value['kamar_mandi'] == 0)
                                       | (df_no_missing_value['luas_bangunan'] == 0)
                                       | (df_no_missing_value['luas_tanah'] == 0))]
print(df_no_zero.info())

# Remove rows with a value of "Kontak agen untuk harga" in "harga" column
df_with_price = df_no_zero.loc[df_no_zero['harga'] != 'Kontak agen untuk harga']
print(df_with_price.info())

# Remove "Rp" and "." from each value in the "harga" column
df_price_format = df_with_price.copy()
df_price_format['harga'] = df_price_format['harga'].str.replace('Rp', '').str.replace('.', '')

# Convert the data type of the "harga" column to numeric
df_price_format['harga'] = pd.to_numeric(df_price_format['harga'])
print(df_price_format.info())

# Creating two new columns for "kecamatan" and "kota"
df_kota_kecamatan = df_price_format.copy()
df_kota_kecamatan['kecamatan'] = df_kota_kecamatan['lokasi'].apply(
    lambda x: re.findall(r'([^,]+),', x)[0] if re.findall(r'([^,]+),', x) else '')
df_kota_kecamatan['kota'] = df_kota_kecamatan['lokasi'].apply(
    lambda x: re.findall(r',\s*([^,]+)', x)[0] if re.findall(r',\s*([^,]+)', x) else '')
print(df_kota_kecamatan.info())

# Modifying the value in the row with index 90975
indeks_baris_yang_diubah = 90975
nilai_baru_kecamatan = 'Lubuk Pakam'
nilai_baru_kota = 'Deli Serdang'

# Modifying the value in a specific row
df_kota_kecamatan.loc[indeks_baris_yang_diubah, 'kecamatan'] = nilai_baru_kecamatan
df_kota_kecamatan.loc[indeks_baris_yang_diubah, 'kota'] = nilai_baru_kota

# Eliminate rows with an empty value ("") in any of the specified columns
df_no_kota_kecamatan = df_kota_kecamatan.loc[~((df_kota_kecamatan['kota'] == "")
                                               | (df_kota_kecamatan['kecamatan'] == ""))]

# Creating a mapping between cities and provinces
mapping = {
    'Aceh': ['Banda Aceh', 'Aceh Besar', 'Aceh Singkil', 'Langsa', 'Aceh Tengah', 'Aceh Barat', 'Aceh Barat Daya',
             'Nagan Raya'],
    'Bali': ['Denpasar', 'Tabanan', 'Badung', 'Gianyar', 'Buleleng', 'Karangasem', 'Klungkung', 'Jembrana', 'Bangli'],
    'Kepulauan Bangka Belitung': ['Pangkal Pinang', 'Bangka'],
    'Banten': ['Tangerang', 'Cilegon', 'Tangerang Selatan', 'Pandeglang', 'Serang', 'Lebak'],
    'Bengkulu': ['Bengkulu Utara', 'Bengkulu', 'Bengkulu Selatan', 'Rejang Lebong', 'Bengkulu Tengah', 'Kaur',
                 'Muko-Muko'],
    'Jawa Tengah': ['Batang', 'Sragen', 'Wonogiri', 'Brebes', 'Pekalongan', 'Semarang', 'Solo', 'Boyolali', 'Salatiga',
                    'Banyumas', 'Klaten', 'Sukoharjo', 'Tegal', 'Karanganyar', 'Magelang', 'Purworejo'],
    'Kalimantan Tengah': ['Palangka Raya', 'Kotawaringin Barat'],
    'Sulawesi Tengah': ['Palu', 'Toli-Toli', 'Sigi'],
    'Jawa Timur': ['Banyuwangi', 'Ponorogo', 'Nganjuk', 'Surabaya', 'Malang', 'Batu', 'Kediri', 'Jember', 'Sidoarjo',
                   'Mojokerto', 'Gresik', 'Pasuruan', 'Lamongan', 'Madiun', 'Jombang'],
    'Kalimantan Timur': ['Penajam Paser Utara', 'Balikpapan', 'Samarinda', 'Panajam Paser Utara', 'Bontang', 'Paser'],
    'Kalimantan Utara': ['Tarakan'],
    'Nusa Tenggara Timur': ['Manggarai Barat', 'Kupang', 'Sikka'],
    'Gorontalo': ['Gorontalo'],
    'DKI Jakarta': ['Kepulauan Seribu', 'Jakarta Selatan', 'Jakarta Barat', 'Jakarta Timur', 'Jakarta Pusat',
                'Jakarta Utara'],
    'Jambi': ['Jambi', 'Muaro Jambi', 'Bungo'],
    'Lampung': ['Lampung Utara', 'Bandar Lampung', 'Lampung Selatan', 'Metro', 'Pesawaran', 'Pringsewu',
                'Lampung Tengah', 'Tulang Bawang', 'Way Kanan'],
    'Maluku Utara': ['Ternate'],
    'Sulawesi Utara': ['Tomohon', 'Manado', 'Minahasa Utara', 'Minahasa', 'Minahasa Selatan'],
    'Sumatera Utara': ['Medan', 'Deli Serdang', 'Binjai', 'Pematang Siantar', 'Tebing Tinggi', 'Langkat',
                       'Serdang Bedagai', 'Karo', 'Asahan', 'Toba Samosir', 'Padang Sidempuan', 'Simalungun'],
    'Papua': ['Jayapura', 'Paniai', 'Mimika'],
    'Riau': ['Pekanbaru', 'Kampar', 'Dumai', 'Bengkalis', 'Siak'],
    'Kepulauan Riau': ['Batam', 'Tanjung Pinang', 'Bintan', 'Karimun', 'Natuna', 'Kepulauan Anambas Kab.'],
    'Sulawesi Tenggara': ['Kendari'],
    'Kalimantan Selatan': ['Banjarmasin', 'Banjarbaru', 'Banjar', 'Tabalong', 'Tanah Laut', 'Barito Kuala',
                           'Hulu Sungai Selatan'],
    'Sulawesi Selatan': ['Makassar', 'Pare-Pare', 'Maros', 'Gowa', 'Takalar', 'Pinrang'],
    'Sumatera Selatan': ['Prabumulih', 'Ogan Komering Ulu Timur', 'Palembang', 'Banyuasin', 'Prambulih', 'Ogan Ilir',
                         'Muara Enim', 'Lubuk Linggau', 'Musi Banyuasin', 'Pagar Alam'],
    'Jawa Barat': ['Subang', 'Majalengka', 'Ciamis', 'Garut', 'Tasikmalaya', 'Kuningan', 'Bandung', 'Bogor', 'Bekasi',
                   'Cirebon', 'Karawang', 'Depok', 'Purwakarta', 'Cianjur', 'Cimahi', 'West Bandung', 'Sumedang',
                   'Sukabumi'],
    'Kalimantan Barat': ['Singkawang', 'Sintang', 'Pontianak', 'Singkawan', 'Ketapang', 'SIntang', 'Kubu Raya Kab.',
                         'Kayong Utara Kab.'],
    'Nusa Tenggara Barat': ['Mataram', 'Lombok Barat', 'Lombok Tengah', 'North Lombok', 'Lombok Utara Kab.'],
    'Papua Barat': ['Sorong'],
    'Sumatera Barat': ['Padang', 'Bukittinggi', 'Padang Pariaman', 'Payakumbuh', 'Solok', 'Dharmasraya',
                       'Pasaman Barat'],
    'DI Yogyakarta': ['Yogyakarta', 'Kulon Progo', 'Sleman', 'Gunung Kidul', 'Bantul'],
}


# Function to find the province based on the city
def cari_provinsi(kota):
    """This function categorizes the city into its respective province."""
    for provinsi, daftar_kota in mapping.items():
        if kota in daftar_kota:
            return provinsi
    return None

# Creating a new column "province" using the function
df_provinsi = df_no_kota_kecamatan.copy()
df_provinsi['provinsi'] = df_provinsi['kota'].map(cari_provinsi)
print(df_provinsi.info())

# Deleting multiple columns at once
kolom_yang_dihapus = ['judul', 'lokasi']
df_provinsi = df_provinsi.drop(kolom_yang_dihapus, axis=1)
print(df_provinsi.info())

# Sorting the order of columns
df_clean = df_provinsi.copy()
kolom_urut_baru = ['kecamatan', 'kota', 'provinsi', 'kamar_tidur', 'kamar_mandi', 'luas_tanah', 'luas_bangunan',
                   'harga']
df_clean = df_clean[kolom_urut_baru]
df_clean['luas_tanah'] = df_clean['luas_tanah'].astype(int)
df_clean['luas_bangunan'] = df_clean['luas_bangunan'].astype(int)

print(df_clean.info())
print(df_clean)

# Saving to CSV file
output_dir = previous_dir / "datasets"
cleaned_listing_data_path = output_dir / "cleaned_listing_data.csv"
df_clean.to_csv(cleaned_listing_data_path, index=False)
