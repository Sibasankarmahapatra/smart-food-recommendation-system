import pandas as pd
import os

def load_data():
    """Load all datasets and perform basic cleaning."""
    data_dir = "data"
    
    # Load datasets
    df_restaurants = pd.read_csv(os.path.join(data_dir, "restaurants.csv"))
    df_menu = pd.read_csv(os.path.join(data_dir, "menu.csv"))
    df_users = pd.read_csv(os.path.join(data_dir, "users.csv"))
    df_ratings = pd.read_csv(os.path.join(data_dir, "ratings.csv"))
    
    # Data Cleaning & Validation
    df_restaurants = clean_dataframe(df_restaurants)
    df_menu = clean_dataframe(df_menu)
    df_users = clean_dataframe(df_users)
    df_ratings = clean_dataframe(df_ratings)
    
    return df_restaurants, df_menu, df_users, df_ratings

def clean_dataframe(df):
    """Perform data curation: remove duplicates and handle missing values."""
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Fill missing values for numerical columns with 0 or mean
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[num_cols] = df[num_cols].fillna(0)
    
    # Fill missing values for categorical columns with 'Unknown'
    cat_cols = df.select_dtypes(include=['object']).columns
    df[cat_cols] = df[cat_cols].fillna('Unknown')
    
    return df

def get_data_summary(df, name):
    """Generate a summary of data quality."""
    summary = {
        "Dataset": name,
        "Total Rows": len(df),
        "Total Columns": len(df.columns),
        "Missing Values": df.isnull().sum().sum(),
        "Duplicate Rows": df.duplicated().sum()
    }
    return summary
