import os
import dask.dataframe as dd
from helpers import config

def delete_files(files):
    for file in files:
        os.remove(file)
       
def merge_generated_files(generated_files,preprocessing_steps=[]):
    #generated_files = glob.glob(config["files"]["results"][signal]["dask_calculation"]["all_best_lags"].format("*"))
    generated_data = dd.read_csv(generated_files)
    
    final_result_path = config["files"]["results"][signal]["all_best_lags"]\
                    .format("_".join(preprocessing_steps))
    generated_data.sort_values(["date"]).compute().to_csv(final_result_path)

def flatten(t):
    return [item for sublist in t for item in sublist]

def dask_compututation(promises):
    generated_files = dask.compute(promises)
    
    generated_files = flatten(list(generated_files))
    
    merge_generated_files(generated_files,preprocessing_steps)
    
    delete_files(generated_files)