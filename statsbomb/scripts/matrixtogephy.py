import os 
import sys
import ast
import pandas as pd
import numpy as np
from matrixgenerator import matrixGenerator

if len(sys.argv) < 3:
    print("Usage: python matrixstocker.py <path_to_folder_with_games> <path_to_store_gephi>")
    sys.exit(1)

path_to_folder = sys.argv[1]
path_to_storage = sys.argv[2]

for filename in os.listdir(path_to_folder):
    full_path = os.path.join(path_to_folder, filename)
    filename_storage=filename.split('.')[0]+"gephi"+".csv"
    full_path_storage= os.path.join(path_to_storage, filename_storage)
    loaded_matrix = np.loadtxt(full_path, delimiter=',')       
    labels = [str(i) for i in range(loaded_matrix.shape[0])]
    df = pd.DataFrame(loaded_matrix, index=labels, columns=labels) 
    df.to_csv(full_path_storage)
        # print (resMatrices[0])
        # print (resMatrices[1])