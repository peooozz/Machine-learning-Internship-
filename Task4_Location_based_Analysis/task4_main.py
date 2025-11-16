"""
TASK 4: LOCATION-BASED ANALYSIS
Main Execution File

Author: [Your Name]
Internship: Machine Learning - Cognifyz Technologies
Date: November 2025

Description:
Performs geographical analysis of restaurants including distribution mapping,
city-wise statistics, and pattern identification.
"""

import warnings
warnings.filterwarnings('ignore')

# Import our custom modules
from location_preprocessing import load_and_prepare_location_data
from location_analysis import LocationAnalyzer
from location_visualization import (
    create_distribution_map,
    plot_city_statistics,
    plot_rating_by_location,
    save_visualizations
)
from location_insights import generate_insights_report

def main():
    """Main function to execute Task 4 pipeline"""
    
    print("="*70)
    print("TASK 4: LOCATION-BASED ANALYSIS")
    print("Cognifyz Technologies - Machine Learning Internship")
    print("="*70)
    
    # Step 1: Load and preprocess data
    print("\n[STEP 1] Loading Location Data...")
    df = load_and_prepare_location_data('Dataset.csv')
    print(f"✓ Data loaded successfully!")
    print(f"  Total restaurants: {len(df)}")
    print(f"  Locations with coordinates: {df[['Latitude', 'Longitude']].notna().all(axis=1).sum()}")
    
    # Step 2: Create location analyzer
    print("\n[STEP 2] Initializing Location Analyzer...")
    analyzer = LocationAnalyzer(df)
    print("✓ Analyzer ready!")
    
    # Step 3: Explore latitude and longitude distribution
    print("\n[STEP 3] Exploring Geographic Distribution...")
    print("="*70)
    analyzer.display_coordinate_statistics()
    
    # Step 4: Analyze by city
    print("\n[STEP 4] Analyzing Restaurant Concentration by City...")
    print("="*70)
    city_stats = analyzer.analyze_by_city(top_n=15)
    
    # Step 5: Analyze by locality
    print("\n[STEP 5] Analyzing by Locality...")
    print("="*70)
    locality_stats = analyzer.analyze_by_locality(top_n=10)
    
    # Step 6: Calculate statistics by location
    print("\n[STEP 6] Calculating Location-based Statistics...")
    print("="*70)
    
    # Average ratings by city
    print("\n📊 Average Ratings by Top Cities:")
    print("-"*70)
    rating_by_city = analyzer.calculate_rating_by_city(top_n=10)
    
    # Average cost by city
    print("\n💰 Average Cost by Top Cities:")
    print("-"*70)
    cost_by_city = analyzer.calculate_cost_by_city(top_n=10)
    
    # Cuisine diversity by city
    print("\n🍽️  Cuisine Diversity by City:")
    print("-"*70)
    cuisine_by_city = analyzer.analyze_cuisine_diversity(top_n=10)
    
    # Price range distribution by city
    print("\n💵 Price Range Distribution by City:")
    print("-"*70)
    price_by_city = analyzer.analyze_price_range_by_city(top_n=5)
    
    # Step 7: Identify patterns and insights
    print("\n[STEP 7] Identifying Geographic Patterns...")
    print("="*70)
    patterns = analyzer.identify_patterns()
    
    # Display key patterns
    print("\n🔍 Key Patterns Identified:")
    print("-"*70)
    for pattern in patterns[:5]:
        print(f"  • {pattern}")
    
    # Step 8: Geographic clustering analysis
    print("\n[STEP 8] Analyzing Geographic Clusters...")
    print("="*70)
    clusters = analyzer.find_restaurant_clusters()
    
    # Step 9: Create visualizations
    print("\n[STEP 9] Creating Visualizations...")
    print("="*70)
    
    try:
        # Note: Map creation requires folium
        print("  Creating interactive map...")
        map_created = create_distribution_map(df, filename='restaurant_map.html')
        if map_created:
            print("  ✓ Interactive map saved: restaurant_map.html")
    except ImportError:
        print("  ⚠ Folium not installed. Skipping map creation.")
        print("  Install with: pip install folium")
    
    # Statistical plots (text-based for now)
    print("\n  Creating statistical visualizations...")
    plot_city_statistics(city_stats)
    plot_rating_by_location(rating_by_city)
    
    # Step 10: Generate comprehensive insights report
    print("\n[STEP 10] Generating Insights Report...")
    print("="*70)
    insights = generate_insights_report(analyzer, df)
    
    # Save all results
    print("\n[STEP 11] Saving Results...")
    print("="*70)
    analyzer.save_analysis_results('location_analysis_results.txt')
    print("✓ Results saved to location_analysis_results.txt")
    
    # Summary
    print("\n" + "="*70)
    print("TASK 4 COMPLETED SUCCESSFULLY! 🎉")
    print("="*70)
    
    print("\n📊 Analysis Summary:")
    print(f"  Total Restaurants Analyzed: {len(df)}")
    print(f"  Cities Covered: {df['City'].nunique()}")
    print(f"  Localities Covered: {df['Locality'].nunique()}")
    print(f"  Geographic Clusters Found: {len(clusters)}")
    
    print("\n🏆 Top Performing Location:")
    top_city = rating_by_city.iloc[0]
    print(f"  City: {top_city['City']}")
    print(f"  Average Rating: {top_city['Average Rating']:.2f}")
    print(f"  Number of Restaurants: {top_city['Count']}")
    
    print("\n🍽️  Most Diverse City:")
    top_diverse = cuisine_by_city.iloc[0]
    print(f"  City: {top_diverse['City']}")
    print(f"  Unique Cuisines: {top_diverse['Unique Cuisines']}")
    
    print("\n💡 Key Insights:")
    for i, insight in enumerate(insights[:5], 1):
        print(f"  {i}. {insight}")
    
    print("\n📁 Output Files Generated:")
    print("  • location_analysis_results.txt - Detailed analysis")
    print("  • restaurant_map.html - Interactive map (if folium installed)")
    
    print("\n" + "="*70)
    print("Thank you for using the Location Analysis System!")
    print("="*70)

if __name__ == "__main__":
    main()