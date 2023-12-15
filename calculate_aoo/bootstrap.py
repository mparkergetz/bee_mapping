import multiprocessing
import pandas as pd
import numpy as np
import math
import json
import os

def point_in_cell(lat, lon, lat_bounds, lon_bounds):
    return (lat_bounds[0] <= lat <= lat_bounds[1]) and (lon_bounds[0] <= lon <= lon_bounds[1])

def calculate_aoo(data_frame, grid_size):

    lat_min, lat_max = 23, 55
    lon_min, lon_max = -126, -66


    km_per_degree_latitude = 111  # Approximate value
    central_latitude = (lat_max + lat_min) / 2  # Central latitude for longitude calculation
    central_latitude_radians = math.radians(central_latitude)

    # Degree change for 100 km
    degree_change_latitude = grid_size / km_per_degree_latitude
    degree_change_longitude = grid_size / (km_per_degree_latitude * math.cos(central_latitude_radians))

    # Define the grid size
    lat_bins = np.arange(lat_min, lat_max, degree_change_latitude)
    lon_bins = np.arange(lon_min, lon_max, degree_change_longitude)

    occupied_cells = set()
    for index, row in data_frame.iterrows():
        lat, lon = row['lat'], row['long']
        for i in range(len(lat_bins) - 1):
            for j in range(len(lon_bins) - 1):
                lat_bounds = (lat_bins[i], lat_bins[i + 1])
                lon_bounds = (lon_bins[j], lon_bins[j + 1])
                if point_in_cell(lat, lon, lat_bounds, lon_bounds):
                    occupied_cells.add((i, j))
    return len(occupied_cells) * (grid_size ** 2)


def bootstrap_iteration(data, grid_size):

    sample = data.sample(len(data), replace=True)

    aoo = calculate_aoo(sample, grid_size) 
    return aoo

def parallel_bootstrap(data, grid_size, n_iterations):

    with multiprocessing.Pool() as pool:

        results = pool.starmap(bootstrap_iteration, [(data, grid_size)] * n_iterations)
    return results

def perform_bootstrapping_for_dfs(dataframes, df_names, grid_size, n_iterations):
    for i, df in enumerate(dataframes):
        print(f'Processing: {df_names[i]}')
        bootstrapped_results = parallel_bootstrap(df, grid_size, n_iterations)
        mean_aoo = np.mean(bootstrapped_results)
        std_aoo = np.std(bootstrapped_results)
        results = {
            'bootstrapped_results': bootstrapped_results,
            'mean_aoo': mean_aoo,
            'std_aoo': std_aoo
        }
        save_results_to_json(results, f'bootstrapping_results_{df_names[i]}.json')

def save_results_to_json(results, file_name):
    with open(file_name, 'w') as f:
        json.dump(results, f, indent=4)

n_iterations = 1000  
grid_size = 10

dir = 'df2csv'
files = os.listdir(dir)
file_paths = [os.path.join(dir, file) for file in files] 

dataframes = []
df_names = [] 

for file in file_paths:
    with open(file) as f:
        df = pd.read_csv(f)
        df_names.append(file.split('/')[-1][:-4])
        dataframes.append(df)


bootstrapped_results = perform_bootstrapping_for_dfs(dataframes, df_names, grid_size, n_iterations)

