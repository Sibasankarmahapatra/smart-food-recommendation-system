import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
from utils.data_loader import load_data, get_data_summary
from utils.geo_utils import get_user_location, calculate_distance
from utils.rec_engine import generate_recommendations
import os

# Page configuration
st.set_page_config(
    page_title="Annapatha (अन्नपथ) - Smart Food Rec",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern, attractive look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background-color: #f5f7f9 !important;
    }
    
    /* Global Visibility and Theme Force */
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    [data-testid="stToolbar"],
    .main {
        background: #f5f7f9 !important;
        background-image: linear-gradient(135deg, #f5f7f9 0%, #eef2f7 100%) !important;
    }

    [data-testid="stAppViewContainer"] * {
        color: #1a1a1a !important;
    }

    /* Exceptions for specific elements */
    div[style*="background-color: rgb(255, 75, 75)"] *,
    div[style*="background-color: #ff4b4b"] *,
    .stButton > button {
        color: #ffffff !important;
    }

    [data-testid="stMetricValue"] {
        color: #ff4b4b !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background-color: #ffffff !important;
        border-right: none !important;
    }
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    
    /* Ensure sidebar headers and labels are extra visible */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }

    /* Fix for black background in all input fields */
    input, select, textarea {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    div[data-baseweb="input"],
    div[data-baseweb="select"],
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
    }
    
    /* Target the container of the input to remove dark background */
    section[data-testid="stSidebar"] div[data-baseweb="input"],
    section[data-testid="stSidebar"] div[data-baseweb="select"],
    section[data-testid="stSidebar"] div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
    }
    
    /* Target the step buttons in number input */
    section[data-testid="stSidebar"] button[kind="secondary"] {
        background-color: #f0f0f0 !important;
        color: #1a1a1a !important;
    }
    
    /* Card styling */
    .stMetric {
        background: #ffffff !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
        border: 1px solid #f0f0f0 !important;
        transition: transform 0.3s ease;
    }
    .stMetric:hover {
        transform: translateY(-5px);
    }
    .stMetric [data-testid="stMetricLabel"] {
        color: #555555 !important;
        font-weight: 600 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #ff4b4b !important;
        font-weight: 700 !important;
    }
    
    .restaurant-card {
        background: #ffffff !important;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #f0f0f0 !important;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
        color: #2c3e50 !important;
    }
    .restaurant-card:hover {
        box-shadow: 0 12px 24px rgba(0,0,0,0.08);
        transform: scale(1.01);
    }
    .restaurant-card h3 {
        color: #1a1a1a !important;
        margin-top: 0;
        font-weight: 700 !important;
    }
    .restaurant-card p, .restaurant-card b {
        color: #555555 !important;
    }
    
    /* Buttons - Unified styling for all button types */
    .stButton>button, .stDownloadButton>button {
        border-radius: 12px !important;
        background-color: #ff4b4b !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        display: block !important;
        box-shadow: 0 4px 6px rgba(255, 75, 75, 0.2) !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #ff3333 !important;
        box-shadow: 0 6px 12px rgba(255, 75, 75, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    .stButton>button p, .stDownloadButton>button p {
        color: white !important;
    }

    /* Fix for number input step buttons appearing black (+ and - buttons) - Global */
    [data-testid="stNumberInputStepUp"], 
    [data-testid="stNumberInputStepDown"],
    [data-testid="stNumberInputStepUp"] button,
    [data-testid="stNumberInputStepDown"] button {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border: none !important;
    }

    /* Target the SVG icons inside the buttons specifically */
    [data-testid="stNumberInputStepUp"] svg,
    [data-testid="stNumberInputStepDown"] svg {
        fill: #1a1a1a !important;
        color: #1a1a1a !important;
    }

    /* Target the base-web buttons specifically */
    button[data-baseweb="button"] {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    /* Ensure all buttons and selectbox arrows have dark icons/text on light background */
    button *, [data-testid="stSelectbox"] svg, [data-baseweb="select"] svg {
        color: #1a1a1a !important;
        fill: #1a1a1a !important;
    }
    
    /* Target the dropdown arrow specifically for selectbox */
    div[data-baseweb="select"] div[role="button"] svg {
        fill: #1a1a1a !important;
    }

    /* Re-exception for the main action buttons which should stay red/white */
    .stButton > button *, .stDownloadButton > button * {
        color: #ffffff !important;
        fill: #ffffff !important;
    }
    
    /* Titles */
    h1 {
        color: #1a1a1a !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    
    /* Ensure all headers in the main area are bold and dark */
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
        font-weight: 700 !important;
    }

    /* Table and Dataframe visibility fix */
    [data-testid="stTable"] *, [data-testid="stDataFrame"] *, [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    
    /* Plotly Chart background fix */
    .js-plotly-plot .plotly, .js-plotly-plot .main-svg {
        background-color: transparent !important;
    }
    
    /* Remove all default vertical lines and borders from Streamlit elements */
    [data-testid="column"] {
        border-left: none !important;
        border-right: none !important;
    }
    
    div.stVerticalBlock {
        border-left: none !important;
    }

    /* Expander labels and arrows */
    .stExpander summary p {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    .stExpander svg {
        fill: #1a1a1a !important;
        color: #1a1a1a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Load data
@st.cache_data
def get_cached_data():
    return load_data()

df_restaurants, df_menu, df_users, df_ratings = get_cached_data()

# Sidebar Navigation
st.sidebar.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🍲 Annapatha</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-style: italic; color: #555555;'>Your Ultimate Food Journey</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🔍 Food Search", "🏪 Restaurant Search", "⭐ Recommendations", "🗺️ Map View", "📈 Analytics", "ℹ️ About Project"]
)

# User Location (Mock for now, can be input by user)
st.sidebar.markdown("---")
st.sidebar.header("📍 Your Location")
user_lat = st.sidebar.number_input("Latitude", value=20.2961, format="%.6f")
user_lon = st.sidebar.number_input("Longitude", value=85.8245, format="%.6f")

# --- Home Page ---
if page == "🏠 Home":
    st.title("Welcome to Annapatha (अन्नपथ)")
    st.markdown("""
    <div style="background-color: #ff4b4b; padding: 20px; border-radius: 15px; color: white; margin-bottom: 30px;">
        <h3 style="margin: 0; color: white;">Discover the Path to Great Food</h3>
        <p style="margin: 5px 0 0 0; opacity: 0.9;">Annapatha is your intelligent companion for finding the best restaurants, exploring diverse cuisines, and getting personalized recommendations tailored to your taste and location.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard Metrics
    st.subheader("📊 System Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Restaurants", len(df_restaurants))
    with col2:
        st.metric("Total Food Items", len(df_menu))
    with col3:
        st.metric("Avg Restaurant Rating", round(df_restaurants['Rating'].mean(), 2))
    with col4:
        st.metric("Available Now", len(df_restaurants[df_restaurants['Availability'] == 'Yes']))

    st.markdown("---")
    
    # Data Quality Summary (Curation)
    st.subheader("🧹 Data Curation & Quality")
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("Data has been cleaned: duplicates removed and missing values handled.")
        summary_df = pd.DataFrame([
            get_data_summary(df_restaurants, "Restaurants"),
            get_data_summary(df_menu, "Menu"),
            get_data_summary(df_users, "Users"),
            get_data_summary(df_ratings, "Ratings")
        ])
        st.table(summary_df)
    with col_b:
        st.success("✅ All datasets validated and ready for analysis.")
        st.write("Last Data Sync: 2026-06-05")

# --- Food Search Page ---
elif page == "🔍 Food Search":
    st.title("🔍 Search Food Items")
    
    # Filters
    with st.expander("Filter Options"):
        col1, col2, col3 = st.columns(3)
        with col1:
            max_p = st.slider("Max Price", 0, 2000, 500)
        with col2:
            min_r = st.slider("Min Rating", 0.0, 5.0, 3.5)
        with col3:
            cat = st.selectbox("Category", ["All"] + list(df_menu['Category'].unique()))

    search_query = st.text_input("What are you craving?", placeholder="e.g. Pasta, Biryani...")
    
    if search_query:
        if search_query not in st.session_state.search_history:
            st.session_state.search_history.append(search_query)
        
        results = df_menu[df_menu['Menu_Item'].str.contains(search_query, case=False, na=False)]
        
        # Merge with restaurant info for price/rating
        results = results.merge(df_restaurants[['Restaurant', 'Rating', 'Availability', 'Address', 'Latitude', 'Longitude']], on='Restaurant')
        
        # Apply filters
        results = results[results['Price'] <= max_p]
        results = results[results['Rating'] >= min_r]
        if cat != "All":
            results = results[results['Category_x'] == cat] # Category_x is from menu

        if not results.empty:
            results['Distance_KM'] = results.apply(lambda row: round(calculate_distance(user_lat, user_lon, row['Latitude'], row['Longitude']), 2), axis=1)
            results = results.sort_values('Distance_KM')
            
            st.write(f"Found {len(results)} items matching your search.")
            for _, row in results.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="restaurant-card">
                        <h3>{row['Menu_Item']} at {row['Restaurant']}</h3>
                        <p><b>Price:</b> ₹{row['Price']} <span style='color: #ff4b4b;'>•</span> <b>Rating:</b> ⭐ {row['Rating']} <span style='color: #ff4b4b;'>•</span> <b>Distance:</b> {row['Distance_KM']} km</p>
                        <p><b>Address:</b> {row['Address']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Add {row['Restaurant']} to Favorites", key=f"fav_{row['Restaurant']}_{row['Menu_Item']}"):
                        if row['Restaurant'] not in st.session_state.favorites:
                            st.session_state.favorites.append(row['Restaurant'])
                            st.success(f"Added {row['Restaurant']} to favorites!")
            
            # Export
            st.download_button("📥 Download Results as CSV", results.to_csv(index=False), "food_search_results.csv", "text/csv")
        else:
            st.warning("No food items found matching your criteria.")

# --- Restaurant Search Page ---
elif page == "🏪 Restaurant Search":
    st.title("🏪 Search Restaurants")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_res = st.text_input("Enter Restaurant Name", placeholder="e.g. Sushi World...")
    with col2:
        dist_filter = st.number_input("Max Distance (km)", value=10.0)

    res_results = df_restaurants[df_restaurants['Restaurant'].str.contains(search_res, case=False, na=False)]
    res_results['Distance_KM'] = res_results.apply(lambda row: round(calculate_distance(user_lat, user_lon, row['Latitude'], row['Longitude']), 2), axis=1)
    res_results = res_results[res_results['Distance_KM'] <= dist_filter]
    res_results = res_results.sort_values('Distance_KM')

    if not res_results.empty:
        for _, row in res_results.iterrows():
            with st.expander(f"{row['Restaurant']} - ⭐ {row['Rating']} ({row['Distance_KM']} km)"):
                st.write(f"**Category:** {row['Category']}")
                st.write(f"**Address:** {row['Address']}")
                st.write(f"**Availability:** {'✅ Available' if row['Availability'] == 'Yes' else '❌ Currently Closed'}")
                
                # Show Menu for this restaurant
                st.subheader("Menu")
                res_menu = df_menu[df_menu['Restaurant'] == row['Restaurant']]
                st.table(res_menu[['Menu_Item', 'Price', 'Category']])
    else:
        st.warning("No restaurants found.")

# --- Recommendations Page ---
elif page == "⭐ Recommendations":
    st.title("⭐ Top Recommended for You")
    st.markdown("Based on Rating, Distance, Availability, and Price.")
    
    # Rec Filters in sidebar or top
    st.sidebar.markdown("---")
    st.sidebar.subheader("Recommendation Filters")
    r_max_p = st.sidebar.slider("Max Budget (₹)", 100, 2000, 1000)
    r_min_r = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 4.0)
    r_cat = st.sidebar.selectbox("Filter by Category", ["All"] + list(df_restaurants['Category'].unique()))

    rec_df = generate_recommendations(df_restaurants, user_lat, user_lon, r_max_p, r_min_r, r_cat)
    
    if not rec_df.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            for i, row in rec_df.head(5).iterrows():
                st.markdown(f"""
                <div class="restaurant-card">
                    <h3>#{i+1} {row['Restaurant']}</h3>
                    <p><b>Rec Score:</b> {round(row['Rec_Score'], 2)}% <span style='color: #ff4b4b;'>•</span> <b>Rating:</b> ⭐ {row['Rating']}</p>
                    <p><b>Distance:</b> {round(row['Distance_KM'], 2)} km <span style='color: #ff4b4b;'>•</span> <b>Price:</b> ₹{row['Price']} avg</p>
                    <p><b>Category:</b> {row['Category']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Quick Stats")
            st.write(f"Top Pick: **{rec_df.iloc[0]['Restaurant']}**")
            st.write(f"Best Price: **{rec_df.sort_values('Price').iloc[0]['Restaurant']}**")
            
            st.download_button("📥 Export Recommendations", rec_df.to_csv(index=False), "recommendations.csv", "text/csv")
    else:
        st.info("Adjust filters to see recommendations.")

# --- Map View Page ---
elif page == "🗺️ Map View":
    st.title("🗺️ Interactive Restaurant Map")
    
    m = folium.Map(location=[user_lat, user_lon], zoom_start=14)
    
    # User Marker
    folium.Marker(
        [user_lat, user_lon],
        popup="You Are Here",
        tooltip="Your Location",
        icon=folium.Icon(color='blue', icon='user')
    ).add_to(m)
    
    # Restaurant Markers
    for _, row in df_restaurants.iterrows():
        dist = round(calculate_distance(user_lat, user_lon, row['Latitude'], row['Longitude']), 2)
        popup_content = f"""
        <b>{row['Restaurant']}</b><br>
        Food: {row['Food']}<br>
        Rating: ⭐ {row['Rating']}<br>
        Distance: {dist} km
        """
        folium.Marker(
            [row['Latitude'], row['Longitude']],
            popup=popup_content,
            tooltip=row['Restaurant'],
            icon=folium.Icon(color='red', icon='cutlery')
        ).add_to(m)
    
    st_folium(m, width=1000, height=600)

# --- Analytics Page ---
elif page == "📈 Analytics":
    st.title("📈 System Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rating Distribution")
        fig1 = px.histogram(df_restaurants, x="Rating", nbins=10, title="Restaurant Ratings")
        st.plotly_chart(fig1, use_container_width=True)
        
        st.subheader("Price Distribution")
        fig2 = px.box(df_restaurants, y="Price", title="Price Range across Restaurants")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.subheader("Food Category Distribution")
        cat_counts = df_menu['Category'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']
        fig3 = px.pie(cat_counts, values='Count', names='Category', title="Menu Items by Category")
        st.plotly_chart(fig3, use_container_width=True)
        
        st.subheader("Top Rated Restaurants")
        top_rated = df_restaurants.nlargest(5, 'Rating')
        fig4 = px.bar(top_rated, x='Restaurant', y='Rating', color='Rating', title="Top 5 Rated Restaurants")
        st.plotly_chart(fig4, use_container_width=True)

# --- About Project Page ---
elif page == "ℹ️ About Project":
    st.title("ℹ️ About Annapatha")
    st.markdown("""
    ### Annapatha (अन्नपथ) - Smart Food & Restaurant Recommendation System
    This project is developed as a **Python Data Curation Academic Project**. 
    It demonstrates the integration of multiple data sources, data cleaning, geospatial analysis, and a custom recommendation engine.

    **Key Technologies:**
    - **Frontend:** Streamlit
    - **Data Processing:** Pandas, NumPy
    - **Geospatial:** Geopy, Folium
    - **Visualization:** Plotly
    - **APIs:** OpenStreetMap (via Geopy/Folium)

    **Developer Notes:**
    - No paid APIs were used.
    - Data is curated from CSV files located in the `data/` directory.
    - The recommendation engine uses a weighted scoring system based on multi-criteria decision making.
    """)
    
    st.subheader("❤️ Your Favorites")
    if st.session_state.favorites:
        for fav in st.session_state.favorites:
            st.write(f"- {fav}")
    else:
        st.write("No favorites added yet.")
    
    st.subheader("🕒 Recent Searches")
    if st.session_state.search_history:
        for s in st.session_state.search_history[-5:]:
            st.write(f"- {s}")
    else:
        st.write("No recent searches.")
