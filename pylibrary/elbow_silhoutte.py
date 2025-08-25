import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def plot_elbow_and_silhouette(profile_df, max_clusters=10, title="Elbow and Silhouette Analysis"):
    # Select only import columns for clustering
    import_columns = [col for col in profile_df.columns if "Import_Hour" in col]  
    wcss = []
    silhouette_scores = []
    
    for i in range(2, max_clusters + 1):  # Start from 2 clusters for silhouette
        kmeans = KMeans(n_clusters=i, random_state=42)
        cluster_labels = kmeans.fit_predict(profile_df[import_columns])
        
        # Compute WCSS for elbow plot
        wcss.append(kmeans.inertia_)
        
        # Compute Silhouette Score for silhouette analysis
        silhouette_avg = silhouette_score(profile_df[import_columns], cluster_labels)
        silhouette_scores.append(silhouette_avg)
    
    # Plotting the elbow graph (WCSS)
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(range(2, max_clusters + 1), wcss, marker='o', linestyle='-')
    plt.title(f"{title} - Elbow Method (WCSS)")
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS')
    
    # Plotting the silhouette scores
    plt.subplot(1, 2, 2)
    plt.plot(range(2, max_clusters + 1), silhouette_scores, marker='o', linestyle='-')
    plt.title(f"{title} - Silhouette Scores")
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.tight_layout()
    plt.show()

    
    optimal_clusters = range(2, max_clusters + 1)[silhouette_scores.index(max(silhouette_scores))]
    print(f"Optimal number of clusters for {title} based on silhouette score: {optimal_clusters}")
    
    return optimal_clusters