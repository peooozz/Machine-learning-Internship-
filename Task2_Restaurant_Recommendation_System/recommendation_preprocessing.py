"""
RECOMMENDATION PREPROCESSING MODULE
Task 2: Restaurant Recommendation System

This module handles:
- Loading restaurant data
- Cleaning and preprocessing
- Feature preparation for recommendations
"""

import pandas as pd
import numpy as np

def load_and_prepare_data(csv_file):
    """
    Load and preprocess restaurant data for recommendations
    
    Parameters:
    -----------
    csv_file : str
        Path to the CSV file
    
    Returns:
    --------
    df : pandas DataFrame
        Cleaned and prepared dataframe
    """
    # Load the dataset
    df = pd.read_csv(csv_file)
    print(f"✓ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Handle missing values
    print("\nHandling missing values...")
    
    # Fill missing cuisines
    if df['Cuisines'].isnull().sum() > 0:
        df['Cuisines'] = df['Cuisines'].fillna('Unknown')
        print(f"  ✓ Filled {df['Cuisines'].isnull().sum()} missing cuisine values")
    
    # Fill missing ratings with median
    if df['Aggregate rating'].isnull().sum() > 0:
        median_rating = df['Aggregate rating'].median()
        df['Aggregate rating'] = df['Aggregate rating'].fillna(median_rating)
        print(f"  ✓ Filled missing ratings with median: {median_rating}")
    
    # Fill missing cost values
    if 'Average Cost for two' in df.columns:
        if df['Average Cost for two'].isnull().sum() > 0:
            median_cost = df['Average Cost for two'].median()
            df['Average Cost for two'] = df['Average Cost for two'].fillna(median_cost)
            print(f"  ✓ Filled missing costs with median: {median_cost}")
    
    # Clean text fields
    print("\nCleaning text fields...")
    
    # Convert text to lowercase for better matching
    df['Cuisines_lower'] = df['Cuisines'].str.lower().str.strip()
    df['City_lower'] = df['City'].str.lower().str.strip()
    
    # Remove restaurants with zero rating (likely invalid)
    initial_count = len(df)
    df = df[df['Aggregate rating'] > 0].copy()
    removed = initial_count - len(df)
    if removed > 0:
        print(f"  ✓ Removed {removed} restaurants with invalid ratings")
    
    # Display data summary
    print("\n" + "="*70)
    print("DATA SUMMARY")
    print("="*70)
    print(f"Total restaurants: {len(df)}")
    print(f"Unique cuisines: {df['Cuisines'].nunique()}")
    print(f"Unique cities: {df['City'].nunique()}")
    print(f"Price range: {df['Price range'].min()} to {df['Price range'].max()}")
    print(f"Rating range: {df['Aggregate rating'].min():.1f} to {df['Aggregate rating'].max():.1f}")
    
    # Display top cuisines
    print("\nTop 10 Cuisines:")
    top_cuisines = df['Cuisines'].value_counts().head(10)
    for cuisine, count in top_cuisines.items():
        print(f"  {cuisine}: {count} restaurants")
    
    # Display top cities
    print("\nTop 10 Cities:")
    top_cities = df['City'].value_counts().head(10)
    for city, count in top_cities.items():
        print(f"  {city}: {count} restaurants")
    
    return df


def get_cuisine_list(df):
    """
    Get list of all unique cuisines
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    
    Returns:
    --------
    cuisines : list
        List of unique cuisines
    """
    # Split multi-cuisine entries (e.g., "Italian, Pizza")
    all_cuisines = set()
    
    for cuisines_str in df['Cuisines'].dropna():
        # Split by comma and add each cuisine
        cuisines = [c.strip() for c in str(cuisines_str).split(',')]
        all_cuisines.update(cuisines)
    
    return sorted(list(all_cuisines))


def get_city_list(df):
    """
    Get list of all unique cities
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    
    Returns:
    --------
    cities : list
        List of unique cities
    """
    return sorted(df['City'].unique().tolist())


def get_price_range_distribution(df):
    """
    Get distribution of restaurants by price range
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    
    Returns:
    --------
    distribution : dict
        Price range distribution
    """
    distribution = df['Price range'].value_counts().sort_index().to_dict()
    
    print("\nPrice Range Distribution:")
    for price_range, count in distribution.items():
        percentage = (count / len(df)) * 100
        print(f"  Price Range {price_range}: {count} restaurants ({percentage:.1f}%)")
    
    return distribution


def filter_by_delivery_options(df):
    """
    Get statistics on delivery and booking options
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    """
    print("\nService Options:")
    
    if 'Has Online delivery' in df.columns:
        delivery_count = (df['Has Online delivery'] == 'Yes').sum()
        delivery_pct = (delivery_count / len(df)) * 100
        print(f"  Online Delivery: {delivery_count} restaurants ({delivery_pct:.1f}%)")
    
    if 'Has Table booking' in df.columns:
        booking_count = (df['Has Table booking'] == 'Yes').sum()
        booking_pct = (booking_count / len(df)) * 100
        print(f"  Table Booking: {booking_count} restaurants ({booking_pct:.1f}%)")


def get_rating_statistics(df):
    """
    Get rating statistics
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    """
    print("\nRating Statistics:")
    print(f"  Mean: {df['Aggregate rating'].mean():.2f}")
    print(f"  Median: {df['Aggregate rating'].median():.2f}")
    print(f"  Std Dev: {df['Aggregate rating'].std():.2f}")
    print(f"  Min: {df['Aggregate rating'].min():.1f}")
    print(f"  Max: {df['Aggregate rating'].max():.1f}")
    
    # Rating distribution
    print("\nRating Distribution:")
    bins = [0, 2, 3, 4, 5]
    labels = ['Poor (0-2)', 'Average (2-3)', 'Good (3-4)', 'Excellent (4-5)']
    df['Rating Category'] = pd.cut(df['Aggregate rating'], bins=bins, labels=labels)
    
    for category in labels:
        count = (df['Rating Category'] == category).sum()
        percentage = (count / len(df)) * 100
        print(f"  {category}: {count} ({percentage:.1f}%)")