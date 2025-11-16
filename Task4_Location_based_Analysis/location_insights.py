"""
LOCATION INSIGHTS MODULE
Task 4: Location-based Analysis

This module generates business insights and recommendations based on
the location analysis performed by LocationAnalyzer.
"""

import pandas as pd

def generate_insights_report(analyzer, df):
    """
    Generates a list of strategic insights and recommendations.
    
    Parameters:
    -----------
    analyzer : LocationAnalyzer instance
    df : pandas DataFrame (The processed data)
    
    Returns:
    --------
    insights : list of str
        Strategic insights and recommendations.
    """
    insights = []
    
    if df.empty or 'City' not in df.columns:
        return ["No valid location data available for insights generation."]

    # --- Retrieve Key Analysis Results ---
    city_counts = df['City'].value_counts().reset_index()
    city_counts.columns = ['City', 'Count']
    
    # Call methods to get dataframes
    rating_by_city = analyzer.calculate_rating_by_city()
    cuisine_diversity = analyzer.analyze_cuisine_diversity()
    cost_by_city = analyzer.calculate_cost_by_city()
    
    # --- INSIGHTS ---

    # 1. Market Concentration
    if not city_counts.empty:
        top_city = city_counts.iloc[0]['City']
        concentration = city_counts.iloc[0]['Count'] / len(df) * 100
        insights.append(f"Market Concentration: **{top_city}** dominates the market, holding **{concentration:.1f}%** of all restaurants. Future expansion should target saturation within this city first, or focus on diversified lower-concentration cities to reduce risk.")

    # 2. Quality vs. Volume
    if not rating_by_city.empty:
        highest_rated_city = rating_by_city.iloc[0]
        insights.append(f"Quality Hotspot: The city with the highest average rating is **{highest_rated_city['City']}** ({highest_rated_city['Average Rating']:.2f}). This location may represent a high-value, quality-sensitive consumer base, ideal for premium brand placement.")

    # 3. Cuisine Diversity Opportunity
    if not cuisine_diversity.empty:
        low_diversity_city = cuisine_diversity.iloc[-1]
        insights.append(f"Cuisine Gap: **{low_diversity_city['City']}** has the lowest cuisine diversity (only {low_diversity_city['Unique Cuisines']} unique cuisines). This presents a strong opportunity to introduce niche or specialty cuisines (e.g., Ethiopian, Peruvian) that are currently undersupplied.")

    # 4. Pricing Strategy
    if not cost_by_city.empty:
        highest_cost_city = cost_by_city.iloc[0]
        insights.append(f"Pricing Sensitivity: **{highest_cost_city['City']}** has the highest average cost for two ({highest_cost_city['Average Cost']:.0f} local currency), suggesting a wealthier or less price-sensitive consumer base. This is the optimal location for testing higher-tier pricing models.")

    # 5. Digital Adoption
    delivery_pct = df['Has Online delivery'].value_counts(normalize=True).get('Yes', 0) * 100
    insights.append(f"Digital Opportunity: Only **{delivery_pct:.1f}%** of all restaurants offer online delivery. Investing in a robust online ordering and delivery infrastructure is critical to capturing the remaining **{100 - delivery_pct:.1f}%** of the market.")
    
    # 6. Geographic Expansion
    clusters = analyzer.find_restaurant_clusters(k=3)
    if clusters:
        insights.append(f"Geographic Clustering: The data shows **{len(clusters)} primary geographic clusters**. New restaurant locations should be positioned near the fringe of these clusters to capture spillover demand without incurring direct head-to-head competition with established dense zones.")
        
    return insights