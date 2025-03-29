import os
import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from collections import Counter
from streamlit_option_menu import option_menu
import nltk

# Download required NLTK data (if not already downloaded)
nltk.download('stopwords')
nltk.download('punkt')

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="IHRG",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "# This Industrial Human Resource Geo-Visualization page is created by *Vivekananda!*"}
)
st.markdown("<h1 style='text-align: center; color: Red;'>Industrial Human Resource Geo-Visualization</h1>", unsafe_allow_html=True)

# -----------------------------
# Load CSV Data
# -----------------------------
csv_path = r"C:\Users\vivsk\CTRT\Industrial Human Resource Geo-Visualization\final_hr.csv"
if not os.path.exists(csv_path):
    st.error(f"CSV file not found at {csv_path}. Please check the file path.")
    st.stop()

data = pd.read_csv(csv_path, encoding='latin')
# Strip extra spaces from column names
data.columns = [col.strip() for col in data.columns]

# -----------------------------
# Sidebar Filters
# -----------------------------
unique_states = sorted(data['State'].unique())
selected_state = st.sidebar.selectbox("Select State", unique_states, key="state_selector_unique")

filtered_districts = sorted(data[data['State'] == selected_state]['District'].unique())
selected_district = st.sidebar.selectbox("Select District", filtered_districts, key="district_selector_unique")

filtered_nic_names = data[data['District'] == selected_district]['NICName'].unique()
filtered_nic_names = [nic.replace('[', '').replace(']', '').replace("'", "").capitalize() for nic in filtered_nic_names]
filtered_nic_names = sorted(filtered_nic_names)
selected_nic_name = st.sidebar.selectbox("Select NIC Name", filtered_nic_names, key="nic_name_selector")

# Filter the DataFrame for the selected state and district
state_data = data[data['State'] == selected_state]
district_data = data[data['District'] == selected_district]

# -----------------------------
# Display Summary Information
# -----------------------------
with st.container():
    st.write(f"### Showing data for {selected_state} - {selected_district}")
    col1, col2 = st.columns(2)
    with col1:
        total_state_workers = state_data['MainWorkersTotalPersons'].sum()
        st.write(f"**Total number of state workers:** {total_state_workers}")
    with col2:
        total_district_workers = district_data['MainWorkersTotalPersons'].sum()
        st.write(f"**Total number of district workers:** {total_district_workers}")
    with st.expander("See Data Summary"):
        st.write(data.describe())

# -----------------------------
# Organize Visualizations in Tabs
# -----------------------------
tabs = st.tabs(["Stacked Bar Chart", "Pie Charts", "Plotly Chart", "Geo-Map"])

# ---- Tab 1: Stacked Bar Chart ----
with tabs[0]:
    st.markdown("#### Workers Distribution (Stacked Bar Chart)")
    fig, ax = plt.subplots(figsize=(10, 6))
    x_labels = ['Rural', 'Main', 'Urban']
    bottom_values = [0] * len(x_labels)
    rural_cols = ['MainWorkersRuralPersons', 'MainWorkersRuralMales', 'MainWorkersRuralFemales']
    main_cols  = ['MainWorkersTotalPersons', 'MainWorkersTotalMales', 'MainWorkersTotalFemales']
    urban_cols = ['MainWorkersUrbanPersons', 'MainWorkersUrbanMales', 'MainWorkersUrbanFemales']
    for label, cols in zip(['Rural', 'Main', 'Urban'], [rural_cols, main_cols, urban_cols]):
        values = data[cols].sum().values
        ax.bar(x_labels, values, label=label, bottom=bottom_values)
        bottom_values = [sum(x) for x in zip(bottom_values, values)]
    ax.set_title(f"{selected_state} - {selected_district} - Workers Distribution")
    ax.legend()
    st.pyplot(fig)

# ---- Tab 2: Pie Charts ----
with tabs[1]:
    st.markdown("#### Marginal Workers Distribution (Pie Charts)")
    col1, col2 = st.columns(2)
    with col1:
        fig_rural, ax_rural = plt.subplots(figsize=(6, 6))
        marginal_cols_rural = ['MarginalWorkersRuralPersons', 'MarginalWorkersRuralMales', 'MarginalWorkersRuralFemales']
        marginal_data_rural = data[marginal_cols_rural].sum().values
        ax_rural.pie(marginal_data_rural, labels=marginal_cols_rural, autopct='%1.1f%%', startangle=90,
                     colors=['#7C00FE', '#F9E400', '#F5004F'])
        ax_rural.set_title(f"{selected_state} - {selected_district} - Rural Marginal Workers")
        st.pyplot(fig_rural)
    with col2:
        fig_urban, ax_urban = plt.subplots(figsize=(6, 6))
        marginal_cols_urban = ['MarginalWorkersUrbanPersons', 'MarginalWorkersUrbanMales', 'MarginalWorkersUrbanFemales']
        marginal_data_urban = data[marginal_cols_urban].sum().values
        ax_urban.pie(marginal_data_urban, labels=marginal_cols_urban, autopct='%1.1f%%', startangle=90,
                     colors=['#7C00FE', '#F9E400', '#F5004F'])
        ax_urban.set_title(f"{selected_state} - {selected_district} - Urban Marginal Workers")
        st.pyplot(fig_urban)

# ---- Tab 3: Plotly Bar Chart ----
with tabs[2]:
    st.markdown("#### Workers Distribution by State (Plotly Bar Chart)")
    main_data_grouped = data[['State'] + main_cols].groupby('State').sum().reset_index()
    main_data_melted = main_data_grouped.melt(id_vars='State', var_name='WorkerType', value_name='Count')
    fig_bar = px.bar(main_data_melted, x='State', y='Count', color='WorkerType',
                     title='Differences in Main, Rural, and Urban Workers Counts (State-wise)',
                     labels={'Count': 'Total Workers Count'},
                     color_discrete_sequence=['#7C00FE', '#F9E400', '#F5004F'],
                     template='plotly_white')
    fig_bar.update_layout(barmode='group', xaxis_title='State', yaxis_title='Total Workers Count (Log Scale)', yaxis_type="log")
    st.plotly_chart(fig_bar)

# ---- Tab 4: Geo-Map ----
with tabs[3]:
    st.markdown("#### Geo-Map with Official Boundaries")
    # Set SHAPE_RESTORE_SHX to restore missing .shx file if needed
    os.environ['SHAPE_RESTORE_SHX'] = 'YES'
    shp_path = r"C:\Users\vivsk\CTRT\Industrial Human Resource Geo-Visualization\India\India_Country_Boundary.shp"
    try:
        gdf = gpd.read_file(shp_path)
        gdf = gdf.to_crs(epsg=4326)
        geojson_data = gdf.to_json()
    except Exception as e:
        st.error(f"Error loading shapefile: {e}")
        geojson_data = None
    
    folium_map = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=5,
        tiles='CartoDB Positron'
    )
    if geojson_data:
        folium.GeoJson(
            geojson_data,
            name="Official Boundaries",
            style_function=lambda feature: {
                'fillColor': 'transparent',
                'color': 'blue',
                'weight': 2,
                'dashArray': '5, 5'
            }
        ).add_to(folium_map)
    else:
        st.warning("Official boundaries could not be loaded.")
    
    marker_cluster = MarkerCluster().add_to(folium_map)
    for idx, row in district_data.iterrows():
        try:
            lat, lon = float(row['latitude']), float(row['longitude'])
            total_workers = row['MainWorkersTotalPersons']
            male_female_ratio = row['MaleFemaleRatio']
            popup_text = f"State: {selected_state}<br>District: {selected_district}<br>Total Workers: {total_workers}<br>Male-Female Ratio: {male_female_ratio}"
            folium.Marker([lat, lon], popup=popup_text).add_to(marker_cluster)
        except Exception as e:
            st.write(f"Error adding marker for row {idx}: {e}")
    
    folium.LayerControl().add_to(folium_map)
    folium_static(folium_map, width=1200, height=600)
