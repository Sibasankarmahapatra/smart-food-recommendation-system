import pandas as pd
import numpy as np

def generate_recommendations(df_restaurants, user_lat, user_lon, max_price, min_rating, category_filter):
    """Generate recommendation score and sort restaurants."""
    df = df_restaurants.copy()
    
    # Apply Filters
    if category_filter != "All":
        df = df[df['Category'] == category_filter]
    
    df = df[df['Price'] <= max_price]
    df = df[df['Rating'] >= min_rating]
    
    if df.empty:
        return df

    # Calculate Distance
    from utils.geo_utils import calculate_distance
    df['Distance_KM'] = df.apply(
        lambda row: calculate_distance(user_lat, user_lon, row['Latitude'], row['Longitude']), 
        axis=1
    )
    
    # Normalize values for scoring
    # Rating: 0 to 5
    # Distance: Lower is better
    # Price: Lower is better
    # Availability: Yes is 1, No is 0
    
    max_dist = df['Distance_KM'].max() if not df['Distance_KM'].empty else 1
    max_price_val = df['Price'].max() if not df['Price'].empty else 1
    
    df['Availability_Score'] = df['Availability'].apply(lambda x: 1 if x == 'Yes' else 0)
    df['Distance_Score'] = 1 - (df['Distance_KM'] / (max_dist + 1))
    df['Price_Score'] = 1 - (df['Price'] / (max_price_val + 1))
    
    # Weighted Score
    df['Rec_Score'] = (
        (df['Rating'] / 5.0) * 0.4 +
        df['Availability_Score'] * 0.3 +
        df['Distance_Score'] * 0.2 +
        df['Price_Score'] * 0.1
    ) * 100
    
    # Sort by Rec_Score
    df = df.sort_values(by='Rec_Score', ascending=False)
    
    return df
