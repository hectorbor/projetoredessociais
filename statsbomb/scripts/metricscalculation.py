import os 
import sys
import ast
import re
import pandas as pd
import numpy as np
import networkx as nx
from decimal import Decimal, getcontext
from matrixgenerator import matrixGenerator

class Country:
    def __init__(self, name):
        self.name = name
        self.matrices=[]
        self.totallinks=[]
        self.density=[]
        self.diameter=[]
        self.clustering=[]
        self.data=[]

if len(sys.argv) < 3:
    print("Usage: python matrixstocker.py <path_to_folder_with_games> <path_to_store_metrics>")
    sys.exit(1)

path_to_folder = sys.argv[1]
path_to_storage = sys.argv[2]

countrienames=[]

for filename in os.listdir(path_to_folder):
    full_path = os.path.join(path_to_folder, filename)
    country = re.search(r'game\d+matrix([A-Za-z ]+)\.csv', filename)
    if country.group(1).strip() not in countrienames:
        countrienames.append(country.group(1).strip())

countries=[]

for countryaux in countrienames:
    countries.append(Country(countryaux))

for countryaux in countries:
    gamecounter=1
    for filename in os.listdir(path_to_folder):
        currentcountry=re.search(r'game\d+matrix([A-Za-z ]+)\.csv', filename)
        #print(currentcountry.group(1).strip())
        if currentcountry.group(1).strip()==countryaux.name:
            full_path = os.path.join(path_to_folder, filename)
            loaded_matrix = np.loadtxt(full_path, delimiter=',')
            G=nx.from_numpy_array(loaded_matrix)
            countryaux.matrices.append(loaded_matrix)
            nedgesA=G.number_of_edges()
            countryaux.totallinks.append(nedgesA)
            densityA=nx.density(G)
            countryaux.density.append(densityA)
            diameterA=nx.diameter(G)
            countryaux.diameter.append(diameterA)
            #print("Is connected?", nx.is_connected(G))
            #print(diameterA)
            clusteringA=nx.average_clustering(G)
            countryaux.clustering.append(clusteringA)
            countryaux.data.append([countryaux.name,str(gamecounter),nedgesA,densityA,diameterA,clusteringA])
            gamecounter+=1

#print("country: "+countries[0].name)
#for clusterA in countries[0].clustering:
#    print("clustering: "+str(clusterA))
    

for countryaux in countries:
    #print(countryaux.totallinks)
    # averageLinks=sum(countryaux.totallinks) / len(countryaux.totallinks)
    # countryaux.totallinks.append(averageLinks)
    # averageDensity=sum(countryaux.density) / len(countryaux.density)
    # countryaux.density.append(averageDensity)
    # averageDiameter=sum(countryaux.density) / len(countryaux.diameter)
    # countryaux.diameter.append(averageDiameter) 
    # averageClustering=sum(countryaux.clustering) / len(countryaux.clustering)
    # countryaux.clustering.append(averageClustering)   
    # countryaux.data.append([countryaux.name,'Average',averageLinks,averageDensity,averageDiameter,averageClustering])
    averageLinks=np.mean(countryaux.totallinks)
    countryaux.totallinks.append(averageLinks)
    averageDensity=np.mean(countryaux.density)
    countryaux.density.append(averageDensity)
    averageDiameter=np.mean(countryaux.diameter)
    countryaux.diameter.append(averageDiameter) 
    averageClustering=np.mean(countryaux.clustering)
    countryaux.clustering.append(averageClustering)   
    countryaux.data.append([countryaux.name,'Average',averageLinks,averageDensity,averageDiameter,averageClustering])
    dfCountry = pd.DataFrame(countryaux.data, columns=['Country', 'Game', 'Total Links','Network Density', 'Diameter', 'Clustering Coefficient'])

        # print (resMatrices[0])
        # print (resMatrices[1])

generalData=[]

for countryaux in countries:
    countrylen=len(countryaux.totallinks)-1
    generalData.append([countryaux.name,countryaux.totallinks[countrylen],countryaux.density[countrylen],countryaux.diameter[countrylen],countryaux.clustering[countrylen]])

dfGeneral = pd.DataFrame(generalData, columns=['Country', 'Average Total Links','Average Network Density', 'Average Diameter', 'Average Clustering Coefficient'])

print(dfGeneral)
