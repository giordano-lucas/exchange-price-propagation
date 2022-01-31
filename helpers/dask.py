import os
import dask.dataframe as dd
from helpers import config
import dask 

def delete_files(files):
    for file in files:
        os.remove(file)
       
def merge_generated_files(generated_files,result_path):
    #generated_files = glob.glob(config["files"]["results"][signal]["dask_calculation"]["all_best_lags"].format("*"))
    generated_data = dd.read_csv(generated_files)
  
    generated_data.sort_values(["date"]).compute().to_csv(result_path)

def flatten(t):
    return [item for sublist in t for item in sublist]

def dask_compututation(promises,result_path):
    print("=== Computing promises ===")
    generated_files = dask.compute(promises)
    generated_files = flatten(list(generated_files))
    
    print(f"=== Merging {len(generated_files)} generated files ===")
    merge_generated_files(generated_files,result_path)
    
    print("=== Deleting files ===")
    delete_files(generated_files)