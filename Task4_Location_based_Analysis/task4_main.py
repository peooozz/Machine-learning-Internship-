"""
TASK 4: LOCATION-BASED ANALYSIS
Main Execution File (task4_main.py)

Description:
Performs geographical analysis of restaurants including distribution mapping,
city-wise statistics, and pattern identification.
"""

import warnings
import os

# Suppress warnings for a clean console output
warnings.filterwarnings('ignore')

# Import modules (assuming they are in the same directory or accessible via PYTHONPATH)
from location_preprocessing import load_and_prepare_location_data
from location_analysis import LocationAnalyzer
from location_visualization import generate_location_visualizations # Unified function
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
    
    if df.empty or len(df) == 0:
        print("\nFATAL ERROR: Could not load data or DataFrame is empty. Exiting.")
        return
        
    print(f"✓ Data loaded successfully!")
    print(f"  Total restaurants: {len(df)}")
    
    # Step 2: Create location analyzer
    print("\n[STEP 2] Initializing Location Analyzer...")
    analyzer = LocationAnalyzer(df)
    print("✓ Analyzer ready!")
    
    # Step 3-6: Run all core analyses
    print("\n[STEP 3-6] Running Core Location Analysis...")
    print("="*70)
    
    analyzer.display_coordinate_statistics()
    city_stats = analyzer.analyze_by_city(top_n=15)
    locality_stats = analyzer.analyze_by_locality(top_n=10)
    
    # These return DataFrames with 'City' as a column (due to the fix in analyzer)
    rating_by_city = analyzer.calculate_rating_by_city(top_n=10)
    cost_by_city = analyzer.calculate_cost_by_city(top_n=10)
    cuisine_by_city = analyzer.analyze_cuisine_diversity(top_n=10)
    price_by_city = analyzer.analyze_price_range_by_city(top_n=5)
    
    # Step 7: Identify patterns
    print("\n[STEP 7] Identifying Geographic Patterns...")
    print("="*70)
    patterns = analyzer.identify_patterns()
    
    print("\n🔍 Key Patterns Identified:")
    print("-"*70)
    for pattern in patterns[:5]:
        print(f"  • {pattern}")
    
    # Step 8: Geographic clustering analysis
    print("\n[STEP 8] Analyzing Geographic Clusters...")
    print("="*70)
    clusters = analyzer.find_restaurant_clusters()
    
    # Step 9: Create visualizations (Unified call)
    print("\n[STEP 9] Creating Visualizations...")
    print("="*70)
    generate_location_visualizations(df, city_stats, rating_by_city) 
    
    # Step 10: Generate comprehensive insights report
    print("\n[STEP 10] Generating Insights Report (Opportunities & Recommendations)...")
    print("="*70)
    insights = generate_insights_report(analyzer, df)
    
    # Step 11: Save all results
    print("\n[STEP 11] Saving Analysis Log and Visualizations...")
    print("="*70)
    # Ensure the output directory exists for the log file
    if not os.path.exists('./output'):
        os.makedirs('./output')
        
    analyzer.save_analysis_results('./output/location_analysis_results.txt') 
    print("✓ Detailed analysis log saved to ./output/location_analysis_results.txt")
    
    # --- Final Summary ---
    print("\n" + "="*70)
    print("TASK 4 COMPLETED SUCCESSFULLY! 🎉")
    print("="*70)
    
    print("\n📊 Analysis Summary:")
    print(f"  Total Restaurants Analyzed: {len(df)}")
    print(f"  Cities Covered: {df['City'].nunique() if 'City' in df.columns else 'N/A'}")
    print(f"  Geographic Clusters Found: {len(clusters)}")
    
    if not rating_by_city.empty:
        print("\n🏆 Top Performing Location (By Avg Rating):")
        top_city = rating_by_city.iloc[0]
        print(f"  City: {top_city['City']}")
        print(f"  Average Rating: {top_city['Average Rating']:.2f}")

    if not cuisine_by_city.empty:
        print("\n🍽️ Most Diverse City:")
        top_diverse = cuisine_by_city.iloc[0]
        print(f"  City: {top_diverse['City']}")
        print(f"  Unique Cuisines: {top_diverse['Unique Cuisines']}")
    
    print("\n💡 Key Insights & Recommendations (Top 5):")
    for i, insight in enumerate(insights[:5], 1):
        print(f"  {i}. {insight}")
    
    print("\n📁 Output Files Generated:")
    print("  • ./output/location_analysis_results.txt - Detailed analysis log")
    print("  • ./output/restaurant_map.html - Interactive map (if folium was installed)")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()