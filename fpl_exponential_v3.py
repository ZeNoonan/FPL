import pandas as pd
import numpy as np
import streamlit as st
from time import time
from pulp import *
#
start_uncached=time()

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
    load1_uncached=time()
    url_2020=prep_data(url1).copy()
    url_2019=prep_data(url2).copy()
    url_2018=prep_data(url3).copy()
    load2_uncached = time()
    pick_2020=pickle_data(raw1).copy()
    pick_2019=pickle_data(raw2).copy()
    pick_2018=pickle_data(raw3).copy()
    load3_uncached = time()
    players_2020 = load_data(url_2020,pick_2020)
    players_2019 = load_data(url_2019,pick_2019)
    players_2018 = load_data(url_2018,pick_2018)
    load4_uncached = time()
    players_2020=clean_format(players_2020)
    players_2019=clean_format(players_2019)
    load5_uncached = time()
    # players_2018_2020 = combine_df(players_2018, players_2019, players_2020)
    players_2018_2020 = pd.concat ([players_2018, players_2019, players_2020], axis=0,sort = True)
    load6_uncached = time()
    players_2018_2020=col_df(players_2018_2020)
    load7_uncached = time()
    cols_to_move = ['Name','Position','team','year','week','round','Cost','week_points','Expo_Pts','EWM_Pts','Clean_Pts','PPG_Total','points_per_game','Games_Total','minutes','Game_1',
    'Games_Total_Rolling', 'Games_Season_Total','Games_Season_Rolling','PPG_Total_Rolling','PPG_Season_Rolling','PPG_Total','PPG_Season_Total']
    cols = cols_to_move + [col for col in players_2018_2020 if col not in cols_to_move]
    players_2018_2020=players_2018_2020[cols]
    load8_uncached = time()
    st.table (players_2018_2020.head())
    finish_uncached = time()

    benchmark_uncached = (
        f"Cached. Total: {finish_uncached - load1_uncached:.2f}s"
        f" Load1: {load2_uncached - load1_uncached:.2f}"
        f" Load2: {load3_uncached - load2_uncached:.2f}"
        f" Load3: {load4_uncached - load3_uncached:.2f}"
        f" Load4: {load5_uncached - load4_uncached:.2f}"
        f" Load5: {load6_uncached - load5_uncached:.2f}"
        f" Load6: {load7_uncached - load6_uncached:.2f}"
        f" Load7: {load8_uncached - load7_uncached:.2f}"
        f" Load8: {finish_uncached - load8_uncached:.2f}"
        )
    st.text(benchmark_uncached)

##
@st.cache
def combine_df(x,y,z):   # Actually turns out that its faster not to do the function here so not using it
    players_2018_2020=pd.concat([x,y,z], axis=0, sort=True) # this is where the timer function came in handy from pbaumgartner
    return players_2018_2020

@st.cache
def prep_data(url):
    return pd.read_csv(url)

@st.cache
def pickle_data(pick_location):
    return pd.read_pickle(pick_location)
##
@st.cache
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

@st.cache
def clean_format(df):
    f=lambda x: x.rsplit('_',1)[0]    # not sure why i'm doing this I know why its cos there is numbers after name
    df['Name']=df['Name'].apply(f)
    return df

@st.cache
def col_df(df):
    df['Game_1'] = np.where((df['minutes'] > 0.5), 1, 0)
    df['Expo_Pts'] = df.groupby(['Name'])['week_points'].transform(lambda x: x.ewm(alpha=0.07).mean())
    df['Clean_Pts'] = np.where(df['Game_1']==1,df['week_points'], np.NaN)
    df = df.sort_values(by=['Name', 'year', 'week'], ascending=[True, True, True]) # THIS IS IMPORTANT!! EWM doesn't work right unless sorted
    df['EWM_Pts'] = df['Clean_Pts'].ewm(alpha=0.07).mean()
    df['Games_Season_Rolling'] = df.groupby (['Name', 'year'])['Game_1'].cumsum()
    df['Games_Season_Total'] = df.groupby (['Name', 'year'])['Game_1'].transform('sum')
    df['Games_Total_Rolling'] = df.groupby (['Name'])['Game_1'].cumsum()
    df['Games_Total'] = df.groupby (['Name'])['Game_1'].transform('sum')
    df['Points_Season_Rolling'] = df.groupby (['Name', 'year'])['week_points'].cumsum()
    df['Points_Season_Total'] = df.groupby (['Name', 'year'])['week_points'].transform('sum')
    df['Points_Total_Rolling'] = df.groupby (['Name'])['week_points'].cumsum()
    df['Points_Total'] = df.groupby (['Name'])['week_points'].transform('sum')
    df['PPG_Total'] = df['Points_Total'] / df['Games_Total']
    df['PPG_Season_Rolling'] = df['Points_Season_Rolling'] / df['Games_Season_Rolling']
    df['PPG_Total_Rolling'] = df['Points_Total_Rolling'] / df['Games_Total_Rolling']
    df['PPG_Season_Total'] = df['Points_Season_Total'] / df['Games_Season_Total']
    df["GK"] = (df["Position"] == 'GK').astype(float)
    df["DF"] = (df["Position"] == 'DF').astype(float)
    df["MD"] = (df["Position"] == 'MD').astype(float)
    df["FW"] = (df["Position"] == 'FW').astype(float)
    df["LIV"] = (df["team"] == 'Liverpool').astype(float)
    df["MC"] = (df["team"] == 'Man_City').astype(float)
    df['team'] = df['team'].map({1: 'Arsenal', 2: 'Aston_Villa', 3:'Bournemouth', 4:'Brighton',5:'Burnley',6:'Chelsea',7:'Crystal_Palace',
    8:'Everton',9:'Leicester',10:'Liverpool',11:'Man_City',12:'Man_Utd',13:'Newcastle',14:'Norwich',15:'Sheffield_Utd',16:'Southampton',17:'Spurs',
    18:'Watford',19:'West_Ham',20:'Wolves'})
    df=df.rename(columns = {'value':'Cost'})

    return df
######





main()