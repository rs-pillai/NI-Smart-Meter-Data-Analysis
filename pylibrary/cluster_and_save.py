import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.signal import find_peaks
from tqdm.notebook import tqdm

def cluster_and_save_profiles(profile_df, num_clusters=2, title="Clustered Daily Profiles", output_csv="clustering_output.csv"):
    import_columns = [col for col in profile_df.columns if "Import_Hour" in col]
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    profile_df['Cluster'] = kmeans.fit_predict(profile_df[import_columns])
    
    cluster_counts = profile_df['Cluster'].value_counts()
    print("Cluster counts:\n", cluster_counts)

    min_threshold = 3
    valid_clusters = cluster_counts[cluster_counts >= min_threshold].index
    filtered_df = profile_df[profile_df['Cluster'].isin(valid_clusters)].copy()
    
    # 🧠 Ensure 'Profile' is preserved as a column
    if 'Profile' not in filtered_df.columns:
        filtered_df.reset_index(inplace=True)

    tariff_counts = filtered_df.groupby(['Cluster', 'Tariff']).size().unstack(fill_value=0)
    print(f"Tariff counts per cluster:\n{tariff_counts}")
    
    # Plot the cluster centroids (average profiles for each cluster)
    plt.figure(figsize=(12, 8))
    for cluster_num in tqdm(range(num_clusters), desc= 'Cluster Plotting'):
        cluster_import_centroid = filtered_df[filtered_df['Cluster'] == cluster_num][import_columns].median()
        hours = [int(col.split('_')[-1]) for col in cluster_import_centroid.index]
        plt.plot(hours, cluster_import_centroid.values, label=f'Cluster {cluster_num} Import')
        
        # Add peaks and valleys
        peaks, _ = find_peaks(cluster_import_centroid.values)
        plt.scatter(np.array(hours)[peaks], cluster_import_centroid.values[peaks], color='red', label=f'Peaks Cluster {cluster_num}')
        for peak in peaks:
            plt.annotate(f"{hours[peak]}", (hours[peak], cluster_import_centroid.values[peak]), 
                         textcoords="offset points", xytext=(0, 5), ha='center', color='red')
        valleys, _ = find_peaks(-cluster_import_centroid.values)
        plt.scatter(np.array(hours)[valleys], cluster_import_centroid.values[valleys], color='blue', label=f'Valleys Cluster {cluster_num}')
        for valley in valleys:
            plt.annotate(f"{hours[valley]}", (hours[valley], cluster_import_centroid.values[valley]), 
                         textcoords="offset points", xytext=(0, -10), ha='center', color='blue')
            

    plt.title(f"{title} - Import Profile")
    plt.xlabel("Hour of Day")
    plt.xticks(ticks=range(24), labels=[f"{h}:00" for h in range(24)])
    plt.ylabel("Normalised Import")
    plt.legend()
    plt.show()
    
    # Plot export centroids
    export_columns = [col for col in filtered_df.columns if "Export_Hour" in col]
    plt.figure(figsize=(12, 8))
    for cluster_num in range(num_clusters):
        cluster_export_centroid = filtered_df[filtered_df['Cluster'] == cluster_num][export_columns].mean()
        hours = [int(col.split('_')[-1]) for col in cluster_export_centroid.index]
        plt.plot(hours, cluster_export_centroid.values, label=f'Cluster {cluster_num} Export')
        
    plt.title(f"{title} - Export Profile")
    plt.xticks(ticks=range(24), labels=[str(h) for h in range(24)])
    plt.xlabel("Hour of Day")
    plt.ylabel("Normalised Export")
    plt.legend()
    plt.show()
    
    # Save to CSV
    if 'Profile' not in filtered_df.columns:
        filtered_df = filtered_df.reset_index()
    elif filtered_df.index.name == 'Profile':
        filtered_df = filtered_df.reset_index()

# Save to CSV
    filtered_df.to_csv(output_csv, index=False)
    print(f"Clustering results saved to {output_csv}")

    return kmeans, filtered_df