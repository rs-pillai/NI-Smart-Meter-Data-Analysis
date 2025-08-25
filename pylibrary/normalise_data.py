import pandas as pd
import numpy as np

def normalize_hourly_consumption(df):
    daily_import_totals = df.groupby(['Profile', df.index.date])['Active import (kW)'].transform('sum')
    daily_export_totals = df.groupby(['Profile', df.index.date])['Active export (kW)'].transform('sum')
    df['Normalized import (kW)'] = (df['Active import (kW)'] / daily_import_totals)
    df['Normalized export (kW)'] = (df['Active export (kW)'] / daily_export_totals)
    df['Normalized import (kW)'].fillna(0, inplace=True)
    df['Normalized export (kW)'].fillna(0, inplace=True)
    return df