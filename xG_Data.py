import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO
import os
import base64 
import altair as alt
from st_aggrid import AgGrid, GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import seaborn as sns


st.set_page_config(layout="wide")

def scraper_pl():
    df=[]
    urls=[
    'https://fbref.com/en/matches/ce4d873f/Newcastle-United-Norwich-City-November-30-2021-Premier-League',
    'https://fbref.com/en/matches/b0ab4044/Leeds-United-Crystal-Palace-November-30-2021-Premier-League',
    'https://fbref.com/en/matches/2049300f/West-Ham-United-Brighton-and-Hove-Albion-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/a3fc2ddc/Wolverhampton-Wanderers-Burnley-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/f475576b/Watford-Chelsea-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/135f5959/Southampton-Leicester-City-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/1993b7ec/Aston-Villa-Manchester-City-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/b46554fb/Merseyside-Derby-Everton-Liverpool-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/4323a38f/Manchester-United-Arsenal-December-2-2021-Premier-League',
    'https://fbref.com/en/matches/a80b3790/Tottenham-Hotspur-Brentford-December-2-2021-Premier-League',
    ]

    week=14
    for x in urls:
        dfa=pd.read_html(x)
        home_stats=dfa[3]
        away_stats=dfa[10] 
        df.append(home_stats)
        df.append(away_stats)
    dx=pd.concat(df)
    dx[('week','week')]=week
    dx.to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_14_test_test_test.pkl')
    return dx
# scraper_pl()

def team_scraper_pl():
    df=[]
    urls=[
    'https://fbref.com/en/matches/ce4d873f/Newcastle-United-Norwich-City-November-30-2021-Premier-League',
    'https://fbref.com/en/matches/b0ab4044/Leeds-United-Crystal-Palace-November-30-2021-Premier-League',
    'https://fbref.com/en/matches/2049300f/West-Ham-United-Brighton-and-Hove-Albion-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/a3fc2ddc/Wolverhampton-Wanderers-Burnley-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/f475576b/Watford-Chelsea-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/135f5959/Southampton-Leicester-City-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/1993b7ec/Aston-Villa-Manchester-City-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/b46554fb/Merseyside-Derby-Everton-Liverpool-December-1-2021-Premier-League',
    'https://fbref.com/en/matches/4323a38f/Manchester-United-Arsenal-December-2-2021-Premier-League',
    'https://fbref.com/en/matches/a80b3790/Tottenham-Hotspur-Brentford-December-2-2021-Premier-League',
    ]

    week=14
    for x in urls:
        dfa=pd.read_html(x)
        team_names_test=dfa[2]
        home_stats_test=dfa[3]
        away_stats_test=dfa[10]
        team_names_test.columns=team_names_test.columns.swaplevel().droplevel()
        home_stats_test.columns=home_stats_test.columns.droplevel()
        away_stats_test.columns=away_stats_test.columns.droplevel()
        home_stats_test=home_stats_test.iloc[-1:,:]
        home_stats_test=home_stats_test.loc[:,['npxG','xA']].reset_index().drop('index',axis=1).rename(index={0:team_names_test.columns[0]})
        away_stats_test=away_stats_test.iloc[-1:,:]
        away_stats_test=away_stats_test.loc[:,['npxG','xA']].reset_index().drop('index',axis=1).rename(index={0:team_names_test.columns[1]})
        
        home_conceded=(away_stats_test*-1).rename(index={team_names_test.columns[1]:team_names_test.columns[0]}).rename(columns={'npxG':'npxG_concede','xA':'xA_concede'})
        home_xg=pd.concat([home_stats_test,home_conceded],axis=1)

        away_conceded=(home_stats_test*-1).rename(index={team_names_test.columns[0]:team_names_test.columns[1]}).rename(columns={'npxG':'npxG_concede','xA':'xA_concede'})
        away_xg=pd.concat([away_stats_test,away_conceded],axis=1)        


        df.append(home_xg)
        df.append(away_xg)
    dx=pd.concat(df)
    dx['week']=week
    dx.to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_14.pkl')
    return dx

# team_scraper_pl()

# check_test=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_test.pkl')
# st.write('lets have a look', check_test)



# urls_test='https://fbref.com/en/matches/17e86f90/Crystal-Palace-Tottenham-Hotspur-September-11-2021-Premier-League'
# dfa=pd.read_html(urls_test)
# # st.write('0',dfa[0])
# # st.write('1',dfa[1]) 
# st.write('2',dfa[2])
# dfa[2].to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_names_test.pkl')
# dfa[3].to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/home_stats_test.pkl')
# dfa[10].to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/away_stats_test.pkl')
# team_names_test=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_names_test.pkl')
# away_stats_test=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/away_stats_test.pkl')
# home_stats_test=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/home_stats_test.pkl')
# st.write('team names', team_names_test)

# team_names_test.columns=team_names_test.columns.swaplevel().droplevel()
# st.write('home names', team_names_test.columns[0])
# st.write('away names', team_names_test.columns[1])
# home_stats_test.columns=home_stats_test.columns.droplevel()
# away_stats_test.columns=away_stats_test.columns.droplevel()
# st.write('home stats', home_stats_test)
# home_stats_test=home_stats_test.iloc[-1:,:]
# home_stats_test=home_stats_test.loc[:,['npxG','xA']].reset_index().drop('index',axis=1).rename(index={0:team_names_test.columns[0]})
# away_stats_test=away_stats_test.iloc[-1:,:]
# away_stats_test=away_stats_test.loc[:,['npxG','xA']].reset_index().drop('index',axis=1).rename(index={0:team_names_test.columns[1]})

# home_conceded=(away_stats_test*-1).rename(index={team_names_test.columns[1]:team_names_test.columns[0]}).rename(columns={'npxG':'npxG_concede','xA':'xA_concede'})
# st.write('conceded for home team',home_conceded)
# home_stats_test=pd.concat([home_stats_test,home_conceded],axis=1)


# st.write('home stats', home_stats_test)
# st.write('away stats', away_stats_test)

# st.write('4',dfa[4])
# st.write('5',dfa[5])
# st.write('6',dfa[6])
# st.write('7',dfa[7])
# st.write('8',dfa[8])
# st.write('9',dfa[9])






# st.write(dx)
# dx.columns=dx.columns.droplevel()

# dx['Week']=week
# # dx = dx.loc[:,["Player","npxG","xA","xG","Sh","SoT","Pos","Min","Week"]]
# dx = dx.loc[:,["Player","npxG","xA","xG","Sh","SoT","Pos","Min","Week"]]
# dx.loc [ (dx['Player']=='gabriel_jesus'), 'Player' ] = 'gabriel_fernando_de_jesus'
# dx.loc [ (dx['Player']=='son_heung-min'), 'Player' ] = 'heung-min_son'
# dx.loc [ (dx['Player']=='dele_alli'), 'Player' ] = 'bamidele_alli'
# dx.loc [ (dx['Player']=='richarlison'), 'Player' ] = 'richarlison_de_andrade'
# dx.loc [ (dx['Player']=='bernardo_silva'), 'Player' ] = 'bernardo_mota_veiga_de_carvalho_e_silva'
# dx.loc [ (dx['Player']=='gylfi_sigursson'), 'Player' ] = 'gylfi_sigurdsson'
# dx.loc [ (dx['Player']=='lucas_moura'), 'Player' ] = 'lucas_rodrigues_moura_da_silva'
# dx.loc [ (dx['Player']=='felipe_anderson'), 'Player' ] = 'felipe_anderson_pereira_gomes'
# dx.loc [ (dx['Player']=='ricardo_pereira'), 'Player' ] = 'ricardo_domingos_barbosa_pereira'
# dx.loc [ (dx['Player']=='ben_chilwell'), 'Player' ] = 'benjamin_chilwell'
# dx.loc [ (dx['Player']=='emerson'), 'Player' ] = 'emerson_palmieri_dos_santos'
# dx.loc [ (dx['Player']=='joao_cancelo'), 'Player' ] = 'joao_pedro_cavaco_cancelo'
# # dx.to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_1_test_test.pkl')

# dx.to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_2_2021_1.pkl')



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

# This is my test for making sure I have imported correctly so total mins should equal mins played in week
# st.write (dx['Min'].sum())
# st.write ('number of estimated minutes', 11*90*20)

# df_fbref = df_fbref.drop_duplicates(subset=['Player'], keep = 'first')
# df_fbref=df_fbref.rename(columns = {'Player':'Name'})
# df_fbref['Name'] = df_fbref['Name'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')



# week_23=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_23_stats.pkl')
# week_22=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_22_stats.pkl')
# week_21=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_21_stats.pkl')
# week_20=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_20_stats.pkl')
# week_19=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_19_stats.pkl')
# week_18=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_18_stats.pkl')
# week_17=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_17_stats.pkl')
# week_16=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_16_stats.pkl')
# week_15=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_15_stats.pkl')
# week_15['Week']=15
week_14=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_14_test_test_test.pkl')
# week_14['Week']=14
week_13=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_13_test_test_test.pkl')
week_12=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_12_test_test_test.pkl')
week_11=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_11_test_test_test.pkl')
week_10=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_10_test_test_test.pkl')
week_9=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_9_test_test_test.pkl')
week_8=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_8_test_test_test.pkl')
week_7=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_7_test_test_test.pkl')
week_6=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_6_test_test_test.pkl')
week_5=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_5_test_test_test.pkl')
week_4=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_4_test_test_test.pkl')
week_3=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_3_test_test_test.pkl')
week_2=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_2_test_test_test.pkl')
week_1=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_1_test_test_test.pkl')

# combined=pd.concat([week_22,week_21,week_20, week_19, week_18, week_17, week_16, week_15, week_14, week_13, week_12, week_11, week_10, week_9, week_8, week_7, week_6, week_5, week_4,week_3,week_2, week_1])

combined=pd.concat([week_1,week_2,week_3,week_4,week_5,week_6,week_7,week_8,week_9,week_10,week_11,week_12,week_13,week_14])
combined[("Unnamed: 0_level_0","Player")]=combined[("Unnamed: 0_level_0","Player")].str.lower()
combined[("Unnamed: 0_level_0","Player")]=combined[("Unnamed: 0_level_0","Player")].replace(" ", "_", regex=True)
combined[("Expected","xg_xa")]=combined[("Expected","npxG")]+combined[("Expected","xA")]
# combined.to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/xg_2021_season_to_date.pkl')

# st.write('combined', combined)
data = combined.loc[:,[("week","week"),("Unnamed: 0_level_0","Player"),("Expected","npxG"),("Expected","xA"),("Expected","xG"),("Performance","Sh"),("Performance","SoT"),
("Unnamed: 3_level_0","Pos"),("Unnamed: 5_level_0","Min"),("Performance","Tkl"),("Performance","Int"),("Performance","Press"),
("Passes","Prog"),("Carries","Prog"),("Expected","xg_xa")]]


data=data.dropna()
data=data[data[("Unnamed: 0_level_0","Player")].str.contains("14_players")==False]
# st.write('salah data')
# st.write(data[data[("Unnamed: 0_level_0","Player")].str.contains('salah')])
with st.beta_expander('Full Data'):
    st.write('full data',data)
    st.write('full data',data[data[("Unnamed: 0_level_0","Player")].str.contains('wang')])

clean_data=data.copy()
clean_data.columns=clean_data.columns.droplevel()
# st.write(clean_data.head())
grouped_clean_data = clean_data.groupby('Player').agg(xg_xa_avg = ('xg_xa', 'mean'), xg_xa_sum = ('xg_xa', 'sum'), xg_xa_count=('xg_xa', 'count'), 
shots_avg=('Sh', 'mean'),std_dev=('xg_xa', 'std') ).sort_values(by='xg_xa_avg',ascending=False)

test_grouped_clean_data = clean_data.groupby(['Player','Pos']).agg(xg_xa_avg = ('xg_xa', 'mean'), xg_xa_sum = ('xg_xa', 'sum'), xg_xa_count=('xg_xa', 'count'), 
shots_avg=('Sh', 'mean'),std_dev=('xg_xa', 'std') ).sort_values(by='xg_xa_avg',ascending=False).reset_index()
# st.write('test', test_grouped_clean_data)

position_data=pd.read_excel('C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/updated_positions.xlsx')
# st.write(position_data)
st.write('Just to note the Positions change on a week by week basis on FB Ref')
updated_data=pd.merge(grouped_clean_data,position_data, on='Player', how='outer')
# st.write(updated_data)

# positions=pd.DataFrame(test_grouped_clean_data['Pos'].unique()).reset_index()

# st.write(test_grouped_clean_data['Pos'].unique())

# st.markdown(get_table_download_link(grouped_clean_data), unsafe_allow_html=True)


# https://stackoverflow.com/questions/64145551/simplest-way-to-heatmap-selected-columns-in-python
# https://seaborn.pydata.org/tutorial/color_palettes.html
cm = sns.color_palette("Spectral", as_cmap=True)

min_games_played = st.number_input ("Minimum number of games ever", min_value=int(0),value=int(6))
updated_data=updated_data[updated_data['xg_xa_count'] >= min_games_played]


st.write(updated_data.style.format(formatter={'xg_xa_avg': "{:,.2f}",'xg_xa_sum': "{:,.1f}",'xg_xa_count': "{:,.0f}",'shots_avg': "{:,.1f}",'std_dev': "{:,.1f}"}).background_gradient(cmap=cm, subset=["std_dev",'xg_xa_avg']))

# updated_data.to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/fpl_1/xg_data.pkl')

defender_data=updated_data[(updated_data['position']=='D')].copy()
midfielder_data=updated_data[updated_data['position']=='M'].copy()
forward_data=updated_data[updated_data['position']=='F'].copy()
st.write('Defenders:')
st.write(defender_data.style.format(formatter={'xg_xa_avg': "{:,.2f}",'xg_xa_count': "{:,.0f}",'xg_xa_sum': "{:,.1f}",'shots_avg': "{:,.1f}",'std_dev': "{:,.1f}"}).background_gradient(cmap=cm, subset=["std_dev",'xg_xa_avg']))
st.write('Midfielders:')
st.write(midfielder_data.style.format(formatter={'xg_xa_avg': "{:,.2f}",'xg_xa_count': "{:,.0f}",'xg_xa_sum': "{:,.1f}",'shots_avg': "{:,.1f}",'std_dev': "{:,.1f}"}).background_gradient(cmap=cm, subset=["std_dev",'xg_xa_avg']))
st.write('Forwards:')
st.write(forward_data.style.format(formatter={'xg_xa_avg': "{:,.2f}",'xg_xa_count': "{:,.0f}",'xg_xa_sum': "{:,.1f}",'shots_avg': "{:,.1f}",'std_dev': "{:,.1f}"}).background_gradient(cmap=cm, subset=["std_dev",'xg_xa_avg']))

# st.write('cumulative figures',grouped_clean_data.sort_values(by='xg_xa_avg',ascending=False))

# st.write(clean_data)
# clean_data['xg_xa_count']=clean_data.groupby(['Player','week'])['Min'].transform('count')
# st.write('check',clean_data)
xg_xa_data=clean_data.loc[:,['Player','week','xg_xa']]
xg_xa_data['average']=xg_xa_data.groupby('Player')['xg_xa'].transform(np.mean)
xg_xa_data['count']=xg_xa_data.groupby('Player')['xg_xa'].transform('count')
xg_xa_data=xg_xa_data[xg_xa_data['count']>= min_games_played]
# st.write(xg_xa_data)


# xg_xa_data['std_dev']=xg_xa_data.groupby('Player')['xg_xa'].transform(np.std)

# xg_xa_data=grouped_clean_data.loc[:,['xg_xa_avg']].reset_index()
# st.write(xg_xa_data.head())

with st.beta_expander('xg_xa by week graph'):
    chart_power= alt.Chart(xg_xa_data).mark_rect().encode(alt.X('week:O',axis=alt.Axis(title='week',labelAngle=0)),
    alt.Y('Player',sort=alt.SortField(field='average', order='descending')),color=alt.Color('xg_xa:Q',scale=alt.Scale(scheme='redyellowgreen')))
    # https://altair-viz.github.io/gallery/layered_heatmap_text.html
    # https://vega.github.io/vega/docs/schemes/
    text=chart_power.mark_text().encode(text=alt.Text('xg_xa:N',format=",.1f"),color=alt.value('black'))
    st.altair_chart(chart_power + text,use_container_width=True)

with st.beta_expander('Team Xg'):
    week_14=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_14.pkl')
    week_13=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_13.pkl')
    week_12=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_12.pkl')
    week_11=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_11.pkl')
    week_10=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_10.pkl')
    week_9=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_9.pkl')
    week_8=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_8.pkl')
    week_7=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_7.pkl')
    week_6=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_6.pkl')
    week_5=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_5.pkl')    
    week_4=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_4.pkl')
    week_3=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_3.pkl')
    week_2=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_2.pkl')
    week_1=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_1.pkl')

    combined_team_xg=pd.concat([week_1,week_2,week_3,week_4,week_5,week_6,week_7,week_8,week_9,week_10,week_11,week_12,week_13,week_14])
    # st.write(combined_team_xg)
    combined_team_xg['xg_xa']=combined_team_xg['npxG']+combined_team_xg['xA']
    combined_team_xg['xg_xa_concede']=combined_team_xg['npxG_concede']+combined_team_xg['xA_concede']
    
    combined_team_xg=combined_team_xg.reset_index().rename(columns={'index':'team'}).sort_values(by='week')
    # combined_team_xg['average']=combined_team_xg.groupby('team')['xg_xa'].transform(np.mean)
    combined_team_xg['average']=combined_team_xg.groupby('team')['npxG'].transform(np.mean)    
    # combined_team_xg['average_concede']=combined_team_xg.groupby('team')['xg_xa_concede'].transform(np.mean)
    combined_team_xg['average_concede']=combined_team_xg.groupby('team')['npxG_concede'].transform(np.mean)
    
    # combined_team_xg.to_csv('C:/Users/Darragh/Documents/Python/premier_league/team_xg.csv')


    chart_power= alt.Chart(combined_team_xg).mark_rect().encode(alt.X('week:O',axis=alt.Axis(title='week',labelAngle=0)),
    alt.Y('team',sort=alt.SortField(field='average', order='descending')),color=alt.Color('npxG:Q',scale=alt.Scale(scheme='redyellowgreen')))
    # https://altair-viz.github.io/gallery/layered_heatmap_text.html
    # https://vega.github.io/vega/docs/schemes/
    text=chart_power.mark_text().encode(text=alt.Text('npxG:N',format=",.1f"),color=alt.value('black'))
    st.altair_chart(chart_power + text,use_container_width=True)

    chart_power= alt.Chart(combined_team_xg).mark_rect().encode(alt.X('week:O',axis=alt.Axis(title='week',labelAngle=0)),
    alt.Y('team',sort=alt.SortField(field='average_concede', order='ascending')),color=alt.Color('npxG_concede:Q',scale=alt.Scale(scheme='redyellowgreen')))
    # https://altair-viz.github.io/gallery/layered_heatmap_text.html
    # https://vega.github.io/vega/docs/schemes/
    text=chart_power.mark_text().encode(text=alt.Text('npxG_concede:N',format=",.1f"),color=alt.value('black'))
    st.altair_chart(chart_power + text,use_container_width=True)




























# df=[]
# urls=[
# # 'https://fbref.com/en/matches/3adf2aa7/Brentford-Arsenal-August-13-2021-Premier-League',
# # 'https://fbref.com/en/matches/e62685d4/Manchester-United-Leeds-United-August-14-2021-Premier-League',
# # 'https://fbref.com/en/matches/0b346a62/Leicester-City-Wolverhampton-Wanderers-August-14-2021-Premier-League',
# # 'https://fbref.com/en/matches/4eb36e37/Burnley-Brighton-and-Hove-Albion-August-14-2021-Premier-League',
# # 'https://fbref.com/en/matches/814b563c/Watford-Aston-Villa-August-14-2021-Premier-League',
# # 'https://fbref.com/en/matches/6f454493/Chelsea-Crystal-Palace-August-14-2021-Premier-League',
# # 'https://fbref.com/en/matches/c99ebbf5/Everton-Southampton-August-14-2021-Premier-League',
# 'https://fbref.com/en/matches/c52500ad/Norwich-City-Liverpool-August-14-2021-Premier-League',
# # 'https://fbref.com/en/matches/41091264/Newcastle-United-West-Ham-United-August-15-2021-Premier-League',
# # 'https://fbref.com/en/matches/ff51efc7/Tottenham-Hotspur-Manchester-City-August-15-2021-Premier-League',
# ]

# urls=['https://fbref.com/en/matches/94d9dac0/Liverpool-Burnley-August-21-2021-Premier-League',
# 'https://fbref.com/en/matches/662d4074/Aston-Villa-Newcastle-United-August-21-2021-Premier-League',
# 'https://fbref.com/en/matches/ab6db0d6/Manchester-City-Norwich-City-August-21-2021-Premier-League',
# 'https://fbref.com/en/matches/c8945d11/Crystal-Palace-Brentford-August-21-2021-Premier-League',
# 'https://fbref.com/en/matches/b9064680/Leeds-United-Everton-August-21-2021-Premier-League',
# 'https://fbref.com/en/matches/072af2f8/Brighton-and-Hove-Albion-Watford-August-21-2021-Premier-League',
# 'https://fbref.com/en/matches/345b3989/Southampton-Manchester-United-August-22-2021-Premier-League',
# 'https://fbref.com/en/matches/26ceb3c9/Wolverhampton-Wanderers-Tottenham-Hotspur-August-22-2021-Premier-League',
# 'https://fbref.com/en/matches/93954213/North-West-London-Derby-Arsenal-Chelsea-August-22-2021-Premier-League',
# 'https://fbref.com/en/matches/1d07228e/West-Ham-United-Leicester-City-August-23-2021-Premier-League',
# ]

# urls=[
# 'https://fbref.com/en/matches/d4650aa2/Manchester-City-Arsenal-August-28-2021-Premier-League',
# 'https://fbref.com/en/matches/78c685cc/Norwich-City-Leicester-City-August-28-2021-Premier-League',
# 'https://fbref.com/en/matches/8e017435/West-Ham-United-Crystal-Palace-August-28-2021-Premier-League',
# 'https://fbref.com/en/matches/d81af076/Newcastle-United-Southampton-August-28-2021-Premier-League',
# 'https://fbref.com/en/matches/a08ef96c/Aston-Villa-Brentford-August-28-2021-Premier-League',
# 'https://fbref.com/en/matches/ec8b667a/Brighton-and-Hove-Albion-Everton-August-28-2021-Premier-League',
# 'https://fbref.com/en/matches/78aa75e6/Liverpool-Chelsea-August-28-2021-Premier-League',
# 'https://fbref.com/en/matches/3cd9a733/Tottenham-Hotspur-Watford-August-29-2021-Premier-League',
# 'https://fbref.com/en/matches/2e5db698/Burnley-Leeds-United-August-29-2021-Premier-League',
# 'https://fbref.com/en/matches/871109e6/Wolverhampton-Wanderers-Manchester-United-August-29-2021-Premier-League',
# ]

# urls=[
#     'https://fbref.com/en/matches/17e86f90/Crystal-Palace-Tottenham-Hotspur-September-11-2021-Premier-League',
#     'https://fbref.com/en/matches/ddff1858/Southampton-West-Ham-United-September-11-2021-Premier-League',
#     'https://fbref.com/en/matches/4ac58f71/Arsenal-Norwich-City-September-11-2021-Premier-League',
#     'https://fbref.com/en/matches/19a03697/Brentford-Brighton-and-Hove-Albion-September-11-2021-Premier-League',
#     'https://fbref.com/en/matches/09db0909/Watford-Wolverhampton-Wanderers-September-11-2021-Premier-League',
#     'https://fbref.com/en/matches/8dd69c8d/Leicester-City-Manchester-City-September-11-2021-Premier-League',
#     'https://fbref.com/en/matches/7794fd6c/Manchester-United-Newcastle-United-September-11-2021-Premier-League',
#     'https://fbref.com/en/matches/67bbc3a5/Chelsea-Aston-Villa-September-11-2021-Premier-League',
#     'https://fbref.com/en/matches/e6a245be/Leeds-United-Liverpool-September-12-2021-Premier-League',
#     'https://fbref.com/en/matches/668b2f97/Everton-Burnley-September-13-2021-Premier-League',
#     ]

    # urls=[
    # 'https://fbref.com/en/matches/aad7d38a/Newcastle-United-Leeds-United-September-17-2021-Premier-League',
    # 'https://fbref.com/en/matches/fd1d60f4/Wolverhampton-Wanderers-Brentford-September-18-2021-Premier-League',
    # 'https://fbref.com/en/matches/59ef8c18/Liverpool-Crystal-Palace-September-18-2021-Premier-League',
    # 'https://fbref.com/en/matches/1576c578/Manchester-City-Southampton-September-18-2021-Premier-League',
    # 'https://fbref.com/en/matches/835fa19c/Norwich-City-Watford-September-18-2021-Premier-League',
    # 'https://fbref.com/en/matches/a427debc/Burnley-Arsenal-September-18-2021-Premier-League',
    # 'https://fbref.com/en/matches/57323feb/Aston-Villa-Everton-September-18-2021-Premier-League',
    # 'https://fbref.com/en/matches/2daea068/West-Ham-United-Manchester-United-September-19-2021-Premier-League',
    # 'https://fbref.com/en/matches/723f5105/Brighton-and-Hove-Albion-Leicester-City-September-19-2021-Premier-League',
    # 'https://fbref.com/en/matches/eaf98461/Tottenham-Hotspur-Chelsea-September-19-2021-Premier-League',
    # ]

# urls=[
#     'https://fbref.com/en/matches/fc59faf7/Chelsea-Manchester-City-September-25-2021-Premier-League',
#     'https://fbref.com/en/matches/7c21232e/Manchester-United-Aston-Villa-September-25-2021-Premier-League',
#     'https://fbref.com/en/matches/6e228b2c/Leeds-United-West-Ham-United-September-25-2021-Premier-League',
#     'https://fbref.com/en/matches/2d61f328/Leicester-City-Burnley-September-25-2021-Premier-League',
#     'https://fbref.com/en/matches/70fda3e9/Watford-Newcastle-United-September-25-2021-Premier-League',
#     'https://fbref.com/en/matches/d516ccbf/Everton-Norwich-City-September-25-2021-Premier-League',
#     'https://fbref.com/en/matches/87140543/Brentford-Liverpool-September-25-2021-Premier-League',
#     'https://fbref.com/en/matches/d99f984c/Southampton-Wolverhampton-Wanderers-September-26-2021-Premier-League',
#     'https://fbref.com/en/matches/a2c07e97/North-London-Derby-Arsenal-Tottenham-Hotspur-September-26-2021-Premier-League',
#     'https://fbref.com/en/matches/3d7659fc/Crystal-Palace-Brighton-and-Hove-Albion-September-27-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/2129c7e9/Manchester-United-Everton-October-2-2021-Premier-League',
#     'https://fbref.com/en/matches/9231df9a/Burnley-Norwich-City-October-2-2021-Premier-League',
#     'https://fbref.com/en/matches/be9d8a45/Leeds-United-Watford-October-2-2021-Premier-League',
#     'https://fbref.com/en/matches/a6466617/Chelsea-Southampton-October-2-2021-Premier-League',
#     'https://fbref.com/en/matches/00dcbdaa/Wolverhampton-Wanderers-Newcastle-United-October-2-2021-Premier-League',
#     'https://fbref.com/en/matches/cdaded7b/Brighton-and-Hove-Albion-Arsenal-October-2-2021-Premier-League',
#     'https://fbref.com/en/matches/f1eead63/West-Ham-United-Brentford-October-3-2021-Premier-League',
#     'https://fbref.com/en/matches/b06fd537/Crystal-Palace-Leicester-City-October-3-2021-Premier-League',
#     'https://fbref.com/en/matches/7bb0a43c/Tottenham-Hotspur-Aston-Villa-October-3-2021-Premier-League',
#     'https://fbref.com/en/matches/2598b046/Liverpool-Manchester-City-October-3-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/2ce6d340/Watford-Liverpool-October-16-2021-Premier-League',
#     'https://fbref.com/en/matches/bc0a1eb5/Norwich-City-Brighton-and-Hove-Albion-October-16-2021-Premier-League',
#     'https://fbref.com/en/matches/45502ded/Leicester-City-Manchester-United-October-16-2021-Premier-League',
#     'https://fbref.com/en/matches/8bde822c/Southampton-Leeds-United-October-16-2021-Premier-League',
#     'https://fbref.com/en/matches/55778d0d/Manchester-City-Burnley-October-16-2021-Premier-League',
#     'https://fbref.com/en/matches/a1668499/Aston-Villa-Wolverhampton-Wanderers-October-16-2021-Premier-League',
#     'https://fbref.com/en/matches/866cfb1f/Brentford-Chelsea-October-16-2021-Premier-League',
#     'https://fbref.com/en/matches/15871600/Everton-West-Ham-United-October-17-2021-Premier-League',
#     'https://fbref.com/en/matches/4bd69343/Newcastle-United-Tottenham-Hotspur-October-17-2021-Premier-League',
#     'https://fbref.com/en/matches/0f3a1892/Arsenal-Crystal-Palace-October-18-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/ac95a75a/Arsenal-Aston-Villa-October-22-2021-Premier-League',
#     'https://fbref.com/en/matches/a6ff9cf9/Chelsea-Norwich-City-October-23-2021-Premier-League',
#     'https://fbref.com/en/matches/49b3afe3/Leeds-United-Wolverhampton-Wanderers-October-23-2021-Premier-League',
#     'https://fbref.com/en/matches/d5164fbe/Southampton-Burnley-October-23-2021-Premier-League',
#     'https://fbref.com/en/matches/6985d123/Everton-Watford-October-23-2021-Premier-League',
#     'https://fbref.com/en/matches/4d1b6f6f/Crystal-Palace-Newcastle-United-October-23-2021-Premier-League',
#     'https://fbref.com/en/matches/dc93611c/Brighton-and-Hove-Albion-Manchester-City-October-23-2021-Premier-League',
#     'https://fbref.com/en/matches/70c508ee/West-Ham-United-Tottenham-Hotspur-October-24-2021-Premier-League',
#     'https://fbref.com/en/matches/b5c25937/Brentford-Leicester-City-October-24-2021-Premier-League',
#     'https://fbref.com/en/matches/b886bec4/North-West-Derby-Manchester-United-Liverpool-October-24-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/719b57c6/Leicester-City-Arsenal-October-30-2021-Premier-League',
#     'https://fbref.com/en/matches/eb6c294f/Manchester-City-Crystal-Palace-October-30-2021-Premier-League',
#     'https://fbref.com/en/matches/c8915e9e/Burnley-Brentford-October-30-2021-Premier-League',
#     'https://fbref.com/en/matches/49478cd2/Newcastle-United-Chelsea-October-30-2021-Premier-League',
#     'https://fbref.com/en/matches/e3521093/Watford-Southampton-October-30-2021-Premier-League',
#     'https://fbref.com/en/matches/c68998b5/Liverpool-Brighton-and-Hove-Albion-October-30-2021-Premier-League',
#     'https://fbref.com/en/matches/5a2b8c26/Tottenham-Hotspur-Manchester-United-October-30-2021-Premier-League',
#     'https://fbref.com/en/matches/52daf8d4/Norwich-City-Leeds-United-October-31-2021-Premier-League',
#     'https://fbref.com/en/matches/a62478a2/Aston-Villa-West-Ham-United-October-31-2021-Premier-League',
#     'https://fbref.com/en/matches/c9ad66cc/Wolverhampton-Wanderers-Everton-November-1-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/868bd31f/Southampton-Aston-Villa-November-5-2021-Premier-League',
#     'https://fbref.com/en/matches/5fa5be28/Manchester-Derby-Manchester-United-Manchester-City-November-6-2021-Premier-League',
#     'https://fbref.com/en/matches/0f029791/Brentford-Norwich-City-November-6-2021-Premier-League',
#     'https://fbref.com/en/matches/3a2fff4d/Crystal-Palace-Wolverhampton-Wanderers-November-6-2021-Premier-League',
#     'https://fbref.com/en/matches/316c0296/Chelsea-Burnley-November-6-2021-Premier-League',
#     'https://fbref.com/en/matches/10d11999/Brighton-and-Hove-Albion-Newcastle-United-November-6-2021-Premier-League',
#     'https://fbref.com/en/matches/8fd004c6/Leeds-United-Leicester-City-November-7-2021-Premier-League',
#     'https://fbref.com/en/matches/e0208fcf/Arsenal-Watford-November-7-2021-Premier-League',
#     'https://fbref.com/en/matches/224d1c99/Everton-Tottenham-Hotspur-November-7-2021-Premier-League',
#     'https://fbref.com/en/matches/63538dc7/West-Ham-United-Liverpool-November-7-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/2fd486d6/Leicester-City-Chelsea-November-20-2021-Premier-League',
#     'https://fbref.com/en/matches/e7ab34c4/Burnley-Crystal-Palace-November-20-2021-Premier-League',
#     'https://fbref.com/en/matches/88f081ac/Aston-Villa-Brighton-and-Hove-Albion-November-20-2021-Premier-League',
#     'https://fbref.com/en/matches/4bddaba4/Norwich-City-Southampton-November-20-2021-Premier-League',
#     'https://fbref.com/en/matches/013c4797/Wolverhampton-Wanderers-West-Ham-United-November-20-2021-Premier-League',
#     'https://fbref.com/en/matches/adbf56bc/Newcastle-United-Brentford-November-20-2021-Premier-League',
#     'https://fbref.com/en/matches/31a03035/Watford-Manchester-United-November-20-2021-Premier-League',
#     'https://fbref.com/en/matches/e9ea66e1/Liverpool-Arsenal-November-20-2021-Premier-League',
#     'https://fbref.com/en/matches/bfbe7402/Manchester-City-Everton-November-21-2021-Premier-League',
#     'https://fbref.com/en/matches/a74a684e/Tottenham-Hotspur-Leeds-United-November-21-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/067e0ab9/Arsenal-Newcastle-United-November-27-2021-Premier-League',
#     'https://fbref.com/en/matches/4a7a9e3b/Crystal-Palace-Aston-Villa-November-27-2021-Premier-League',
#     'https://fbref.com/en/matches/ff3bd755/Norwich-City-Wolverhampton-Wanderers-November-27-2021-Premier-League',
#     'https://fbref.com/en/matches/aa9b882d/Liverpool-Southampton-November-27-2021-Premier-League',
#     'https://fbref.com/en/matches/5d651cd7/Brighton-and-Hove-Albion-Leeds-United-November-27-2021-Premier-League',
#     'https://fbref.com/en/matches/286c4c1c/Brentford-Everton-November-28-2021-Premier-League',
#     'https://fbref.com/en/matches/c2e426c8/Leicester-City-Watford-November-28-2021-Premier-League',
#     'https://fbref.com/en/matches/c37446de/Manchester-City-West-Ham-United-November-28-2021-Premier-League',
#     'https://fbref.com/en/matches/08b3c5d8/Chelsea-Manchester-United-November-28-2021-Premier-League',
#     ]


# week=1
# for x in urls:
#     dfa=pd.read_html(x)
#     home_stats=dfa[3]
#     away_stats=dfa[5]
#     st.write('away 1',dfa[4])
#     st.write('away 2',dfa[5])
#     st.write('away 3',dfa[6]) 
#     df.append(home_stats)
#     df.append(away_stats)
# dx=pd.concat(df)
# st.write(dx)

# dfa=pd.read_html('https://fbref.com/en/matches/c52500ad/Norwich-City-Liverpool-August-14-2021-Premier-League')
# st.write(dfa[10])
# st.write(dfa[11])
# st.write(dfa[12])










# data=pd.from

# https://stackoverflow.com/questions/42462530/how-to-replace-the-white-space-in-a-string-in-a-pandas-dataframe
# st.write ('below shows the highest xg_xa in the one game in the season')
# st.table (combined.sort_values(by='xg_xa', ascending=False))






# st.write (week_21['Min'].sum())
# st.write ('number of estimated minutes', 11*90*20)

# filt = combined['Week'].isin(['20','23','22','21'])
# last_4 = combined[filt]
# # st.table ( last_4.head() )
# # st.write ('dataframe sum mins this is a check', last_4['Min'].sum(), 'my estimate', 11*90*20*4 )
# xg_last4 = last_4.groupby('Player').agg(xg_xa_avg = ('xg_xa', 'mean'), xg_xa_sum = ('xg_xa', 'sum'), xg_xa_count=('xg_xa', 'count') ) 
# st.write ('below is the average over the past 4 gameweeks')
# st.table ( xg_last4.sort_values(by='xg_xa_avg', ascending=False).head(4) )

# df=combined.copy().sort_values(by='Week', ascending=True)
# df['moving_avg'] = df.groupby('Player')['xg_xa'].transform(lambda x: x.rolling(4, 4).mean())
# df['moving_sum'] = df.groupby('Player')['xg_xa'].transform(lambda x: x.rolling(4, 4).sum())
# df['moving_count'] = df.groupby('Player')['xg_xa'].transform(lambda x: x.rolling(4, 4).count())
# df['cum_sum'] = df.groupby('Player')['xg_xa'].transform(lambda x: x.cumsum())
# # Column for total goals and assists, then see the under or overperformance, but then regression to the mean
# st.table ( df[df['Player']=='harry_maguire'] )
# # st.write ('below shows the highest xg_xa cumulative for season')

# # cols_to_move = ['Name','Position','Count','AvgPointsPerGame','Salary']
# # cols = cols_to_move + [col for col in test2 if col not in cols_to_move]
# # test2=test2[cols]
# # st.table ( df.sort_values(by='cum_sum', ascending=False).head(10) )
# df=df.sort_values(by='cum_sum', ascending=False)
# df = df.drop_duplicates(subset=['Player'], keep = 'first')
