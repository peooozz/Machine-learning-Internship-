"""
LOCATION PREPROCESSING MODULE
Task 4: Location-based Analysis

This module handles:
- Loading restaurant location data
- Cleaning coordinate data
- Validating geographic information
"""

import pandas as pd
import numpy as np
import os
import sys

def load_and_prepare_location_data(csv_file='Dataset.csv'):
    """
    Load and preprocess restaurant location data, including standardization
    for compatibility with the Analyzer module.
    
    Parameters:
    -----------
    csv_file : str
        Path to the CSV file (defaults to 'Dataset.csv').
    
    Returns:
    --------
    df : pandas DataFrame
        Cleaned dataframe with location data and standardized column names.
    """
    try:
        # Load the dataset, trying common encodings
        try:
            df = pd.read_csv(csv_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, encoding='latin-1')
            
        print(f"✓ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    except FileNotFoundError:
        print(f"FATAL ERROR: Data file '{csv_file}' not found.")
        return pd.DataFrame() 
    
    # 1. Column Standardization (CRITICAL FIX FOR KEYERROR)
    
    # Clean up column names to lowercase/snake_case for consistent internal use
    df.columns = df.columns.str.replace(' ', '_').str.replace('[()]', '', regex=True).str.lower()
    
    # Map the cleaned/raw names to the exact required internal names
    # This block must be accurate to your 'Dataset.csv' columns. 
    # Assuming 'city' and 'locality' are the results of the lowercase operation.
    required_rename = {
        'latitude': 'Latitude',
        'longitude': 'Longitude',
        'aggregate_rating': 'Aggregate rating',
        'average_cost_for_two': 'Average Cost for two',
        'price_range': 'Price range',
        'has_online_delivery': 'Has Online delivery',
        'currency': 'Currency',
        'cuisines': 'Cuisines',
        'restaurant_name': 'Restaurant Name',
        'country_code': 'Country Code',
        'votes': 'Votes',
        'city': 'City',          # <-- MAPPING TO REQUIRED NAME
        'locality': 'Locality',  # <-- MAPPING TO REQUIRED NAME
    }
    
    # Only rename columns that actually exist in the DataFrame
    rename_dict = {
        k: v for k, v in required_rename.items() if k in df.columns
    }
    df.rename(columns=rename_dict, inplace=True)
    
    # Drop duplicates early
    df.drop_duplicates(inplace=True)
    
    # Convert 'Aggregate rating' and 'Votes' to numeric
    for col in ['Aggregate rating', 'Votes', 'Average Cost for two']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 2. Coordinate Cleaning and Validation
    df = clean_coordinates(df)
    
    # 3. Text Cleaning
    df = clean_location_text(df)
    
    # 4. Final Validation Check and Fix for KeyError
    # Check if critical columns exist before dropping NA
    if 'City' not in df.columns or 'Locality' not in df.columns:
         print(f"FATAL ERROR: Missing critical columns. Found: {df.columns.tolist()}")
         return pd.DataFrame() # Return empty DataFrame to halt execution
         
    df.dropna(subset=['City', 'Locality'], inplace=True)
    
    # 5. Feature Engineering
    df = add_location_features(df)
    
    # Final Validation Report (for console output)
    validate_location_data(df)
    get_coordinate_bounds(df) 
    
    return df


def clean_coordinates(df):
    """Clean and validate latitude/longitude data."""
    print("\nCleaning coordinate data...")
    
    if 'Latitude' in df.columns and 'Longitude' in df.columns:
        # Convert to numeric, coercing errors to NaN
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        
        df['has_coordinates'] = df['Latitude'].notna() & df['Longitude'].notna()
        
        valid_coords = df['has_coordinates'].sum()
        print(f"  Valid coordinates: {valid_coords} ({valid_coords/len(df)*100:.1f}%)")
        
        # Validate coordinate ranges 
        invalid_lat = ((df['Latitude'] < -90) | (df['Latitude'] > 90)).sum()
        if invalid_lat > 0:
            df.loc[(df['Latitude'] < -90) | (df['Latitude'] > 90), 'Latitude'] = np.nan
        
        invalid_lon = ((df['Longitude'] < -180) | (df['Longitude'] > 180)).sum()
        if invalid_lon > 0:
            df.loc[(df['Longitude'] < -180) | (df['Longitude'] > 180), 'Longitude'] = np.nan
    
    print("  ✓ Coordinate validation complete")
    return df


def clean_location_text(df):
    """Clean city and locality text fields."""
    print("\nCleaning location text fields...")
    
    if 'City' in df.columns:
        df['City'] = df['City'].astype(str).str.strip()
        df['City_clean'] = df['City'].str.title()
        print(f"  ✓ Cleaned {df['City'].nunique()} unique cities")
    
    if 'Locality' in df.columns:
        df['Locality'] = df['Locality'].astype(str).str.strip()
        df['Locality_clean'] = df['Locality'].str.title()
        print(f"  ✓ Cleaned {df['Locality'].nunique()} unique localities")
    
    return df


def add_location_features(df):
    """Add derived location features."""
    print("\nAdding derived location features...")
    
    if 'City' in df.columns and 'Locality' in df.columns:
        df['City_Locality'] = df['City'] + ' - ' + df['Locality']
        
    if 'City' in df.columns:
        city_counts = df['City'].value_counts()
        df['Restaurants_in_City'] = df['City'].map(city_counts)
        df['City_Category'] = pd.cut(
            df['Restaurants_in_City'],
            bins=[0, 10, 50, 100, float('inf')],
            labels=['Small', 'Medium', 'Large', 'Metro'],
            right=False
        ).astype(str).replace('nan', 'Unknown')
    
    print("  ✓ Derived features added")
    return df


def get_coordinate_bounds(df):
    """Get the geographic bounds of the dataset."""
    if 'Latitude' in df.columns and 'Longitude' in df.columns and df['Latitude'].notna().any():
        bounds = {
            'min_lat': df['Latitude'].min(),
            'max_lat': df['Latitude'].max(),
            'min_lon': df['Longitude'].min(),
            'max_lon': df['Longitude'].max(),
        }
        
        print("\nGeographic Bounds:")
        print(f"  Latitude: {bounds['min_lat']:.4f} to {bounds['max_lat']:.4f}")
        print(f"  Longitude: {bounds['min_lon']:.4f} to {bounds['max_lon']:.4f}")
        
        return bounds
    else:
        print("⚠ No valid coordinates found for bounds calculation.")
        return None


def validate_location_data(df):
    """Validate location data quality and print a report."""
    print("\n" + "="*70)
    print("LOCATION DATA QUALITY REPORT")
    print("="*70)
    
    total = len(df)
    
    has_coords = df.get('has_coordinates', pd.Series([False] * total)).sum()
    print(f"\nCoordinate Coverage:")
    print(f"  Complete: {has_coords} ({has_coords/total*100:.1f}%)")
    
    has_city = df.get('City', pd.Series()).notna().sum()
    print(f"\nCity Information:")
    print(f"  Available: {has_city} ({has_city/total*100:.1f}%)")
    print(f"  Unique Cities: {df.get('City', pd.Series()).nunique()}")
    
    has_locality = df.get('Locality', pd.Series()).notna().sum()
    print(f"\nLocality Information:")
    print(f"  Available: {has_locality} ({has_locality/total*100:.1f}%)")
    
    quality_score = (has_coords/total * 0.5 + has_city/total * 0.3 + has_locality/total * 0.2) * 100
    print(f"\nOverall Data Quality Score: {quality_score:.1f}/100")
    
    if quality_score >= 90:
        print("  Rating: EXCELLENT ✓✓✓")
    else:
        print("  Rating: GOOD/FAIR/NEEDS IMPROVEMENT")