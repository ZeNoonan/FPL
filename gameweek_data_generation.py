import pandas as pd
import numpy as np
import streamlit as st

week_number = 5
weeks = range(1, week_number+1)
year = 2021
raw_data = []
# @st.cache
def run_function():
    for week in weeks:
        path = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2019-20/gws/gw%d.csv' % week
        frame = pd.read_csv(path, encoding = "ISO-8859-1")
        frame ['week']= week
        frame ['year']= year
        raw_data.append(frame)

run_function()
df1 = pd.concat(raw_data, ignore_index=True)
df1=df1.rename(columns = {'element':'player_id'})
st.table(df1.head())
df1.to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/raw_data_%d.pkl' % year)

# Gotta figure out cache, the concat is causing issues now, need to back to streamlit and see how it works 
# 