import pandas as pd
from pathlib import Path
from sklearn.cluster import KMeans

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
previous_dir = current_dir.parent

# --- CREATE A DATAFRAME ---
cleaned_income_province_path = previous_dir / "datasets" / "cleaned_ump_data.csv"
df_income = pd.read_csv(cleaned_income_province_path)

# Assuming df_income is your original DataFrame
df_cluster = df_income.copy()

# Assuming 'provinsi' is a categorical feature you want to one-hot encode
df_cluster = pd.get_dummies(df_cluster, columns=['provinsi'])

# Assuming 'ump' is a feature you want to include in the clustering
X = df_cluster[['ump']].to_numpy()

# Specify the desired number of clusters
samples_num = 5

# Check if you have enough samples for clustering
if len(X) >= samples_num:
    # Train K-means clustering
    kmeans = KMeans(random_state=28, n_clusters=samples_num)
    kmeans.fit(X)

    # Assign cluster labels to the original DataFrame
    df_cluster['cluster'] = kmeans.labels_

    # Set opsi tampilan angka agar tidak menggunakan notasi ilmiah
    pd.set_option('display.float_format', lambda x: '%.3f' % x)

    # Display cluster centroids
    centroid_df = df_cluster.groupby('cluster').agg({'ump': ['mean', 'count']}).reset_index()
    centroid_df.columns = ['cluster', 'num_status', 'count']
    centroid_df['cluster'] = [f'Cluster {i + 1}' for i in range(samples_num)]
    print(centroid_df)

    # Create a combined DataFrame for all clusters
    combined_df = pd.DataFrame()

    # Create separate dataframes for each cluster and display the contents
    for i in range(samples_num):
        cluster_data = df_cluster[df_cluster['cluster'] == i]
        cluster_data['provinsi'] = cluster_data.apply(
            lambda row: row.index[row == True][0].split('_')[1] if any(row == True) else None, axis=1)
        cluster_data.loc[:, 'provinsi'] = cluster_data.apply(
            lambda row: row.index[row == True][0].split('_')[1] if any(row == True) else None, axis=1)
        kolom_urut_baru = ['provinsi']
        cluster_data = cluster_data[kolom_urut_baru]

        # Add the 'cluster' column with the cluster index (i)
        cluster_data['cluster'] = i + 1

        # Append the cluster_data DataFrame to the combined DataFrame
        combined_df = combined_df._append(cluster_data, ignore_index=True)

        print(f"\nCluster {i + 1}:")
        print(cluster_data)

    # Display the combined DataFrame
    print("\nCombined DataFrame:")
    print(combined_df)
    output_dir = previous_dir / "datasets"
    cluster_path = output_dir / "cluster.csv"
    combined_df.to_csv(cluster_path, index=False)

else:
    print("Insufficient data points for clustering.")
