import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import dill
from scipy.stats import pearsonr
from pathlib import Path
from sklearn.cluster import KMeans

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
cleaned_listing_data = current_dir / "datasets" / "cleaned_listing_data.csv"
cleaned_population_data = current_dir / "datasets" / "cleaned_population_data.csv"
cleaned_income_province = current_dir / "datasets" / "cleaned_ump_data.csv"
cleaned_rumah_tangga = current_dir / "datasets" / "cleaned_rumah_tangga_data.csv"
cluster = current_dir / "datasets" / "cluster.csv"

# --- SET PAGE CONFIG ---
st.set_page_config(
    page_title="Apakah Kebijakan KPR 35 Tahun Sudah Tepat?",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


# --- CREATE A DATAFRAME ---
df_house = pd.read_csv(cleaned_listing_data)
df_population = pd.read_csv(cleaned_population_data)
df_income = pd.read_csv(cleaned_income_province)
df_rt = pd.read_csv(cleaned_rumah_tangga)
df_cluster = pd.read_csv(cluster)


# --- TITLE ---
st.markdown("<h1 style='text-align: center; font-size: 48px;'>Apakah Kebijakan KPR 35 Tahun Sudah Tepat?</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)



# --- IMAGE ---
house_image = "https://raw.githubusercontent.com/luthfifathurrahman/The-35-Year-Mortgage-Policy-In-Indonesia/main/image/rumah.jpg"
st.image(house_image, use_column_width=True, output_format='auto')
caption_style = "text-align: center; font-size: 18px;"
link = "https://www.pexels.com/id-id/foto/fotografi-udara-rumah-3392324/"

st.markdown(f"""
    <div>
        <p style="{caption_style}">
            Foto oleh <a href="{link}" style="color: #f5f5f5; text-decoration: none;">Tom Fisk</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)




# --- INTRODUCTION ---
st.markdown("""
    <div>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Kepemilikan rumah bukan hanya sekadar memenuhi kebutuhan dasar masyarakat, tetapi juga menjadi penanda kemajuan dan kesejahteraan suatu bangsa. Di Indonesia, sedang terjadi yang namanya fenomena backlog kepemilikan rumah<sup>[1]</sup>. Apa itu backlog kepemilikan rumah? Backlog kepemilikan rumah merujuk pada jumlah unit rumah atau properti yang belum dapat dimiliki oleh individu atau keluarga pada suatu periode waktu tertentu. Biasanya, backlog ini muncul ketika ada permintaan yang melebihi pasokan atau ketersediaan rumah. Backlog kepemilikan rumah di Indonesia sudah mencapai 11.84 juta rumah tangga<sup>[2]</sup> dan ini telah menjadi sorotan utama, menimbulkan tantangan signifikan dalam mencapai tujuan pemerataan akses perumahan.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# List of columns to sum
columns_to_sum = ['kontrak_sewa', 'bebas_sewa', 'lainnya', 'total_rt_no_house', 'total_rt_have_house', 'total_rt']

# Calculate the sum of each column and store the results in a dictionary
sum_values = {column: df_rt[column].sum() for column in columns_to_sum}

# Add 'provinsi' to the dictionary
sum_values['provinsi'] = 'Indonesia'

# Add a new row with the calculated sums
df_rt.loc[len(df_rt)] = sum_values

col_grafik1, col_grafik2, col_grafik3 = st.columns(3)
with col_grafik2:
    # Create a selectbox for 'provinsi'
    selected_provinsi = st.selectbox('', df_rt['provinsi'].unique(), index=df_rt['provinsi'].unique().tolist().index('Indonesia'))

    # Filter the DataFrame based on the selected 'provinsi'
    df_filtered = df_rt[df_rt['provinsi'] == selected_provinsi]

    # Create a DataFrame for the pie chart
    df_pie = pd.DataFrame({
        'category': ["Punya Rumah", "Tidak Punya Rumah"],
        'value': [df_filtered['total_rt_have_house'].sum(), df_filtered['total_rt_no_house'].sum()],
        'Location': [selected_provinsi, selected_provinsi],
        'Amount of Households': [df_filtered['total_rt_have_house'].sum(), df_filtered['total_rt_no_house'].sum()],
        'Rent a House': [None, df_filtered['kontrak_sewa'].sum()],
        'Free Rent': [None, df_filtered['bebas_sewa'].sum()],
        'Other': [None, df_filtered['lainnya'].sum()]
    })

    # Create a pie chart
    chart = alt.Chart(df_pie).mark_arc(innerRadius=50).encode(
        theta=alt.Theta('value:Q', sort='ascending'),
        color=alt.Color('category:N', scale=alt.Scale(domain=["Punya Rumah", "Tidak Punya Rumah"], range=['#2a9d8f', '#e76f51']), legend=alt.Legend(title=None, orient='top', labelFontSize=15)),
        tooltip=[
        alt.Tooltip('Location:N'),
        alt.Tooltip('Amount of Households:Q'),
        alt.Tooltip('Rent a House:Q'),
        alt.Tooltip('Free Rent:Q'),
        alt.Tooltip('Other:Q')
    ]
    ).properties(
        width=500,
        height=500
    )

    # Display the chart in Streamlit
    st.write("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True)
    st.write("</div>", unsafe_allow_html=True)
    
st.markdown("""
    <div>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Permasalahan ini semakin menarik perhatian seiring dengan rencana penambahan waktu tenor Kredit Pemilikan Rumah (KPR). KPR sendiri adalah kredit yang diberikan oleh bank atau lembaga keuangan lainnya kepada individu untuk membeli atau membangun rumah. Peminjam membayar kembali pinjaman tersebut dalam jangka waktu tertentu dengan suku bunga tertentu. Rencana penambahan tenor KPR ini hingga 35 tahun<sup>[3]</sup>, yang sebelumnya menurut OJK waktu maksimal tenor KPR itu umumnya 20 tahun<sup>[4]</sup>. Rencana KPR 35 tahun ini mucul menjadi solusi yang diusung untuk mengatasi kesulitan akses perumahan. Namun, pertanyaan mendasar pun muncul: Apakah kebijakan KPR 35 tahun sudah tepat? Untuk menjawabnya, report ini melakukan analisis mendalam terkait faktor-faktor yang mempengaruhi kepemilikan rumah di Indonesia.
        </p>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Berita tentang backlog kepemilikan rumah yang menggemparkan menjadi pemicu utama penyusunan report ini. Dengan memanfaatkan data statistik dan analisis, terinci beberapa aspek kunci yang memengaruhi tren kepemilikan rumah di Indonesia. Dengan fokus pada korelasi antara populasi dan penjualan rumah, analisis kesenjangan kemampuan membeli rumah di berbagai wilayah, dan dampak regional terhadap durasi pinjaman KPR, report ini berusaha menguraikan kompleksitas masalah tersebut.
        </p>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Melalui penelusuran yang teliti, report ini tidak hanya mencari jawaban terhadap kebijakan KPR 35 tahun, tetapi juga memberikan wawasan mendalam terkait tantangan nyata yang dihadapi oleh masyarakat dalam mencapai kepemilikan rumah di Indonesia. Dengan demikian, diharapkan report ini dapat memberikan kontribusi konstruktif bagi perencanaan kebijakan perumahan di masa depan.
        </p>       
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)




# --- Analisis Hubungan Jumlah Rumah yang Dijual di Setiap Provinsi Indonesia dengan Faktor-faktor Terkait ---
st.markdown("<h2 style='text-align: left; font-size: 44px;'>Analisis Hubungan Jumlah Rumah yang Dijual di Setiap Provinsi Indonesia dengan Beberapa Parameter Terkait</h2>", unsafe_allow_html=True)

# Amount of house in each province
province_amount_house = df_house.groupby('provinsi').agg(amount_house = ('provinsi','count'))

# Sorting by the 'amount_house' column in descending order
province_amount_house_sorted = province_amount_house.sort_values(by='amount_house', ascending=False)

# Merge df_population with province_amount_house based on the 'provinsi' column using an inner join
amount_population = pd.merge(province_amount_house, df_population, on='provinsi', how='inner')

# Sort the merged dataframe based on the 'amount_house' column in descending order
amount_population_sorted = amount_population.sort_values(by='amount_house', ascending=False)

# Merge amount_population_sorted with df_rt based on the 'provinsi' column using an inner join
df_rt_amount_house = pd.merge(amount_population_sorted, df_rt, on='provinsi', how='inner')
df_rt_amount_house = pd.merge(df_rt_amount_house, df_income, on='provinsi', how='inner')

# Transform the 'nilai_awal' column to base 10 logarithm
df_rt_amount_house['jumlah_penduduk_log'] = np.log10(df_rt_amount_house['jumlah_penduduk'])
df_rt_amount_house['amount_house_log'] = np.log10(df_rt_amount_house['amount_house'])
df_rt_amount_house['total_rt_log'] = np.log10(df_rt_amount_house['total_rt'])
df_rt_amount_house['total_rt_no_house_log'] = np.log10(df_rt_amount_house['total_rt_no_house'])
df_rt_amount_house['ump_log'] = np.log10(df_rt_amount_house['ump'])

# Create a selectbox with options A and B
option = st.selectbox('', ['Jumlah Populasi', "Jumlah Rumah Tangga", 'Jumlah Rumah Tangga Tidak Memiliki Rumah', 'Upah Minimum Provinsi'], index=3)

if option == "Jumlah Populasi":
    # Calculate the correlation between the logarithmic population and amount of houses
    correlation_population, p_value_population = pearsonr(df_rt_amount_house['jumlah_penduduk_log'], df_rt_amount_house['amount_house_log'])

    # Create a scatter plot using Altair and replace the marks with text
    text_chart = alt.Chart(df_rt_amount_house).mark_text().encode(
        x=alt.X('amount_house_log:Q', title='Amount of Houses', axis=alt.Axis(labels=False, titleFontSize=20)),
        y=alt.Y('jumlah_penduduk_log:Q', scale=alt.Scale(domain=[5.5, 8]), title='Population', axis=alt.Axis(labels=False, titleFontSize=20)),
        text='provinsi:N',  # Use values from the "provinsi" column as text
        tooltip=[alt.Tooltip('provinsi:N', title='Province'),
                alt.Tooltip('jumlah_penduduk:Q', title='Population', format=".2s"),
                alt.Tooltip('amount_house:Q', title='Amount of Houses')]  # Add "amount_house" and "jumlah_penduduk" columns to the tooltip
    ).configure_text(
        font='Montserrat',  # Set the font to Montserrat
        fontSize=18,  # Set the font size to 20px
        color='#f5f5f5'  # Set the font color to #f5f5f5
    ).interactive().properties(
        height=500  # Set the desired height here
    )   

    st.altair_chart(text_chart, use_container_width=True)

    st.markdown("""
    <div style="margin-top: 20px;">
        <h3 style="text-align: left; font-size: 39px;">
            <span style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; color: #262626;">
                Pearson Correlation = {:.2f}
            </span>
        </h3>
    </div>
    """.format(correlation_population), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Analisis statistik yang dilakukan menyoroti korelasi yang signifikan antara jumlah rumah yang dijual di setiap provinsi dengan jumlah populasi di wilayah tersebut, dengan nilai korelasi Pearson mencapai {:.2f}. Temuan ini menggambarkan adanya hubungan positif yang kuat antara pertumbuhan populasi suatu provinsi dan ketersediaan real estate di pasar lokal. Penggunaan korelasi Pearson sebagai alat analisis statistik menjadi kunci dalam mengukur kekuatan serta arah hubungan antara kedua variabel tersebut. Dalam konteks ini, korelasi yang tinggi mengindikasikan bahwa <strong>semakin besar jumlah penduduk di suatu provinsi, semakin melimpah pula rumah yang ditawarkan untuk dijual.</strong> Implikasi dari temuan ini dapat memberikan pandangan berharga dalam perencanaan kota dan pengembangan real estate, memberikan dukungan strategis bagi pemerintah daerah dan pengembang untuk dapat memahami serta memenuhi kebutuhan perumahan yang berkaitan dengan pertumbuhan populasi. Dengan pemahaman yang lebih mendalam terhadap dinamika ini, langkah-langkah yang tepat dapat diambil untuk mencapai keseimbangan optimal antara penawaran dan permintaan perumahan di berbagai provinsi.
        </p>
   </div>
    """.format(correlation_population), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

elif option == "Jumlah Rumah Tangga":
    # Calculate the correlation between the logarithmic population and amount of houses
    correlation_household, p_value_household = pearsonr(df_rt_amount_house['total_rt_log'], df_rt_amount_house['amount_house_log'])

    # Create a scatter plot using Altair and replace the marks with text
    text_chart = alt.Chart(df_rt_amount_house).mark_text().encode(
        x=alt.X('amount_house_log:Q', title='Amount of Houses', axis=alt.Axis(labels=False, titleFontSize=20)),
        y=alt.Y('total_rt_log:Q', scale=alt.Scale(domain=[5.1, 7.2]), title='Amount of Household', axis=alt.Axis(labels=False, titleFontSize=20)),
        text='provinsi:N',  # Use values from the "provinsi" column as text
        tooltip=[alt.Tooltip('provinsi:N', title='Province'),
                alt.Tooltip('total_rt:Q', title='Amount of Household', format=".2s"),
                alt.Tooltip('amount_house:Q', title='Amount of Houses')]
    ).configure_text(
        font='Montserrat',  # Set the font to Montserrat
        fontSize=18,  # Set the font size to 20px
        color='#f5f5f5'  # Set the font color to #f5f5f5
    ).interactive().properties(
        height=500  # Set the desired height here
    )

    st.altair_chart(text_chart, use_container_width=True)

    st.markdown("""
    <div style="margin-top: 20px;">
        <h3 style="text-align: left; font-size: 39px;">
            <span style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; color: #262626;">
                Pearson Correlation = {:.2f}
            </span>
        </h3>
    </div>
    """.format(correlation_household), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Analisis statistik terbaru yang dilakukan menunjukkan hasil yang menarik terkait hubungan antara jumlah rumah yang dijual di setiap provinsi dan jumlah rumah tangga di wilayah tersebut. Dengan korelasi Pearson sebesar {:.2f}, tergambar sebuah korelasi yang signifikan dan positif antara jumlah rumah tangga suatu provinsi dengan ketersediaan rumah di pasar real estate lokal. Metode analisis statistik ini memberikan gambaran mengenai kekuatan dan arah hubungan antara dua variabel tersebut. Temuan ini memberikan pemahaman lebih lanjut bahwa <strong>semakin besar jumlah rumah tangga suatu provinsi, semakin meningkat pula jumlah rumah yang dijual.</strong> Implikasi dari hasil analisis ini sangat relevan dalam konteks perencanaan kota dan pengembangan real estate, memberikan pandangan berharga bagi pemerintah daerah dan pengembang untuk dapat mengantisipasi dan memenuhi kebutuhan perumahan seiring dengan pertumbuhan penduduk. Dengan pemahaman yang lebih baik tentang dinamika ini, langkah-langkah strategis dapat diambil untuk memastikan keseimbangan antara penawaran dan permintaan perumahan di setiap provinsi. 
        </p>
    </div>
    """.format(correlation_household), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

elif option == "Jumlah Rumah Tangga Tidak Memiliki Rumah":
    # Calculate the correlation between the logarithmic population and amount of houses
    correlation_household_no_home, p_value_household_no_home = pearsonr(df_rt_amount_house['total_rt_no_house_log'], df_rt_amount_house['amount_house_log'])

    # Create a scatter plot using Altair and replace the marks with text
    text_chart = alt.Chart(df_rt_amount_house).mark_text().encode(
        x=alt.X('amount_house_log:Q', title='Amount of Houses', axis=alt.Axis(labels=False, titleFontSize=20)),
        y=alt.Y('total_rt_no_house_log:Q', scale=alt.Scale(domain=[4.4, 6.6]), title='Amount of Households Do Not Have A House', axis=alt.Axis(labels=False, titleFontSize=20)),
        text='provinsi:N',  # Use values from the "provinsi" column as text
        tooltip=[alt.Tooltip('provinsi:N', title='Province'),
                alt.Tooltip('total_rt_no_house:Q', title='Amount of Households Do Not Have A House', format=".2s"),
                alt.Tooltip('amount_house:Q', title='Amount of Houses')]
    ).configure_text(
        font='Montserrat',  # Set the font to Montserrat
        fontSize=18,  # Set the font size to 20px
        color='#f5f5f5'  # Set the font color to #f5f5f5
    ).interactive().properties(
        height=500  # Set the desired height here
    )

    st.altair_chart(text_chart, use_container_width=True)

    st.markdown("""
    <div style="margin-top: 20px;">
        <h3 style="text-align: left; font-size: 39px;">
            <span style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; color: #262626;">
                Pearson Correlation = {:.2f}
            </span>
        </h3>
    </div>
    """.format(correlation_household_no_home), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Analisis statistik terkini menyoroti korelasi yang sangat signifikan antara jumlah rumah yang dijual di setiap provinsi dan jumlah rumah tangga yang tidak memiliki rumah sendiri di wilayah tersebut, dengan nilai korelasi Pearson mencapai {:.2f}. Temuan ini menggambarkan sebuah hubungan positif yang sangat kuat antara pertumbuhan jumlah rumah yang tersedia di pasar real estate lokal dengan kebutuhan rumah bagi rumah tangga yang belum memiliki tempat tinggal. Korelasi Pearson, sebagai alat analisis statistik yang diandalkan, digunakan untuk mengukur dengan akurat kekuatan dan arah hubungan antara kedua variabel ini. Dalam konteks ini, tingkat korelasi yang tinggi mengindikasikan bahwa <strong>semakin besar jumlah rumah yang dijual di suatu provinsi, semakin banyak pula rumah tangga yang tidak memiliki rumah sendiri yang dapat memanfaatkannya.</strong> Implikasi dari temuan ini memiliki dampak strategis dalam perencanaan kota dan pengembangan real estate, memberikan panduan yang berharga bagi pemerintah daerah dan pengembang untuk memahami serta memenuhi kebutuhan perumahan yang terkait dengan kelompok rumah tangga yang belum memiliki tempat tinggal. Dengan pemahaman mendalam terhadap dinamika ini, kebijakan dan proyek pengembangan dapat diarahkan untuk lebih efektif memenuhi kebutuhan rumah tangga yang rentan tersebut. 
        </p>
    </div>
    """.format(correlation_household_no_home), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

elif option == "Upah Minimum Provinsi":
    # Calculate the correlation between the logarithmic population and amount of houses
    correlation_ump, p_value_ump = pearsonr(df_rt_amount_house['ump_log'], df_rt_amount_house['amount_house_log'])

    # Create a scatter plot using Altair and replace the marks with text
    text_chart = alt.Chart(df_rt_amount_house).mark_text().encode(
        x=alt.X('amount_house_log:Q', title='Amount of Houses', axis=alt.Axis(labels=True, titleFontSize=20)),
        y=alt.Y('ump_log:Q', scale=alt.Scale(domain=[6.29, 6.7]), title='Minimum Wage', axis=alt.Axis(labels=True, titleFontSize=20)),
        text='provinsi:N',  # Use values from the "provinsi" column as text
        tooltip=[alt.Tooltip('provinsi:N', title='Province'),
                alt.Tooltip('ump:Q', title='Minimum Wage', format=".2s"),
                alt.Tooltip('amount_house:Q', title='Amount of Houses')]
    ).configure_text(
        font='Montserrat',  # Set the font to Montserrat
        fontSize=18,  # Set the font size to 20px
        color='#f5f5f5'  # Set the font color to #f5f5f5
    ).interactive().properties(
        height=500  # Set the desired height here
    )

    st.altair_chart(text_chart, use_container_width=True)

    st.markdown("""
    <div style="margin-top: 20px;">
        <h3 style="text-align: left; font-size: 39px;">
            <span style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; color: #262626;">
                Pearson Correlation = {:.2f}
            </span>
        </h3>
    </div>
    """.format(correlation_ump), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Analisis statistik terbaru mengungkapkan sebuah korelasi yang menarik antara jumlah rumah yang dijual di setiap provinsi dan upah minimum di wilayah tersebut, dengan nilai korelasi Pearson sebesar {:.2f}. Temuan ini menunjukkan adanya hubungan yang signifikan, namun berlawanan arah, antara penawaran rumah di pasar real estate lokal dengan tingkat upah minimum di provinsi-provinsi tersebut. Korelasi Pearson, sebagai alat analisis statistik, memberikan indikasi kuat terkait kekuatan dan arah hubungan antara kedua variabel ini. Dalam konteks ini, korelasi yang negatif menandakan bahwa <strong>semakin tinggi upah minimum di suatu provinsi, semakin sedikit jumlah rumah yang ditawarkan untuk dijual</strong>. 
        </p>
    </div>
    """.format(correlation_ump), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


# --- Analisis Kesenjangan Kemampuan Membeli Rumah di Berbagai Wilayah Indonesia ---
st.markdown("<h2 style='text-align: left; font-size: 44px;'>Analisis Kesenjangan Kemampuan Membeli Rumah di Berbagai Wilayah Indonesia</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Median house price in each province
province_price = df_house.groupby('provinsi').agg(median_price = ('harga','median'))
# st.dataframe(province_price)

# Sorting by the 'median_price' column in descending order
province_price_sorted = province_price.sort_values(by='median_price', ascending=False)

# Merging province_price and df_income
ump_merge = pd.merge(province_price, df_income, on='provinsi', how='inner')

# Sorting DataFrame based on ump column in descending order
ump_merge_sorted = ump_merge.sort_values(by='ump', ascending=False)

# Selecting top 4 and bottom 4
selected_data = pd.concat([ump_merge_sorted.head(4), ump_merge_sorted.tail(4)])

# Creating Altair chart without legend
chart = alt.Chart(selected_data).mark_bar().encode(
    x=alt.X('provinsi:N', sort=alt.EncodingSortField(field='ump', op='sum', order='descending'), title='Province', 
            axis=alt.Axis(labelAngle=0, labelLimit=0, labelFlush=True, titleFontSize=20, labelFontSize=18)),
    y=alt.Y('ump:Q', title='Minimum Wage', axis=alt.Axis(titleFontSize=20, labelFontSize=18)),
    color=alt.value('#e9c46a')  # Changing the color to #e9c46a
).properties(
    height=500  # Set your desired height here
)

# Adding a horizontal line for rata_rata_angsuran
rule = alt.Chart(pd.DataFrame({'rata_rata_angsuran': [1620000]})).mark_rule(strokeWidth=2.5).encode(
    y='rata_rata_angsuran:Q', 
    color=alt.value('#e76f51'),  # You can change the color as needed
    tooltip=[alt.Tooltip('rata_rata_angsuran:Q', title='Avg. Installment per Month')]
)

# Layering the rule on top of the bar chart
chart_with_rule = (chart + rule)

# Displaying chart using Streamlit
st.altair_chart(chart_with_rule, use_container_width=True)

st.markdown("""
<div>
    <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
        Terdapat perbedaan signifikan dalam upah minimum di berbagai provinsi di Indonesia<sup>[5]</sup>. Beberapa provinsi, seperti Papua dan DKI Jakarta, memiliki upah minimum yang lebih tinggi daripada rata-rata ambang batas pembayaran Kredit Kepemilikan Rumah (KPR) sebesar 1,62 juta per bulan pada tahun 2022<sup>[6]</sup>. Di sisi lain, provinsi-provinsi seperti Jawa Barat dan Jawa Tengah memiliki upah minimum yang lebih tinggi, namun hanya sedikit di atas ambang batas tersebut. Faktanya, hal ini mencerminkan tantangan besar terkait keterjangkauan perumahan di Indonesia, terutama di provinsi-provinsi dengan upah minimum yang rendah. Situasi ini menunjukkan bahwa walaupun upah minimum mungkin lebih tinggi, namun ketersediaan rumah yang terjangkau tetap menjadi isu penting bagi masyarakat, terutama di provinsi-provinsi dengan kondisi ekonomi yang lebih rendah.
    </p>
</div>
""", unsafe_allow_html=True)

cluster_income = pd.merge(df_income, df_cluster, on='provinsi', how='inner')
cluster_income['ump_log'] = np.log10(cluster_income['ump'])

# Create a dict for mapping the cluster column
color_dict = {
    1: '#264653',
    2: '#2a9d8f',
    3: '#e9c46a',
    4: '#f4a261',
    5: '#e76f51'
}

# Change the cluster column data type to category
cluster_income['cluster'] = cluster_income['cluster'].astype('category')

# Mapping the color of 'cluster'
cluster_income['color'] = cluster_income['cluster'].map(color_dict)

text_chart = alt.Chart(cluster_income).mark_text().encode(
    x=alt.X('ump_log:Q', scale=alt.Scale(domain=[6.29, 6.72]), title='', axis=alt.Axis(labels=False, titleFontSize=20)),
    y=alt.Y('ump_log:Q', scale=alt.Scale(domain=[6.29, 6.73]), title='', axis=alt.Axis(labels=False, titleFontSize=20)),
    color=alt.Color('color:N', legend=None),
    text='provinsi:N',  # Use values from the "provinsi" column as text
    tooltip=[alt.Tooltip('provinsi:N', title='Province'),
            alt.Tooltip('ump:Q', title='Minimum Wage')]
).configure_text(
    font='Montserrat',  # Set the font to Montserrat
    fontSize=18,  # Set the font size to 20px
    color='#f5f5f5'  # Set the font color to #f5f5f5
).interactive().properties(
    height=500  # Set the desired height here
)

st.altair_chart(text_chart, use_container_width=True)

st.markdown("""
<div>
    <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
        Hasil clustering menunjukkan bahwa provinsi-provinsi di Indonesia dapat dibagi menjadi lima kelompok berdasarkan upah minimum:
    </p>
    <ol>
        <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Cluster 1</strong> dengan rata-rata upah minimum sebesar 5,067,381.000, mencakup provinsi DKI Jakarta</li>
        <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Cluster 2</strong> dengan rata-rata upah minimum sebesar 4,024,270.000, mencakup provinsi Papua, Papua Tengah, Papua Pegunungan, dan Papua Selatan.</li>
        <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Cluster 3</strong> dengan rata-rata upah minimum sebesar 3,391,992.912, mencakup provinsi Aceh, Riau, Sumatera Selatan, Kepulauan Bangka Belitung, Kepulauan Riau, Kalimantan Tengah, Kalimantan Selatan, Kalimantan Timur, Kalimantan Utara, Sulawesi Utara, Sulawesi Selatan, Maluku Utara, Papua Barat, dan Papua Barat Daya.</li>
        <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Cluster 4</strong> dengan rata-rata upah minimum sebesar 2,844,313.029, mencakup provinsi Sumatera Utara, Sumatera Barat, Jambi, Lampung, Banten, Bali, Kalimantan Barat, Sulawesi Tengah, Gorontalo, Sulawesi Barat, dan Maluku.</li>
        <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Cluster 5</strong> dengan rata-rata upah minimum sebesar 2,217,650.879, mencakup provinsi Bengkulu, Jawa Barat, Jawa Tengah, DI Yogyakarta, Jawa Timur, Nusa Tenggara Barat, dan Nusa Tenggara Timur.</li>        
    </ol>
    <br>
    <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
        Kesenjangan upah minimum ini dapat menimbulkan beberapa implikasi, seperti:
    </p>
    <ol>
        <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;">Masyarakat di provinsi dengan upah minimum rendah akan kesulitan untuk membeli rumah, terutama melalui KPR. Hal ini sangat relevan untuk provinsi-provinsi di Cluster 5.</li>
        <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;">Hal ini dapat mendorong pengembangan perumahan informal, seperti pembangunan perumahan yang tidak memiliki izin atau berkualitas buruk.</li>
        <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;">Pemerintah harus mengambil langkah-langkah untuk mengurangi kesenjangan upah minimum dan meningkatkan keterjangkauan perumahan di Indonesia, dengan mempertimbangkan perbedaan antar cluster ini.</li>
    </ol>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)




# --- Dampak Regional terhadap Durasi Pinjaman KPR ---
st.markdown("<h2 style='text-align: left; font-size: 44px;'>Dampak Regional terhadap Durasi Pinjaman KPR</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
def bulan_angsuran(df):
    df['total_bulan'] = df['median_price'] / df['rata_rata_angsuran']
    df['total_bulan'] = round(df['total_bulan'])
    return df

def tahun_angsuran(df):
    df['total_tahun'] = df['total_bulan'] / 12
    df['total_tahun'] = round(df['total_tahun'])
    return df

total_bulan_angsuran = ump_merge_sorted.copy()
total_bulan_angsuran = bulan_angsuran(total_bulan_angsuran)
total_bulan_angsuran = tahun_angsuran(total_bulan_angsuran)
total_bulan_angsuran_sorted = total_bulan_angsuran.sort_values(by='total_tahun', ascending=False)

# Selecting top 4 and bottom 4
selected_data = pd.concat([total_bulan_angsuran_sorted.head(4), total_bulan_angsuran_sorted.tail(4)])

# Creating Altair chart without legend
chart = alt.Chart(selected_data).mark_bar().encode(
    x=alt.X('provinsi:N', sort=alt.EncodingSortField(field='total_tahun', op='sum', order='descending'), title='Province',
            axis=alt.Axis(labelAngle=0, labelLimit=0, labelFlush=True, titleFontSize=20, labelFontSize=18)),
    y=alt.Y('total_tahun:Q', title='Duration of A Mortgage Loan (Year)', axis=alt.Axis(titleFontSize=20, labelFontSize=18)),
    color=alt.value('#e9c46a'),  # Changing the color to #e9c46a
    tooltip=[
        alt.Tooltip('provinsi:N', title='Province'),
        alt.Tooltip('median_price:Q', title='Median Price'),
        alt.Tooltip('total_bulan:Q', title='Duration of A Mortgage in Months'),
        alt.Tooltip('total_tahun:Q', title='Duration of A Mortgage in Years')
    ]
).properties(
    height=500  # Set your desired height here
)

# Adding a horizontal line for 20 Years
rule = alt.Chart(pd.DataFrame({'ojk': [20]})).mark_rule(strokeWidth=2.5).encode(
    y='ojk:Q', 
    color=alt.value('#2A9D8F'),  # You can change the color as needed
    tooltip=[alt.Tooltip('ojk:Q', title="The optimal duration as per OJK's guidelines")]
)

# Adding a horizontal line for 35 Years
rule1 = alt.Chart(pd.DataFrame({'new': [35]})).mark_rule(strokeWidth=2.5).encode(
    y='new:Q', 
    color=alt.value('#E76F51'),  # You can change the color as needed
    tooltip=[alt.Tooltip('new:Q', title="The duration currently under contemplation in its design")]
)

# Layering the rule on top of the bar chart
chart_with_rule = (chart + rule + rule1)

# Displaying chart using Streamlit
st.altair_chart(chart_with_rule, use_container_width=True)

st.markdown("""
<div>
    <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
        Durasi pinjaman KPR memiliki pengaruh besar terhadap kemampuan finansial masyarakat dalam memiliki rumah. Grafik di atas menunjukkan durasi pinjaman KPR yang ideal di setiap provinsi di Indonesia berdasarkan Rata-Rata Angsuran KPR per Bulan<sup>[6]</sup> dan median harga rumah.
    </p>
    <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
        Hanya 1 provinsi (Kalimantan Utara) yang memungkinkan tenor KPR maksimal 20 tahun sesuai aturan OJK<sup>[4]</sup>. Hal ini menunjukkan bahwa mayoritas masyarakat di Indonesia, memiliki keterbatasan finansial dalam membeli rumah dengan tenor KPR yang singkat.
    </p>
    <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
        Jika rancangan untuk memperpanjang tenor KPR hingga 35 tahun diberlakukan, 11 provinsi (Kalimantan Utara, Sulawesi Tengah, Papua Barat, Lampung, Jambi, Jawa Tengah, Aceh, Sumatera Barat, Kalimantan Barat, Kalimantan Selatan, dan Kalimantan Tengah) akan memiliki akses ke KPR dengan tenor yang lebih panjang dan cicilan yang lebih ringan.
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)




# --- Lalu, Apakah Kebijakan KPR 35 Tahun Sudah Tepat? ---
st.markdown("<h2 style='text-align: left; font-size: 44px;'>Lalu, Apakah Kebijakan KPR 35 Tahun Sudah Tepat?</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div>
    <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
        Pertanyaan mengenai apakah solusi KPR dengan tenor 35 tahun sudah tepat atau tidak untuk mengatasi masalah backlog kepemilikan rumah bisa dilihat dari beberapa sudut pandang. Berikut adalah beberapa dampak positif dan negatif yang dapat dipertimbangkan:
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    people_icon = "https://raw.githubusercontent.com/luthfifathurrahman/The-35-Year-Mortgage-Policy-In-Indonesia/main/image/team.png"
    st.image(people_icon, use_column_width=False, output_format='auto')
    caption_style1 = "text-align: left; font-size: 12px;"
    link = "https://www.flaticon.com/free-icon/team_476761?related_id=476863&origin=search"

    st.markdown(f"""
        <div>
            <p style="{caption_style1}">
                Source: <a href="{link}" style="color: #f5f5f5; text-decoration: none;">flaticon</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Dampak <strong>POSITIF</strong> bagi Individu atau Masyarakat:
        </p>
        <ol>
            <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Aksesibilitas Perumahan:</strong> Perpanjangan tenor KPR hingga 35 tahun dapat meningkatkan aksesibilitas perumahan bagi masyarakat di provinsi-provinsi dengan upah minimum rendah. Hal ini dapat membantu lebih banyak orang memiliki rumah sendiri.</li>
            <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Cicilan yang Lebih Ringan:</strong> Dengan tenor yang lebih panjang, cicilan bulanan KPR dapat menjadi lebih ringan, sehingga memungkinkan masyarakat memiliki rumah tanpa memberatkan keuangan mereka secara berlebihan.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with col2:
    bank_icon = "https://raw.githubusercontent.com/luthfifathurrahman/The-35-Year-Mortgage-Policy-In-Indonesia/main/image/bank.png"
    st.image(bank_icon, use_column_width=False, output_format='auto')
    caption_style1 = "text-align: left; font-size: 12px;"
    link = "https://www.flaticon.com/free-icon/bank_2830284?term=bank&page=1&position=1&origin=search&related_id=2830284"

    st.markdown(f"""
        <div>
            <p style="{caption_style1}">
                Source: <a href="{link}" style="color: #f5f5f5; text-decoration: none;">flaticon</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Dampak <strong>POSITIF</strong> bagi Perbankan/Organisasi Terkait:
        </p>
        <ol>
            <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Stimulasi Pembangunan Perumahan:</strong> Solusi ini dapat merangsang pertumbuhan sektor properti dan konstruksi.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Dampak <strong>NEGATIF</strong> bagi Individu atau Masyarakat:
        </p>
        <ol>
            <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Total Pembayaran Bunga yang Lebih Tinggi:</strong> Tenor yang lebih panjang akan meningkatkan total pembayaran bunga yang harus dibayarkan oleh peminjam, sehingga secara keseluruhan pembelian rumah dapat menjadi lebih mahal.</li>
            <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Risiko Gagal Bayar yang Lebih Besar:</strong> Dengan tenor yang lebih panjang, risiko gagal bayar atau kesulitan finansial dalam jangka panjang dapat meningkat. Hal ini dapat memberikan tekanan tambahan pada kestabilan keuangan individu.</li>
            <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Beban Finansial yang Lebih Lama:</strong> Peminjam akan membayar cicilan lebih lama, yang dapat berdampak pada kebebasan finansial mereka dalam jangka panjang.</li>   
        </ol>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div>
        <p style="text-indent: 45px; text-align: justify; hyphens: auto; font-size: 24px;">
            Dampak <strong>NEGATIF</strong> bagi Perbankan/Organisasi Terkait:
        </p>
        <ol>
            <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Risiko Kredit yang Lebih Tinggi:</strong> Dengan pemberian tenor yang lebih panjang, risiko gagal bayar atau kesulitan finansial jangka panjang dapat meningkat bagi pemberi pinjaman. Hal ini dapat menimbulkan tekanan tambahan pada kestabilan portofolio kredit bank.</li>
            <li  style="text-align: justify; word-spacing:-2px; hyphens: auto; font-size: 24px;"><strong>Pertimbangan Ekonomi Makro:</strong> Solusi ini juga perlu dipertimbangkan dari perspektif ekonomi makro, termasuk potensi dampak terhadap inflasi, likuiditas perbankan, dan stabilitas sistem keuangan.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)




# # Machine Learning
# st.markdown("<h2 style='text-align: center; font-size: 44px;'>Prediksi Harga Real Estate Anda Di Sini.</h2>", unsafe_allow_html=True)
# st.markdown("<br>", unsafe_allow_html=True)
# df_house_baru = df_house.copy()

# col1, col2, col3 = st.columns(3)

# # Removing houses that have a price under 50 million
# df_house_baru = df_house_baru[df_house_baru['harga'] >= 50000000]

# # Drop columns
# df_house_baru = df_house_baru.drop(['kecamatan'], axis=1)

# with col2:
#     # Displaying a warning message  
#     st.warning("Peringatan: Proses ini dapat memakan waktu yang bervariasi bergantung pada kecepatan internet Anda. Mohon maaf atas segala ketidaknyamanan yang mungkin timbul.", icon="⚠️")
#     st.markdown("<br>", unsafe_allow_html=True)  

#     # Create select box for provinsi
#     provinsi_options = sorted(df_house_baru['provinsi'].unique())
#     selected_provinsi = st.selectbox('Pilih Provinsi', provinsi_options)

#     # Filter DataFrame based on provinsi
#     filtered_df_province = df_house_baru[df_house_baru['provinsi'] == selected_provinsi]

#     # create select box for kota based on provinsi
#     kota_options = sorted(filtered_df_province['kota'].unique())
#     selected_kota = st.selectbox('Pilih Kota', kota_options)

#     # Create input boxes for kamar_tidur
#     kamar_tidur = st.number_input('Masukkan Jumlah Kamar Tidur', value=0, step=1)
#     kamar_tidur = max(0, int(kamar_tidur))  # Ensure the value is at least 0

#     # Do the same for kamar_mandi, luas_tanah, and luas_bangunan
#     kamar_mandi = max(0, int(st.number_input('Masukkan Jumlah Kamar Mandi', value=0, step=1)))
#     luas_tanah = max(0, int(st.number_input('Masukkan Luas Tanah (Meter Persegi)', value=0.0, step=1.0)))
#     luas_bangunan = max(0, int(st.number_input('Masukkan Luas Bangunan (Meter Persegi)', value=0.0, step=1.0)))

#     # Check if all values are greater than 0 and luas_bangunan is not greater than luas_tanah
#     if kamar_tidur > 0 and kamar_mandi > 0 and luas_tanah > 0 and luas_bangunan > 0 and luas_bangunan <= luas_tanah:
#         # Create a dictionary with the selected values
#         new_data = {
#             'kota': [selected_kota],
#             'provinsi': [selected_provinsi],
#             'kamar_tidur': [kamar_tidur],
#             'kamar_mandi': [kamar_mandi],
#             'luas_tanah': [luas_tanah],
#             'luas_bangunan': [luas_bangunan]
#         }

#         # Create a new DataFrame with the new data
#         new_row_df = pd.DataFrame(new_data)

#         # Append the new row to the original DataFrame
#         new_data = df_house_baru.drop(['harga'], axis=1)
#         df_machine_learning = pd.concat([new_row_df, new_data], ignore_index=True)

#         # Performing one-hot encoding
#         df_machine_learning = pd.get_dummies(df_machine_learning, columns=[ 'provinsi', 'kota'])
#         df_machine_learning = df_machine_learning[:1]

#         # setup load model
#         model_path = current_dir / "machine_learning" / "rf_regressor_model.pkl"
        
#         # Load the pickled model
#         with open(model_path, 'rb') as file:
#             load_model = dill.load(file)

#         # Make prediction
#         prediction = load_model.predict(df_machine_learning)

#         # Round the prediction to 2 decimal places
#         rounded_prediction = round(prediction[0], 2)

#         # Format the rounded prediction with thousands separator
#         formatted_prediction = "{:,.2f}".format(rounded_prediction)

#         # Displaying prediction as text
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.markdown("""
#             <div>
#                 <p style="text-align: center; font-size: 24px;">
#                     ESTIMASI HARGA REAL ESTATE ANDA ADALAH
#                 </p>
#             </div>
#         """, unsafe_allow_html=True)

#         st.markdown("""
#         <div style="margin-top: 20px;">
#             <h3 style="text-align: center; font-size: 39px;">
#                 <span style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; color: #262626;">
#                     <strong>Rp. {}</strong>
#                 </span>
#             </h3>
#         </div>
#         """.format(formatted_prediction), unsafe_allow_html=True)
#         st.markdown("<br>", unsafe_allow_html=True)

#     else:
#         st.warning("Dimohon untuk memasukkan angka di atas 0 pada Kamar Tidur, Kamar Mandi, Luas Tanah, dan Luas Bangunan. Pastikan juga Luas Bangunan tidak lebih besar dari Luas Tanah.", icon="⚠️")
    

# # Displaying a warning message  
# st.markdown("<br>", unsafe_allow_html=True)    
# st.warning("Tolong diingat, hasil prediksi harga rumah dari model machine learning ini hanyalah perkiraan berdasarkan data yang ada. Keputusan terkait pembelian atau penjualan rumah sebaiknya tetap dipertimbangkan dengan hati-hati dan disertai dengan penelitian lebih lanjut. Model ini tidak dapat memperhitungkan faktor-faktor yang mungkin tidak terdokumentasi dalam data, dan keputusan akhir sebaiknya didasarkan pada pemahaman menyeluruh tentang pasar dan kondisi spesifik properti yang bersangkutan. Selalu konsultasikan dengan profesional real estate sebelum mengambil keputusan besar terkait properti.", icon="⚠️")

# Citation
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: left; font-size: 44px;'>Daftar Pustaka</h2>", unsafe_allow_html=True)
caption_style = "text-align: left; font-size: 24px;"

data = [
    {
        "title": "Backlog Perumahan di Indonesia Tinggi, Ini Pemicunya",
        "source": "CNBC Indonesia TV, CNBC Indonesia",
        "date": "9 Agustus 2023",
        "link": "https://www.cnbcindonesia.com/news/20230809195212-8-461619/backlog-perumahan-di-indonesia-tinggi-ini-pemicunya"
    },
    {
        "title": "Jumlah Rumah Tangga menurut Wilayah,Daerah Perkotaan/Perdesaan, dan Status Kepemilikan Bangunan Tempat Tinggal yang Ditempati, INDONESIA, Tahun 2022",
        "source": "Badan Pusat Statistik",
        "link": "https://sensus.bps.go.id/topik/tabular/sp2022/178"
    },
    {
        "title": "Rencana Tenor KPR hingga 35 Tahun, Ini Kata Dirut Bank BTN",
        "source": "Pratomo, Gagas Yoga. Liputan6",
        "date": "12 Februari 2024",
        "link": "https://www.liputan6.com/bisnis/read/5526399/rencana-tenor-kpr-hingga-35-tahun-ini-kata-dirut-bank-btn?page=3"
    },
    {
        "title": "Nyicil Rumah Nggak Perlu Takut, Asal Perhatikan Hal-Hal Berikut",
        "source": "Otoritas Jasa Keuangan",
        "link": "http://sikapiuangmu.ojk.go.id/FrontEnd/CMS/Article/10415"
    },
    {
        "title": "Upah Minimum Provinsi (UMP) Tahun 2024",
        "source": "Kementerian Ketenagakerjaan",
        "date": "5 Januari 2024",
        "link": "https://satudata.kemnaker.go.id/data/kumpulan-data/1611"
    },
    {
        "title": "Rata-Rata Biaya Angsuran KPR Rumah Tangga per Bulan di Indonesia",
        "source": "Hidayah, Fitri Nur. GoodStats",
        "date": "12 September 2023",
        "link": "https://data.goodstats.id/statistic/Fitrinurhdyh/rata-rata-biaya-angsuran-kpr-rumah-tangga-perbulan-di-indonesia-ZXNum"
    },
]

for index, item in enumerate(data, start=1):
    st.markdown(f"""
        <div>
            <p style="{caption_style}">
                [{index}] {item['source']}, "{item['title']}" {item.get('date', '')}. <a href="{item['link']}" style="color: #f5f5f5; text-decoration: none;">{item['link']}</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- SOCIAL LINKS ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: left; font-size: 44px;'>My Profile</h2>", unsafe_allow_html=True)
caption_style = "text-align: left; font-size: 24px;"
SOCIAL_MEDIA = {
    "GitHub Repository for This Project": "https://github.com/luthfifathurrahman/The-35-Year-Mortgage-Policy-In-Indonesia",
    "LinkedIn Profile": "https://www.linkedin.com/in/luthfi-fathurrahman/"
}

for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    st.markdown(f"""
        <div>
            <p style="{caption_style}">
                <a href="{link}" style="color: #f5f5f5; text-decoration: none;">
                    {platform}
                </a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
