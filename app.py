import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the data
drought_data = pd.read_csv('indian_states_drought.csv')

# Aggregate the data
drought_data = drought_data.groupby('State').agg({
    'Drought_Percentage': 'mean',
    'Crop_Type': lambda x: x.mode()[0]
}).reset_index()

drought_data.columns = ['States', 'Drought Percentage', 'Affected Crop by Drought']

# Load the shapefile
shp_gdf = gpd.read_file('data/')
merged = shp_gdf.set_index('st_nm').join(drought_data.set_index('States'))

# Streamlit layout
st.title('Drought Analysis in Indian States')

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login block
if not st.session_state.logged_in:
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        if username == "Admin" and password == "Admin":
            st.session_state.logged_in = True
            st.success('Login successful')
        else:
            st.error('Invalid username or password')

# If logged in, show the main content
if st.session_state.logged_in:
    st.subheader('Aggregated Drought Data')
    st.dataframe(drought_data)

    # Pie Chart
    st.subheader('Mean Drought Percentage by State')
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(drought_data['Drought Percentage'], labels=drought_data['States'], autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

    # Indian Map with Drought Percentages
    st.subheader('Drought Percentage by State Map')
    fig, ax = plt.subplots(1, figsize=(15, 30))
    ax.axis('off')
    ax.set_title('Drought Percentage by State', fontdict={'fontsize': '15', 'fontweight': '3'})

    merged.plot(column='Drought Percentage', cmap='OrRd', linewidth=0.5, ax=ax, edgecolor='0.8', legend=False)

    for idx, row in merged.iterrows():
        if pd.notna(row['Drought Percentage']):
            centroid = row['geometry'].centroid
            plt.annotate(text=idx, xy=(centroid.x, centroid.y), xytext=(3, 3), textcoords="offset points", fontsize=8, ha='center', color='black')
            plt.annotate(text=f"{row['Drought Percentage']:.2f}%", xy=(centroid.x, centroid.y), xytext=(3, -12), textcoords="offset points", fontsize=8, ha='center', color='black')

    st.pyplot(fig)

# Option to log out
if st.session_state.logged_in:
    if st.button('Logout'):
        st.session_state.logged_in = False
        st.success('Logged out successfully')
