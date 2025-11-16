"""
LOCATION VISUALIZATION MODULE
Task 4: Location-based Analysis

This module contains:
- Map creation (using folium if available)
- Statistical charts (text-based)
- Visual representations
"""

import pandas as pd
import numpy as np
import os

# --- 1. INTERACTIVE MAP FUNCTIONS (Folium) ---

def create_distribution_map(df, filename='restaurant_map.html', sample_size=500):
    """
    Create an interactive map showing restaurant distribution
    """
    try:
        import folium
        from folium.plugins import MarkerCluster
    except ImportError:
        print("\n⚠ Folium not installed. Cannot create interactive map.")
        return False
    
    # Filter restaurants with valid coordinates and required data
    required_map_cols = ['Latitude', 'Longitude', 'Restaurant Name', 'Aggregate rating', 'Cuisines', 'Average Cost for two', 'Currency', 'Locality', 'City']
    df_with_coords = df[df[required_map_cols].notna().all(axis=1)].copy()
    
    if len(df_with_coords) == 0:
        print("✗ No restaurants with valid coordinates found to map.")
        return False
    
    # Sample if dataset is too large
    current_sample_size = min(sample_size, len(df_with_coords))
    if len(df_with_coords) > sample_size:
        df_map = df_with_coords.sample(n=current_sample_size, random_state=42)
    else:
        df_map = df_with_coords
        
    print(f"Creating map with {current_sample_size} restaurants...")
    
    center_lat = df_map['Latitude'].mean()
    center_lon = df_map['Longitude'].mean()
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6, 
        tiles='OpenStreetMap'
    )
    
    marker_cluster = MarkerCluster().add_to(m)
    
    for _, row in df_map.iterrows():
        cuisines_short = row['Cuisines'].split(',')[0].strip() + ('...' if len(row['Cuisines']) > 30 else '')
        
        popup_text = f"""
        <b>{row['Restaurant Name']}</b><br>
        Rating: {row['Aggregate rating']:.1f}/5.0<br>
        Cuisines: {cuisines_short}<br>
        Cost: {row['Average Cost for two']:.0f} {row['Currency']}<br>
        Location: {row['Locality']}, {row['City']}
        """
        
        rating = row['Aggregate rating']
        if rating >= 4.0:
            color = 'green'
        elif rating >= 3.0:
            color = 'blue'
        elif rating >= 2.0:
            color = 'orange'
        else:
            color = 'red'
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=color, icon='cutlery', prefix='fa')
        ).add_to(marker_cluster)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                 bottom: 50px; right: 50px; width: 200px; height: 140px; 
                 background-color: white; z-index:9999; font-size:14px;
                 border:2px solid grey; border-radius: 5px; padding: 10px">
    <b>Rating Legend</b><br>
    <i style="color:green">&#9679;</i> Excellent (4.0+)<br>
    <i style="color:blue">&#9679;</i> Good (3.0-4.0)<br>
    <i style="color:orange">&#9679;</i> Average (2.0-3.0)<br>
    <i style="color:red">&#9679;</i> Poor (&lt;2.0)
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    m.save(filename)
    print(f"✓ Interactive map saved: {filename}")
    
    return True

# --- 2. TEXT-BASED VISUALIZATIONS (For console output) ---

def plot_city_statistics(city_stats):
    """
    Display city statistics in text format (Count)
    """
    print("\n" + "="*70)
    print("CITY RESTAURANT COUNT DISTRIBUTION")
    print("="*70)
    
    if city_stats is None or len(city_stats) == 0:
        print("No city statistics available")
        return

    # Robustness Check
    if 'City' not in city_stats.columns and city_stats.index.name == 'City':
        city_stats = city_stats.reset_index()
        
    if 'City' not in city_stats.columns or 'Restaurant Count' not in city_stats.columns:
        print("⚠ Error: Input DataFrame for count visualization is missing 'City' or 'Restaurant Count' columns.")
        return
    
    print("\nRestaurant Count by City (Top 10):")
    print("-"*70)
    
    top_10 = city_stats.sort_values(by='Restaurant Count', ascending=False).head(10)
    max_count = top_10['Restaurant Count'].max()
    
    for _, row in top_10.iterrows():
        city = row['City']
        count = row['Restaurant Count']
        bar_length = int((count / max_count) * 50)
        bar = '█' * bar_length
        print(f"{city:<20} {bar} {count}")


def plot_rating_by_location(rating_stats):
    """
    Display rating statistics in text format (Average Rating)
    """
    print("\n" + "="*70)
    print("RATING DISTRIBUTION BY CITY")
    print("="*70)
    
    if rating_stats is None or len(rating_stats) == 0:
        print("No rating statistics available")
        return
        
    # Robustness Check
    if 'City' not in rating_stats.columns and rating_stats.index.name == 'City':
        rating_stats = rating_stats.reset_index()

    if 'City' not in rating_stats.columns or 'Average Rating' not in rating_stats.columns:
        print("⚠ Error: Input DataFrame for rating visualization is missing 'City' or 'Average Rating' columns.")
        return
    
    print("\nAverage Rating by City (Top 10 by Rating):")
    print("-"*70)
    
    top_10 = rating_stats.sort_values(by='Average Rating', ascending=False).head(10)
    
    for _, row in top_10.iterrows():
        city = row['City']
        rating = row['Average Rating']
        stars = '★' * int(rating)
        print(f"{city:<20} {stars:<5} {rating:.2f}/5.0")


def create_ascii_map(df, width=60, height=20):
    """
    Create a simple ASCII map of restaurant distribution
    """
    df_coords = df[df[['Latitude', 'Longitude']].notna().all(axis=1)]
    
    if len(df_coords) == 0:
        print("No coordinates available for mapping")
        return
    
    print("\n" + "="*70)
    print("ASCII DISTRIBUTION MAP")
    print("="*70)
    print("(Each symbol represents restaurant density)")
    
    # Get bounds
    min_lat, max_lat = df_coords['Latitude'].min(), df_coords['Latitude'].max()
    min_lon, max_lon = df_coords['Longitude'].min(), df_coords['Longitude'].max()
    
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    density_map = {}

    for _, row in df_coords.iterrows():
        lat = row['Latitude']
        lon = row['Longitude']
        
        y = height // 2
        if max_lat != min_lat:
            y = int((lat - min_lat) / (max_lat - min_lat) * (height - 1))
            y = height - 1 - y
        
        x = width // 2
        if max_lon != min_lon:
            x = int((lon - min_lon) / (max_lon - min_lon) * (width - 1))
        
        y = max(0, min(height - 1, y))
        x = max(0, min(width - 1, x))
        
        cell = (y, x)
        density_map[cell] = density_map.get(cell, 0) + 1

    # Map density counts to symbols
    for (y, x), count in density_map.items():
        if count == 1:
            grid[y][x] = '.'
        elif 2 <= count <= 5:
            grid[y][x] = '*'
        elif 6 <= count <= 15:
            grid[y][x] = '#'
        else:
            grid[y][x] = '@'

    # Print grid
    print("\n  " + "-" * width)
    for row in grid:
        print("  |" + ''.join(row) + "|")
    print("  " + "-" * width)
    print(f"\n  Legend: . = 1  * = 2-5  # = 6-15  @ = 16+ restaurants (Approximate density)")


def save_visualizations(df, city_stats, rating_stats, output_dir='./output'):
    """
    Save all key data and visualizations to files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"\n📊 SAVING VISUALIZATIONS TO: {output_dir}")
    print("-"*70)
    
    # 1. Save map
    map_created = create_distribution_map(df, f'{output_dir}/restaurant_map.html')
    
    # 2. Save city count statistics
    if city_stats is not None:
        if 'City' not in city_stats.columns and city_stats.index.name == 'City':
            city_stats = city_stats.reset_index()
        city_stats.to_csv(f'{output_dir}/city_statistics.csv', index=False)
        print(f"✓ City statistics saved to {output_dir}/city_statistics.csv")
    
    # 3. Save coordinate data
    if all(col in df.columns for col in ['Latitude', 'Longitude']):
        coord_data = df[df[['Latitude', 'Longitude']].notna().all(axis=1)][
            ['Restaurant Name', 'City', 'Latitude', 'Longitude', 'Aggregate rating']
        ]
        coord_data.to_csv(f'{output_dir}/restaurant_coordinates.csv', index=False)
        print(f"✓ Coordinates saved to {output_dir}/restaurant_coordinates.csv")
    
    return True


def display_geographic_summary(df):
    """
    Display a comprehensive geographic summary
    """
    print("\n" + "="*70)
    print("GEOGRAPHIC DISTRIBUTION SUMMARY")
    print("="*70)
    
    if 'Country Code' in df.columns:
        print("\nCountry Distribution (Top 10):")
        print("-"*70)
        country_counts = df['Country Code'].value_counts().head(10)
        for country, count in country_counts.items():
            percentage = count / len(df) * 100
            print(f"  Country {country}: {count} restaurants ({percentage:.1f}%)")
    
    if 'City' in df.columns:
        print("\nCity Concentration:")
        print("-"*70)
        city_counts = df['City'].value_counts()
        if not city_counts.empty:
            top_5_cities = city_counts.head(5).sum()
            concentration = top_5_cities / len(df) * 100
            print(f"  Top 5 cities ({', '.join(city_counts.head(5).index)}) contain: {concentration:.1f}% of all restaurants.")
    
    if df['Latitude'].notna().any() and df['Longitude'].notna().any():
        print("\nGeographic Spread:")
        print("-"*70)
        lat_range = df['Latitude'].max() - df['Latitude'].min()
        lon_range = df['Longitude'].max() - df['Longitude'].min()
        print(f"  Latitude range: {lat_range:.2f}°")
        print(f"  Longitude range: {lon_range:.2f}°")
    
    return True


def generate_location_visualizations(df, city_stats, rating_stats):
    """
    Orchestrates the creation and display of all location-based visualizations.
    """
    print("\n" + "#"*70)
    print("### LOCATION VISUALIZATION MODULE EXECUTION ###")
    print("#"*70)
    
    # 1. Display Summary Statistics (Text-based)
    display_geographic_summary(df)
    
    # 2. Display Charts (Text-based)
    plot_city_statistics(city_stats)
    plot_rating_by_location(rating_stats)
    
    # 3. Display ASCII Map
    create_ascii_map(df)
    
    # 4. Save Files (Interactive Map and CSVs)
    save_visualizations(df, city_stats, rating_stats)
    
    return True