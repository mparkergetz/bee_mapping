import os
import rasterio
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def get_value_from_array(lat, long, src, array):
    try:
        row, col = src.index(long, lat)
        return array[row, col]
    except Exception as e:
        print(f'Error at {lat}, {long}: {e}')
        return None

directory = '/home/mpgetz/repos/bee_mapping/data/wc2.1_30s_bio'
all_files = [f for f in os.listdir(directory) if f.endswith('.tif') and "wc2.1_30s_" in f]
all_files = sorted(all_files)
print(all_files)

def process_file(file):
    column_name = file.split("wc2.1_30s_")[1].replace(".tif", "")
    file_path = os.path.join(directory, file)
    print(f'Processing: {column_name}\n')

    with rasterio.open(file_path) as src:
        array = src.read(1)  
        df[column_name] = df.apply(lambda row: get_value_from_array(row['lat'], row['lon'], src, array), axis=1)

df = pd.read_csv('points.csv')

with ThreadPoolExecutor(max_workers=4) as executor:  
    executor.map(process_file, all_files)

df.to_csv('bio_vars.csv')