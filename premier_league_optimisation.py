import numpy as np
import pandas as pd
import requests
from PIL import Image
from pulp import *
import base64
from io import BytesIO

import streamlit as st

st.set_page_config(layout='wide')
current_week = 38
current_year = 2023 # row 495
st.write('See who played 90 mins in the last 10 gameweeks or 20 gameweeks')

url2023 = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2022-23/players_raw.csv'
url2022 = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2021-22/players_raw.csv'
url2021 = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2020-21/players_raw.csv'
url2020 = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2019-20/players_raw.csv'
url2019 = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2018-19/players_raw.csv'
url2018 = 'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2017-18/players_raw.csv'
fantasy_url = 'https://fantasy.premierleague.com'
# pick2022 = 'https://raw.githubusercontent.com/ZeNoonan/FPL/master/raw_data_2022.csv'
# pick2023 = 'C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/raw_data_2023.csv'
pick2023 = 'C:/Users/Darragh/Documents/Python/premier_league/raw_data_2023.csv'
# pick2022 = 'C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/raw_data_2022.csv'
pick2022 = 'C:/Users/Darragh/Documents/Python/premier_league/raw_data_2022.csv'
pick2021 = 'https://raw.githubusercontent.com/ZeNoonan/FPL/master/raw_data_2021.csv'
pick2020 = 'https://raw.githubusercontent.com/ZeNoonan/FPL/master/raw_data_2020.csv'
# pick2019 = 'https://github.com/ZeNoonan/FPL/blob/master/raw_data_2019.pkl?raw=true'
# pick2018 = 'https://github.com/ZeNoonan/FPL/blob/master/raw_data_2018.pkl?raw=true'
# https://stackoverflow.com/questions/61786481/why-cant-i-read-a-joblib-file-from-my-github-repo
# https://stackoverflow.com/questions/50777849/from-conda-create-requirements-txt-for-pip3

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download csv file</a>' # decode b'abc' => abc

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data



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
    # image=get_image()
    # st.sidebar.image(image, use_column_width=True)
    test_url_2023=pd.read_csv(url2023)
    test_pick_2023=pd.read_csv(pick2023)
    # st.write('merged on player id check')
    # st.write('url 2023', test_url_2023[test_url_2023['second_name'].str.contains('arrison')])
    # st.write('pick 2023', test_pick_2023[test_pick_2023['name'].str.contains('Jack Harrison')])
    data_2023 = (data_2023_team_names( (prep_base_data(url2023, pick2023)).rename(columns = {'team_x':'team'}))).copy()
    data_2022 = (data_2022_team_names( (prep_base_data(url2022, pick2022)).rename(columns = {'team_x':'team'}))).copy()
    # st.write('data 2023',data_2023[data_2023['second_name'].str.contains('arrison')])
    data_2021 = (data_2021_team_names( (prep_base_data(url2021, pick2021)).rename(columns = {'team_x':'team'}))).copy()
    data_2020 = (data_2020_team_names( (prep_base_data(url2020, pick2020)).copy() )).copy()
    # data_2019 = (data_2019_team_names( (prep_base_data(url2019, pick2019)).copy() )).copy()
    # data_2018 = (data_2018_team_names( (prep_base_data(url2018, pick2018)).copy() )).copy()
    data_2020 = (data_2020_clean_double_gw(data_2020)).copy()

    # st.write('2022 check',data_2022.sort_values(by='now_cost', ascending=False))
    
    # test_vaastav=pd.read_csv(url2022)
    # test_dn = pd.read_csv(pick2022)
    # st.write('check the vaastav raw data')
    # # st.write(test_vaastav)
    # st.write(test_vaastav.loc[test_vaastav['web_name'].str.contains('Barnes')])
    # st.write('check  DN weekly info')
    # st.write(test_dn)    

    # st.write('this is after processing applied the prepbasedata function')
    # st.write(test_dn.loc[test_dn['name'].str.contains('Harvey_Barnes')])

    @st.cache(suppress_st_warning=True)
    def combine_dataframes_2(a,b,c,d):
        return pd.concat ([a,b,c,d], axis=0,sort = True)


    combined_df_before_names= (combine_dataframes_2(data_2020,data_2021,data_2022,data_2023)).reset_index().copy()

    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='heung-min_son'), 'full_name' ] = 'son_heung-min'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='gabriel teodoro_martinelli silva'), 'full_name' ] = 'gabriel_martinelli silva'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='benjamin_chilwell'), 'full_name' ] = 'ben_chilwell'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='gabriel_magalhães'), 'full_name' ] = 'gabriel_dos santos magalhães'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='bruno miguel_borges fernandes'), 'full_name' ] = 'bruno_borges fernandes'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='joão pedro cavaco_cancelo'), 'full_name' ] = 'joão_cancelo'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='gabriel fernando_de jesus'), 'full_name' ] = 'gabriel_fernando de jesus'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='diogo_jota'), 'full_name' ] = 'diogo_teixeira da silva'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='emerson aparecido_leite de souza junior'), 'full_name' ] = 'emerson_leite de souza junior'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='josé diogo_dalot teixeira'), 'full_name' ] = 'diogo_dalot teixeira'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='miguel_almirón'), 'full_name' ] = 'miguel_almirón rejala'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='aleksandar_mitrovic'), 'full_name' ] = 'aleksandar_mitrović'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='emiliano_martínez'), 'full_name' ] = 'emiliano_martínez romero'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='andreas_pereira'), 'full_name' ] = 'andreas_hoelgebaum pereira'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='ben_white'), 'full_name' ] = 'benjamin_white'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='solomon_march'), 'full_name' ] = 'solly_march'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='rúben santos_gato alves dias'), 'full_name' ] = 'rúben_gato alves dias'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='bernardo mota_veiga de carvalho e silva'), 'full_name' ] = 'bernardo_veiga de carvalho e silva'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='marc_cucurella'), 'full_name' ] = 'marc_cucurella saseta'
    combined_df_before_names.loc [ (combined_df_before_names['full_name']=='matthew_cash'), 'full_name' ] = 'matty_cash'

    # all_seasons_df = (column_calcs( (combine_dataframes(data_2018,data_2019,data_2020,data_2021)).reset_index().copy() )).copy() # have added reset index duplicates in index?
    all_seasons_df = (column_calcs( combined_df_before_names )).copy()
    # all_seasons_df = (column_calcs( data_2021)).reset_index().copy()
    cols_to_move = ['full_name','week','year','Price' ,'minutes','Clean_Pts','Game_1','week_points','4_games_rolling_mins',
    'years_last_8_games_calc','years_last_4_games_calc','years_last_2_games_calc','years_last_1_games_calc',
    'years_last_15_games','years_last_14_games','years_last_12_games',
    'years_sum_games','years_sum_points','years_sum_ppg','years_sum_mins','years_mins_ppg',
    'years_last_8_points_calc','years_last_4_points_calc','years_last_2_points_calc','years_last_1_points_calc',
    
    'years_last_15_points','years_last_14_points','years_last_12_points',
    ]
    cols = cols_to_move + [col for col in all_seasons_df if col not in cols_to_move]
    all_seasons_df=all_seasons_df[cols]



    # this relates to the detail by player which is at bottom of app / webpage
    all_seasons_df_1=all_seasons_df.copy()
    player_listing_data_analysis=all_seasons_df.copy()


    format_dict = {'EWM_Pts':'{0:,.1f}','PPG_Season_Total':'{0:,.1f} ppg','years_sum_games':'{0:,.0f}','years_mins_ppg':'{0:,.0f}','mins_ppg':'{0:,.0f}',
                   'years_sum_ppg':'{0:,.1f}','sum_ppg':'{0:,.1f}','Weighted_ma':'{0:,.1f}','Weighted_mins':'{0:,.0f}','Points_Season_Total':'{0:,.0f}',
                   'last_2_years_Games_Total':'{0:,.0f}','year':'{0:.0f}','Game_1':'{0:,.0f}','Clean_Pts':'{0:,.0f}','PPG_Total_Rolling':'{0:,.1f}',
                   'Games_Total':'{0:,.0f}','Gms_Ssn_to_Date':'{0:,.0f}','Games_Total_Rolling':'{0:,.0f}','minutes':'{0:,.0f}','value':'{0:,.2f}',
    'points_per_game':'{0:,.1f}','Price':'£{0:,.1f}m','PPG_Sn_Rmg':'{0:,.1f}','Gms_Ssn_Total':'{0:,.0f}','last_2_years_PPG':'{0:,.1f}','last_2_years_MPG':'{0:,.0f}',
    'ppg_last_10_games':'{0:,.1f}','Value':'{0:,.2f}','last_10_points_total':'{0:,.0f}','PPG_Sn_Rllg':'{0:,.1f}','Price':'{0:,.1f}','Price':'{0:,.1f}',
    'Pts_Sn_Rllg':'{0:,.0f}','Pts_Sn_Rllg_Rnk':'{0:,.0f}','Pts_Sn_Rllg_Rmg_Rnk':'{0:,.0f}','PPG_Sn_Rllg_Rmg_Rnk':'{0:,.0f}','PPG_Rllg_Rnk_Diff':'{0:,.0f}',
    'Pts_Sn_Rmg':'{0:,.0f}','Pts_Rllg_Rnk_Diff':'{0:,.0f}','PPG_Sn_Rllg_Rnk':'{0:,.0f}','Games_Ssn_Rmg':'{0:,.0f}','week':'{0:,.0f}','PPG_Total':'{0:,.1f}'}


    # player_data=column_calcs( ((data_2022)).reset_index().copy() )
    player_data=column_calcs( ((data_2023)).reset_index().copy() )
    # player_listing_data_analysis=player_data.copy()
    player_data=player_data.loc[:,['full_name','week','year', 'minutes','Clean_Pts','Game_1','week_points',
    'years_last_8_games_calc','years_last_4_games_calc','years_last_2_games_calc','years_last_1_games_calc',
    'years_last_8_points_calc','years_last_4_points_calc','years_last_2_points_calc','years_last_1_points_calc',
    'years_last_15_games','years_last_14_games','years_last_12_games',
    'years_last_15_points','years_last_14_points','years_last_12_points',
    'years_sum_games','years_sum_points','years_sum_ppg','years_sum_mins','years_mins_ppg',

    'last_8_games_calc','last_4_games_calc','last_2_games_calc','last_1_games_calc',
    'last_8_points_calc','last_4_points_calc','last_2_points_calc','last_1_points_calc',
    'last_15_games','last_14_games','last_12_games',
    'last_15_points','last_14_points','last_12_points',
    'sum_games','sum_points','sum_ppg','sum_mins','mins_ppg',
    'PPG_Sn_Rllg','Gms_Ssn_Total','ppg_last_10_games',
    'Games_Total_Rolling', 'Games_Ssn_Rmg','Weighted_ma','Weighted_mins',
    'Gms_Ssn_to_Date','PPG_Total',
    'points_per_game','Pts_Sn_Rllg_Rnk','Pts_Sn_Rllg_Rmg_Rnk','Pts_Rllg_Rnk_Diff','PPG_Sn_Rmg','PPG_Sn_Rllg_Rnk',
    'PPG_Sn_Rllg_Rmg_Rnk','PPG_Rllg_Rnk_Diff',

    'last_10_games_total','last_10_points_total','Pts_Sn_Rllg','Pts_Sn_Rmg','last_2_years_PPG','last_2_years_MPG','last_2_years_Games_Total']]
    player_detail=player_data['full_name'].unique()


    # name_of_player = st.multiselect('Pick player for detail',player_detail)
    # willock=player_data.loc[player_data['full_name'].str.contains('jack_harrison')]
    # chilwell=player_data.loc[player_data['full_name'].str.contains('chilwell')].tail(20)
    # st.markdown(get_table_download_link(willock), unsafe_allow_html=True)
    # st.write(willock.style.format(format_dict))
    
    # st.write(player_data.loc[player_data['full_name'].str.contains('chilwell')].tail(15).style.format(format_dict))


    year = st.sidebar.selectbox("Select a year",(2023,2022,2021,2020))
    st.sidebar.header("1. Select FPL Game Week.")
    week = st.sidebar.number_input ("Select period from GW1 up to GW user select", min_value=int(0),max_value=int(38.0), value=int(current_week)) 
    st.sidebar.header("2. Squad Cost")
    squad_cost=st.sidebar.number_input ("Select how much you want to spend on 11 players", 78.0,100.0, value=82.0, step=.5)
    st.sidebar.header("3. Min Number of Games Played by Player")
    min_games_played = st.sidebar.number_input ("Minimum number of games ever", min_value=int(0),value=int(1))
    min_current_season_games_played = st.sidebar.number_input("Minimum number of games played from start of current Season",
    min_value=int(0),max_value=int(38), value=int(3))
    last_2_years_games=st.sidebar.number_input ("Min last 2 years games ever", min_value=int(0),value=int(20))

    # st.write('haaland is in the all seasons df go to row 515 for function details',all_seasons_df.loc[all_seasons_df['full_name'].str.contains('aaland')])
    check_haaland=all_seasons_df.loc[all_seasons_df['full_name'].str.contains('aaland')].copy()
    cols_to_move = ['full_name','year','week','Position','Price','minutes','Game_1','Games_Total','Gms_Ssn_to_Date','last_2_years_Games_Total']
    cols = cols_to_move + [col for col in check_haaland if col not in cols_to_move]
    check_haaland=check_haaland[cols]
    # st.write('haalnd', check_haaland)
    data=show_data(all_seasons_df, year, week, min_games_played, min_current_season_games_played,last_2_years_games)    
    # st.write('check this')
    # st.write('data row 174', data[data['full_name'].str.contains('haaland')])
    
    # st.write(player_data.loc[player_data['full_name'].str.contains('aaland')])
    

    player_names=data['full_name'].unique()
    names_selected = st.multiselect('Select which players you want excluded from lineup (e.g. due to injuries or suspension)',player_names)
    # st.write('data',data.head())
    
    data_1=exclude_players(data,names_selected)

    additional_info=data_1.loc[:,['full_name','week', 'Games_Total','years_sum_ppg','years_mins_ppg','years_sum_mins','years_sum_games','sum_ppg','mins_ppg','sum_mins','sum_games','ppg_last_10_games','Games_Total_Rolling', 'Gms_Ssn_Total','Games_Ssn_Rmg', 'Gms_Ssn_to_Date','PPG_Total',
    'points_per_game','Pts_Sn_Rllg_Rnk','Pts_Sn_Rllg_Rmg_Rnk','Pts_Rllg_Rnk_Diff','PPG_Sn_Rllg','PPG_Sn_Rmg','PPG_Sn_Rllg_Rnk','PPG_Sn_Rllg_Rmg_Rnk','PPG_Rllg_Rnk_Diff',
    'last_10_games_total','last_10_points_total','Pts_Sn_Rllg','Pts_Sn_Rmg','last_2_years_PPG','Weighted_ma','last_2_years_MPG','last_2_years_Games_Total']]

    

    st.sidebar.header("4. Optimise on which Points")
    select_pts=st.sidebar.radio('Select the points you want to optimise',['years_sum_ppg','sum_ppg','Weighted_ma','PPG_Sn_Rllg','PPG_Sn_Rmg','Pts_Sn_Rmg','Pts_Sn_Rllg','Points_Season_Total', 'last_2_years_PPG','PPG_Total'])
    data_2=opt_data(data_1,select_pts)
    # st.write('this is correct data 2 I hope', data_2.head(10))

    # data_2022=pd.read_pickle('https://github.com/ZeNoonan/FPL/blob/master/raw_data_2022.pkl?raw=true')
    # data_2022=pd.read_csv('https://raw.githubusercontent.com/ZeNoonan/FPL/master/raw_data_2022.csv')
    # data_2022=data_2022.rename(columns={'Price':'Price_2022','team':'team_2022'})
    # st.write('dallas', data_2022[data_2022['full_name'].str.contains('harrison')])
    # data_2022.loc [ (data_2022['full_name']=='jack_harrison'), 'team_2022' ] = 'Leeds_Utd'
    # st.write('dallas', data_2022[data_2022['full_name'].str.contains('harrison')])
    # st.write('dallas', data_2022[data_2022['full_name'].str.contains('bamford')])
    # st.write('2022 data', data_2022.head())
    # st.write('add info',additional_info.head())
    # st.write('data 2',data_2.head())
    # data_update=pd.merge(data_2,data_2022,on='full_name',how='outer')
    # data_update=data_update[data_update['Price_2022'].notnull()].copy()
    # data_update=data_update.drop(['team','Price','Position_x'], axis=1).rename(columns={'team_2022':'team','Price_2022':'Price','Position_y':'Position'})
    data_2["GK"] = (data_2["Position"] == 'GK').astype(float)
    data_2["DF"] = (data_2["Position"] == 'DF').astype(float)
    data_2["MD"] = (data_2["Position"] == 'MD').astype(float)
    data_2["FW"] = (data_2["Position"] == 'FW').astype(float)
    data_2["LIV"] = (data_2["team"] == 'Liverpool').astype(float)
    data_2["MC"] = (data_2["team"] == 'Man_City').astype(float)
    data_2["ARS"] = (data_2["team"] == 'Arsenal').astype(float)
    data_2["LEI"] = (data_2["team"] == 'Leicester').astype(float)
    # st.write('after merge', data_2)
    # st.write('dallas', data_2[data_2['full_name'].str.contains('dallas')])
    
    # DO A MERGE HERE WITH THE NEW SPREADSHEET WHICH WILL HAVE THE PRICES, PRACTICE THIS
    data_2=data_2.dropna()
    data_2=exclude_players(data_2,names_selected)
    cols_to_move = ['full_name','team','Position','Price','years_sum_ppg']
    cols = cols_to_move + [col for col in data_2 if col not in cols_to_move]
    data_2=data_2[cols].reset_index().drop('index',axis=1)

# st.expander('Workings for 2024 '):
    data_2024=pd.read_csv('C:/Users/Darragh/Documents/Python/premier_league/fantasy_2024_06_07_23.csv')
    data_2024_for_optimisation=data_2024.loc[:,['full_name','team','Position','Price']]
    data_2_for_optimisation=data_2.drop(['team','Position','Price'],axis=1)
    merged_opt_data_2024=pd.merge(data_2024_for_optimisation,data_2_for_optimisation,how='left',on='full_name')
    # st.write('This is orignal data 2 before 2024', data_2)
    data_2=merged_opt_data_2024.dropna().reset_index(drop=True)
    data_2=data_2[~(data_2['full_name']=='ivan_toney')].reset_index(drop=True).copy()
    data_2=data_2[~(data_2['full_name']=='joel_matip')].reset_index(drop=True).copy()
    data_2=data_2[~(data_2['full_name']=='marcus_tavernier')].reset_index(drop=True).copy()
    data_2=data_2[~(data_2['full_name']=='joão_cancelo')].reset_index(drop=True).copy()
    # st.write('ivan',data_2[~(data_2['full_name']=='ivan_toney')])
    # st.write('This is data 2 after fixing up for 2024', data_2)

    # st.write('merged showing both', merged_opt_data_2024)
    # st.write('Filtered out NaN', merged_opt_data_2024.dropna())
    st.write('NaN rows just to check', merged_opt_data_2024[merged_opt_data_2024.isna().any(axis=1)].sort_values(by=['Price'],ascending=False))
    st.write('I have taken out Ivan Toney and Matip and Tavernier and Cancelo')
    # st.write('merge into this', data_2.head())

    # st.write('check for arsenal players in here', data_2)
    
    xg_data=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/xg_data.pkl').rename(columns={'Player':'full_name'})
    # st.write('xg_data', xg_data)
    xg_data.loc [ (xg_data['full_name']=='son_heung-min'), 'full_name' ] = 'heung-min_son'
    xg_data.loc [ (xg_data['full_name']=='bruno_fernandes'), 'full_name' ] = 'bruno miguel_borges fernandes'
    xg_data.loc [ (xg_data['full_name']=='i̇lkay_gündoğan'), 'full_name' ] = 'ilkay_gündogan'
    xg_data.loc [ (xg_data['full_name']=='bernardo_silva'), 'full_name' ] = 'bernardo mota_veiga de carvalho e silva'
    xg_data.loc [ (xg_data['full_name']=='joão_cancelo'), 'full_name' ] = 'joão pedro cavaco_cancelo'
    xg_data.loc [ (xg_data['full_name']=='ben_chilwell'), 'full_name' ] = 'benjamin_chilwell'
    xg_data.loc [ (xg_data['full_name']=='raphael_dias_belloli'), 'full_name' ] = 'raphael_dias belloli'
    xg_data.loc [ (xg_data['full_name']=='gabriel_jesus'), 'full_name' ] = 'gabriel fernando_de jesus'
    xg_data.loc [ (xg_data['full_name']=='emile_smith-rowe'), 'full_name' ] = 'emile_smith rowe'
    xg_data.loc [ (xg_data['full_name']=='robert_sánchez'), 'xg_xa_avg' ] = 1
    # xg_data.loc [ (xg_data['full_name']=='emile_smith-rowe'), 'full_name' ] = 'francisco_trincão'
    xg_data=xg_data.loc[:,['full_name','xg_xa_avg']]

    df_try=pd.merge(data_2,xg_data,on='full_name',how='left')
    # data_2=df_try.loc[:,['full_name', 'Position','team', 'xg_xa_avg', 'Price','PPG_Season_Value','GK','DF','MD','FW','LIV','MC','LEI']].fillna(0).rename(columns={'xg_xa_avg':'years_sum_ppg'})

    
    F_3_5_2=optimise_fpl(3,5,2, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_4_5_1=optimise_fpl(4,5,1, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_4_4_2=optimise_fpl(4,4,2, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_5_3_2=optimise_fpl(5,3,2, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_5_4_1=optimise_fpl(5,4,1, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_3_4_3=optimise_fpl(3,4,3, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_5_2_3=optimise_fpl(5,2,3, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    F_4_3_3=optimise_fpl(4,3,3, squad_cost=squad_cost, fpl_players1=data_2, select_pts=select_pts)
    formations=[F_3_5_2,F_4_5_1,F_4_4_2,F_5_3_2,F_5_4_1,F_3_4_3,F_5_2_3,F_4_3_3]

    # st.write('check optimisation', F_3_5_2)

    data_3=table(formations,select_pts)
    data_4=pd.merge(data_3, additional_info, on='full_name', how='left',suffixes=('', '_y'))
    cols_to_move = ['full_name','Position','Count','team','Price','years_sum_ppg','years_sum_games','PPG_Sn_Rllg','Gms_Ssn_to_Date','Games_Total','PPG_Total',
                    'years_mins_ppg','sum_ppg','mins_ppg','ppg_last_10_games',
                    'last_2_years_PPG','last_2_years_MPG','last_2_years_Games_Total',
    'Pts_Sn_Rllg','Pts_Sn_Rllg_Rnk',
    'F_3_4_3','F_4_3_3','F_3_5_2','F_4_5_1','F_4_4_2','F_5_3_2','F_5_4_1','F_5_2_3',
    'PPG_Sn_Rllg_Rnk','PPG_Sn_Rmg','PPG_Sn_Rllg_Rmg_Rnk','PPG_Rllg_Rnk_Diff','Games_Ssn_Rmg','Pts_Sn_Rmg','Pts_Sn_Rllg_Rmg_Rnk',
    'last_10_points_total','last_10_games_total','Value','Gms_Ssn_Total',
    'Games_Total_Rolling','week','points_per_game']
    cols = cols_to_move + [col for col in data_4 if col not in cols_to_move]
    data_5=data_4[cols]

    

    data_5=data_5.reset_index(drop=True)  # https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-dataframe cos of duplicate index causing issue with style
    st.write (data_5.set_index('full_name').style.format(format_dict))
    st.write('years_sum_games = last 15 games * 1, 15*0.5=7.5, 15*.25=3.25, 15*0.125=1.875')
    st.write('Total Games = 15+7.5+3.25+1.875 = 27.625')
    st.write('years_sum_ppg = take last 15 games/points x 1, then 15 games before that multipy by 0.5 and so on so basically you have 60 games in total weighted towards\
             last 15 games played')
    # st.write('Now where is Haaland?')


    st.write (cost_total(data_5,selection1='Price', selection2=select_pts))
    with st.expander('Listing of players'):
        # cols_to_move = ['full_name','team','Position','Price','years_sum_ppg']
        # cols = cols_to_move + [col for col in data_2 if col not in cols_to_move]
        # data_2=data_2[cols].reset_index().drop('index',axis=1)
        st.write('Note that the PPG season value is the 15 game 1/0.5 etc Aaron Brown adj')
        # st.write('data 2024',data_2024_for_optimisation)



        player_listing_data_analysis_to_merge=player_listing_data_analysis.drop(['Price','team','Position'],axis=1)\
        .sort_values(by=['full_name','year','week'],ascending=[True,True,True]).drop_duplicates(subset=['full_name'],keep='last')
        # st.write('luiz?', player_listing_data_analysis_to_merge[player_listing_data_analysis_to_merge['full_name'].str.contains('luis')])


        cols_to_move = ['full_name','year','week','years_sum_ppg','PPG_Sn_Rllg','value','PPG_Total_Rolling','Games_Total','Gms_Ssn_to_Date',
                        'Pts_Sn_Rllg','Points_Season_Total','PPG_Total',
                        'Game_1','Clean_Pts']
        cols = cols_to_move + [col for col in player_listing_data_analysis_to_merge if col not in cols_to_move]
        player_listing_data_analysis_to_merge=player_listing_data_analysis_to_merge[cols]

        combined_listing=pd.merge(data_2024_for_optimisation,player_listing_data_analysis_to_merge,how='left',on='full_name')
        combined_listing['value']=combined_listing['years_sum_ppg'] / combined_listing['Price']
        combined_listing=combined_listing[combined_listing['Games_Total']>3].copy()



        st.write('player listing', combined_listing.sort_values(by=['years_sum_ppg','Price'],ascending=False).style.format(format_dict))
        st.write('useful for sense checking',data_2.sort_values(by=['years_sum_ppg','Price'],ascending=False))
        # st.markdown(get_table_download_link(data_2.sort_values(by='Price',ascending=False)), unsafe_allow_html=True)

    with st.expander('Click to select a player detail'):
        player_names_pick=all_seasons_df_1['full_name'].unique()
        names_selected_pick = st.selectbox('Select players',player_names_pick, key='player_pick',index=1)
        player_selected_detail_by_week = all_seasons_df_1[all_seasons_df_1['full_name']==names_selected_pick]

        cols_to_move = ['full_name','Position','Price','team','year','week','Game_1','Clean_Pts','minutes','Games_Total','Gms_Ssn_to_Date',
                        'years_sum_ppg','value','PPG_Sn_Rllg','PPG_Total',
                        'last_2_years_Games_Total',
                        'years_last_12_points','years_last_8_points_calc','years_last_12_games','years_last_8_games_calc',
                        'last_10_points_total','last_10_games_total',
                        'ppg_last_10_games','Games_Total_Rolling',
        ]
        cols = cols_to_move + [col for col in player_selected_detail_by_week if col not in cols_to_move]
        player_selected_detail_by_week=player_selected_detail_by_week[cols]

        st.write( player_selected_detail_by_week.sort_values(by=['year','week'],ascending=[False,False]).style.format(format_dict) )
        st.download_button(label="Download data as CSV",data=player_selected_detail_by_week.sort_values(by=['year','week'],ascending=[False,False])\
                           .to_csv().encode('utf-8'),
                           file_name='df_player_listing.csv',mime='text/csv',key='after_merge_spread')
        # st.markdown(get_table_download_link(player_selected_detail_by_week), unsafe_allow_html=True)

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

    

    pick_data = pd.read_csv(pick).rename(columns = {'total_points':'week_points'})
    return pd.merge(url_csv,pick_data, on='player_id',how ='outer')

@st.cache(suppress_st_warning=True)
def data_2020_clean_double_gw(url_pick2020):
    url_pick2020=url_pick2020[ ~(url_pick2020['round']==29) | ~(url_pick2020['fixture']==275)]
    url_pick2020.loc[:,'week']=url_pick2020['week'].replace({39:30,40:31,41:32,42:33,43:34,44:35,45:36,46:37,47:38})
    url_pick2020.loc[:,'round']=url_pick2020['round'].replace({39:30,40:31,41:32,42:33,43:34,44:35,45:36,46:37,47:38})
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
def data_2024_team_names(file):
    file['team'] = file['team'].map({1: 'Arsenal', 2: 'Aston_Villa', 3: 'Bournemouth', 4:'Brentford', 5:'Brighton',6:'Burnley',7:'Chelsea',8:'Crystal_Palace',
    9:'Everton',10:'Fulham',11:'Liverpool',12:'Luton_Town',13:'Man_City',14:'Man_Utd',15:'Newcastle',16:'Nottingham_Forest',17:'Sheffield_Utd',
    18:'Spurs',19:'West_Ham',20:'Wolves'})
    return file


@st.cache(suppress_st_warning=True)
def data_2023_team_names(file):
    file['team'] = file['team'].map({1: 'Arsenal', 2: 'Aston_Villa', 3: 'Bournemouth', 4:'Brentford', 5:'Brighton',6:'Chelsea',7:'Crystal_Palace',8:'Everton',
    9:'Fulham',10:'Leicester',11:'Leeds_Utd',12:'Liverpool',13:'Man_City',14:'Man_Utd',15:'Newcastle',16:'Nottingham_Forest',17:'Southampton',
    18:'Spurs',19:'West_Ham',20:'Wolves'})
    return file

@st.cache(suppress_st_warning=True)
def data_2022_team_names(file):
    file['team'] = file['team'].map({1: 'Arsenal', 2: 'Aston_Villa', 3: 'Brentford', 4:'Brighton', 5:'Burnley',6:'Chelsea',7:'Crystal_Palace',8:'Everton',
    9:'Leicester',10:'Leeds_Utd',11:'Liverpool',12:'Man_City',13:'Man_Utd',14:'Newcastle',15:'Norwich',16:'Southampton',17:'Spurs',
    18:'Watford',19:'West_Ham',20:'Wolves'})
    return file

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
    
    df['Game_1'] = np.where((df['minutes'] > 0.5), 1, 0) # if you change this to np Nan, the games season to date doesn't work
    # just be careful, i initially changed the 0 to np.Nan, why, something wasn't working, what was i trying to fix, i think it was
    # the 15 game average thing, but its called 10 game rolling points cos i didn't bother to change


    df['Clean_Pts'] = np.where(df['Game_1']==1,df['week_points'], np.NaN) # setting a slice on a slice - just suppresses warning....
    df = df.sort_values(by=['full_name', 'year', 'week'], ascending=[True, True, True]) # THIS IS IMPORTANT!! EWM doesn't work right unless sorted
    df['EWM_Pts'] = df['Clean_Pts'].ewm(alpha=0.07).mean()
    weights = np.array([0.125, 0.25,0.25,0.5,0.5,0.5,0.5,1,1,1,1,1,1,1,1]) # the order mattered!! took me a while to figure this out
    sum_weights = np.sum(weights)
    df['Weighted_ma'] = (df['Clean_Pts'].fillna(0).rolling(window=15, center=False)\
        .apply(lambda x: np.sum(weights*x) / sum_weights, raw=False)) # raw=False
        # using the fillna ensures no NaN as this function requires min 4 data points in a row - .fillna(method='ffill')
        # so just be careful the result is the last time player had 4 weeks in a row
        # don't think this is working right, think it is including 0 in previous week if you didn't play
    df['Weighted_mins'] = (df['minutes'].rolling(window=15, center=False)\
    .apply(lambda x: np.sum(weights*x) / sum_weights, raw=False)) # raw=False

    df['last_10_games_total'] = df.groupby(['full_name'])['Game_1'].rolling(window=15,min_periods=3, center=False).sum().reset_index(0,drop=True)
    df['last_10_points_total'] = df.groupby(['full_name'])['Clean_Pts'].rolling(window=15,min_periods=3, center=False).sum().reset_index(0,drop=True)
    df['ppg_last_10_games'] = (df['last_10_points_total'] / df['last_10_games_total']).fillna(0)

    df=df.reset_index().rename(columns={'index':'id_merge'})
    df_calc=df[df['Game_1']>0].copy()
    df_calc['last_15_games']=df_calc.groupby(['full_name'])['Game_1'].rolling(window=15,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_14_games']=df_calc.groupby(['full_name'])['Game_1'].rolling(window=14,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_12_games']=df_calc.groupby(['full_name'])['Game_1'].rolling(window=12,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_8_games_calc']=df_calc.groupby(['full_name'])['Game_1'].rolling(window=8,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_15_points']=df_calc.groupby(['full_name'])['Clean_Pts'].rolling(window=15,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_14_points']=df_calc.groupby(['full_name'])['Clean_Pts'].rolling(window=14,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_12_points']=df_calc.groupby(['full_name'])['Clean_Pts'].rolling(window=12,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_8_points_calc']=df_calc.groupby(['full_name'])['Clean_Pts'].rolling(window=8,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_4_points_calc']=(df_calc['last_12_points']-df_calc['last_8_points_calc'])/2
    df_calc['last_2_points_calc']=(df_calc['last_14_points']-df_calc['last_12_points'])/4
    df_calc['last_1_points_calc']=(df_calc['last_15_points']-df_calc['last_14_points'])/8
    df_calc['last_4_games_calc']=(df_calc['last_12_games']-df_calc['last_8_games_calc'])/2
    df_calc['last_2_games_calc']=(df_calc['last_14_games']-df_calc['last_12_games'])/4
    df_calc['last_1_games_calc']=(df_calc['last_15_games']-df_calc['last_14_games'])/8
    df_calc['last_15_mins']=df_calc.groupby(['full_name'])['minutes'].rolling(window=15,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_14_mins']=df_calc.groupby(['full_name'])['minutes'].rolling(window=14,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_12_mins']=df_calc.groupby(['full_name'])['minutes'].rolling(window=12,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_8_mins_calc']=df_calc.groupby(['full_name'])['minutes'].rolling(window=8,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['last_4_mins_calc']=(df_calc['last_12_mins']-df_calc['last_8_mins_calc'])/2
    df_calc['last_2_mins_calc']=(df_calc['last_14_mins']-df_calc['last_12_mins'])/4
    df_calc['last_1_mins_calc']=(df_calc['last_15_mins']-df_calc['last_14_mins'])/8
    df_calc['sum_games']=df_calc.loc[:,['last_8_games_calc','last_4_games_calc','last_2_games_calc','last_1_games_calc']].sum(axis=1)
    df_calc['sum_points']=df_calc.loc[:,['last_8_points_calc','last_4_points_calc','last_2_points_calc','last_1_points_calc']].sum(axis=1)
    df_calc['sum_ppg']=df_calc['sum_points']/df_calc['sum_games']
    df_calc['sum_mins']=df_calc.loc[:,['last_8_mins_calc','last_4_mins_calc','last_2_mins_calc','last_1_mins_calc']].sum(axis=1)
    df_calc['mins_ppg']=df_calc['sum_mins']/df_calc['sum_games']
    df_calc['4_games_rolling_mins']=df_calc.groupby(['full_name'])['minutes'].rolling(window=4,min_periods=1, center=False).sum().reset_index(0,drop=True)
    # df_calc['4_games_rolling_mins']=df_calc['4_games_rolling_mins'].fillna(method='ffill')

    df=pd.merge(df,df_calc,how='outer')
    df['sum_ppg']=df['sum_ppg'].fillna(method='ffill')
    df['mins_ppg']=df['mins_ppg'].fillna(method='ffill')

    df_calc['years_last_15_games']=df_calc.groupby(['full_name'])['Game_1'].rolling(window=60,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_14_games']=df_calc.groupby(['full_name'])['Game_1'].rolling(window=45,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_12_games']=df_calc.groupby(['full_name'])['Game_1'].rolling(window=30,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_8_games_calc']=df_calc.groupby(['full_name'])['Game_1'].rolling(window=15,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_4_games_calc']=(df_calc['years_last_12_games']-df_calc['years_last_8_games_calc'])/2
    df_calc['years_last_2_games_calc']=(df_calc['years_last_14_games']-df_calc['years_last_12_games'])/4
    df_calc['years_last_1_games_calc']=(df_calc['years_last_15_games']-df_calc['years_last_14_games'])/8
    
    
    
    df_calc['years_last_15_points']=df_calc.groupby(['full_name'])['Clean_Pts'].rolling(window=60,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_14_points']=df_calc.groupby(['full_name'])['Clean_Pts'].rolling(window=45,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_12_points']=df_calc.groupby(['full_name'])['Clean_Pts'].rolling(window=30,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_8_points_calc']=df_calc.groupby(['full_name'])['Clean_Pts'].rolling(window=15,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_4_points_calc']=(df_calc['years_last_12_points']-df_calc['years_last_8_points_calc'])/2
    df_calc['years_last_2_points_calc']=(df_calc['years_last_14_points']-df_calc['years_last_12_points'])/4
    df_calc['years_last_1_points_calc']=(df_calc['years_last_15_points']-df_calc['years_last_14_points'])/8
    df_calc['years_last_15_mins']=df_calc.groupby(['full_name'])['minutes'].rolling(window=60,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_14_mins']=df_calc.groupby(['full_name'])['minutes'].rolling(window=45,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_12_mins']=df_calc.groupby(['full_name'])['minutes'].rolling(window=30,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_8_mins_calc']=df_calc.groupby(['full_name'])['minutes'].rolling(window=15,min_periods=1, center=False).sum().reset_index(0,drop=True)
    df_calc['years_last_4_mins_calc']=(df_calc['years_last_12_mins']-df_calc['years_last_8_mins_calc'])/2
    df_calc['years_last_2_mins_calc']=(df_calc['years_last_14_mins']-df_calc['years_last_12_mins'])/4
    df_calc['years_last_1_mins_calc']=(df_calc['years_last_15_mins']-df_calc['years_last_14_mins'])/8
    df_calc['years_sum_games']=df_calc.loc[:,['years_last_8_games_calc','years_last_4_games_calc','years_last_2_games_calc','years_last_1_games_calc']].sum(axis=1)
    df_calc['years_sum_points']=df_calc.loc[:,['years_last_8_points_calc','years_last_4_points_calc','years_last_2_points_calc','years_last_1_points_calc']].sum(axis=1)
    df_calc['years_sum_ppg']=df_calc['years_sum_points']/df_calc['years_sum_games']
    df_calc['value_years_sum_ppg']=df_calc['years_sum_ppg']/df_calc['Price']
    df_calc['years_sum_mins']=df_calc.loc[:,['years_last_8_mins_calc','years_last_4_mins_calc','years_last_2_mins_calc','years_last_1_mins_calc']].sum(axis=1)
    df_calc['years_mins_ppg']=df_calc['years_sum_mins']/df_calc['years_sum_games']
    
    df=pd.merge(df,df_calc,how='outer')
    df['years_sum_ppg']=df['years_sum_ppg'].fillna(method='ffill')
    df['value_years_sum_ppg']=df['value_years_sum_ppg'].fillna(method='ffill')
    df['years_mins_ppg']=df['years_mins_ppg'].fillna(method='ffill')

    df['years_sum_games']=df['years_sum_games'].fillna(method='ffill')


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
    # df['PPG_Season_Value'] = df['PPG_Season_Total'] / df['Price']
    df['PPG_Season_Value'] = df['years_sum_ppg'] / df['Price']
    df['Pts_Sn_Rmg'] = df['Points_Season_Total'] - df['Pts_Sn_Rllg']
    df['Games_Ssn_Rmg'] = (df['Gms_Ssn_Total'] - df['Gms_Ssn_to_Date'])
    df['PPG_Sn_Rmg'] = (df['Pts_Sn_Rmg'] / df['Games_Ssn_Rmg']).fillna(0)
    df['PPG_Sn_Rllg_Rnk'] = df.groupby(['week','year','Position'])['PPG_Sn_Rllg'].rank(method='dense', ascending=False)
    df['PPG_Sn_Rllg_Rmg_Rnk'] = df.groupby(['week','year','Position'])['PPG_Sn_Rmg'].rank(method='dense', ascending=False)
    df['PPG_Rllg_Rnk_Diff'] = (df['PPG_Sn_Rllg_Rnk'] - df['PPG_Sn_Rllg_Rmg_Rnk'])
    df['Pts_Sn_Rllg_Rnk'] = df.groupby(['week','year','Position'])['Pts_Sn_Rllg'].rank(method='dense', ascending=False)
    df['Pts_Sn_Rllg_Rmg_Rnk'] = df.groupby(['week','year','Position'])['Pts_Sn_Rmg'].rank(method='dense', ascending=False)
    df['Pts_Rllg_Rnk_Diff'] = (df['Pts_Sn_Rllg_Rnk'] - df['Pts_Sn_Rllg_Rmg_Rnk'])
    
    year_filter=((df['year']==2021) | (df['year']==2020) | (df['year']==2022) | (df['year']==current_year))
    df['last_2_years_games'] = df['Game_1'].where(year_filter)
    df['last_2_years_points'] = df['week_points'].where(year_filter)
    df['last_2_years_mins'] = df['minutes'].where(year_filter)
    df['last_2_years_Games_Total'] = df.groupby (['full_name'])['last_2_years_games'].transform('sum')
    df['last_2_years_mins_Total'] = df.groupby (['full_name'])['last_2_years_mins'].transform('sum')
    df['last_2_years_Points_Total'] = df.groupby (['full_name'])['last_2_years_points'].transform('sum')
    df['last_2_years_PPG'] = df['last_2_years_Points_Total'] / df['last_2_years_Games_Total']
    df['last_2_years_MPG'] = df['last_2_years_mins_Total'] / df['last_2_years_Games_Total']
    
    df["GK"] = (df["Position"] == 'GK').astype(float)
    df["DF"] = (df["Position"] == 'DF').astype(float)
    df["MD"] = (df["Position"] == 'MD').astype(float)
    df["FW"] = (df["Position"] == 'FW').astype(float)
    df["LIV"] = (df["team"] == 'Liverpool').astype(float)
    df["MC"] = (df["team"] == 'Man_City').astype(float)
    df["LEI"] = (df["team"] == 'Leicester').astype(float)
    df["ARS"] = (df["team"] == 'Arsenal').astype(float)
    return df

def show_data(df, year, week, min_games_played, season_games_played, last_2_years):
    df= df [ (df['year']==year) & (df['week']==week) & (df['Games_Total'] >= min_games_played) & (df['Gms_Ssn_to_Date'] >= season_games_played) \
            & (df['last_2_years_Games_Total'] >= last_2_years) ]    
    # df= df [ (df['year']==year) & (df['week']==week) & (df['Games_Total'] >= min_games_played) & (df['Gms_Ssn_to_Date'] >= season_games_played) & (df['last_2_years_Games_Total'] >= last_2_years) ]
    df=df.sort_values (by ='kickoff_time', ascending=True).drop_duplicates(subset=['full_name'], keep='last') # this is for Double Gameweeks as was an issue for concating dataframes where name was in twice as played twice
    return df

def exclude_players(df, *args):
    for x in args:
        df.loc [ (df['full_name'].isin(x)), 'Price' ] = 1000 # for some reason isin worked rather than == sometime to do with lengths dont match 
    return df # think it might be do with == returns a value dont know

def opt_data(x,select_pts):
    return x[['full_name', 'Position','team', select_pts, 'Price','PPG_Season_Value','GK','DF','MD','FW','LIV','MC','LEI','ARS']].reset_index().drop('index', axis=1)

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
    ARSs={}
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
        ARSs[decision_var] = player["ARS"]
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
    ARS_constraint = LpAffineExpression(ARSs)
    total_players = LpAffineExpression(number_of_players)
    model += (GK_constraint == 1)
    model += (DF_constraint == df)
    model += (MD_constraint == md)
    model += (FW_constraint == fw)
    model += (LIV_constraint <= 3)
    model += (MC_constraint <= 3)
    model += (LEI_constraint <= 3)
    model += (ARS_constraint <= 3)
    model += (total_players <= number_players)
    model.solve()
    fpl_players1["is_drafted"] = 0.0 # HERE
    # st.write (fpl_players1.head())
    for var in model.variables():
        # st.write('this is the model variables below:', model.variables())
        # st.write('this is the var.varValue below:', var.varValue)
        fpl_players1.iloc[int(var.name[1:]),14] = var.varValue # HERE IF you are adding team constraints increase this by 1
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