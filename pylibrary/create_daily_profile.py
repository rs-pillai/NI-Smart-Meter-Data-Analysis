import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def create_daily_profile(df, season=None, day_type=None, tariff_info=None):
    df_filtered = df.copy()
    if season:
        df_filtered = df_filtered[df_filtered['Season'] == season]
    if day_type:
        df_filtered = df_filtered[df_filtered['DayType'] == day_type]
    daily_import_profile = df_filtered.groupby(['Profile', df_filtered.index.hour])['Normalized import (kW)'].mean().unstack()
    daily_export_profile = df_filtered.groupby(['Profile', df_filtered.index.hour])['Normalized export (kW)'].mean().unstack()
    daily_import_profile.columns = [f'Import_Hour_{i}' for i in daily_import_profile.columns]
    daily_export_profile.columns = [f'Export_Hour_{i}' for i in daily_export_profile.columns]
    daily_profile = pd.concat([daily_import_profile, daily_export_profile], axis=1)
    daily_profile = daily_profile.round(7)
    daily_profile.columns = daily_profile.columns.astype(str)
    daily_profile = daily_profile.merge(tariff_info, left_index=True, right_index=True, how='left')
    return daily_profile