# Annapatha (अन्नपथ) - Smart Food & Restaurant Recommendation System

Annapatha (meaning "The Path to Food") is a professional, visually stunning food and restaurant recommendation system built with Python and Streamlit. This project is designed for academic data curation purposes, focusing on geospatial analysis, data quality, and a modern user interface.

## 🚀 Features

- **Modern UI/UX:** Clean, responsive design using custom CSS and Poppins typography.
- **Smart Recommendations:** Weighted scoring system based on rating, distance, availability, and price.
- **Interactive Mapping:** Visualize restaurants and user location using Folium and OpenStreetMap.
- **Data Curation:** Automated data cleaning, duplicate removal, and quality validation.
- **Advanced Analytics:** Interactive charts for rating distributions, price analysis, and category splits.
- **User Personalization:** Favorite restaurants list and search history tracking via session state.
- **Export Capabilities:** Download filtered results and recommendations as CSV.

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Typography:** Google Fonts (Poppins)
- **Data Analysis:** Pandas, NumPy
- **Geospatial:** Geopy, Folium, Streamlit-Folium
- **Visualization:** Plotly
- **Maps/Geocoding:** OpenStreetMap (Free), Nominatim API (Free)

## 📂 Project Structure

```text
FoodRec/
├── app.py              # Main Streamlit application (Annapatha)
├── data/               # Sample datasets
│   ├── restaurants.csv # Restaurant details & locations
│   ├── menu.csv        # Detailed food menus
│   ├── users.csv       # User profiles
│   └── ratings.csv     # User ratings and reviews
├── utils/              # Modular utility functions
│   ├── data_loader.py  # Data loading and cleaning
│   ├── geo_utils.py    # Geocoding and distance logic
│   └── rec_engine.py   # Recommendation scoring engine
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

## ⚙️ Setup Instructions

1. **Clone or Download** the repository.
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application:**
   ```bash
   streamlit run app.py
   ```
4. **Usage:**
   - Navigate through the modern sidebar menu.
   - Enter your coordinates or use the defaults for distance-based results.
   - Filter results based on your budget and rating preferences.

## 📝 Data Curation Notes

Annapatha implements a robust data curation pipeline:
1. **Deduplication:** Automatically identifies and removes duplicate entries.
2. **Missing Value Handling:** Imputes missing numerical values with 0/means and categorical values with 'Unknown'.
3. **Validation:** Ensures data consistency across different datasets.

## ⚠️ Important Information

- **No Paid APIs Required:** This project uses only free and open-source APIs.
- **Local Execution:** Designed to run entirely on your local machine.
- **Privacy:** No user images or thumbnails are required or stored.

---
*Developed as a Python Data Curation Academic Project.*
