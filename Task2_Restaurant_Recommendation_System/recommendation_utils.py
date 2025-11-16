"""
RECOMMENDATION UTILITIES MODULE
Task 2: Restaurant Recommendation System

This module contains:
- Display functions for recommendations
- Testing and validation utilities
- Result formatting
"""

import pandas as pd
import numpy as np

def display_recommendations(recommendations, user_profile="User"):
    """
    Display recommendations in a formatted way
    
    Parameters:
    -----------
    recommendations : pandas DataFrame
        Recommended restaurants
    user_profile : str
        Description of user preferences
    """
    if len(recommendations) == 0:
        print(f"❌ No recommendations found for {user_profile}")
        print("Try adjusting your preferences (lower rating, different cuisine, etc.)")
        return
    
    print(f"\n🎯 Top {len(recommendations)} Recommendations for: {user_profile}")
    print("="*90)
    
    for idx, (_, restaurant) in enumerate(recommendations.iterrows(), 1):
        print(f"\n{idx}. {restaurant['Restaurant Name']}")
        print("-"*90)
        
        # Basic info
        print(f"   📍 Location: {restaurant['City']}, {restaurant['Locality']}")
        print(f"   🍽️  Cuisines: {restaurant['Cuisines']}")
        
        # Rating and popularity
        rating = restaurant['Aggregate rating']
        votes = restaurant['Votes']
        rating_text = restaurant['Rating text']
        print(f"   ⭐ Rating: {rating:.1f}/5.0 ({rating_text}) - {int(votes)} votes")
        
        # Cost and price range
        cost = restaurant['Average Cost for two']
        price_range = restaurant['Price range']
        price_symbols = '₹' * int(price_range)
        print(f"   💰 Cost for 2: {cost} {restaurant['Currency']} ({price_symbols})")
        
        # Services
        services = []
        if restaurant['Has Online delivery'] == 'Yes':
            services.append("🚚 Delivery")
        if restaurant['Has Table booking'] == 'Yes':
            services.append("📅 Booking")
        
        if services:
            print(f"   ✨ Services: {', '.join(services)}")
        
        # Match score if available
        if 'match_score' in restaurant:
            match = restaurant['match_score']
            print(f"   🎯 Match Score: {match:.1f}/100")
    
    print("\n" + "="*90)


def display_recommendation_summary(recommendations):
    """
    Display summary statistics of recommendations
    
    Parameters:
    -----------
    recommendations : pandas DataFrame
        Recommended restaurants
    """
    if len(recommendations) == 0:
        return
    
    print("\n📊 RECOMMENDATION SUMMARY")
    print("="*70)
    
    print(f"Total Recommendations: {len(recommendations)}")
    print(f"\nRating Statistics:")
    print(f"  Average Rating: {recommendations['Aggregate rating'].mean():.2f}")
    print(f"  Rating Range: {recommendations['Aggregate rating'].min():.1f} - {recommendations['Aggregate rating'].max():.1f}")
    
    print(f"\nCost Statistics:")
    print(f"  Average Cost: {recommendations['Average Cost for two'].mean():.0f}")
    print(f"  Cost Range: {recommendations['Average Cost for two'].min():.0f} - {recommendations['Average Cost for two'].max():.0f}")
    
    print(f"\nTop Cuisines:")
    top_cuisines = recommendations['Cuisines'].value_counts().head(3)
    for cuisine, count in top_cuisines.items():
        print(f"  - {cuisine}: {count} restaurants")
    
    print(f"\nTop Cities:")
    top_cities = recommendations['City'].value_counts().head(3)
    for city, count in top_cities.items():
        print(f"  - {city}: {count} restaurants")


def test_recommendation_system(recommender):
    """
    Run automated tests on the recommendation system
    
    Parameters:
    -----------
    recommender : RestaurantRecommender
        Recommendation engine instance
    """
    print("\n🧪 TESTING RECOMMENDATION SYSTEM")
    print("="*70)
    
    # Test 1: Cuisine-based recommendation
    print("\n[Test 1] Cuisine-Based Recommendation")
    print("-"*70)
    test_cuisines = ['Chinese', 'Mexican', 'Japanese']
    for cuisine in test_cuisines:
        recs = recommender.get_recommendations({'cuisines': cuisine}, top_n=3)
        print(f"  {cuisine}: {len(recs)} restaurants found")
    
    # Test 2: Price range recommendation
    print("\n[Test 2] Price Range Recommendation")
    print("-"*70)
    for price in [1, 2, 3, 4]:
        recs = recommender.get_recommendations({'price_range': price}, top_n=5)
        print(f"  Price Range {price}: {len(recs)} restaurants found")
    
    # Test 3: Rating threshold
    print("\n[Test 3] Rating Threshold")
    print("-"*70)
    for rating in [3.0, 3.5, 4.0, 4.5]:
        recs = recommender.get_recommendations({'min_rating': rating}, top_n=5)
        print(f"  Min Rating {rating}: {len(recs)} restaurants found")
    
    # Test 4: Combined filters
    print("\n[Test 4] Combined Filters")
    print("-"*70)
    combined_prefs = {
        'cuisines': 'Italian',
        'price_range': 3,
        'min_rating': 4.0,
        'has_online_delivery': 'Yes'
    }
    recs = recommender.get_recommendations(combined_prefs, top_n=5)
    print(f"  Italian + Price 3 + Rating 4.0 + Delivery: {len(recs)} restaurants")
    
    print("\n✓ All tests completed!")


def save_recommendations(recommendations, filename='recommendations.csv'):
    """
    Save recommendations to CSV file
    
    Parameters:
    -----------
    recommendations : pandas DataFrame
        Recommended restaurants
    filename : str
        Output filename
    """
    # Select relevant columns
    columns_to_save = [
        'Restaurant Name', 
        'City', 
        'Cuisines', 
        'Aggregate rating',
        'Rating text',
        'Votes',
        'Average Cost for two',
        'Price range',
        'Has Online delivery',
        'Has Table booking'
    ]
    
    # Add match score if available
    if 'match_score' in recommendations.columns:
        columns_to_save.append('match_score')
    
    # Save to CSV
    recommendations[columns_to_save].to_csv(filename, index=False)
    print(f"\n✓ Recommendations saved to {filename}")


def compare_recommendations(recommender, preferences_list, labels):
    """
    Compare recommendations for different user preferences
    
    Parameters:
    -----------
    recommender : RestaurantRecommender
        Recommendation engine
    preferences_list : list of dict
        List of user preferences
    labels : list of str
        Labels for each preference set
    """
    print("\n📊 COMPARING DIFFERENT USER PREFERENCES")
    print("="*70)
    
    results = []
    
    for prefs, label in zip(preferences_list, labels):
        recs = recommender.get_recommendations(prefs, top_n=5)
        
        results.append({
            'User Type': label,
            'Restaurants Found': len(recs),
            'Avg Rating': recs['Aggregate rating'].mean() if len(recs) > 0 else 0,
            'Avg Cost': recs['Average Cost for two'].mean() if len(recs) > 0 else 0,
            'Top Restaurant': recs.iloc[0]['Restaurant Name'] if len(recs) > 0 else 'None'
        })
    
    # Display comparison
    comparison_df = pd.DataFrame(results)
    print("\nComparison Results:")
    print(comparison_df.to_string(index=False))


def generate_user_report(recommendations, user_preferences):
    """
    Generate a detailed report for user
    
    Parameters:
    -----------
    recommendations : pandas DataFrame
        Recommended restaurants
    user_preferences : dict
        User preferences used for recommendation
    """
    print("\n" + "="*70)
    print("PERSONALIZED RESTAURANT RECOMMENDATION REPORT")
    print("="*70)
    
    print("\n📋 Your Preferences:")
    for key, value in user_preferences.items():
        key_display = key.replace('_', ' ').title()
        print(f"  • {key_display}: {value}")
    
    print(f"\n🔍 Search Results:")
    print(f"  Found {len(recommendations)} matching restaurants")
    
    if len(recommendations) > 0:
        print(f"\n⭐ Best Match:")
        best = recommendations.iloc[0]
        print(f"  Restaurant: {best['Restaurant Name']}")
        print(f"  Rating: {best['Aggregate rating']:.1f}/5.0")
        print(f"  Location: {best['City']}")
        print(f"  Cuisines: {best['Cuisines']}")
        
        print(f"\n💡 Recommendations at a Glance:")
        print(f"  Average Rating: {recommendations['Aggregate rating'].mean():.2f}")
        print(f"  Average Cost: {recommendations['Average Cost for two'].mean():.0f}")
        print(f"  Delivery Available: {(recommendations['Has Online delivery'] == 'Yes').sum()} restaurants")
        print(f"  Booking Available: {(recommendations['Has Table booking'] == 'Yes').sum()} restaurants")
    
    print("\n" + "="*70)


def interactive_recommendation(recommender):
    """
    Interactive recommendation session (for demo purposes)
    
    Parameters:
    -----------
    recommender : RestaurantRecommender
        Recommendation engine
    """
    print("\n🎯 INTERACTIVE RECOMMENDATION DEMO")
    print("="*70)
    print("Simulating user interaction...\n")
    
    # Sample interactive session
    scenarios = [
        {
            'description': "User wants Italian food for a date night",
            'preferences': {
                'cuisines': 'Italian',
                'price_range': 3,
                'min_rating': 4.0,
                'has_table_booking': 'Yes'
            }
        },
        {
            'description': "Student looking for cheap eats with delivery",
            'preferences': {
                'max_cost': 400,
                'has_online_delivery': 'Yes',
                'min_rating': 3.0
            }
        },
        {
            'description': "Tourist exploring local cuisine",
            'preferences': {
                'min_rating': 4.0,
                'has_table_booking': 'Yes'
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n💭 Scenario: {scenario['description']}")
        print("-"*70)
        recs = recommender.get_recommendations(scenario['preferences'], top_n=3)
        
        if len(recs) > 0:
            print(f"✓ Found {len(recs)} recommendations!")
            print(f"  Top suggestion: {recs.iloc[0]['Restaurant Name']}")
            print(f"  Rating: {recs.iloc[0]['Aggregate rating']:.1f}/5.0")
        else:
            print("✗ No matches found for these preferences")