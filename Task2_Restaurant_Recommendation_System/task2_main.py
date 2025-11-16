"""
TASK 2: RESTAURANT RECOMMENDATION SYSTEM
Main Execution File

Author: [Your Name]
Internship: Machine Learning - Cognifyz Technologies
Date: November 2025

Description:
This system recommends restaurants based on user preferences using
content-based filtering approach.
"""

import warnings
warnings.filterwarnings('ignore')

# Import our custom modules
from recommendation_preprocessing import load_and_prepare_data
from recommendation_engine import RestaurantRecommender
from recommendation_utils import display_recommendations, test_recommendation_system

def main():
    """Main function to execute Task 2 pipeline"""
    
    print("="*70)
    print("TASK 2: RESTAURANT RECOMMENDATION SYSTEM")
    print("Cognifyz Technologies - Machine Learning Internship")
    print("="*70)
    
    # Step 1: Load and preprocess data
    print("\n[STEP 1] Loading and Preparing Data...")
    df = load_and_prepare_data('Dataset.csv')
    print(f"✓ Data prepared successfully!")
    print(f"  Total restaurants: {len(df)}")
    
    # Step 2: Create recommendation engine
    print("\n[STEP 2] Building Recommendation Engine...")
    recommender = RestaurantRecommender(df)
    recommender.prepare_features()
    print("✓ Recommendation engine ready!")
    
    # Step 3: Test with sample user preferences
    print("\n[STEP 3] Testing Recommendation System...")
    print("="*70)
    
    # Test Case 1: User prefers Indian cuisine, mid-price range
    print("\n🔍 TEST CASE 1: Indian Cuisine, Mid-Price Range")
    print("-"*70)
    user_preferences_1 = {
        'cuisines': 'Indian',
        'price_range': 2,
        'min_rating': 3.5,
        'has_online_delivery': 'Yes'
    }
    
    recommendations_1 = recommender.get_recommendations(
        user_preferences_1, 
        top_n=5
    )
    display_recommendations(recommendations_1, "Indian Cuisine Lover")
    
    # Test Case 2: User prefers Italian, high-end restaurants
    print("\n🔍 TEST CASE 2: Italian Cuisine, Premium Dining")
    print("-"*70)
    user_preferences_2 = {
        'cuisines': 'Italian',
        'price_range': 3,
        'min_rating': 4.0,
        'has_table_booking': 'Yes'
    }
    
    recommendations_2 = recommender.get_recommendations(
        user_preferences_2,
        top_n=5
    )
    display_recommendations(recommendations_2, "Italian Food Enthusiast")
    
    # Test Case 3: Budget-friendly with delivery
    print("\n🔍 TEST CASE 3: Budget-Friendly with Delivery")
    print("-"*70)
    user_preferences_3 = {
        'price_range': 1,
        'min_rating': 3.0,
        'has_online_delivery': 'Yes',
        'max_cost': 500
    }
    
    recommendations_3 = recommender.get_recommendations(
        user_preferences_3,
        top_n=5
    )
    display_recommendations(recommendations_3, "Budget-Conscious Diner")
    
    # Test Case 4: Highly-rated restaurants in a specific city
    print("\n🔍 TEST CASE 4: Top Restaurants in Makati City")
    print("-"*70)
    user_preferences_4 = {
        'city': 'Makati City',
        'min_rating': 4.0,
        'has_table_booking': 'Yes'
    }
    
    recommendations_4 = recommender.get_recommendations(
        user_preferences_4,
        top_n=5
    )
    display_recommendations(recommendations_4, "Makati Food Explorer")
    
    # Step 4: Interactive Recommendation (Optional)
    print("\n[STEP 4] Interactive Recommendation Demo")
    print("="*70)
    test_recommendation_system(recommender)
    
    # Summary
    print("\n" + "="*70)
    print("TASK 2 COMPLETED SUCCESSFULLY! 🎉")
    print("="*70)
    print("\n📊 System Statistics:")
    print(f"  Total restaurants in database: {len(df)}")
    print(f"  Available cuisines: {df['Cuisines'].nunique()}")
    print(f"  Cities covered: {df['City'].nunique()}")
    print(f"  Average rating: {df['Aggregate rating'].mean():.2f}")
    
    print("\n💡 Key Features:")
    print("  ✓ Content-based filtering")
    print("  ✓ Multi-criteria matching (cuisine, price, rating)")
    print("  ✓ Real-time recommendations")
    print("  ✓ Customizable preferences")
    
    print("\n🎯 Use Cases:")
    print("  • Food delivery apps")
    print("  • Restaurant discovery platforms")
    print("  • Travel and tourism websites")
    print("  • Personalized dining suggestions")
    print("="*70)

if __name__ == "__main__":
    main()