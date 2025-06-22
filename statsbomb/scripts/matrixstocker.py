import os 
import sys
import ast
import pandas as pd
import numpy as np
from matrixgenerator import matrixGenerator

if len(sys.argv) < 3:
    print("Usage: python matrixstocker.py <path_to_folder_with_games> <path_to_store_matrices>")
    sys.exit(1)

path_to_folder = sys.argv[1]
path_to_storage = sys.argv[2]

for filename in os.listdir(path_to_folder):
    full_path = os.path.join(path_to_folder, filename)
    if filename.startswith("game"):
        resMatrices=matrixGenerator(full_path)
        filename_storage1=filename.split('.')[0]+"matrix"+resMatrices[0]+".csv"
        filename_storage2=filename.split('.')[0]+"matrix"+resMatrices[1]+".csv"
        full_path_storage1= os.path.join(path_to_storage, filename_storage1)
        full_path_storage2= os.path.join(path_to_storage, filename_storage2)
        np.savetxt(full_path_storage1, resMatrices[2], delimiter=',')
        np.savetxt(full_path_storage2, resMatrices[3], delimiter=',')
        # print (resMatrices[0])
        # print (resMatrices[1])
        