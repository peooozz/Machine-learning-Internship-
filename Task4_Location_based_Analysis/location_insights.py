"""
LOCATION INSIGHTS MODULE
Task 4: Location-based Analysis

This module generates:
- Business insights
- Pattern discoveries
- Recommendations
"""

import pandas as pd
import numpy as np

def generate_insights_report(analyzer, df):
    """
    Generate comprehensive insights from location analysis
    
    Parameters:
    -----------
    analyzer : LocationAnalyzer
        Analyzer instance with computed statistics
    df : pandas DataFrame
        Restaurant dataframe
    
    Returns:
    --------
    insights : list
        List of key insights
    """
    insights = []
    
    print("\n" + "="*70)
    print("LOCATION-BASED INSIGHTS & PATTERNS")
    print("="*70)
    
    # Insight 1: Market concentration
    top_city = df['City'].value_counts().index[0]
    top_city_count = df['City'].value_counts().iloc[0]
    concentration = top_city_count / len(df) * 100
    
    insight_1 = f"Market Concentration: {top_city} dominates with {concentration:.1f}% of all restaurants"
    insights.append(insight_1)
    print(f"\n💡 {insight_1}")
    
    # Insight 2: Rating-Location correlation
    city_ratings = df.groupby('City')['Aggregate rating'].mean().sort_values(ascending=False)
    best_city = city_ratings.index[0]
    best_rating = city_ratings.iloc[0]
    
    insight_2 = f"Quality Leader: {best_city} has highest average rating ({best_rating:.2f})"
    insights.append(insight_2)
    print(f"\n💡 {insight_2}")
    
    # Insight 3: Cost variation
    city_costs = df.groupby('City')['Average Cost for two'].mean()
    cost_std = city_costs.std()
    
    if cost_std > city_costs.mean() * 0.3:
        insight_3 = f"High cost variation across cities (std: {cost_std:.0f})"
    else:
        insight_3 = f"Relatively uniform pricing across cities"
    insights.append(insight_3)
    print(f"\n💡 {insight_3}")
    
    # Insight 4: Service availability
    delivery_cities = df[df['Has Online delivery'] == 'Yes'].groupby('City').size()
    if len(delivery_cities) > 0:
        top_delivery_city = delivery_cities.sort_values(ascending=False).index[0]
        delivery_count = delivery_cities.max()
        
        insight_4 = f"Delivery Hub: {top_delivery_city} leads with {delivery_count} delivery restaurants"
        insights.append(insight_4)
        print(f"\n💡 {insight_4}")
    
    # Insight 5: Geographic coverage
    if df['Latitude'].notna().any() and df['Longitude'].notna().any():
        lat_spread = df['Latitude'].max() - df['Latitude'].min()
        lon_spread = df['Longitude'].max() - df['Longitude'].min()
        
        if lat_spread > 10 or lon_spread > 10:
            coverage = "Wide geographic coverage across multiple regions"
        else:
            coverage = "Concentrated in a specific geographic area"
        
        insight_5 = f"Geographic Scope: {coverage}"
        insights.append(insight_5)
        print(f"\n💡 {insight_5}")
    
    # Insight 6: Cuisine diversity
    cuisine_diversity = df.groupby('City')['Cuisines'].nunique().sort_values(ascending=False)
    diverse_city = cuisine_diversity.index[0]
    cuisine_count = cuisine_diversity.iloc[0]
    
    insight_6 = f"Culinary Diversity: {diverse_city} offers {cuisine_count} different cuisine types"
    insights.append(insight_6)
    print(f"\n💡 {insight_6}")
    
    # Insight 7: Price positioning
    price_dist = df['Price range'].value_counts(normalize=True) * 100
    dominant_price = price_dist.index[0]
    
    price_labels = {1: 'Budget', 2: 'Mid-range', 3: 'Premium', 4: 'Luxury'}
    insight_7 = f"Market Positioning: {price_labels.get(dominant_price, 'Unknown')} segment dominates ({price_dist.iloc[0]:.1f}%)"
    insights.append(insight_7)
    print(f"\n💡 {insight_7}")
    
    return insights


def identify_growth_opportunities(df):
    """
    Identify potential growth opportunities based on location data
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    """
    print("\n" + "="*70)
    print("GROWTH OPPORTUNITIES")
    print("="*70)
    
    opportunities = []
    
    # Opportunity 1: Underserved high-rating cities
    city_stats = df.groupby('City').agg({
        'Restaurant ID': 'count',
        'Aggregate rating': 'mean'
    }).rename(columns={'Restaurant ID': 'count'})
    
    high_rating_low_count = city_stats[
        (city_stats['Aggregate rating'] > 3.5) & 
        (city_stats['count'] < 50)
    ].sort_values('Aggregate rating', ascending=False)
    
    if len(high_rating_low_count) > 0:
        print("\n🎯 Underserved High-Quality Markets:")
        for city in high_rating_low_count.head(3).index:
            count = high_rating_low_count.loc[city, 'count']
            rating = high_rating_low_count.loc[city, 'Aggregate rating']
            print(f"   • {city}: Only {count} restaurants but {rating:.2f} avg rating")
            opportunities.append(f"Expand in {city} - high quality, low competition")
    
    # Opportunity 2: Cities lacking delivery
    delivery_gap = df.groupby('City').agg({
        'Restaurant ID': 'count',
        'Has Online delivery': lambda x: (x == 'Yes').sum()
    })
    delivery_gap['delivery_pct'] = delivery_gap['Has Online delivery'] / delivery_gap['Restaurant ID'] * 100
    
    low_delivery = delivery_gap[
        (delivery_gap['Restaurant ID'] > 20) & 
        (delivery_gap['delivery_pct'] < 30)
    ].sort_values('delivery_pct')
    
    if len(low_delivery) > 0:
        print("\n🚚 Delivery Service Opportunities:")
        for city in low_delivery.head(3).index:
            pct = low_delivery.loc[city, 'delivery_pct']
            count = low_delivery.loc[city, 'Restaurant ID']
            print(f"   • {city}: Only {pct:.1f}% have delivery ({count} restaurants)")
            opportunities.append(f"Introduce delivery services in {city}")
    
    # Opportunity 3: Premium dining gaps
    premium_gap = df[df['Price range'] >= 3].groupby('City').size()
    all_restaurants = df.groupby('City').size()
    premium_pct = (premium_gap / all_restaurants * 100).sort_values()
    
    low_premium = premium_pct[premium_pct < 10]
    if len(low_premium) > 0:
        print("\n💎 Premium Dining Opportunities:")
        for city in low_premium.head(3).index:
            pct = low_premium[city]
            total = all_restaurants[city]
            print(f"   • {city}: Only {pct:.1f}% premium restaurants ({total} total)")
            opportunities.append(f"Open premium restaurants in {city}")
    
    return opportunities


def analyze_competitive_landscape(df):
    """
    Analyze competitive landscape by location
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    """
    print("\n" + "="*70)
    print("COMPETITIVE LANDSCAPE ANALYSIS")
    print("="*70)
    
    # Competition intensity by city
    city_competition = df.groupby('City').agg({
        'Restaurant ID': 'count',
        'Aggregate rating': ['mean', 'std'],
        'Votes': 'sum'
    })
    
    city_competition.columns = ['Count', 'Avg_Rating', 'Rating_Std', 'Total_Votes']
    city_competition['Competition_Index'] = (
        city_competition['Count'] * 
        city_competition['Avg_Rating'] / 
        (city_competition['Rating_Std'] + 0.1)
    )
    
    print("\nTop 10 Most Competitive Markets:")
    print("-"*70)
    print(f"{'City':<25} {'Restaurants':<12} {'Avg Rating':<12} {'Competition':<12}")
    print("-"*70)
    
    top_competitive = city_competition.nlargest(10, 'Competition_Index')
    for city, row in top_competitive.iterrows():
        print(f"{city:<25} {row['Count']:<12.0f} {row['Avg_Rating']:<12.2f} {row['Competition_Index']:<12.1f}")


def generate_recommendations(df):
    """
    Generate business recommendations based on location analysis
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    """
    print("\n" + "="*70)
    print("STRATEGIC RECOMMENDATIONS")
    print("="*70)
    
    recommendations = []
    
    # Recommendation 1: Geographic expansion
    top_cities = df['City'].value_counts().head(5).index.tolist()
    print("\n📍 Geographic Strategy:")
    print("   Focus on expanding in these proven markets:")
    for i, city in enumerate(top_cities[:3], 1):
        count = df[df['City'] == city].shape[0]
        print(f"   {i}. {city} - Already {count} restaurants, strong market presence")
        recommendations.append(f"Expand in {city}")
    
    # Recommendation 2: Service enhancement
    delivery_pct = (df['Has Online delivery'] == 'Yes').sum() / len(df) * 100
    booking_pct = (df['Has Table booking'] == 'Yes').sum() / len(df) * 100
    
    print("\n🔧 Service Enhancement:")
    if delivery_pct < 50:
        print(f"   • Increase delivery coverage (currently {delivery_pct:.1f}%)")
        recommendations.append("Expand delivery services")
    if booking_pct < 30:
        print(f"   • Implement booking systems (currently {booking_pct:.1f}%)")
        recommendations.append("Add booking capabilities")
    
    # Recommendation 3: Quality improvement
    low_rating_cities = df.groupby('City')['Aggregate rating'].mean().sort_values().head(3)
    if len(low_rating_cities) > 0:
        print("\n⭐ Quality Improvement:")
        print("   Target these cities for quality enhancement:")
        for city, rating in low_rating_cities.items():
            print(f"   • {city}: Current avg rating {rating:.2f}")
            recommendations.append(f"Improve quality in {city}")
    
    # Recommendation 4: Market positioning
    avg_cost = df.groupby('City')['Average Cost for two'].mean().mean()
    print("\n💰 Pricing Strategy:")
    print(f"   • Overall average cost: {avg_cost:.0f}")
    
    expensive_cities = df.groupby('City')['Average Cost for two'].mean().nlargest(3)
    print("   • Premium market opportunities in:")
    for city, cost in expensive_cities.items():
        print(f"     - {city} (avg cost: {cost:.0f})")
        recommendations.append(f"Target premium segment in {city}")
    
    return recommendations


def create_location_report(df, filename='location_insights_report.txt'):
    """
    Create a comprehensive location insights report
    
    Parameters:
    -----------
    df : pandas DataFrame
        Restaurant dataframe
    filename : str
        Output filename
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("COMPREHENSIVE LOCATION INSIGHTS REPORT\n")
        f.write("Task 4: Location-based Analysis\n")
        f.write("Cognifyz Technologies - Machine Learning Internship\n")
        f.write("="*70 + "\n\n")
        
        # Executive Summary
        f.write("EXECUTIVE SUMMARY\n")
        f.write("-"*70 + "\n")
        f.write(f"Total Restaurants Analyzed: {len(df)}\n")
        f.write(f"Geographic Coverage: {df['City'].nunique()} cities\n")
        f.write(f"Localities Covered: {df['Locality'].nunique()}\n")
        f.write(f"Average Rating: {df['Aggregate rating'].mean():.2f}/5.0\n")
        f.write(f"Average Cost: {df['Average Cost for two'].mean():.0f}\n\n")
        
        # Top Markets
        f.write("TOP MARKETS\n")
        f.write("-"*70 + "\n")
        top_cities = df['City'].value_counts().head(10)
        for i, (city, count) in enumerate(top_cities.items(), 1):
            pct = count / len(df) * 100
            f.write(f"{i:2d}. {city:<25} {count:>4d} restaurants ({pct:.1f}%)\n")
        
        f.write("\n")
        f.write("="*70 + "\n")
        f.write("End of Report\n")
        f.write("="*70 + "\n")
    
    print(f"\n✓ Comprehensive report saved to {filename}")