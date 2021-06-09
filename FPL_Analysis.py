from io import BytesIO

import numpy as np
import pandas as pd
import requests
from PIL import Image
from pulp import *

import streamlit as st

st.set_page_config(layout='wide')
current_week = 38

url2021 = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2020-21/players_raw.csv'
url2020 = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2019-20/players_raw.csv'
url2019 = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2018-19/players_raw.csv'
url2018 = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2017-18/players_raw.csv'
fantasy_url = 'https://fantasy.premierleague.com'
pick2021 = 'https://github.com/ZeNoonan/FPL/blob/master/raw_data_2021.pkl?raw=true'
pick2020 = 'https://github.com/ZeNoonan/FPL/blob/master/raw_data_2020.pkl?raw=true'
pick2019 = 'https://github.com/ZeNoonan/FPL/blob/master/raw_data_2019.pkl?raw=true'
pick2018 = 'https://github.com/ZeNoonan/FPL/blob/master/raw_data_2018.pkl?raw=true'
# https://stackoverflow.com/questions/61786481/why-cant-i-read-a-joblib-file-from-my-github-repo
# https://stackoverflow.com/questions/50777849/from-conda-create-requirements-txt-for-pip3

def main():
    """
    Main function
    """
    st.title ('FPL Lineup Optimisation')
    st.info("""
    This app helps you select the optimal line-up for your fantasy football team for the Premier League ⚽.
    """)
    # use double space for new line in markdown
    st.markdown(f"""See link [here]({fantasy_url}) to game""")
    st.markdown("""
    Using historical points, we can calculate the optimal line up selection to maximise the points based on certain constraints.  
    The output of this app is a table showing the optimal fantasy line-up.
    """)
    # https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json
    st.markdown(f"""Source Data: [2021 Player Info]({url2021}))
    """)
    image=get_image()
    st.sidebar.image(image, use_column_width=True)

    data_2021 = (data_2021_team_names( (prep_base_data(url2021, pick2021)).rename(columns = {'team_x':'team'}))).copy()
    data_2020 = (data_2020_team_names( (prep_base_data(url2020, pick2020)).copy() )).copy()
    data_2019 = (data_2019_team_names( (prep_base_data(url2019, pick2019)).copy() )).copy()
    data_2018 = (data_2018_team_names( (prep_base_data(url2018, pick2018)).copy() )).copy()
    data_2020 = (data_2020_clean_double_gw(data_2020)).copy()

    # st.write('2021 check for GW30',data_2021)

    all_seasons_df = (column_calcs( (combine_dataframes(data_2018,data_2019,data_2020,data_2021)).reset_index().copy() )).copy() # have added reset index duplicates in index?
    

    year = st.sidebar.selectbox("Select a year",(2021,2020,2019,2018))
    st.sidebar.header("1. Select FPL Game Week.")
    week = st.sidebar.number_input ("Select period from GW1 up to GW user select", min_value=int(0),max_value=int(38.0), value=int(current_week-1)) 
    st.sidebar.header("2. Squad Cost")
    squad_cost=st.sidebar.number_input ("Select how much you want to spend on 11 players", 80.0,100.0, value=82.0, step=.5)
    st.sidebar.header("3. Min Number of Games Played by Player")
    min_games_played = st.sidebar.number_input ("Minimum number of games played in last 10 games", min_value=int(0),max_value=int(10),value=int(1))
    min_current_season_games_played = st.sidebar.number_input("Minimum number of games played from start of current Season",
    min_value=int(0),max_value=int(38), value=int(15))

    data=show_data(all_seasons_df, year, week, min_games_played, min_current_season_games_played)    
    player_names=data['full_name'].unique()
    names_selected = st.multiselect('Select which players you want excluded from lineup (e.g. due to injuries or suspension)',player_names)
    data_1=exclude_players(data,names_selected)
    additional_info=data_1.loc[:,['full_name','week', 'Games_Total','Games_Total_Rolling', 'Gms_Ssn_Total','Games_Ssn_Rmg', 'Gms_Ssn_to_Date',
    'points_per_game','Pts_Sn_Rllg_Rnk','Pts_Sn_Rllg_Rmg_Rnk','Pts_Rllg_Rnk_Diff','PPG_Sn_Rllg','PPG_Sn_Rmg','PPG_Sn_Rllg_Rnk','PPG_Sn_Rllg_Rmg_Rnk','PPG_Rllg_Rnk_Diff',
    'last_10_games_total','last_10_points_total','Pts_Sn_Rllg','Pts_Sn_Rmg',]]

    st.sidebar.header("4. Optimise on which Points")
    select_pts=st.sidebar.radio('Select the points you want to optimise',['PPG_Sn_Rllg','PPG_Sn_Rmg','Pts_Sn_Rmg','Pts_Sn_Rllg','Points_Season_Total', 'ppg_last_10_games','PPG_Total'])
    data_2=opt_data(data_1,select_pts)

    F_3_5_2=optimise_fpl(3,5,2, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_4_5_1=optimise_fpl(4,5,1, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_4_4_2=optimise_fpl(4,4,2, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_5_3_2=optimise_fpl(5,3,2, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_5_4_1=optimise_fpl(5,4,1, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_3_4_3=optimise_fpl(3,4,3, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_5_2_3=optimise_fpl(5,2,3, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_4_3_3=optimise_fpl(4,3,3, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    formations=[F_3_5_2,F_4_5_1,F_4_4_2,F_5_3_2,F_5_4_1,F_3_4_3,F_5_2_3,F_4_3_3]

    data_3=table(formations,select_pts)
    data_4=pd.merge(data_3, additional_info, on='full_name', how='left',suffixes=('', '_y'))
    cols_to_move = ['full_name','Position','Count','team','Price','Gms_Ssn_to_Date','Games_Ssn_Rmg','Pts_Sn_Rllg','Pts_Sn_Rllg_Rnk','Pts_Sn_Rmg','Pts_Sn_Rllg_Rmg_Rnk',
    'PPG_Sn_Rllg','PPG_Sn_Rllg_Rnk','PPG_Sn_Rmg','PPG_Sn_Rllg_Rmg_Rnk','PPG_Rllg_Rnk_Diff',
    'last_10_points_total','last_10_games_total','Value','Gms_Ssn_Total','F_3_4_3','F_4_3_3','F_3_5_2','F_4_5_1',
    'F_4_4_2','F_5_3_2','F_5_4_1','F_5_2_3','Games_Total_Rolling','week','points_per_game']
    cols = cols_to_move + [col for col in data_4 if col not in cols_to_move]
    data_5=data_4[cols]

    format_dict = {'EWM_Pts':'{0:,.1f}','PPG_Season_Total':'{0:,.1f} ppg','Weighted_ma':'{0:,.1f}','Points_Season_Total':'{0:,.0f}',
    'points_per_game':'{0:,.1f}','Price':'£{0:,.1f}m','PPG_Sn_Rmg':'{0:,.1f}','Gms_Ssn_Total':'{0:,.0f}','last_10_games_total':'{0:,.0f}',
    'ppg_last_10_games':'{0:,.1f}','Value':'{0:,.2f}','last_10_points_total':'{0:,.0f}','PPG_Sn_Rllg':'{0:,.1f}','Price':'{0:,.1f}',
    'Pts_Sn_Rllg':'{0:,.0f}','Pts_Sn_Rllg_Rnk':'{0:,.0f}','Pts_Sn_Rllg_Rmg_Rnk':'{0:,.0f}','PPG_Sn_Rllg_Rmg_Rnk':'{0:,.0f}','PPG_Rllg_Rnk_Diff':'{0:,.0f}',
    'Pts_Sn_Rmg':'{0:,.0f}','Pts_Rllg_Rnk_Diff':'{0:,.0f}','PPG_Sn_Rllg_Rnk':'{0:,.0f}','Games_Ssn_Rmg':'{0:,.0f}','week':'{0:,.0f}'}

    data_5=data_5.reset_index(drop=True)  # https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-dataframe cos of duplicate index causing issue with style
    st.write (data_5.set_index('full_name').style.format(format_dict))

    st.write (cost_total(data_5,selection1='Price', selection2=select_pts))

def get_image():
    response = requests.get("https://raw.githubusercontent.com/ZeNoonan/FPL/master/FPL_Image.jpg")
    return Image.open(BytesIO(response.content))

@st.cache(suppress_st_warning=True)
def prep_base_data(url_csv, pick):
    url_csv = pd.read_csv(url_csv).rename(columns = {'id':'player_id','element_type':'Position','assists':'assists_season',
    'bonus':'bonus_season','bps':'bps_season','clean_sheets':'clean_sheets_season','creativity':'creativity_season','goals_conceded':'goals_conceded_season',
    'goals_scored':'goals_scored_season','ict_index':'ict_index_season','influence':'influence_season','minutes':'minutes_season',
    'saves':'saves_season','threat':'threat_season','transfers_in':'transfers_in_season','transfers_out':'transfers_out_season'})
    url_csv['Position'] = url_csv['Position'].map({1: 'GK', 2: 'DF', 3:'MD', 4:'FW'})
    url_csv['full_name'] = (url_csv['first_name']+'_'+url_csv['second_name']).str.lower()
    pick_data = pd.read_pickle(pick).rename(columns = {'total_points':'week_points'})
    return pd.merge(url_csv,pick_data, on='player_id',how ='outer')

@st.cache(suppress_st_warning=True)
def data_2020_clean_double_gw(url_pick2020):
    url_pick2020=url_pick2020[ ~(url_pick2020['round']==29) | ~(url_pick2020['fixture']==275)]
    url_pick2020['week']=url_pick2020['week'].replace({39:30,40:31,41:32,42:33,43:34,44:35,45:36,46:37,47:38})
    url_pick2020['round']=url_pick2020['round'].replace({39:30,40:31,41:32,42:33,43:34,44:35,45:36,46:37,47:38})
    gw_18_blank = clean_blank_gw(url_pick2020,10,19,17)
    gw_28_blank = clean_blank_gw(url_pick2020,11,3,27)
    gw_28_blank_1 = clean_blank_gw(url_pick2020,2,15,27)
    return pd.concat([url_pick2020,gw_18_blank,gw_28_blank,gw_28_blank_1])

@st.cache(suppress_st_warning=True)
def clean_blank_gw(x,team1,team2,week_no):
    x = x [ ((x ['team']==team1) | (x ['team']==team2)) & (x['week']==week_no) ].copy()
    x['round']=week_no + 1
    x['week'] =week_no + 1
    x['minutes']=np.NaN
    x['week_points']=np.NaN
    x['fixture'] =np.NaN
    return x

@st.cache(suppress_st_warning=True)
def data_2021_team_names(file):
    file['team'] = file['team'].map({1: 'Arsenal', 2: 'Aston_Villa', 3:'Brighton', 4:'Burnley',5:'Chelsea',6:'Crystal_Palace',7:'Everton',
    8:'Fulham',9:'Leicester',10:'Leeds_Utd',11:'Liverpool',12:'Man_City',13:'Man_Utd',14:'Newcastle',15:'Sheffield_Utd',16:'Southampton',17:'Spurs',
    18:'West_Brow',19:'West_Ham',20:'Wolves'})
    return file

@st.cache(suppress_st_warning=True)
def data_2020_team_names(file):
    file['team'] = file['team'].map({1: 'Arsenal', 2: 'Aston_Villa', 3:'Bournemouth', 4:'Brighton',5:'Burnley',6:'Chelsea',7:'Crystal_Palace',
    8:'Everton',9:'Leicester',10:'Liverpool',11:'Man_City',12:'Man_Utd',13:'Newcastle',14:'Norwich',15:'Sheffield_Utd',16:'Southampton',17:'Spurs',
    18:'Watford',19:'West_Ham',20:'Wolves'})
    return file

@st.cache(suppress_st_warning=True)
def data_2019_team_names(file):
    file['team'] = file['team'].map({1: 'Arsenal', 2: 'Bournemouth', 3:'Brighton', 4:'Burnley',5:'Cardiff',6:'Chelsea',7:'Crystal_Palace',
    8:'Everton',9:'Fulham',10:'Huddersfield',11:'Leicester',12:'Liverpool',13:'Man_City',14:'Man_Utd',15:'Newcastle',16:'Southampton',17:'Spurs',
    18:'Watford',19:'West_Ham',20:'Wolves'})
    return file

@st.cache(suppress_st_warning=True)
def data_2018_team_names(file):
    file['team'] = file['team'].map({1: 'Arsenal', 2: 'Bournemouth', 3:'Brighton', 4:'Burnley',5:'Chelsea',6:'Crystal_Palace',7:'Everton',
    8:'Hull',9:'Leicester',10:'Liverpool',11:'Man_City',12:'Man_Utd',13:'Newcastle',14:'Southampton',15:'Stoke',16:'Swansea',17:'Spurs',
    18:'Watford',19:'West_Brom',20:'West_Ham'})
    return file

@st.cache(suppress_st_warning=True)
def combine_dataframes(a,b,c,d):
    return pd.concat ([a,b,c,d], axis=0,sort = True)

@st.cache(suppress_st_warning=True)
def column_calcs(df):
    df['Price'] =df['value'] / 10
    df['Game_1'] = np.where((df['minutes'] > 0.5), 1, 0)
    df['Clean_Pts'] = np.where(df['Game_1']==1,df['week_points'], np.NaN) # setting a slice on a slice - just suppresses warning....
    df = df.sort_values(by=['full_name', 'year', 'week'], ascending=[True, True, True]) # THIS IS IMPORTANT!! EWM doesn't work right unless sorted
    df['EWM_Pts'] = df['Clean_Pts'].ewm(alpha=0.07).mean()
    weights = np.array([0.125, 0.25,0.5,1]) # the order mattered!! took me a while to figure this out
    sum_weights = np.sum(weights)
    df['Weighted_ma'] = (df['Clean_Pts'].fillna(0).rolling(window=4, center=False)\
        .apply(lambda x: np.sum(weights*x) / sum_weights, raw=False)) # raw=False
        # using the fillna ensures no NaN as this function requires min 4 data points in a row - .fillna(method='ffill')
        # so just be careful the result is the last time player had 4 weeks in a row
        # don't think this is working right, think it is including 0 in previous week if you didn't play
    df['last_10_games_total'] = df.groupby(['full_name'])['Game_1'].rolling(window=10,min_periods=3, center=False).sum().reset_index(0,drop=True)
    df['last_10_points_total'] = df.groupby(['full_name'])['Clean_Pts'].rolling(window=10,min_periods=3, center=False).sum().reset_index(0,drop=True)
    df['ppg_last_10_games'] = (df['last_10_points_total'] / df['last_10_games_total']).fillna(0)
    df['Gms_Ssn_to_Date'] = df.groupby (['full_name', 'year'])['Game_1'].cumsum()
    df['Gms_Ssn_Total'] = df.groupby (['full_name', 'year'])['Game_1'].transform('sum')
    df['Games_Total_Rolling'] = df.groupby (['full_name'])['Game_1'].cumsum()
    df['Games_Total'] = df.groupby (['full_name'])['Game_1'].transform('sum')
    df['week_points'] = pd.to_numeric(df['week_points'])
    df['Pts_Sn_Rllg'] = df.groupby (['full_name', 'year'])['week_points'].cumsum() # THIS IS THE ISSUE
    df['Points_Season_Total'] = df.groupby (['full_name', 'year'])['week_points'].transform('sum')
    df['Points_Total_Rolling'] = df.groupby (['full_name'])['week_points'].cumsum()
    df['Points_Total'] = df.groupby (['full_name'])['week_points'].transform('sum')
    df['PPG_Total'] = df['Points_Total'] / df['Games_Total']
    df['PPG_Sn_Rllg'] = df['Pts_Sn_Rllg'] / df['Gms_Ssn_to_Date']
    df['PPG_Total_Rolling'] = df['Points_Total_Rolling'] / df['Games_Total_Rolling']
    df['PPG_Season_Total'] = df['Points_Season_Total'] / df['Gms_Ssn_Total']
    df['PPG_Season_Value'] = df['PPG_Season_Total'] / df['Price']
    df['Pts_Sn_Rmg'] = df['Points_Season_Total'] - df['Pts_Sn_Rllg']
    df['Games_Ssn_Rmg'] = (df['Gms_Ssn_Total'] - df['Gms_Ssn_to_Date'])
    df['PPG_Sn_Rmg'] = (df['Pts_Sn_Rmg'] / df['Games_Ssn_Rmg']).fillna(0)
    df['PPG_Sn_Rllg_Rnk'] = df.groupby(['week','year','Position'])['PPG_Sn_Rllg'].rank(method='dense', ascending=False)
    df['PPG_Sn_Rllg_Rmg_Rnk'] = df.groupby(['week','year','Position'])['PPG_Sn_Rmg'].rank(method='dense', ascending=False)
    df['PPG_Rllg_Rnk_Diff'] = (df['PPG_Sn_Rllg_Rnk'] - df['PPG_Sn_Rllg_Rmg_Rnk'])
    df['Pts_Sn_Rllg_Rnk'] = df.groupby(['week','year','Position'])['Pts_Sn_Rllg'].rank(method='dense', ascending=False)
    df['Pts_Sn_Rllg_Rmg_Rnk'] = df.groupby(['week','year','Position'])['Pts_Sn_Rmg'].rank(method='dense', ascending=False)
    df['Pts_Rllg_Rnk_Diff'] = (df['Pts_Sn_Rllg_Rnk'] - df['Pts_Sn_Rllg_Rmg_Rnk'])
    df["GK"] = (df["Position"] == 'GK').astype(float)
    df["DF"] = (df["Position"] == 'DF').astype(float)
    df["MD"] = (df["Position"] == 'MD').astype(float)
    df["FW"] = (df["Position"] == 'FW').astype(float)
    df["LIV"] = (df["team"] == 'Liverpool').astype(float)
    df["MC"] = (df["team"] == 'Man_City').astype(float)
    df["LEI"] = (df["team"] == 'Leicester').astype(float)
    return df

def show_data(df, year, week, min_games_played, season_games_played):
    df= df [ (df['year']==year) & (df['week']==week) & (df['last_10_games_total'] >= min_games_played) & (df['Gms_Ssn_to_Date'] >= season_games_played) ]
    df=df.sort_values (by ='kickoff_time', ascending=True).drop_duplicates(subset=['full_name'], keep='last') # this is for Double Gameweeks as was an issue for concating dataframes where name was in twice as played twice
    return df

def exclude_players(df, *args):
    for x in args:
        df.loc [ (df['full_name'].isin(x)), 'Price' ] = 1000 # for some reason isin worked rather than == sometime to do with lengths dont match 
    return df # think it might be do with == returns a value dont know

def opt_data(x,select_pts):
    return x[['full_name', 'Position','team', select_pts, 'Price','PPG_Season_Value','GK','DF','MD','FW','LIV','MC','LEI']].reset_index().drop('index', axis=1)

def optimise_fpl(df,md,fw,fpl_players1,squad_cost,select_pts,number_players=11):
    model = LpProblem("FPL", LpMaximize)
    total_points = {}
    cost = {}
    GKs = {}
    DFs = {}
    MDs = {}
    FWs = {}
    LIVs= {}
    MCs={}
    LEIs={}
    number_of_players = {}
    for i, player in fpl_players1.iterrows(): # HERE
        var_name = 'x' + str(i) 
        decision_var = LpVariable(var_name, cat='Binary')
        total_points[decision_var] = player[select_pts] 
        cost[decision_var] = player["Price"] 
        GKs[decision_var] = player["GK"]
        DFs[decision_var] = player["DF"]
        MDs[decision_var] = player["MD"]
        FWs[decision_var] = player["FW"]
        LIVs[decision_var] = player["LIV"]
        MCs[decision_var] = player["MC"]
        LEIs[decision_var] = player["LEI"]
        number_of_players[decision_var] = 1.0
    objective_function = LpAffineExpression(total_points)
    model += objective_function
    total_cost = LpAffineExpression(cost)
    model += (total_cost <= squad_cost)
    GK_constraint = LpAffineExpression(GKs)
    DF_constraint = LpAffineExpression(DFs)
    MD_constraint = LpAffineExpression(MDs)
    FW_constraint = LpAffineExpression(FWs)
    LIV_constraint = LpAffineExpression(LIVs)
    MC_constraint = LpAffineExpression(MCs)
    LEI_constraint = LpAffineExpression(LEIs)
    total_players = LpAffineExpression(number_of_players)
    model += (GK_constraint == 1)
    model += (DF_constraint == df)
    model += (MD_constraint == md)
    model += (FW_constraint == fw)
    model += (LIV_constraint <= 3)
    model += (MC_constraint <= 3)
    model += (LEI_constraint <= 3)
    model += (total_players <= number_players)
    model.solve()
    fpl_players1["is_drafted"] = 0.0 # HERE
    # st.write (fpl_players1.head())
    for var in model.variables():
        # st.write('this is the var', var)
        fpl_players1.iloc[int(var.name[1:]),13] = var.varValue # HERE
    return (fpl_players1[fpl_players1["is_drafted"] == 1.0]).sort_values(['GK','DF','MD','FW'], ascending=False)

def table(x,select_pts): 
    # https://stackoverflow.com/questions/55652704/merge-multiple-dataframes-pandas
    dfs = [df.set_index(['full_name','Position','team',select_pts,'Price','PPG_Season_Value']) for df in x]
    a=pd.concat(dfs,axis=1).reset_index() # issue is not reset index
    a=a.loc[:,['full_name','Position','team',select_pts,'Price','PPG_Season_Value','is_drafted']]
    a.columns=['full_name','Position','team',select_pts,'Price','PPG_Season_Value','F_3_5_2','F_4_5_1','F_4_4_2','F_5_3_2','F_5_4_1','F_3_4_3','F_5_2_3','F_4_3_3']
    a['Pos'] = a['Position'].map({'GK': 1, 'DF': 2, 'MD':3, 'FW':4})
    a['Count']=a.loc[:,'F_3_5_2':'F_4_3_3'].count(axis=1)
    cols=['F_3_5_2','F_4_5_1','F_4_4_2','F_5_3_2','F_5_4_1','F_3_4_3','F_5_2_3','F_4_3_3']
    for n in cols:
        a[n]=(a[n]>0).astype(int) # to clean up the NaN
    a=a.sort_values(by=['Pos','Count'],ascending=[True,False])
    a['Value'] = a[select_pts]/a['Price']
    return a

def cost_total(df,selection1,selection2):
    cols=['F_3_5_2','F_4_5_1','F_4_4_2','F_5_3_2','F_5_4_1','F_3_4_3','F_5_2_3','F_4_3_3']
    cost=[]
    points=[]
    for n in cols:
        df[n]=(df[n]>0).astype(int)
        x=((df[selection1]*df[n]).sum())
        y=((df[selection2]*df[n]).sum())
        cost.append(x)
        points.append(y)
    # df=pd.DataFrame([cost], columns=cols) #https://stackoverflow.com/questions/50874117/pandas-dataframe-shape-of-passed-values-is-1-4-indices-imply-4-4
    df1=pd.concat([pd.DataFrame([cost],columns=cols,index=['Price']), pd.DataFrame([points],columns=cols, index=['Points'])], axis=0)
    df1.loc['Price']=df1.loc['Price'].apply('£{0:,.1f}m'.format)
    df1.loc['Points']=df1.loc['Points'].apply('{0:,.1f}'.format)
    return df1

main()