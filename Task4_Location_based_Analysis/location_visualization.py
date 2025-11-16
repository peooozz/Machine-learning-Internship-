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

def create_distribution_map(df, filename='restaurant_map.html', sample_size=500):
    """
    Create an interactive map showing restaurant distribution
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe with coordinates
    filename : str
        Output HTML filename
    sample_size : int
        Number of restaurants to plot (for performance)
    
    Returns:
    --------
    success : bool
        True if map created successfully
    """
    try:
        import folium
        from folium.plugins import MarkerCluster
    except ImportError:
        print("⚠ Folium not installed. Cannot create interactive map.")
        print("Install with: pip install folium")
        return False
    
    # Filter restaurants with valid coordinates
    df_with_coords = df[df[['Latitude', 'Longitude']].notna().all(axis=1)].copy()
    
    if len(df_with_coords) == 0:
        print("✗ No restaurants with valid coordinates found")
        return False
    
    print(f"Creating map with {min(sample_size, len(df_with_coords))} restaurants...")
    
    # Sample if dataset is too large
    if len(df_with_coords) > sample_size:
        df_map = df_with_coords.sample(n=sample_size, random_state=42)
    else:
        df_map = df_with_coords
    
    # Calculate center point
    center_lat = df_map['Latitude'].mean()
    center_lon = df_map['Longitude'].mean()
    
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add markers
    for idx, row in df_map.iterrows():
        # Create popup with restaurant info
        popup_text = f"""
        <b>{row['Restaurant Name']}</b><br>
        Rating: {row['Aggregate rating']}/5.0<br>
        Cuisines: {row['Cuisines']}<br>
        Cost: {row['Average Cost for two']} {row['Currency']}<br>
        Location: {row['Locality']}, {row['City']}
        """
        
        # Color based on rating
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
    <i class="fa fa-circle" style="color:green"></i> Excellent (4.0+)<br>
    <i class="fa fa-circle" style="color:blue"></i> Good (3.0-4.0)<br>
    <i class="fa fa-circle" style="color:orange"></i> Average (2.0-3.0)<br>
    <i class="fa fa-circle" style="color:red"></i> Poor (<2.0)
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save map
    m.save(filename)
    print(f"✓ Interactive map saved: {filename}")
    print(f"  Open this file in a web browser to view the map")
    
    return True


def plot_city_statistics(city_stats):
    """
    Display city statistics in text format
    
    Parameters:
    -----------
    city_stats : pandas DataFrame
        City statistics
    """
    print("\n" + "="*70)
    print("CITY STATISTICS VISUALIZATION")
    print("="*70)
    
    if city_stats is None or len(city_stats) == 0:
        print("No city statistics available")
        return
    
    # Create text-based bar chart
    print("\nRestaurant Count by City (Top 10):")
    print("-"*70)
    
    max_count = city_stats['Restaurant Count'].max()
    
    for _, row in city_stats.head(10).iterrows():
        city = row['City']
        count = row['Restaurant Count']
        bar_length = int((count / max_count) * 50)
        bar = '█' * bar_length
        print(f"{city:<20} {bar} {count}")


def plot_rating_by_location(rating_stats):
    """
    Display rating statistics in text format
    
    Parameters:
    -----------
    rating_stats : pandas DataFrame
        Rating statistics by location
    """
    print("\n" + "="*70)
    print("RATING DISTRIBUTION BY CITY")
    print("="*70)
    
    if rating_stats is None or len(rating_stats) == 0:
        print("No rating statistics available")
        return
    
    print("\nAverage Rating by City (Top 10):")
    print("-"*70)
    
    for _, row in rating_stats.head(10).iterrows():
        city = row['City']
        rating = row['Average Rating']
        stars = '★' * int(rating)
        print(f"{city:<20} {stars} {rating:.2f}/5.0")


def create_heatmap_data(df):
    """
    Prepare data for heatmap visualization
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    
    Returns:
    --------
    heatmap_data : list
        List of [lat, lon, weight] for heatmap
    """
    df_coords = df[df[['Latitude', 'Longitude']].notna().all(axis=1)]
    
    if len(df_coords) == 0:
        return []
    
    # Create heatmap data (lat, lon, weight)
    heatmap_data = []
    for _, row in df_coords.iterrows():
        # Weight by rating or vote count
        weight = row['Votes'] if row['Votes'] > 0 else 1
        heatmap_data.append([row['Latitude'], row['Longitude'], weight])
    
    return heatmap_data


def save_visualizations(df, output_dir='.'):
    """
    Save all visualizations to files
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    output_dir : str
        Output directory for files
    """
    print("\n📊 SAVING VISUALIZATIONS")
    print("-"*70)
    
    # Save map
    map_created = create_distribution_map(df, f'{output_dir}/restaurant_map.html')
    
    # Save statistics to CSV
    city_counts = df['City'].value_counts().reset_index()
    city_counts.columns = ['City', 'Restaurant Count']
    city_counts.to_csv(f'{output_dir}/city_statistics.csv', index=False)
    print(f"✓ City statistics saved to {output_dir}/city_statistics.csv")
    
    locality_counts = df['Locality'].value_counts().reset_index()
    locality_counts.columns = ['Locality', 'Restaurant Count']
    locality_counts.to_csv(f'{output_dir}/locality_statistics.csv', index=False)
    print(f"✓ Locality statistics saved to {output_dir}/locality_statistics.csv")
    
    # Save coordinate data
    coord_data = df[df[['Latitude', 'Longitude']].notna().all(axis=1)][
        ['Restaurant Name', 'City', 'Latitude', 'Longitude', 'Aggregate rating']
    ]
    coord_data.to_csv(f'{output_dir}/restaurant_coordinates.csv', index=False)
    print(f"✓ Coordinates saved to {output_dir}/restaurant_coordinates.csv")
    
    print("\n✓ All visualizations saved successfully!")


def display_geographic_summary(df):
    """
    Display a comprehensive geographic summary
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    """
    print("\n" + "="*70)
    print("GEOGRAPHIC DISTRIBUTION SUMMARY")
    print("="*70)
    
    # Continental distribution (if country code available)
    if 'Country Code' in df.columns:
        print("\nCountry Distribution:")
        print("-"*70)
        country_counts = df['Country Code'].value_counts().head(10)
        for country, count in country_counts.items():
            percentage = count / len(df) * 100
            print(f"  Country {country}: {count} restaurants ({percentage:.1f}%)")
    
    # City concentration
    print("\nCity Concentration:")
    print("-"*70)
    top_5_cities = df['City'].value_counts().head(5).sum()
    concentration = top_5_cities / len(df) * 100
    print(f"  Top 5 cities contain: {concentration:.1f}% of all restaurants")
    
    # Geographic spread
    if df['Latitude'].notna().any() and df['Longitude'].notna().any():
        print("\nGeographic Spread:")
        print("-"*70)
        lat_range = df['Latitude'].max() - df['Latitude'].min()
        lon_range = df['Longitude'].max() - df['Longitude'].min()
        print(f"  Latitude range: {lat_range:.2f}°")
        print(f"  Longitude range: {lon_range:.2f}°")
        print(f"  Approximate area covered: {lat_range * lon_range:.2f} sq degrees")


def create_ascii_map(df, width=60, height=20):
    """
    Create a simple ASCII map of restaurant distribution
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    width : int
        Width of ASCII map
    height : int
        Height of ASCII map
    """
    df_coords = df[df[['Latitude', 'Longitude']].notna().all(axis=1)]
    
    if len(df_coords) == 0:
        print("No coordinates available for mapping")
        return
    
    print("\n" + "="*70)
    print("ASCII DISTRIBUTION MAP")
    print("="*70)
    print("(Each '*' represents restaurant density)")
    print()
    
    # Get bounds
    min_lat = df_coords['Latitude'].min()
    max_lat = df_coords['Latitude'].max()
    min_lon = df_coords['Longitude'].min()
    max_lon = df_coords['Longitude'].max()
    
    # Create grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Map restaurants to grid
    for _, row in df_coords.iterrows():
        lat = row['Latitude']
        lon = row['Longitude']
        
        # Normalize to grid coordinates
        if max_lat != min_lat:
            y = int((lat - min_lat) / (max_lat - min_lat) * (height - 1))
            y = height - 1 - y  # Flip y-axis
        else:
            y = height // 2
        
        if max_lon != min_lon:
            x = int((lon - min_lon) / (max_lon - min_lon) * (width - 1))
        else:
            x = width // 2
        
        # Ensure within bounds
        y = max(0, min(height - 1, y))
        x = max(0, min(width - 1, x))
        
        # Mark on grid
        if grid[y][x] == ' ':
            grid[y][x] = '.'
        elif grid[y][x] == '.':
            grid[y][x] = '*'
        elif grid[y][x] == '*':
            grid[y][x] = '#'
    
    # Print grid
    print("  " + "-" * width)
    for row in grid:
        print("  |" + ''.join(row) + "|")
    print("  " + "-" * width)
    print(f"\n  Legend: . = 1-2  * = 3-5  # = 6+ restaurants")