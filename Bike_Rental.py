import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

def background():
    st.set_page_config(layout="wide",
                       page_title="Analysis Dashboard",
                       page_icon=":rocket:",
                       initial_sidebar_state="expanded")
background()

st.write("""
        # :sparkles: Welcome to :bike: "Bike Sharing" :bike: Dashboard :sparkles:
        """)

#Add picture
bike_img = Image.open("bike.jpg")
idcamp_img = Image.open("IDCamp.jpg")

image_file = ["indosat.jpg", "dicoding.jpg"]
desired_width = 150
desired_height = 60


with st.sidebar:
    st.markdown("""
        <style>
            div {
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    st.image (bike_img, use_column_width=True)

    st.header("""
              This Dashboard is deployed as one of the final projects of [IDCamp](https://www.idcamp.ioh.co.id/)
               """)
    st.image (idcamp_img, use_column_width=True)
    st.write('IDCamp is a scholarship program organized by Indosat Ooredoo Hutchison with the aim of cultivating young Indonesian developers ready to compete in the global digital economy.')
    st.write('The online training module for IDCamp is developed by Dicoding, which is a Google Authorized Training Partner in Indonesia.')
    st.write('In the development of its materials, Dicoding collaborates with Indosat Ooredoo Hutchison, utilizing use cases commonly encountered in the industrial world.')
    
    col1, col2 = st.columns(2)
    for idx, image_file in enumerate(image_file):
        iohd = Image.open(image_file)
        resized_img = iohd.resize((desired_width, desired_height))
        if idx == 0:
                col1.image(resized_img, use_column_width=True)
        else:
                col2.image(resized_img, use_column_width=True)
    
    st.write('Submitted by: [ERIKA BUDIARTI](https://www.linkedin.com/in/erika-budiarti/)')         

def read_data(csv):
    bike_df = pd.read_csv(csv)
    return bike_df

bike_df = read_data("bike_data.csv")
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])
bike_df.resample('M', on='dteday').sum()

st.markdown(
    """
    <style>
    div[data-baseweb="tab-list"] {
        display: flex;
        justify-content: space-between;
    }
    </style>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["Casual & Registered User", "User by Nature Factors", "User by Month and Hour"])

with tab1:
    st.header("Daily Users")
    cola, colb = st.columns(2)
    
    with cola:
        total_casual = bike_df.casual.sum()
        st.markdown(f"<h2 style='text-align: center;'>Total Casual Users</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>{total_casual:,}</h3>", unsafe_allow_html=True)
    
    with colb:
        total_registered = bike_df.registered.sum()
        st.markdown(f"<h2 style='text-align: center;'>Total Registered Users</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>{total_registered:,}</h3>", unsafe_allow_html=True)
        
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=bike_df, x='dteday', y='casual', ax=ax, color='#9B5DE5', label='Casual Users')
    sns.lineplot(data=bike_df, x='dteday', y='registered', ax=ax, color='#EB8317', label='Registered Users')
    ax.set_title('Casual vs Registered Users', fontsize=12)
    ax.set_xlabel('Date', fontsize=10)
    ax.set_ylabel('User Count', fontsize=10)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

with tab2:
    st.header("Nature Factor Influences on Total Rent")
    col1, col2 = st.columns(2)
    
    def weather_rent(bike_df):
        bike_df['weathersit'] = bike_df['weathersit'].map({
            1: 'Clear or Partly Cloudy',
            2: 'Misty or Few Clouds',
            3: 'Light Snow or Light Rain',
            4: 'Heavy Rain or Ice Pallets'
        }) 
        sorted_weather_df = bike_df.groupby('weathersit').agg({'cnt': 'sum'}).reset_index().sort_values(by='cnt', ascending=True)

        fig1 = px.bar(sorted_weather_df, 
                        x='weathersit', 
                        y='cnt', 
                        color='weathersit', 
                        title='Total Rent of Different Weather',
                        color_discrete_sequence= ['#a9def9', '#a9def9', '#a9def9', '#00bbf9'])
            
        fig1.update_xaxes(title_text='Weather')
        fig1.update_yaxes(title_text='Total Rent', range=[0, 2500000], dtick=250000, autorange=False)
        fig1.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
        fig1.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
        fig1.update_layout(title='Total Rent of Different Weather', title_font=dict(size=30))
        fig1.update_layout(width=600, height=800)
        fig1.update_layout(showlegend=False)
        return fig1

    def season_rent(bike_df):
        bike_df['season'] = bike_df['season'].map({
            1: 'Spring',
            2: 'Summer',
            3: 'Fall',
            4: 'Winter'
        })
        season_df = bike_df.groupby('season').agg({'cnt': 'sum'})

        fig2 = px.bar(season_df, 
                    x='season', 
                    y='cnt', 
                    color='season', 
                    title='Total Rent of Different Season',
                    color_discrete_sequence= ['#efc3e6', '#efc3e6', '#f15bb5', '#efc3e6'])

        fig2.update_xaxes(title_text='Season')
        fig2.update_yaxes(title_text='Total Rent', range=[0, 1100000], dtick=100000, autorange=False)
        fig2.update_xaxes(title_font=dict(size=15), tickfont=dict(size=12))
        fig2.update_yaxes(title_font=dict(size=15), tickfont=dict(size=12))
        fig2.update_layout(title='Total Rent of Different Season', title_font=dict(size=30))
        fig2.update_layout(width=600, height=800)
        fig2.update_layout(showlegend=False)
        return fig2

    with col1:
        st.plotly_chart(weather_rent(bike_df))
    with col2:
        st.plotly_chart(season_rent(bike_df))


with tab3:
    st.header("Users by Month and Hour")
    col1, col2 = st.columns(2)

    def total_monthly_rent(bike_df):
        start_month = 1
        end_month = 12
        filtered_df = bike_df[
            (bike_df['mnth'] >= start_month) & (bike_df['mnth'] <= end_month)]
        total_sewa = filtered_df['cnt'].sum()
        total_monthly_rent = bike_df.groupby('mnth').agg({
            'cnt': 'sum'
        }).reset_index()
        fig1 = px.bar(total_monthly_rent, x='mnth', y='cnt')
        # Mengatur warna batang secara manual
        fig1.update_traces(marker_color='#fee440')
        fig1.update_xaxes(title_text='Month')
        fig1.update_yaxes(title_text='Total Rent',range=[0, 350000], dtick=50000, autorange=(False))
        fig1.update_layout(title='Total Monthly Rent',title_font=dict(size=30))
        fig1.update_layout(showlegend=False)
        fig1.update_layout(width=600, height=600)
        return fig1

    def total_hourly_rent(bike_df):
        start_hour = 0
        end_hour = 23
        filtered_df = bike_df[
            (bike_df['hr'] >= start_hour) & (bike_df['hr'] <= end_hour)]
        total_sewa = filtered_df['cnt'].sum()
        total_hourly_rent = bike_df.groupby('hr').agg({
            'cnt': 'sum'
        }).reset_index()
        fig2 = px.bar(total_hourly_rent, x='hr', y='cnt')
        # Mengatur warna batang secara manual
        fig2.update_traces(marker_color='#00c49a')
        fig2.update_xaxes(title_text='Hour')
        fig2.update_yaxes(title_text='Total Rent',range=[0, 350000], dtick=50000, autorange=(False))
        fig2.update_layout(title='Total Hourly Rent',title_font=dict(size=30))
        fig2.update_layout(showlegend=False)
        fig2.update_layout(width=600, height=600)
        return fig2

    with col1:
        st.plotly_chart(total_hourly_rent(bike_df))
    with col2:
        st.plotly_chart(total_monthly_rent(bike_df))

def main():
    bike_df = read_data('bike_data.csv')
    total_hourly_rent(bike_df)
    total_monthly_rent(bike_df)
    weather_rent(bike_df)
    season_rent(bike_df)

    if __name__ == "__main__":
        main()
        day_df = read_data('day.csv')
        hour_df = read_data('hour.csv')
        bike_df = read_data('bike_data.csv')

st.caption(f"Copyright © 2023-2024 All Rights Reserved [ERIKA BUDIARTI](https://www.linkedin.com/in/erika-budiarti/)")
st.snow()
