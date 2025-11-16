"""
FEATURE ANALYSIS MODULE
Task 1: Restaurant Rating Prediction

This module analyzes:
- Feature importance
- Feature weights
- Impact on predictions
"""

import numpy as np
import pandas as pd

def analyze_feature_importance(model, feature_names):
    """
    Analyze and display feature importance
    
    Parameters:
    -----------
    model : LinearRegressionModel
        Trained model
    feature_names : list
        Names of features
    """
    # Get feature weights (excluding bias)
    feature_weights = model.get_feature_weights()
    
    # Create importance dataframe
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Weight': feature_weights,
        'Absolute Weight': np.abs(feature_weights)
    })
    
    # Sort by absolute importance
    importance_df = importance_df.sort_values('Absolute Weight', ascending=False)
    
    print("\n" + "="*70)
    print("FEATURE IMPORTANCE ANALYSIS")
    print("="*70)
    
    print("\nFeature Weights (sorted by importance):")
    print("-" * 70)
    print(f"{'Rank':<6} {'Feature':<30} {'Weight':<12} {'Impact':<15}")
    print("-" * 70)
    
    for idx, (_, row) in enumerate(importance_df.iterrows(), 1):
        feature = row['Feature']
        weight = row['Weight']
        abs_weight = row['Absolute Weight']
        
        # Determine impact direction
        if weight > 0:
            impact = "Increases ↑"
        elif weight < 0:
            impact = "Decreases ↓"
        else:
            impact = "Neutral →"
        
        print(f"{idx:<6} {feature:<30} {weight:>10.4f}  {impact:<15}")
    
    print("-" * 70)
    
    # Key insights
    print("\n💡 KEY INSIGHTS:")
    print("-" * 70)
    
    top_feature = importance_df.iloc[0]
    print(f"• Most influential: {top_feature['Feature']}")
    print(f"  Weight: {top_feature['Weight']:.4f}")
    
    if top_feature['Weight'] > 0:
        print(f"  → Increases rating by {top_feature['Weight']:.4f} per unit increase")
    else:
        print(f"  → Decreases rating by {abs(top_feature['Weight']):.4f} per unit increase")
    
    # List top 3 features
    print(f"\n• Top 3 Most Important Features:")
    for idx, (_, row) in enumerate(importance_df.head(3).iterrows(), 1):
        print(f"  {idx}. {row['Feature']} (weight: {row['Weight']:.4f})")
    
    # Recommendations
    print("\n📋 RECOMMENDATIONS:")
    print("-" * 70)
    
    positive_features = importance_df[importance_df['Weight'] > 0.1].sort_values('Weight', ascending=False)
    if len(positive_features) > 0:
        print("• To increase ratings, focus on:")
        for _, row in positive_features.iterrows():
            print(f"  - {row['Feature']} (impact: +{row['Weight']:.4f})")
    
    negative_features = importance_df[importance_df['Weight'] < -0.05].sort_values('Weight')
    if len(negative_features) > 0:
        print("\n• Features that may lower ratings:")
        for _, row in negative_features.iterrows():
            print(f"  - {row['Feature']} (impact: {row['Weight']:.4f})")
    
    return importance_df


def interpret_weights(importance_df):
    """
    Provide business interpretations of feature weights
    
    Parameters:
    -----------
    importance_df : pandas DataFrame
        Feature importance dataframe
    """
    print("\n" + "="*70)
    print("BUSINESS INTERPRETATION")
    print("="*70)
    
    for _, row in importance_df.iterrows():
        feature = row['Feature']
        weight = row['Weight']
        
        print(f"\n{feature}:")
        
        if 'Online delivery' in feature or 'delivery' in feature.lower():
            if weight > 0:
                print(f"  → Restaurants with online delivery get {weight:.2f} higher ratings")
                print(f"  → Recommendation: Implement delivery services")
        
        elif 'Price' in feature or 'price' in feature.lower():
            if weight > 0:
                print(f"  → Higher price range correlates with {weight:.2f} better ratings")
                print(f"  → Premium positioning may improve perception")
        
        elif 'Table booking' in feature or 'booking' in feature.lower():
            if weight < 0:
                print(f"  → Table booking shows {abs(weight):.2f} negative impact")
                print(f"  → May indicate casual dining preference")
            else:
                print(f"  → Table booking adds {weight:.2f} to ratings")
        
        elif 'Votes' in feature or 'votes' in feature.lower():
            if weight > 0:
                print(f"  → Each additional vote adds {weight:.4f} to rating")
                print(f"  → Popular restaurants tend to be rated higher")
        
        elif 'Cost' in feature or 'cost' in feature.lower():
            if abs(weight) < 0.001:
                print(f"  → Cost has minimal direct impact on ratings")
                print(f"  → Quality matters more than price")


def save_feature_importance(importance_df, filename='feature_importance.csv'):
    """
    Save feature importance to CSV
    
    Parameters:
    -----------
    importance_df : pandas DataFrame
        Feature importance dataframe
    filename : str
        Output filename
    """
    importance_df.to_csv(filename, index=False)
    print(f"\n✓ Feature importance saved to {filename}")


def calculate_feature_impact(model, feature_names, feature_index, change_amount=1):
    """
    Calculate impact of changing a specific feature
    
    Parameters:
    -----------
    model : LinearRegressionModel
        Trained model
    feature_names : list
        Names of features
    feature_index : int
        Index of feature to analyze
    change_amount : float
        Amount to change the feature by
    
    Returns:
    --------
    impact : float
        Expected change in rating
    """
    weights = model.get_feature_weights()
    impact = weights[feature_index] * change_amount
    
    print(f"\n📊 IMPACT ANALYSIS:")
    print(f"If {feature_names[feature_index]} increases by {change_amount}:")
    print(f"Rating will change by: {impact:+.4f} points")
    
    return impact