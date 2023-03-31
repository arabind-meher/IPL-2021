from os import listdir
from os.path import join

import pandas as pd
import streamlit as st
from PIL import Image

from match import Match

st.set_page_config(
    page_title='IPL 2021',
    page_icon=Image.open('assets/india-flag'),
    layout='wide'
)

with open('styles/main.css') as style:
    st.markdown(f'<style>{style.read()}</style>', unsafe_allow_html=True)

if __name__ == '__main__':
    st.title('IPL 2021 (**Winner: Chennai Super Kings**)')
    st.markdown('---')

    matches_data = pd.read_csv(join('dataset', 'Matches Details.csv'), index_col=0)
    point_table = pd.read_csv(join('dataset', 'Point Table.csv'), index_col=0)
    match_dict = dict(zip(matches_data.index, listdir('dataset')[:-2]))

    matches_button = st.sidebar.button('Matches')
    point_table_button = st.sidebar.button('Point Table')

    st.sidebar.markdown('---')

    st.sidebar.header('Matches:')
    match = st.sidebar.selectbox('Select Match:', match_dict.keys())
    search = st.sidebar.button('Search')

    if matches_button:
        matches_df = matches_data.copy()
        matches_df.columns = [x.replace('_', ' ').title() for x in matches_df.columns]
        st.dataframe(matches_df)
        del matches_df

    if point_table_button:
        point_table_df = point_table.copy()
        point_table_df.columns = [x.replace('_', ' ').title() for x in point_table_df.columns]
        st.dataframe(point_table_df)
        del point_table_df

    if search:
        st.markdown(f'''
        ## {match} - (Winner: {matches_data.loc[match, "winner"]})
        - ##### :beginner: {matches_data.loc[match, "team_1"]} :vs: {matches_data.loc[match, "team_2"]}
        - ##### :beginner: Date: {matches_data.loc[match, "date"]} ({matches_data.loc[match, "day"]})
        - ##### :beginner: Player of the Match: {matches_data.loc[match, "player_of_match"]}
        - ##### :beginner: Umpires: {matches_data.loc[match, "umpire_1"]}, {matches_data.loc[match, "umpire_2"]}
        - ##### :beginner: Venue: {matches_data.loc[match, "venue"]}
        ''')

        match_data = Match(match_dict[match], matches_data.loc[match, :])

        st.markdown('---')

        st.pyplot(match_data.teams_score())

        st.markdown('---')

        st.pyplot(match_data.runs_per_over_bar())

        st.markdown('---')

        st.pyplot(match_data.runs_per_over_line())

        st.markdown('---')

        st.pyplot(match_data.team_1_batting_score())

        st.markdown('---')

        st.pyplot(match_data.team_2_batting_score())

        st.markdown('---')
        
        del search
