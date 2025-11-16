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

def load_and_prepare_location_data(csv_file):
    """
    Load and preprocess restaurant location data
    
    Parameters:
    -----------
    csv_file : str
        Path to the CSV file
    
    Returns:
    --------
    df : pandas DataFrame
        Cleaned dataframe with location data
    """
    # Load the dataset
    df = pd.read_csv(csv_file)
    print(f"✓ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Check for required location columns
    required_columns = ['Latitude', 'Longitude', 'City', 'Locality']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"⚠ Warning: Missing columns: {missing_columns}")
    
    # Display initial location data summary
    print("\nInitial Location Data:")
    print(f"  Restaurants with Latitude: {df['Latitude'].notna().sum()}")
    print(f"  Restaurants with Longitude: {df['Longitude'].notna().sum()}")
    print(f"  Unique Cities: {df['City'].nunique()}")
    print(f"  Unique Localities: {df['Locality'].nunique()}")
    
    # Clean and validate coordinates
    df = clean_coordinates(df)
    
    # Clean text fields
    df = clean_location_text(df)
    
    # Add derived location features
    df = add_location_features(df)
    
    return df


def clean_coordinates(df):
    """
    Clean and validate latitude/longitude data
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    
    Returns:
    --------
    df : pandas DataFrame
        Cleaned dataframe
    """
    print("\nCleaning coordinate data...")
    
    initial_count = len(df)
    
    # Remove rows with missing coordinates (optional - depends on use case)
    # For analysis, we keep all rows but flag missing coordinates
    df['has_coordinates'] = df[['Latitude', 'Longitude']].notna().all(axis=1)
    
    valid_coords = df['has_coordinates'].sum()
    print(f"  Valid coordinates: {valid_coords} ({valid_coords/len(df)*100:.1f}%)")
    
    # Validate coordinate ranges
    # Latitude: -90 to 90, Longitude: -180 to 180
    if df['Latitude'].notna().any():
        invalid_lat = ((df['Latitude'] < -90) | (df['Latitude'] > 90)).sum()
        if invalid_lat > 0:
            print(f"  ⚠ Invalid latitudes found: {invalid_lat}")
            df.loc[(df['Latitude'] < -90) | (df['Latitude'] > 90), 'Latitude'] = np.nan
    
    if df['Longitude'].notna().any():
        invalid_lon = ((df['Longitude'] < -180) | (df['Longitude'] > 180)).sum()
        if invalid_lon > 0:
            print(f"  ⚠ Invalid longitudes found: {invalid_lon}")
            df.loc[(df['Longitude'] < -180) | (df['Longitude'] > 180), 'Longitude'] = np.nan
    
    print("  ✓ Coordinate validation complete")
    
    return df


def clean_location_text(df):
    """
    Clean city and locality text fields
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    
    Returns:
    --------
    df : pandas DataFrame
        Cleaned dataframe
    """
    print("\nCleaning location text fields...")
    
    # Clean city names
    if 'City' in df.columns:
        df['City'] = df['City'].str.strip()
        df['City_clean'] = df['City'].str.title()  # Proper case
        print(f"  ✓ Cleaned {df['City'].nunique()} unique cities")
    
    # Clean locality names
    if 'Locality' in df.columns:
        df['Locality'] = df['Locality'].str.strip()
        df['Locality_clean'] = df['Locality'].str.title()
        print(f"  ✓ Cleaned {df['Locality'].nunique()} unique localities")
    
    # Clean address if present
    if 'Address' in df.columns:
        df['Address'] = df['Address'].str.strip()
    
    return df


def add_location_features(df):
    """
    Add derived location features
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    
    Returns:
    --------
    df : pandas DataFrame
        Dataframe with added features
    """
    print("\nAdding derived location features...")
    
    # Create city-locality combination
    if 'City' in df.columns and 'Locality' in df.columns:
        df['City_Locality'] = df['City'] + ' - ' + df['Locality']
        print("  ✓ Created City-Locality identifier")
    
    # Count restaurants per city
    if 'City' in df.columns:
        city_counts = df['City'].value_counts()
        df['Restaurants_in_City'] = df['City'].map(city_counts)
        print("  ✓ Added restaurant count per city")
    
    # Count restaurants per locality
    if 'Locality' in df.columns:
        locality_counts = df['Locality'].value_counts()
        df['Restaurants_in_Locality'] = df['Locality'].map(locality_counts)
        print("  ✓ Added restaurant count per locality")
    
    # Categorize cities by restaurant density
    if 'Restaurants_in_City' in df.columns:
        df['City_Category'] = pd.cut(
            df['Restaurants_in_City'],
            bins=[0, 10, 50, 100, float('inf')],
            labels=['Small', 'Medium', 'Large', 'Metro']
        )
        print("  ✓ Categorized cities by density")
    
    return df


def get_coordinate_bounds(df):
    """
    Get the geographic bounds of the dataset
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    
    Returns:
    --------
    bounds : dict
        Dictionary with min/max coordinates
    """
    if df['Latitude'].notna().any() and df['Longitude'].notna().any():
        bounds = {
            'min_lat': df['Latitude'].min(),
            'max_lat': df['Latitude'].max(),
            'min_lon': df['Longitude'].min(),
            'max_lon': df['Longitude'].max(),
            'center_lat': df['Latitude'].mean(),
            'center_lon': df['Longitude'].mean()
        }
        
        print("\nGeographic Bounds:")
        print(f"  Latitude: {bounds['min_lat']:.4f} to {bounds['max_lat']:.4f}")
        print(f"  Longitude: {bounds['min_lon']:.4f} to {bounds['max_lon']:.4f}")
        print(f"  Center: ({bounds['center_lat']:.4f}, {bounds['center_lon']:.4f})")
        
        return bounds
    else:
        print("⚠ No valid coordinates found")
        return None


def validate_location_data(df):
    """
    Validate location data quality
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    """
    print("\n" + "="*70)
    print("LOCATION DATA QUALITY REPORT")
    print("="*70)
    
    total = len(df)
    
    # Coordinate completeness
    has_coords = df[['Latitude', 'Longitude']].notna().all(axis=1).sum()
    print(f"\nCoordinate Coverage:")
    print(f"  Complete: {has_coords} ({has_coords/total*100:.1f}%)")
    print(f"  Missing: {total - has_coords} ({(total-has_coords)/total*100:.1f}%)")
    
    # City information
    has_city = df['City'].notna().sum()
    print(f"\nCity Information:")
    print(f"  Available: {has_city} ({has_city/total*100:.1f}%)")
    print(f"  Unique Cities: {df['City'].nunique()}")
    
    # Locality information
    has_locality = df['Locality'].notna().sum()
    print(f"\nLocality Information:")
    print(f"  Available: {has_locality} ({has_locality/total*100:.1f}%)")
    print(f"  Unique Localities: {df['Locality'].nunique()}")
    
    # Overall quality score
    quality_score = (has_coords/total * 0.5 + has_city/total * 0.3 + has_locality/total * 0.2) * 100
    print(f"\nOverall Data Quality Score: {quality_score:.1f}/100")
    
    if quality_score >= 90:
        print("  Rating: EXCELLENT ✓✓✓")
    elif quality_score >= 70:
        print("  Rating: GOOD ✓✓")
    elif quality_score >= 50:
        print("  Rating: FAIR ✓")
    else:
        print("  Rating: NEEDS IMPROVEMENT ⚠")