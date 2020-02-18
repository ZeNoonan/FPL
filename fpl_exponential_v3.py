import pandas as pd
import numpy as np
import streamlit as st
from time import time
from pulp import *

url1='https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2019-20/players_raw.csv'
url2='https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2018-19/players_raw.csv'
url3='https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2017-18/players_raw.csv'
raw1='raw_data_2020.pkl'
raw2='raw_data_2019.pkl'
raw3='raw_data_2018.pkl'

def main():
    st.title ('FPL Optimisation')
    st.header('Summary')
    st.info("""
    **FPL Optimisation** is where the optimal team is selected based on points per game to date
    """)
    st.markdown( f"""Source Data: [2020 Player Info]({url1}), [2019 Player Info]({url2})
    """)


@st.cache
def prep_data(url):
    return pd.read_csv(url)

@st.cache
def pickle_data(pick_location):
    return pd.read_pickle(pick_location)

start_uncached=time()

url_2020=prep_data(url1).copy()
url_2019=prep_data(url2).copy()
url_2018=prep_data(url3).copy()
pick_2020=pickle_data(raw1).copy()
pick_2019=pickle_data(raw2).copy()
pick_2018=pickle_data(raw3).copy()

load1_uncached=time()


def load_data(url, pick_location):
    players_raw=url
    players_raw=players_raw.rename(columns = {'id':'player_id'})
    players_raw1=players_raw.loc[:,['player_id','element_type','team','points_per_game' ]]
    df1=pick_location
    data=pd.merge(df1,players_raw1, on='player_id')
    players=data
    players=players.rename(columns = {'element_type':'Position', 'total_points':'week_points'})
    players['Position'] = players['Position'].map({1: 'GK', 2: 'DF', 3:'MD', 4:'FW'})
    players['name']=players['name'].str.lower()
    players=players.rename(columns = {'name':'Name'})
    return players

load2_uncached = time()

players_2020 = load_data(url_2020,pick_2020)
players_2019 = load_data(url_2019,pick_2019)
players_2018 = load_data(url_2018,pick_2018)
# # players_2017 = load_data('https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2016-17/players_raw.csv','raw_data_2017.pkl')

load3_uncached = time()

f=lambda x: x.rsplit('_',1)[0]
players_2019['Name']=players_2019['Name'].apply(f)
players_2020['Name']=players_2020['Name'].apply(f)  # not sure why i'm doing this I know why its cos there is numbers after name

players_2018_2020 = pd.concat ([players_2018, players_2019, players_2020], axis=0,sort = True)
players_2018_2020['Game_1'] = np.where((players_2018_2020['minutes'] > 0.5), 1, 0)
players_2018_2020['Expo_Pts'] = players_2018_2020.groupby(['Name'])['week_points'].transform(lambda x: x.ewm(alpha=0.07).mean())

players_2018_2020['Clean_Pts'] = np.where(players_2018_2020['Game_1']==1,players_2018_2020['week_points'], np.NaN)
players_2018_2020 = players_2018_2020.sort_values(by=['Name', 'year', 'week'], ascending=[True, True, True]) # THIS IS IMPORTANT!! EWM doesn't work right unless sorted
players_2018_2020['EWM_Pts'] = players_2018_2020['Clean_Pts'].ewm(alpha=0.07).mean()

players_2018_2020['Games_Season_Rolling'] = players_2018_2020.groupby (['Name', 'year'])['Game_1'].cumsum()
players_2018_2020['Games_Season_Total'] = players_2018_2020.groupby (['Name', 'year'])['Game_1'].transform('sum')
players_2018_2020['Games_Total_Rolling'] = players_2018_2020.groupby (['Name'])['Game_1'].cumsum()
players_2018_2020['Games_Total'] = players_2018_2020.groupby (['Name'])['Game_1'].transform('sum')

players_2018_2020['Points_Season_Rolling'] = players_2018_2020.groupby (['Name', 'year'])['week_points'].cumsum()
players_2018_2020['Points_Season_Total'] = players_2018_2020.groupby (['Name', 'year'])['week_points'].transform('sum')
players_2018_2020['Points_Total_Rolling'] = players_2018_2020.groupby (['Name'])['week_points'].cumsum()
players_2018_2020['Points_Total'] = players_2018_2020.groupby (['Name'])['week_points'].transform('sum')

players_2018_2020['PPG_Total'] = players_2018_2020['Points_Total'] / players_2018_2020['Games_Total']
players_2018_2020['PPG_Season_Rolling'] = players_2018_2020['Points_Season_Rolling'] / players_2018_2020['Games_Season_Rolling']
players_2018_2020['PPG_Total_Rolling'] = players_2018_2020['Points_Total_Rolling'] / players_2018_2020['Games_Total_Rolling']
players_2018_2020['PPG_Season_Total'] = players_2018_2020['Points_Season_Total'] / players_2018_2020['Games_Season_Total']

st.table (players_2018_2020.head())

load4_uncached = time()

finish_uncached = time()

benchmark_uncached = (
    f"Cached. Total: {finish_uncached - load1_uncached:.2f}s"
    f" Load1: {load2_uncached - load1_uncached:.2f}"
    f" Load2: {load3_uncached - load2_uncached:.2f}"
    f" Load3: {load4_uncached - load3_uncached:.2f}"
    # f" Load5: {load5_uncached - load4_uncached:.2f}"
    # f" Load6: {load6_uncached - load5_uncached:.2f}"
    # f" Load7: {load7_uncached - load6_uncached:.2f}"
    # f" Load8: {finish_uncached - load7_uncached:.2f}"
    )
st.text(benchmark_uncached)

main()