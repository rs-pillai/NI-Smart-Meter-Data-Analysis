import pandas as pd
import numpy as np


def manage_anomaly(data):
    indices_to_drop = []
    an_indices = data[data['Active import (kW)'] > 23].index
    print(an_indices)
    for index in an_indices:
        index_flag = True
        
        try:
            index_loc = data.index.get_loc(index)
            preceding_index = index_loc - 1
            succeeding_index = index_loc + 1
            print(f"index location {index_loc}")
            print(f"Preceding index position: {preceding_index}, Type: {type(preceding_index)}")
            print(f"Succeeding index position: {succeeding_index}, Type: {type(succeeding_index)}")
        except KeyError:
            print(f"Anomalous index {index} not found in DataFrame.")
            indices_to_drop.append(index)
            continue
    
        if preceding_index < 0 or succeeding_index >= len(data):
            indices_to_drop.append(index)
            print(f"Dropping index {index} as no valid nearby indices")
            index_flag = False
        
            
        if index_flag:
            preceding_row = data.iloc[preceding_index]
            succeeding_row = data.iloc[succeeding_index]
            condition_1 = (preceding_row['Active import (kW)'] < 23) and (succeeding_row['Active import (kW)'] < 23)
            condition_2 = (preceding_row['Profile'] == data.loc[index, 'Profile']) and (succeeding_row['Profile'] == 
                                                                                                              data.loc[index, 'Profile'])
            time_diff_1 = data.loc[index, 'DateTime'] - preceding_row['DateTime']
            time_diff_2 = succeeding_row['DateTime'] - data.loc[index, 'DateTime']
            condition_3 = (time_diff_1 == pd.Timedelta(minutes=30)) and (time_diff_2 == pd.Timedelta(minutes=30))
            if condition_1:
                print('Condition 1 met')
            else:
                print('Condition 1 not met')
            if condition_2:
                print('Condition 2 met')
            else:
                print('Condition 2 not met')
            if condition_3:
                print(f"Condition 3 met. Time differences = {time_diff_1, time_diff_2}")
            else:
                print(f"Condition 3 not met. Time differences = {time_diff_1, time_diff_2}")
                    
            if np.all([condition_1, condition_2, condition_3]):
                data.loc[index, 'Active import (kW)'] = (preceding_row['Active import (kW)'] + succeeding_row['Active import (kW)']) / 2
                print(f"Replaced anomalous value at index {index} with mean of {preceding_row['Active import (kW)']} and {succeeding_row['Active import (kW)']}")
            else:
                indices_to_drop.append(index)
                print(f"Dropped row at index {index} as it did not meet the replacement criteria.")
        
    data.drop(index=indices_to_drop, inplace=True)
    return data
