import pandas as pd
import numpy as np
import streamlit as st
from time import time
from pulp import *
from io import BytesIO
import requests
from PIL import Image

url_2021='https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2020-21/players_raw.csv'
url_2020='https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2019-20/players_raw.csv'
url_2019='https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2018-19/players_raw.csv'
url_2018='https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2017-18/players_raw.csv'
pick_2021='C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/raw_data_2021.pkl'
pick_2020='C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/raw_data_2020.pkl'
pick_2019='C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/raw_data_2019.pkl'
pick_2018='C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/raw_data_2018.pkl'

def main():

    st.title ('FPL Lineup Optimisation')
    st.info("""
    This app helps you select the optimal line-up for your fantasy football team for the Premier League ⚽.
    """)
    # use double space for new line in markdown
    st.markdown("""
    Using historical points, we can calculate the optimal line up selection to maximise the points based on certain constraints.  
    The output of this app is a table showing what the optimal line-up is for each possible selection.
    """)
    # https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json
    st.markdown(f"""Source Data: [2021 Player Info]({url_2021}))
    """)
    image=get_image()
    st.sidebar.image(image, use_column_width=True)

    data_2021 = (data_2021_team_names( (prep_base_data(url_2021, pick_2021)).rename(columns = {'team_x':'team'}))).copy()
    data_2020 = (data_2020_team_names( (prep_base_data(url_2020, pick_2020)).copy() )).copy()
    data_2019 = (data_2019_team_names( (prep_base_data(url_2019, pick_2019)).copy() )).copy()
    data_2018 = (data_2018_team_names( (prep_base_data(url_2018, pick_2018)).copy() )).copy()
    
    data_2020 = (data_2020_clean_double_gw(data_2020)).copy()

    all_seasons_df = (column_calcs( (combine_dataframes(data_2018,data_2019,data_2020,data_2021)).reset_index().copy() )).copy() # have added reset index duplicates in index?

    # st.write ('2021 data')
    # st.write ( data_2021[ data_2021['full_name'].str.contains('salah')])
    # url_master = pd.read_csv(url_2021)
    # st.write ('url 2021')
    # st.table (url_master[ url_master['second_name'].str.contains('Salah')])
    # st.write ('pickle 2021 data')
    # pick_2021_data = pd.read_pickle(pick_2021)
    # st.write (pick_2021_data[ pick_2021_data['name'].str.contains('Salah')])
    # # st.write (data_2021.head())

    # st.write ('testing combine dataframes which is just pd.concat def an issue maybe index needs to be set')
    # st.write ('this is data_2021 check the index?')
    # st.write ('issue is before this')
    # testing = prep_base_data(url_2021, pick_2021)
    # st.write ('prep base data looks ok i think')
    # st.write (testing[ testing['full_name'].str.contains('salah')])
    # st.write ('test the data team names function')

    # test_test = data_2021_team_names( prep_base_data(url_2021, pick_2021))
    # st.write('is the issue with combine dataframes')
    # xxx = combine_dataframes(data_2018,data_2019,data_2020,data_2021)
    # st.write (xxx[ xxx['full_name'].str.contains('salah')])

    # st.write('is the issue with say data 2021 which is just url and csv')
    # st.write(data_2021[ data_2021['full_name'].str.contains('salah')])

    year = st.sidebar.selectbox("Select a year",(2021,2020,2019,2018))
    st.sidebar.header("1. Select FPL Game Week.")
    week = st.sidebar.number_input ("Select period from GW1 up to GW user select", min_value=int(0),max_value=int(38.0), value=int(8.0)) 
    st.sidebar.header("2. Squad Cost")
    squad_cost=st.sidebar.number_input ("Select how much you want to spend on 11 players", 80.0,100.0, value=82.0, step=.5)
    st.sidebar.header("3. Min Number of Games Played by Player")
    min_games_played = st.sidebar.number_input ("Minimum number of games played in last 10 games", min_value=int(0),max_value=int(10),value=int(1))
    min_current_season_games_played = st.sidebar.number_input("Minimum number of games played from start of current Season",
    min_value=int(0),max_value=int(38), value=int(1))

    data=show_data(all_seasons_df, year, week, min_games_played, min_current_season_games_played)    
    # st.write( data[ data['full_name'].str.contains('salah')])

    player_names=data['full_name'].unique()
    names_selected = st.multiselect('Select which players you want excluded from lineup (e.g. due to injuries or suspension)',player_names)
    data_1=exclude_players(data,names_selected)
    # st.table (data_1.columns.to_list())
    additional_info=data_1.loc[:,['full_name','week','round', 'Games_Total','Games_Total_Rolling', 'Gms_Ssn_Total','Games_Ssn_Rmg', 'Gms_Ssn_to_Date',
    'points_per_game','Pts_Sn_Rllg_Rnk','Pts_Sn_Rllg_Rmg_Rnk','Pts_Rllg_Rnk_Diff','PPG_Sn_Rmg','PPG_Sn_Rllg_Rnk','PPG_Sn_Rllg_Rmg_Rnk','PPG_Rllg_Rnk_Diff',
    'last_10_games_total','last_10_points_total','Pts_Sn_Rllg','Pts_Sn_Rmg','PPG_Sn_Rllg',]]

    st.sidebar.header("4. Optimise on which Points")
    select_pts=st.sidebar.radio('Select the points you want to optimise',['PPG_Sn_Rllg','PPG_Sn_Rmg','Pts_Sn_Rmg','Points_Season_Total', 'ppg_last_10_games','PPG_Total'])
    data_2=opt_data(data_1,select_pts)

    # st.write ('trying to figure out the PPG remaining')
    # st.write (data_2.head())
    # st.write( data_2[ data_2['full_name'].str.contains('salah')])

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
    # cols_to_use = additional_info.columns.difference(data_3.columns)
    data_4=pd.merge(data_3, additional_info, on='full_name', how='left',suffixes=('', '_y'))
    # data_4 =data_4.loc[:,~data_4.columns.duplicated()]
    # st.write ('looking at data 4 to see what the problem is')
    # st.write(data_4.head())
    
    # cols_to_move = ['full_name','Position','Count','team',select_pts,'Price','Gms_Ssn_to_Date','Games_Ssn_Rmg','Pts_Sn_Rllg_Rnk',
    # 'Pts_Sn_Rllg_Rmg_Rnk','Pts_Rllg_Rnk_Diff','PPG_Sn_Rllg_Rnk','PPG_Sn_Rllg_Rmg_Rnk','PPG_Rllg_Rnk_Diff','Pts_Sn_Rllg','Pts_Sn_Rmg',
    # 'last_10_points_total','last_10_games_total','Value','Gms_Ssn_Total','F_3_4_3','F_4_3_3','F_3_5_2','F_4_5_1',
    # 'F_4_4_2','F_5_3_2','F_5_4_1','F_5_2_3','Games_Total_Rolling','week','points_per_game']
    
    cols_to_move = ['full_name','Position','Count','team','Price','Gms_Ssn_to_Date','Games_Ssn_Rmg','Pts_Sn_Rllg','Pts_Sn_Rllg_Rnk','Pts_Sn_Rmg','Pts_Sn_Rllg_Rmg_Rnk',
    'PPG_Sn_Rllg','PPG_Sn_Rllg_Rnk','PPG_Sn_Rmg','PPG_Sn_Rllg_Rmg_Rnk','PPG_Rllg_Rnk_Diff',
    'last_10_points_total','last_10_games_total','Value','Gms_Ssn_Total','F_3_4_3','F_4_3_3','F_3_5_2','F_4_5_1',
    'F_4_4_2','F_5_3_2','F_5_4_1','F_5_2_3','Games_Total_Rolling','week','points_per_game']
    cols = cols_to_move + [col for col in data_4 if col not in cols_to_move]
    # data_5=data_4.loc[:,cols]
    data_5=data_4[cols]
    # data_5 =data_5.loc[:,~data_5.columns.duplicated()]

    # cols_to_move = ['full_name','Position','Count','team',select_pts,'Price','Gms_Ssn_to_Date','Games_Ssn_Rmg','Pts_Sn_Rllg_Rnk',
    # 'Pts_Sn_Rllg_Rmg_Rnk','Pts_Rllg_Rnk_Diff','PPG_Sn_Rllg_Rnk','PPG_Sn_Rllg_Rmg_Rnk']
    # cols = cols_to_move + [col for col in data_4 if col not in cols_to_move]
    # # data_5=data_4.loc[:,cols]
    # data_5=data_4[cols]



    # cols_to_order = ['full_name','Position','Count','team',select_pts,'Price','Gms_Ssn_to_Date','Games_Ssn_Rmg','Pts_Sn_Rllg_Rnk',
    # 'Pts_Sn_Rllg_Rmg_Rnk','Pts_Rllg_Rnk_Diff','PPG_Sn_Rllg_Rnk','PPG_Sn_Rllg_Rmg_Rnk','PPG_Sn_Rmg','PPG_Rllg_Rnk_Diff','Pts_Sn_Rllg','Pts_Sn_Rmg',
    # 'last_10_points_total','last_10_games_total','Value','Gms_Ssn_Total','F_3_4_3','F_4_3_3','F_3_5_2','F_4_5_1',
    # 'F_4_4_2','F_5_3_2','F_5_4_1','F_5_2_3','Games_Total_Rolling','week','points_per_game']
    # # new_columns = cols_to_order + (data_4.columns.drop(cols_to_order).tolist())
    # frame = data_4[new_columns]



    format_dict = {'EWM_Pts':'{0:,.1f}','PPG_Season_Total':'{0:,.1f} ppg','Weighted_ma':'{0:,.1f}','Points_Season_Total':'{0:,.0f}',
    'points_per_game':'{0:,.1f}','Price':'£{0:,.1f}m','PPG_Sn_Rmg':'{0:,.1f}','Gms_Ssn_Total':'{0:,.0f}','last_10_games_total':'{0:,.0f}',
    'ppg_last_10_games':'{0:,.1f}','Value':'{0:,.2f}','last_10_points_total':'{0:,.0f}','PPG_Sn_Rllg':'{0:,.1f}','Price':'{0:,.1f}',
    'Pts_Sn_Rllg':'{0:,.0f}','Pts_Sn_Rllg_Rnk':'{0:,.0f}','Pts_Sn_Rllg_Rmg_Rnk':'{0:,.0f}','PPG_Sn_Rllg_Rmg_Rnk':'{0:,.0f}','PPG_Rllg_Rnk_Diff':'{0:,.0f}',
    'Pts_Sn_Rmg':'{0:,.0f}','Pts_Rllg_Rnk_Diff':'{0:,.0f}','PPG_Sn_Rllg_Rnk':'{0:,.0f}'}
    # format_dict = {'Price':'{0:,.1f}'}
    # st.dataframe(data_4.style.format(format_dict))
    # st.dataframe(frame.style.format(format_dict))

    data_5=data_5.reset_index(drop=True)  # https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-dataframe cos of duplicate index causing issue with style
    # data_5 = data_5.set_index('full_name')
    # st.write ('should be normal index')
    # st.write(data_5.style.format("{:,.0f}",na_rep="-"))
    st.write (data_5.set_index('full_name').style.format(format_dict))
    # data_test = data_5.reset_index()
    # st.write ('this is duplicated')
    # st.write(data_test[data_test.index.duplicated(keep=False)])
    # st.write(data_test.style.format(format_dict))

    # st.write(data_5.reset_index().drop('index', axis=1).set_index('full_name').style.format(format_dict))
    # st.write(data_5.set_index('full_name'))
    # st.write ('this is duplicated')
    # st.write(data_5[data_5.set_index('full_name').index.duplicated(keep=False)])

    # st.write ('this is duplicated')
    # st.write(data_5[data_5.index.duplicated(keep=False)])

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
def data_2020_clean_double_gw(url_pick_2020):
    url_pick_2020=url_pick_2020[ ~(url_pick_2020['round']==29) | ~(url_pick_2020['fixture']==275)]
    url_pick_2020['week']=url_pick_2020['week'].replace({39:30,40:31,41:32,42:33,43:34,44:35,45:36,46:37,47:38})
    url_pick_2020['round']=url_pick_2020['round'].replace({39:30,40:31,41:32,42:33,43:34,44:35,45:36,46:37,47:38})
    gw_18_blank = clean_blank_gw(url_pick_2020,10,19,17)
    gw_28_blank = clean_blank_gw(url_pick_2020,11,3,27)
    gw_28_blank_1 = clean_blank_gw(url_pick_2020,2,15,27)
    return pd.concat([url_pick_2020,gw_18_blank,gw_28_blank,gw_28_blank_1])

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
    # st.write (df['Game_1'].dtype)
    # df['Game_1'] = df['Game_1'].astype('int64')
    # st.write (df['Game_1'].dtype)    
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
    df['Games_Ssn_Rmg'] = df['Gms_Ssn_Total'] - df['Gms_Ssn_to_Date']
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
    return df [ (df['year']==year) & (df['week']==week) & (df['last_10_games_total'] >= min_games_played) & (df['Gms_Ssn_to_Date'] >= season_games_played) ]

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

def table(x,select_pts): #Honestly don't understand why GW29 is messing up the multiindex just for EWM. The moving average works fine  just wait until GW29 is rerun?
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