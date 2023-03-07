import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(layout="wide")

week_number = 26
weeks = range(1, week_number+1)
# weeks=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
year = 2023
raw_data = []
# @st.cache
def run_function():
    for week in weeks:
        
        # path = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2021-22/gws/gw%d.csv' % week
        # path = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2017-18/gws/gw%d.csv' % week
        path = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2022-23/gws/gw%d.csv' % week
        frame = pd.read_csv(path, encoding = "ISO-8859-1")
        st.write('week passed',week)
        frame ['week']= week
        frame ['year']= year
        raw_data.append(frame)

run_function()
df1 = pd.concat(raw_data, ignore_index=True)
df1=df1.rename(columns = {'element':'player_id'})
st.table(df1.head())
df1.to_csv('C:/Users/Darragh/Documents/Python/premier_league/raw_data_%d.csv' % year)

raw_data_xp = []
weeks=[1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24]
def run_function_xp():
    for week in weeks:
        # path = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2021-22/gws/gw%d.csv' % week
        # path = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2017-18/gws/gw%d.csv' % week
        path = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2022-23/gws/xP%d.csv' % week
        frame = pd.read_csv(path, encoding = "ISO-8859-1")
        st.write('week passed XP',week)
        frame ['week']= week
        frame ['year']= year
        raw_data_xp.append(frame)

run_function_xp()
df_xp = pd.concat(raw_data_xp, ignore_index=True)
df_xp=df_xp.rename(columns = {'id':'player_id'})
st.table(df_xp.head())
df_xp.to_csv('C:/Users/Darragh/Documents/Python/premier_league/raw_data_xp_%d.csv' % year)


# df1.to_csv('C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/raw_data_%d.csv' % year)

# Gotta figure out cache, the concat is causing issues now, need to back to streamlit and see how it works 
# 