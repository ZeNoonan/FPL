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
current_week=29

def scraper_pl():
    df=[]
    urls=[
    'https://fbref.com/en/matches/4d3331bb/Brighton-and-Hove-Albion-Liverpool-March-12-2022-Premier-League',
    'https://fbref.com/en/matches/9718a901/Brentford-Burnley-March-12-2022-Premier-League',
    'https://fbref.com/en/matches/e5e7becb/Manchester-United-Tottenham-Hotspur-March-12-2022-Premier-League',
    'https://fbref.com/en/matches/0dcf103b/Chelsea-Newcastle-United-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/2c627dd8/Southampton-Watford-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/81f2f022/West-Ham-United-Aston-Villa-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/9e5d1f93/Everton-Wolverhampton-Wanderers-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/b13fb9b9/Leeds-United-Norwich-City-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/47ea9ab2/Arsenal-Leicester-City-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/f5b6f5c5/Crystal-Palace-Manchester-City-March-14-2022-Premier-League',
    'https://fbref.com/en/matches/59b3ee40/Brighton-and-Hove-Albion-Tottenham-Hotspur-March-16-2022-Premier-League',
    'https://fbref.com/en/matches/8ef5cc6b/Arsenal-Liverpool-March-16-2022-Premier-League',
    'https://fbref.com/en/matches/029e5f94/Everton-Newcastle-United-March-17-2022-Premier-League',
    ]

    week=current_week
    for x in urls:
        dfa=pd.read_html(x)
        home_stats=dfa[3]
        away_stats=dfa[10] 
        df.append(home_stats)
        df.append(away_stats)
    dx=pd.concat(df)
    dx[('week','week')]=week
    dx.to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_%d.pkl' % week)
    return dx
# scraper_pl()

def team_scraper_pl():
    df=[]
    urls=[
    'https://fbref.com/en/matches/4d3331bb/Brighton-and-Hove-Albion-Liverpool-March-12-2022-Premier-League',
    'https://fbref.com/en/matches/9718a901/Brentford-Burnley-March-12-2022-Premier-League',
    'https://fbref.com/en/matches/e5e7becb/Manchester-United-Tottenham-Hotspur-March-12-2022-Premier-League',
    'https://fbref.com/en/matches/0dcf103b/Chelsea-Newcastle-United-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/2c627dd8/Southampton-Watford-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/81f2f022/West-Ham-United-Aston-Villa-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/9e5d1f93/Everton-Wolverhampton-Wanderers-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/b13fb9b9/Leeds-United-Norwich-City-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/47ea9ab2/Arsenal-Leicester-City-March-13-2022-Premier-League',
    'https://fbref.com/en/matches/f5b6f5c5/Crystal-Palace-Manchester-City-March-14-2022-Premier-League',
    'https://fbref.com/en/matches/59b3ee40/Brighton-and-Hove-Albion-Tottenham-Hotspur-March-16-2022-Premier-League',
    'https://fbref.com/en/matches/8ef5cc6b/Arsenal-Liverpool-March-16-2022-Premier-League',
    'https://fbref.com/en/matches/029e5f94/Everton-Newcastle-United-March-17-2022-Premier-League',
    ]

    week=current_week
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
    dx.to_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_%d.pkl' % week)
    return dx

# team_scraper_pl()


# week_30=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_30.pkl')
# week_29=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_29.pkl')
week_28=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_28_test_test_test.pkl')
week_27=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_27_test_test_test.pkl')
week_26=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_26_test_test_test.pkl')
week_25=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_25_test_test_test.pkl')
week_24=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_24_test_test_test.pkl')
week_23=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_23_test_test_test.pkl')
week_22=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_22_test_test_test.pkl')
week_21=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_21_test_test_test.pkl')
week_20=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_20_test_test_test.pkl')
week_19=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_19_test_test_test.pkl')
week_18=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_18_test_test_test.pkl')
week_17=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_17_test_test_test.pkl')
week_16=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_16_test_test_test.pkl')
week_15=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_15_test_test_test.pkl')
week_14=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/week_14_test_test_test.pkl')
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

combined=pd.concat([week_1,week_2,week_3,week_4,week_5,week_6,week_7,week_8,week_9,week_10,week_11,week_12,week_13,week_14,
week_15,week_16,week_17,week_18,week_19,week_20,week_21,week_22,week_23,week_24,week_25,week_26,week_27,week_28])
# week_15,week_16,week_17,week_18,week_19,week_20,week_21,week_22,week_23,week_24,week_25,week_26,week_27,week_28,week_29])
combined[("Unnamed: 0_level_0","Player")]=combined[("Unnamed: 0_level_0","Player")].str.lower()
combined[("Unnamed: 0_level_0","Player")]=combined[("Unnamed: 0_level_0","Player")].replace(" ", "_", regex=True)
combined[("Expected","xg_xa")]=combined[("Expected","npxG")]+combined[("Expected","xA")]

data = combined.loc[:,[("week","week"),("Unnamed: 0_level_0","Player"),("Expected","npxG"),("Expected","xA"),("Expected","xG"),("Performance","Sh"),("Performance","SoT"),
("Unnamed: 3_level_0","Pos"),("Unnamed: 5_level_0","Min"),("Performance","Tkl"),("Performance","Int"),("Performance","Press"),
("Passes","Prog"),("Carries","Prog"),("Expected","xg_xa")]]

# st.write(data)
data=data.dropna()
data=data[data[("Unnamed: 0_level_0","Player")].str.contains("14_players")==False]
# st.write('salah data')
# st.write(data[data[("Unnamed: 0_level_0","Player")].str.contains('salah')])
with st.expander('Full Data'):
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

# https://stackoverflow.com/questions/64145551/simplest-way-to-heatmap-selected-columns-in-python
# https://seaborn.pydata.org/tutorial/color_palettes.html
cm = sns.color_palette("Spectral", as_cmap=True)

min_games_played = st.number_input ("Minimum number of games ever", min_value=int(0),value=int(8))
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


xg_xa_data=clean_data.loc[:,['Player','week','xg_xa']]
xg_xa_data['average']=xg_xa_data.groupby('Player')['xg_xa'].transform(np.mean)
xg_xa_data['count']=xg_xa_data.groupby('Player')['xg_xa'].transform('count')
xg_xa_data=xg_xa_data[xg_xa_data['count']>= min_games_played]
graph_data=xg_xa_data.groupby(['week','Player']).agg(xg_xa=('xg_xa','mean')).reset_index()
graph_data['average']=graph_data.groupby('Player')['xg_xa'].transform(np.mean)

with st.expander('xg_xa by week graph'):
    chart_power= alt.Chart(graph_data).mark_rect().encode(alt.X('week:O',axis=alt.Axis(title='week',labelAngle=0)),
    alt.Y('Player',sort=alt.SortField(field='average', order='descending')),color=alt.Color('xg_xa:Q',scale=alt.Scale(scheme='redyellowgreen')))
    # https://altair-viz.github.io/gallery/layered_heatmap_text.html
    # https://vega.github.io/vega/docs/schemes/
    text=chart_power.mark_text().encode(text=alt.Text('xg_xa:N',format=",.1f"),color=alt.value('black'))
    st.altair_chart(chart_power + text,use_container_width=True)

with st.expander('Team Xg'):
    # week_29=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_29.pkl')
    week_28=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_28.pkl')
    week_27=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_27.pkl')
    week_26=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_26.pkl')
    week_25=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_25.pkl')
    week_24=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_24.pkl')
    week_23=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_23.pkl')
    week_22=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_22.pkl')
    week_21=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_21.pkl')
    week_20=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_20.pkl')
    week_19=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_19.pkl')
    week_18=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_18.pkl')
    week_17=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_17.pkl')
    week_16=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_16.pkl')
    week_15=pd.read_pickle('C:/Users/Darragh/Documents/Python/Fantasy_Football/1. Data/xG_Data/team_xg_week_15.pkl')
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

    combined_team_xg=pd.concat([week_1,week_2,week_3,week_4,week_5,week_6,week_7,week_8,week_9,week_10,week_11,week_12,
    week_13,week_14,week_15,week_16,week_17,week_18,week_19,week_20,week_21,week_22,week_23,week_24,week_25,week_26,week_27,week_28])
    # week_13,week_14,week_15,week_16,week_17,week_18,week_19,week_20,week_21,week_22,week_23,week_24,week_25,week_26,week_27,week_28,week_29])
    # st.write(combined_team_xg)
    combined_team_xg['xg_xa']=combined_team_xg['npxG']+combined_team_xg['xA']
    combined_team_xg['xg_xa_concede']=combined_team_xg['npxG_concede']+combined_team_xg['xA_concede']
    
    combined_team_xg=combined_team_xg.reset_index().rename(columns={'index':'team'}).sort_values(by='week')
    # st.write('data', combined_team_xg)
    combined_team_xg=combined_team_xg.groupby(['week','team']).agg(npxG=('npxG','mean'),npxG_concede=('npxG_concede','mean')).reset_index()
    # st.write('data combine', test)
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

# urls=[
#     'https://fbref.com/en/matches/ce4d873f/Newcastle-United-Norwich-City-November-30-2021-Premier-League',
#     'https://fbref.com/en/matches/b0ab4044/Leeds-United-Crystal-Palace-November-30-2021-Premier-League',
#     'https://fbref.com/en/matches/2049300f/West-Ham-United-Brighton-and-Hove-Albion-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/a3fc2ddc/Wolverhampton-Wanderers-Burnley-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/f475576b/Watford-Chelsea-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/135f5959/Southampton-Leicester-City-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/1993b7ec/Aston-Villa-Manchester-City-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/b46554fb/Merseyside-Derby-Everton-Liverpool-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/4323a38f/Manchester-United-Arsenal-December-2-2021-Premier-League',
#     'https://fbref.com/en/matches/a80b3790/Tottenham-Hotspur-Brentford-December-2-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/ce4d873f/Newcastle-United-Norwich-City-November-30-2021-Premier-League',
#     'https://fbref.com/en/matches/b0ab4044/Leeds-United-Crystal-Palace-November-30-2021-Premier-League',
#     'https://fbref.com/en/matches/2049300f/West-Ham-United-Brighton-and-Hove-Albion-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/a3fc2ddc/Wolverhampton-Wanderers-Burnley-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/f475576b/Watford-Chelsea-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/135f5959/Southampton-Leicester-City-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/1993b7ec/Aston-Villa-Manchester-City-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/b46554fb/Merseyside-Derby-Everton-Liverpool-December-1-2021-Premier-League',
#     'https://fbref.com/en/matches/4323a38f/Manchester-United-Arsenal-December-2-2021-Premier-League',
#     'https://fbref.com/en/matches/a80b3790/Tottenham-Hotspur-Brentford-December-2-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/49a36a4e/Brentford-Watford-December-10-2021-Premier-League',
#     'https://fbref.com/en/matches/d46b4a18/Manchester-City-Wolverhampton-Wanderers-December-11-2021-Premier-League',
#     'https://fbref.com/en/matches/6ad3036b/Chelsea-Leeds-United-December-11-2021-Premier-League',
#     'https://fbref.com/en/matches/678d7dca/Liverpool-Aston-Villa-December-11-2021-Premier-League',
#     'https://fbref.com/en/matches/6a35f07c/Arsenal-Southampton-December-11-2021-Premier-League',
#     'https://fbref.com/en/matches/11a67612/Norwich-City-Manchester-United-December-11-2021-Premier-League',
#     'https://fbref.com/en/matches/6d236ce6/Burnley-West-Ham-United-December-12-2021-Premier-League',
#     'https://fbref.com/en/matches/8805978d/Leicester-City-Newcastle-United-December-12-2021-Premier-League',
#     'https://fbref.com/en/matches/02abf29a/Crystal-Palace-Everton-December-12-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/c78a1d7d/Norwich-City-Aston-Villa-December-14-2021-Premier-League',
#     'https://fbref.com/en/matches/5730a84c/Manchester-City-Leeds-United-December-14-2021-Premier-League',
#     'https://fbref.com/en/matches/60178542/Brighton-and-Hove-Albion-Wolverhampton-Wanderers-December-15-2021-Premier-League',
#     'https://fbref.com/en/matches/9ebb60f0/Crystal-Palace-Southampton-December-15-2021-Premier-League',
#     'https://fbref.com/en/matches/3f1ff3a5/Arsenal-West-Ham-United-December-15-2021-Premier-League',
#     'https://fbref.com/en/matches/70209eb1/Chelsea-Everton-December-16-2021-Premier-League',
#     'https://fbref.com/en/matches/5aec4772/Liverpool-Newcastle-United-December-16-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/53b542d8/Leeds-United-Arsenal-December-18-2021-Premier-League',
#     'https://fbref.com/en/matches/73d478fb/Wolverhampton-Wanderers-Chelsea-December-19-2021-Premier-League',
#     'https://fbref.com/en/matches/4d9bcee9/Newcastle-United-Manchester-City-December-19-2021-Premier-League',
#     'https://fbref.com/en/matches/4ac8dee4/Tottenham-Hotspur-Liverpool-December-19-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/49e84e17/Manchester-City-Leicester-City-December-26-2021-Premier-League',
#     'https://fbref.com/en/matches/83ce723b/Norwich-City-Arsenal-December-26-2021-Premier-League',
#     'https://fbref.com/en/matches/36a056cf/West-Ham-United-Southampton-December-26-2021-Premier-League',
#     'https://fbref.com/en/matches/ac4560d6/Tottenham-Hotspur-Crystal-Palace-December-26-2021-Premier-League',
#     'https://fbref.com/en/matches/61396bd8/Aston-Villa-Chelsea-December-26-2021-Premier-League',
#     'https://fbref.com/en/matches/1f64133b/Brighton-and-Hove-Albion-Brentford-December-26-2021-Premier-League',
#     'https://fbref.com/en/matches/f91fee43/Newcastle-United-Manchester-United-December-27-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/bbfa96c9/Manchester-United-Burnley-December-30-2021-Premier-League',
#     'https://fbref.com/en/matches/1a0df937/Brentford-Manchester-City-December-29-2021-Premier-League',
#     'https://fbref.com/en/matches/8fbe2e12/Chelsea-Brighton-and-Hove-Albion-December-29-2021-Premier-League',
#     'https://fbref.com/en/matches/8ad7b26f/Leicester-City-Liverpool-December-28-2021-Premier-League',
#     'https://fbref.com/en/matches/59ef01ea/Crystal-Palace-Norwich-City-December-28-2021-Premier-League',
#     'https://fbref.com/en/matches/b56fd899/Watford-West-Ham-United-December-28-2021-Premier-League',
#     'https://fbref.com/en/matches/08d5ef01/Southampton-Tottenham-Hotspur-December-28-2021-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/a9903a63/Arsenal-Manchester-City-January-1-2022-Premier-League',
#     'https://fbref.com/en/matches/9c831c07/Watford-Tottenham-Hotspur-January-1-2022-Premier-League',
#     'https://fbref.com/en/matches/b0b5cba6/Crystal-Palace-West-Ham-United-January-1-2022-Premier-League',
#     'https://fbref.com/en/matches/dfaa1817/Brentford-Aston-Villa-January-2-2022-Premier-League',
#     'https://fbref.com/en/matches/cff8022b/Leeds-United-Burnley-January-2-2022-Premier-League',
#     'https://fbref.com/en/matches/e22bb565/Everton-Brighton-and-Hove-Albion-January-2-2022-Premier-League',
#     'https://fbref.com/en/matches/3480cc09/Chelsea-Liverpool-January-2-2022-Premier-League',
#     'https://fbref.com/en/matches/8e966b52/Manchester-United-Wolverhampton-Wanderers-January-3-2022-Premier-League',
#     'https://fbref.com/en/matches/0859817d/Southampton-Brentford-January-11-2022-Premier-League',
#     'https://fbref.com/en/matches/7d53d1ea/West-Ham-United-Norwich-City-January-12-2022-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/96630936/Brighton-and-Hove-Albion-Crystal-Palace-January-14-2022-Premier-League',
#     'https://fbref.com/en/matches/febd7f38/Manchester-City-Chelsea-January-15-2022-Premier-League',
#     'https://fbref.com/en/matches/64dd3e3f/Newcastle-United-Watford-January-15-2022-Premier-League',
#     'https://fbref.com/en/matches/dd7b8b8b/Wolverhampton-Wanderers-Southampton-January-15-2022-Premier-League',
#     'https://fbref.com/en/matches/4574a1a6/Norwich-City-Everton-January-15-2022-Premier-League',
#     'https://fbref.com/en/matches/745dc664/Aston-Villa-Manchester-United-January-15-2022-Premier-League',
#     'https://fbref.com/en/matches/62c16969/West-Ham-United-Leeds-United-January-16-2022-Premier-League',
#     'https://fbref.com/en/matches/c8c457d6/Liverpool-Brentford-January-16-2022-Premier-League',
#     'https://fbref.com/en/matches/b4c9c369/Brighton-and-Hove-Albion-Chelsea-January-18-2022-Premier-League',
#     'https://fbref.com/en/matches/77d28549/Leicester-City-Tottenham-Hotspur-January-19-2022-Premier-League',
#     'https://fbref.com/en/matches/f7c0bd68/Brentford-Manchester-United-January-19-2022-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/5c592680/Watford-Norwich-City-January-21-2022-Premier-League',
#     'https://fbref.com/en/matches/83bac3da/Everton-Aston-Villa-January-22-2022-Premier-League',
#     'https://fbref.com/en/matches/9f91ec9b/Brentford-Wolverhampton-Wanderers-January-22-2022-Premier-League',
#     'https://fbref.com/en/matches/07df6328/Leeds-United-Newcastle-United-January-22-2022-Premier-League',
#     'https://fbref.com/en/matches/7c23f694/Manchester-United-West-Ham-United-January-22-2022-Premier-League',
#     'https://fbref.com/en/matches/9bfa5945/Southampton-Manchester-City-January-22-2022-Premier-League',
#     'https://fbref.com/en/matches/60ad7e25/Crystal-Palace-Liverpool-January-23-2022-Premier-League',
#     'https://fbref.com/en/matches/845ec84d/Arsenal-Burnley-January-23-2022-Premier-League',
#     'https://fbref.com/en/matches/a28f6f69/Leicester-City-Brighton-and-Hove-Albion-January-23-2022-Premier-League',
#     'https://fbref.com/en/matches/29e164e3/Chelsea-Tottenham-Hotspur-January-23-2022-Premier-League',
#     'https://fbref.com/en/matches/5c31d723/Burnley-Watford-February-5-2022-Premier-League',
#     ]

    # urls=[
    # 'https://fbref.com/en/matches/3778ac3f/West-Ham-United-Watford-February-8-2022-Premier-League',
    # 'https://fbref.com/en/matches/fde8d97d/Newcastle-United-Everton-February-8-2022-Premier-League',
    # 'https://fbref.com/en/matches/cb262ab8/Burnley-Manchester-United-February-8-2022-Premier-League',
    # 'https://fbref.com/en/matches/0613df22/Tottenham-Hotspur-Southampton-February-9-2022-Premier-League',
    # 'https://fbref.com/en/matches/3b077554/Manchester-City-Brentford-February-9-2022-Premier-League',
    # 'https://fbref.com/en/matches/22d9fbc9/Norwich-City-Crystal-Palace-February-9-2022-Premier-League',
    # 'https://fbref.com/en/matches/f1e84229/Aston-Villa-Leeds-United-February-9-2022-Premier-League',
    # 'https://fbref.com/en/matches/911fa284/Liverpool-Leicester-City-February-10-2022-Premier-League',
    # 'https://fbref.com/en/matches/bf5f0f9e/Wolverhampton-Wanderers-Arsenal-February-10-2022-Premier-League',
    # ]

# urls=[
#     'https://fbref.com/en/matches/d15dca2c/Manchester-United-Southampton-February-12-2022-Premier-League',
#     'https://fbref.com/en/matches/0a51943e/Everton-Leeds-United-February-12-2022-Premier-League',
#     'https://fbref.com/en/matches/427597d4/Brentford-Crystal-Palace-February-12-2022-Premier-League',
#     'https://fbref.com/en/matches/e04d98c4/Watford-Brighton-and-Hove-Albion-February-12-2022-Premier-League',
#     'https://fbref.com/en/matches/522300d0/Norwich-City-Manchester-City-February-12-2022-Premier-League',
#     'https://fbref.com/en/matches/59b88877/Newcastle-United-Aston-Villa-February-13-2022-Premier-League',
#     'https://fbref.com/en/matches/ee0b72dd/Burnley-Liverpool-February-13-2022-Premier-League',
#     'https://fbref.com/en/matches/fe93b491/Tottenham-Hotspur-Wolverhampton-Wanderers-February-13-2022-Premier-League',
#     'https://fbref.com/en/matches/c2c20295/Leicester-City-West-Ham-United-February-13-2022-Premier-League',
#     'https://fbref.com/en/matches/a1fb5fa2/Manchester-United-Brighton-and-Hove-Albion-February-15-2022-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/4e263347/West-Ham-United-Newcastle-United-February-19-2022-Premier-League',
#     'https://fbref.com/en/matches/28c4ee0a/Aston-Villa-Watford-February-19-2022-Premier-League',
#     'https://fbref.com/en/matches/401c8cc8/Arsenal-Brentford-February-19-2022-Premier-League',
#     'https://fbref.com/en/matches/53cc3dbd/Southampton-Everton-February-19-2022-Premier-League',
#     'https://fbref.com/en/matches/700c9eaf/Liverpool-Norwich-City-February-19-2022-Premier-League',
#     'https://fbref.com/en/matches/b1df8cfd/Brighton-and-Hove-Albion-Burnley-February-19-2022-Premier-League',
#     'https://fbref.com/en/matches/ddd2eed6/Crystal-Palace-Chelsea-February-19-2022-Premier-League',
#     'https://fbref.com/en/matches/cd797899/Manchester-City-Tottenham-Hotspur-February-19-2022-Premier-League',
#     'https://fbref.com/en/matches/002f0ff0/Leeds-United-Manchester-United-February-20-2022-Premier-League',
#     'https://fbref.com/en/matches/63d95af6/Wolverhampton-Wanderers-Leicester-City-February-20-2022-Premier-League',
#     'https://fbref.com/en/matches/f8d646cb/Burnley-Tottenham-Hotspur-February-23-2022-Premier-League',
#     'https://fbref.com/en/matches/daa35440/Watford-Crystal-Palace-February-23-2022-Premier-League',
#     'https://fbref.com/en/matches/6d0f3b48/Liverpool-Leeds-United-February-23-2022-Premier-League',
#     'https://fbref.com/en/matches/3c516ed6/Arsenal-Wolverhampton-Wanderers-February-24-2022-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/17c79d36/Southampton-Norwich-City-February-25-2022-Premier-League',
#     'https://fbref.com/en/matches/05d37de9/Leeds-United-Tottenham-Hotspur-February-26-2022-Premier-League',
#     'https://fbref.com/en/matches/086dcb8d/Crystal-Palace-Burnley-February-26-2022-Premier-League',
#     'https://fbref.com/en/matches/43737c9c/Manchester-United-Watford-February-26-2022-Premier-League',
#     'https://fbref.com/en/matches/8cabd787/Brighton-and-Hove-Albion-Aston-Villa-February-26-2022-Premier-League',
#     'https://fbref.com/en/matches/fd61d442/Brentford-Newcastle-United-February-26-2022-Premier-League',
#     'https://fbref.com/en/matches/ab729bd6/Everton-Manchester-City-February-26-2022-Premier-League',
#     'https://fbref.com/en/matches/b1dcaf8d/West-Ham-United-Wolverhampton-Wanderers-February-27-2022-Premier-League',
#     'https://fbref.com/en/matches/a47f5f21/Burnley-Leicester-City-March-1-2022-Premier-League',
#     ]

# urls=[
#     'https://fbref.com/en/matches/1d777dcd/Leicester-City-Leeds-United-March-5-2022-Premier-League',
#     'https://fbref.com/en/matches/02337bda/Newcastle-United-Brighton-and-Hove-Albion-March-5-2022-Premier-League',
#     'https://fbref.com/en/matches/1aa40463/Aston-Villa-Southampton-March-5-2022-Premier-League',
#     'https://fbref.com/en/matches/926192f8/Burnley-Chelsea-March-5-2022-Premier-League',
#     'https://fbref.com/en/matches/9ccef73f/Wolverhampton-Wanderers-Crystal-Palace-March-5-2022-Premier-League',
#     'https://fbref.com/en/matches/fcb61cff/Norwich-City-Brentford-March-5-2022-Premier-League',
#     'https://fbref.com/en/matches/bc1944c3/Liverpool-West-Ham-United-March-5-2022-Premier-League',
#     'https://fbref.com/en/matches/9d5abf8b/Watford-Arsenal-March-6-2022-Premier-League',
#     'https://fbref.com/en/matches/2dc5b8b0/Manchester-Derby-Manchester-City-Manchester-United-March-6-2022-Premier-League',
#     'https://fbref.com/en/matches/6e11eac6/Tottenham-Hotspur-Everton-March-7-2022-Premier-League',
#     'https://fbref.com/en/matches/d0ee0e9a/Wolverhampton-Wanderers-Watford-March-10-2022-Premier-League',
#     'https://fbref.com/en/matches/2d6fb488/Southampton-Newcastle-United-March-10-2022-Premier-League',
#     'https://fbref.com/en/matches/4371c286/Norwich-City-Chelsea-March-10-2022-Premier-League',
#     'https://fbref.com/en/matches/79b8fb6e/Leeds-United-Aston-Villa-March-10-2022-Premier-League',
#     ]

