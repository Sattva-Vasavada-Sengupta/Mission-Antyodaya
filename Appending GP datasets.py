import os
import pandas as pd
import glob

path = os.getcwd()
filenames = glob.glob(path + "\*.csv")

df_to_append = pd.DataFrame()
for file in filenames:
    df = pd.read_csv(file)
    df_to_append = pd.concat([df_to_append, df], axis = 0)    
    
df_to_append.to_csv("gp_appended_1.csv")
