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

# Change cost presentation to add decimal point 
# ISSUE WITH GW29 EWM selection not working but weighted ma is.  Very wierd.  GW29 updated 10 March not sure if issue with my data or code
# Issue is to do with the concat in table function wierd non unique in multi index maybe should upgrade pandas
# get presentation to add the other points in the columns
# would be nice to backtest some sort of strategy

def main():
    st.title ('FPL Optimisation')
    st.header('Summary')
    st.info("""
    **FPL Optimisation** is where the optimal team is selected based on points per game to date
    """)
    st.markdown( f"""Source Data: [2020 Player Info]({url1}), [2019 Player Info]({url2})
    """)
    load1_uncached=time()
    ##  
    # players_2018_2020 = combine_df(players_2018, players_2019, players_2020)
    # players_2018_2020 = pd.concat ([players_2018, players_2019, players_2020], axis=0,sort = True) ##this was quicker I found than using in a function
    load2_uncached = time()
    
    players_2018_2020=combine_functions().copy()
    
    # st.write(players_2018_2020.loc [ players_2018_2020['Name']=='jamie_vardy'])
    
    data = combine_functions()
    load3_uncached = time()
    year = st.sidebar.selectbox ("Select a year",(2020,2019))
    week = st.sidebar.number_input ("Select a week", 1,29, value=28) # update for week 29 when issue fixed I think theres an issue with week 29 although its wierd that EWM doesn't work
    squad_cost=st.sidebar.number_input ("Select how much you want to spend on 11 players", 80.0,100.0, value=83.0, step=.5)
    min_games_played = st.sidebar.number_input ("Minimum number of games played from start of 2019 Season", 1,150)
    min_current_season_games_played = st.sidebar.number_input("Minimum number of games played from start of current Season", 1,38)
    players_2018_2020=show_data(players_2018_2020, year, week, min_games_played, min_current_season_games_played)
    
    player_names=players_2018_2020['Name'].unique()
    names_selected = st.multiselect('Select which players you want excluded',player_names)
    players_2018_2020=exclude_players(players_2018_2020,names_selected)
    
    additional_info=players_2018_2020.loc[:,['Name','week','round', 'Games_Total','Games_Total_Rolling', 'Games_Season_Total', 'Games_Season_to_Date',
    'points_per_game']] 
    load4_uncached = time()

    select_pts=st.radio('Select the points you want to optimise',['EWM_Pts', 'Weighted_ma'])
    players=opt_data(players_2018_2020,select_pts)
    
    load5_uncached = time()
    F_3_5_2=optimise_fpl(3,5,2, squad_cost=squad_cost, fpl_players1=players, select_pts=select_pts)
    F_4_5_1=optimise_fpl(4,5,1, squad_cost=squad_cost, fpl_players1=players, select_pts=select_pts)
    F_4_4_2=optimise_fpl(4,4,2, squad_cost=squad_cost, fpl_players1=players, select_pts=select_pts)
    F_5_3_2=optimise_fpl(5,3,2, squad_cost=squad_cost, fpl_players1=players, select_pts=select_pts)
    F_5_4_1=optimise_fpl(5,4,1, squad_cost=squad_cost, fpl_players1=players, select_pts=select_pts)
    F_3_4_3=optimise_fpl(3,4,3, squad_cost=squad_cost, fpl_players1=players, select_pts=select_pts)
    formations=[F_3_5_2,F_4_5_1,F_4_4_2,F_5_3_2,F_5_4_1,F_3_4_3]

    load6_uncached = time()
    
    players=table(formations,select_pts)

    load7_uncached = time()
    players=pd.merge(players, additional_info, on='Name', how='left')
    load8_uncached = time()

    cols_to_move = ['Name','Position','Count','team',select_pts,'Cost','Games_Season_to_Date','F_3_5_2','F_4_5_1','F_4_4_2','F_5_3_2','F_5_4_1','F_3_4_3','Games_Total_Rolling',
    'week','round','Games_Total', 'Games_Season_Total','points_per_game']
    cols = cols_to_move + [col for col in players if col not in cols_to_move]
    players=players[cols]
    format_dict = {'EWM_Pts':'{0:,.1f}','PPG_Season_Rolling':'{0:,.1f}','Weighted_ma':'{0:,.1f}','Cost':'£{0:,.1f}m'}

    st.write(players.style.format(format_dict))
    # st.write(data.loc [ data['Name']=='jamie_vardy'])

    st.write (cost_total(players,selection1='Cost', selection2=select_pts))

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

@st.cache
def cost_total(df,selection1,selection2):
    cols=['F_3_5_2','F_4_5_1','F_4_4_2','F_5_3_2','F_5_4_1','F_3_4_3']
    cost=[]
    points=[]
    for n in cols:
        df[n]=(df[n]>0).astype(int)
        x=((df[selection1]*df[n]).sum())
        y=((df[selection2]*df[n]).sum())
        cost.append(x)
        points.append(y)
    # df=pd.DataFrame([cost], columns=cols) #https://stackoverflow.com/questions/50874117/pandas-dataframe-shape-of-passed-values-is-1-4-indices-imply-4-4
    df1=pd.concat([pd.DataFrame([cost],columns=cols,index=['Cost']), pd.DataFrame([points],columns=cols, index=['Points'])], axis=0)
    df1.loc['Cost']=df1.loc['Cost'].apply('£{0:,.1f}m'.format)
    df1.loc['Points']=df1.loc['Points'].apply('{0:,.1f}'.format)
    return df1

def exclude_players(df, *args):
    for x in args:
        df.loc [ (df['Name'].isin(x)), 'Cost' ] = 1000 # for some reason isin worked rather than == sometime to do with lengths dont match 
    return df # think it might be do with == returns a value dont know



def show_data(df, year, week, min_games_played, season_games_played):
    # df=df.copy()
    return df [ (df['year']==year) & (df['week']==week) & (df['Games_Total_Rolling'] >= min_games_played) & (df['Games_Season_to_Date'] >= season_games_played) ]

#
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

# https://stackoverflow.com/questions/40994756/pandas-rolling-and-ewm-to-completely-ignore-na-and-use-last-n-valid-data
# https://stackoverflow.com/questions/9621362/how-do-i-compute-a-weighted-moving-average-using-pandas

@st.cache
def col_df(df):
    df['Game_1'] = np.where((df['minutes'] > 0.5), 1, 0)
    # df['Expo_Pts'] = df.groupby(['Name'])['week_points'].transform(lambda x: x.ewm(alpha=0.07).mean())
    df['Clean_Pts'] = np.where(df['Game_1']==1,df['week_points'], np.NaN) # setting a slice on a slice - just suppresses warning....
    df = df.sort_values(by=['Name', 'year', 'week'], ascending=[True, True, True]) # THIS IS IMPORTANT!! EWM doesn't work right unless sorted
    df['EWM_Pts'] = df['Clean_Pts'].ewm(alpha=0.07).mean()

    weights = np.array([0.125, 0.25,0.5,1]) # the order mattered!! took me a while to figure this out
    sum_weights = np.sum(weights)
    df['Weighted_ma'] = (df['Clean_Pts'].fillna(0).rolling(window=4, center=False)\
        .apply(lambda x: np.sum(weights*x) / sum_weights, raw=False)) # raw=False
        # using the fillna ensures no NaN as this function requires min 4 data points in a row - .fillna(method='ffill')
        # so just be careful the result is the last time player had 4 weeks in a row

    df['Games_Season_to_Date'] = df.groupby (['Name', 'year'])['Game_1'].cumsum()
    df['Games_Season_Total'] = df.groupby (['Name', 'year'])['Game_1'].transform('sum')
    df['Games_Total_Rolling'] = df.groupby (['Name'])['Game_1'].cumsum()
    df['Games_Total'] = df.groupby (['Name'])['Game_1'].transform('sum')
    df['Points_Season_Rolling'] = df.groupby (['Name', 'year'])['week_points'].cumsum()
    df['Points_Season_Total'] = df.groupby (['Name', 'year'])['week_points'].transform('sum')
    df['Points_Total_Rolling'] = df.groupby (['Name'])['week_points'].cumsum()
    df['Points_Total'] = df.groupby (['Name'])['week_points'].transform('sum')
    df['PPG_Total'] = df['Points_Total'] / df['Games_Total']
    df['PPG_Season_Rolling'] = df['Points_Season_Rolling'] / df['Games_Season_to_Date']
    df['PPG_Total_Rolling'] = df['Points_Total_Rolling'] / df['Games_Total_Rolling']
    df['PPG_Season_Total'] = df['Points_Season_Total'] / df['Games_Season_Total']
    df["GK"] = (df["Position"] == 'GK').astype(float)
    df["DF"] = (df["Position"] == 'DF').astype(float)
    df["MD"] = (df["Position"] == 'MD').astype(float)
    df["FW"] = (df["Position"] == 'FW').astype(float)
    df['team'] = df['team'].map({1: 'Arsenal', 2: 'Aston_Villa', 3:'Bournemouth', 4:'Brighton',5:'Burnley',6:'Chelsea',7:'Crystal_Palace',
    8:'Everton',9:'Leicester',10:'Liverpool',11:'Man_City',12:'Man_Utd',13:'Newcastle',14:'Norwich',15:'Sheffield_Utd',16:'Southampton',17:'Spurs',
    18:'Watford',19:'West_Ham',20:'Wolves'})
    df["LIV"] = (df["team"] == 'Liverpool').astype(float)
    df["MC"] = (df["team"] == 'Man_City').astype(float)
    df2=df.rename(columns = {'value':'Cost'})

    return df2

# @st.cache
def opt_data(x,select_pts):
    return x[['Name', 'Position','team', select_pts, 'Cost','GK','DF','MD','FW','LIV','MC']].reset_index().drop('index', axis=1)

def optimise_fpl(df,md,fw,fpl_players1,squad_cost,select_pts,number_players=11):
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
        total_points[decision_var] = player[select_pts] 
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

@st.cache
def table(x,select_pts): #Honestly don't understand why GW29 is messing up the multiindex just for EWM. The moving average works fine  just wait until GW29 is rerun?
    # https://stackoverflow.com/questions/55652704/merge-multiple-dataframes-pandas
    dfs = [df.set_index(['Name','Position','team',select_pts,'Cost']) for df in x]
    a=pd.concat(dfs,axis=1).reset_index() # issue is not reset index
    a=a.loc[:,['Name','Position','team',select_pts,'Cost','is_drafted']]
    a.columns=['Name','Position','team',select_pts,'Cost','F_3_5_2','F_4_5_1','F_4_4_2','F_5_3_2','F_5_4_1','F_3_4_3']
    a['Pos'] = a['Position'].map({'GK': 1, 'DF': 2, 'MD':3, 'FW':4})
    a['Count']=a.loc[:,'F_3_5_2':'F_3_4_3'].count(axis=1)
    cols=['F_3_5_2','F_4_5_1','F_4_4_2','F_5_3_2','F_5_4_1','F_3_4_3']
    for n in cols:
        a[n]=(a[n]>0).astype(int) # to clean up the NaN
    a=a.sort_values(by=['Pos','Count'],ascending=[True,False])
    return a

@st.cache
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
    players_2018_2020['Cost']=players_2018_2020['Cost']/10
    return players_2018_2020




main()
