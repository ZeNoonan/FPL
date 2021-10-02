import requests
import json
import time
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
# data = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
# data = json.loads(data.content)
# # st.write(data)
# gameweeks = data['elements']
# # st.write(gameweeks)
# names=pd.DataFrame(data['elements']).apply(pd.Series)
# st.write('names')
# # st.write(names)
# names.to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/fpl_data_2021.pkl') 

fpl_2021_data=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/fpl_data_2021.pkl')
url_csv = fpl_2021_data.rename(columns = {'now_cost':'Price','id':'player_id','element_type':'Position','assists':'assists_season',
'bonus':'bonus_season','bps':'bps_season','clean_sheets':'clean_sheets_season','creativity':'creativity_season','goals_conceded':'goals_conceded_season',
'goals_scored':'goals_scored_season','ict_index':'ict_index_season','influence':'influence_season','minutes':'minutes_season',
'saves':'saves_season','threat':'threat_season','transfers_in':'transfers_in_season','transfers_out':'transfers_out_season'})
url_csv['Position'] = url_csv['Position'].map({1: 'GK', 2: 'DF', 3:'MD', 4:'FW'})
url_csv['full_name'] = (url_csv['first_name']+'_'+url_csv['second_name']).str.lower()
url_csv['week']=1
url_csv['year']=2022
cols_to_move = ['full_name','team','Position','Price','week','year']
cols = cols_to_move + [col for col in url_csv if col not in cols_to_move]
url_csv=url_csv[cols]

url_csv['team'] = url_csv['team'].map({1: 'Arsenal', 2: 'Aston_Villa', 3:'Brentford', 4:'Brighton',5:'Burnley',6:'Chelsea',7:'Crystal_Palace',
8:'Everton',9:'Leicester',10:'Leeds_Utd',11:'Liverpool',12:'Man_City',13:'Man_Utd',14:'Newcastle',15:'Norwich',16:'Southampton',17:'Spurs',
18:'Watford',19:'West_Ham',20:'Wolves'})
url_csv['Price']=url_csv['Price']/10

# map({1: 'Arsenal', 2: 'Aston_Villa', 3:'Brighton', 4:'Burnley',5:'Chelsea',6:'Crystal_Palace',7:'Everton',
# 8:'Fulham',9:'Leicester',10:'Leeds_Utd',11:'Liverpool',12:'Man_City',13:'Man_Utd',14:'Newcastle',15:'Sheffield_Utd',16:'Southampton',17:'Spurs',
# 18:'West_Brow',19:'West_Ham',20:'Wolves'})
filter_2021=url_csv.loc[:,['full_name','team','Position','Price']].copy()
filter_2021.to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/fpl_2022.pkl')

st.write(filter_2021)