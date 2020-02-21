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
    # url_2020=prep_data(url1).copy()
    # url_2019=prep_data(url2).copy()
    # url_2018=prep_data(url3).copy()
    load2_uncached = time()
    # pick_2020=pickle_data(raw1).copy()
    # pick_2019=pickle_data(raw2).copy()
    # pick_2018=pickle_data(raw3).copy()
    load3_uncached = time()
    # players_2020 = pd.merge(url_2020,pick_2020, on='player_id')
    # players_2019 = pd.merge(url_2019,pick_2019, on='player_id')
    # players_2018 = pd.merge(url_2018,pick_2018, on='player_id')
    load4_uncached = time()
    # players_2020=clean_format(players_2020)
    # players_2019=clean_format(players_2019)
    load5_uncached = time()
    # players_2018_2020 = combine_df(players_2018, players_2019, players_2020)
    # players_2018_2020 = pd.concat ([players_2018, players_2019, players_2020], axis=0,sort = True) ##this was quicker I found than using in a function
    # st.table (players_2018_2020.head())
    load6_uncached = time()
    # players_2018_2020=col_df(players_2018_2020)
    # st.table (players_2018_2020.head())

    players_2018_2020=combine_functions()

    load7_uncached = time()
    year = st.selectbox ("Select a year",(2019,2020))
    week = st.slider ("Select a week", 1,26)
    min_games_played = st.slider ("Minimum number of games played", 1,150)
    players_2018_2020=show_data(players_2018_2020, year, week, min_games_played)
    additional_info=players_2018_2020.loc[:,['Name','week','round', 'Games_Total','Games_Total_Rolling', 'Games_Season_Total', 'Games_Season_Rolling']] 
    # cols_to_move = ['Name','Position','team','year','week','round','Cost','week_points','EWM_Pts','Clean_Pts','PPG_Total','points_per_game','Games_Total','minutes','Game_1',
    # 'Games_Total_Rolling', 'Games_Season_Total','Games_Season_Rolling','PPG_Total_Rolling','PPG_Season_Rolling','PPG_Total','PPG_Season_Total']
    # cols = cols_to_move + [col for col in players_2018_2020 if col not in cols_to_move]
    # players_2018_2020=players_2018_2020[cols]
    load8_uncached = time()
    players=opt_data(players_2018_2020)
    # st.table (players_2018_2020.head(3))
    # st.table (players.sort_values(by='Cost', ascending=False).head())

    F_3_5_2=optimise_fpl(3,5,2, players)
    F_4_5_1=optimise_fpl(4,5,1, players)
    F_4_4_2=optimise_fpl(4,4,2, players)
    F_5_3_2=optimise_fpl(5,3,2, players)
    F_5_4_1=optimise_fpl(5,4,1, players)
    F_3_4_3=optimise_fpl(3,4,3, players)
    formations=[F_3_5_2,F_4_5_1,F_4_4_2,F_5_3_2,F_5_4_1,F_3_4_3]
    
    col_df(players_2018_2020)
    players=table(formations)
    players=pd.merge(players, additional_info, on='Name', how='left')

    cols_to_move = ['Name','Position','Count','team','EWM_Pts','Cost','F_3_5_2','F_4_5_1','F_4_4_2','F_5_3_2','F_5_4_1','F_3_4_3','Games_Total_Rolling',
    'week','round','Games_Season_Rolling','Games_Total', 'Games_Season_Total']
    cols = cols_to_move + [col for col in players if col not in cols_to_move]
    players=players[cols]
    
    st.table(players)
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

def show_data(df, year, week, min_games_played):
    return df [ (df['year']==year) & (df['week']==week) & (df['Games_Total_Rolling'] > min_games_played) ]


# @st.cache
def combine_df(x,y,z):   # Actually turns out that its faster not to do the function here so not using it
    players_2018_2020=pd.concat([x,y,z], axis=0, sort=True) # this is where the timer function came in handy from pbaumgartner
    return players_2018_2020

@st.cache
def prep_data(url):
    players_raw = pd.read_csv(url)
    players_raw=players_raw.rename(columns = {'id':'player_id'})
    players_raw1=players_raw.loc[:,['player_id','element_type','team','points_per_game' ]]
    players_raw1=players_raw1.rename(columns = {'element_type':'Position'})
    players_raw1['Position'] = players_raw1['Position'].map({1: 'GK', 2: 'DF', 3:'MD', 4:'FW'})
    return players_raw1

@st.cache
def pickle_data(pick_location):
    df1 = pd.read_pickle(pick_location)
    df1=df1.rename(columns = {'name':'Name','total_points':'week_points'})
    df1['Name']=df1['Name'].str.lower()
    return df1

@st.cache
def clean_format(df):
    f=lambda x: x.rsplit('_',1)[0]    # not sure why i'm doing this I know why its cos there is numbers after name
    df['Name']=df['Name'].apply(f)
    return df

@st.cache
def col_df(df):
    df['Game_1'] = np.where((df['minutes'] > 0.5), 1, 0)
    # df['Expo_Pts'] = df.groupby(['Name'])['week_points'].transform(lambda x: x.ewm(alpha=0.07).mean())
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
    df2=df.rename(columns = {'value':'Cost'})

    return df2

def opt_data(x):
    return x[['Name', 'Position','team', 'EWM_Pts', 'Cost','GK','DF','MD','FW','LIV','MC']].reset_index().drop('index', axis=1)

def optimise_fpl(df,md,fw,fpl_players1,squad_cost=830,number_players=11):
    model = pulp.LpProblem("FPL", pulp.LpMaximize)
    total_points = {}
    cost = {}
    GKs = {}
    DFs = {}
    MDs = {}
    FWs = {}
    LIVs= {}
    MCs={}
    number_of_players = {}
    for i, player in fpl_players1.iterrows(): # HERE
        var_name = 'x' + str(i) 
        decision_var = pulp.LpVariable(var_name, cat='Binary')
        total_points[decision_var] = player["EWM_Pts"] 
        cost[decision_var] = player["Cost"] 
        GKs[decision_var] = player["GK"]
        DFs[decision_var] = player["DF"]
        MDs[decision_var] = player["MD"]
        FWs[decision_var] = player["FW"]
        LIVs[decision_var] = player["LIV"]
        MCs[decision_var] = player["MC"]
        number_of_players[decision_var] = 1.0
    objective_function = pulp.LpAffineExpression(total_points)
    model += objective_function
    total_cost = pulp.LpAffineExpression(cost)
    model += (total_cost <= squad_cost)
    GK_constraint = pulp.LpAffineExpression(GKs)
    DF_constraint = pulp.LpAffineExpression(DFs)
    MD_constraint = pulp.LpAffineExpression(MDs)
    FW_constraint = pulp.LpAffineExpression(FWs)
    LIV_constraint = pulp.LpAffineExpression(LIVs)
    MC_constraint = pulp.LpAffineExpression(MCs)
    total_players = pulp.LpAffineExpression(number_of_players)
    model += (GK_constraint == 1)
    model += (DF_constraint == df)
    model += (MD_constraint == md)
    model += (FW_constraint == fw)
    model += (LIV_constraint <= 3)
    model += (MC_constraint <= 3)
    model += (total_players <= number_players)
    model.solve()
    fpl_players1["is_drafted"] = 0.0 # HERE
    for var in model.variables():
        # st.write('this is the var', var)
        fpl_players1.iloc[int(var.name[1:]),11] = var.varValue # HERE
    return (fpl_players1[fpl_players1["is_drafted"] == 1.0]).sort_values(['GK','DF','MD','FW'], ascending=False)

def table(x):
    # https://stackoverflow.com/questions/55652704/merge-multiple-dataframes-pandas
    dfs = [df.set_index(['Name','Position','team','EWM_Pts','Cost']) for df in x]
    a=pd.concat(dfs,axis=1).reset_index()
    a=a.loc[:,['Name','Position','team','EWM_Pts','Cost','is_drafted']]
    a.columns=['Name','Position','team','EWM_Pts','Cost','F_3_5_2','F_4_5_1','F_4_4_2','F_5_3_2','F_5_4_1','F_3_4_3']
    a['Pos'] = a['Position'].map({'GK': 1, 'DF': 2, 'MD':3, 'FW':4})
    a['Count']=a.loc[:,'F_3_5_2':'F_3_4_3'].count(axis=1)
    cols=['F_3_5_2','F_4_5_1','F_4_4_2','F_5_3_2','F_5_4_1','F_3_4_3']
    for n in cols:
        a[n]=(a[n]>0).astype(int) # to clean up the NaN
    a=a.sort_values(by=['Pos','Count'],ascending=[True,False])
    return a

def combine_functions():
    url_2020=prep_data(url1).copy()
    url_2019=prep_data(url2).copy()
    url_2018=prep_data(url3).copy()
    pick_2020=pickle_data(raw1).copy()
    pick_2019=pickle_data(raw2).copy()
    pick_2018=pickle_data(raw3).copy()
    players_2020 = pd.merge(url_2020,pick_2020, on='player_id')
    players_2019 = pd.merge(url_2019,pick_2019, on='player_id')
    players_2018 = pd.merge(url_2018,pick_2018, on='player_id')
    players_2020=clean_format(players_2020)
    players_2019=clean_format(players_2019)
    players_2018_2020 = pd.concat ([players_2018, players_2019, players_2020], axis=0,sort = True)
    players_2018_2020=col_df(players_2018_2020)
    return players_2018_2020

main()