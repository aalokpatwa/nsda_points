#!/usr/bin/env python
# coding: utf-8

# In[105]:


import os
import pandas as pd
import numpy as np

#Provide the path to the competitor's entries
CSV_PATH = "insert_path_here"

#Provide the path to the location where the output DataFrame will be saved.
OUTPATH = "insert_path_here"

#Provide a list of names of the coaches who have ever entered points for this competitor.
#This is necessary because of a bug in the NSDA entries csv
#The entries contain commas between ranks, so the csv puts them in separate columns
#So, there cannot be an absolute way to find the column with the points -- it must be relative
#However, in all cases, the points come right after the coaches' name.
COACHLIST = ["Coach 1", "Coach 2", "Coach 3"]

#Read the entries CSV into a dataframe
df = pd.read_csv(CSV_PATH, delimiter=",")

#Create an "empty" DataFrame to hold the points tallies
tally_df = pd.DataFrame(index=[0])

#Iterate through all of the competitor's entries and see what unique events they have done
for index in range(len(df.index)):
    category = str(df.at[index, "Category"])
    
    #The entries csv has a bug where some extra rows are included
    if category == "nan":
        continue
        
    #The NSDA sometimes splits up regular tournaments and NSDA-sponsored tournaments
    #This step treats them the same in the final tally.
    if "(" in category:
        category = category.split(" (")[0]
        
    #If a new category is discovered, create a new column for it.
    if category not in tally_df.columns:
        tally_df[category] = 0
        
#Iterate again over all of the tournaments. 
for index in range(len(df.index)):
    category = str(df.at[index, "Category"])
    if "(" in category:
        category = category.split(" (")[0]
        
    #Iterate through each column in this row to find the column with the points
    for column in range(len(df.columns)):
        current_cell = df.at[index, df.columns[column]]
        if str(current_cell) in COACHLIST:
            points_column = int(column + 1)
            points_str = df.columns[points_column]
            break
    
    #How many points were given for this tournament?
    try:        
        points_for_this_event = int(df.at[index, points_str])

    #Catch all exceptions in accessing the DataFrame
    except:
        continue
    
    #Add these new points to the ongoing tally
    tally_df.at[0, category] += points_for_this_event

#Save as a csv
tally_df.to_csv(OUTPATH, index=False)

