"""
RECOMMENDATION ENGINE MODULE
Task 2: Restaurant Recommendation System

This module implements:
- Content-based filtering
- Multi-criteria recommendation
- Similarity scoring
"""

import pandas as pd
import numpy as np

class RestaurantRecommender:
    """
    Content-based restaurant recommendation system
    
    Recommends restaurants based on user preferences:
    - Cuisine type
    - Price range
    - Rating threshold
    - Location
    - Delivery/booking options
    """
    
    def __init__(self, dataframe):
        """
        Initialize recommender with restaurant data
        
        Parameters:
        -----------
        dataframe : pandas DataFrame
            Restaurant data
        """
        self.df = dataframe.copy()
        self.features_prepared = False
        
    def prepare_features(self):
        """
        Prepare features for recommendation
        """
        # Create lowercase versions for matching
        self.df['Cuisines_lower'] = self.df['Cuisines'].str.lower()
        self.df['City_lower'] = self.df['City'].str.lower()
        
        # Create feature for sorting
        self.df['popularity_score'] = self.df['Votes'] * self.df['Aggregate rating']
        
        self.features_prepared = True
        print("✓ Features prepared for recommendation")
        
    def get_recommendations(self, user_preferences, top_n=10):
        """
        Get restaurant recommendations based on user preferences
        
        Parameters:
        -----------
        user_preferences : dict
            Dictionary containing:
            - 'cuisines' (str, optional): Preferred cuisine
            - 'price_range' (int, optional): Price range (1-4)
            - 'min_rating' (float, optional): Minimum rating
            - 'city' (str, optional): Preferred city
            - 'has_online_delivery' (str, optional): 'Yes'/'No'
            - 'has_table_booking' (str, optional): 'Yes'/'No'
            - 'max_cost' (float, optional): Maximum cost for two
        top_n : int
            Number of recommendations to return
            
        Returns:
        --------
        recommendations : pandas DataFrame
            Top N recommended restaurants
        """
        if not self.features_prepared:
            self.prepare_features()
        
        # Start with all restaurants
        filtered_df = self.df.copy()
        
        # Apply filters based on preferences
        filters_applied = []
        
        # Filter by cuisine
        if 'cuisines' in user_preferences and user_preferences['cuisines']:
            cuisine = user_preferences['cuisines'].lower()
            filtered_df = filtered_df[
                filtered_df['Cuisines_lower'].str.contains(cuisine, na=False)
            ]
            filters_applied.append(f"Cuisine: {user_preferences['cuisines']}")
        
        # Filter by price range
        if 'price_range' in user_preferences:
            price = user_preferences['price_range']
            # Allow ±1 price range for flexibility
            filtered_df = filtered_df[
                (filtered_df['Price range'] >= price - 1) & 
                (filtered_df['Price range'] <= price + 1)
            ]
            filters_applied.append(f"Price Range: {price}")
        
        # Filter by minimum rating
        if 'min_rating' in user_preferences:
            min_rating = user_preferences['min_rating']
            filtered_df = filtered_df[
                filtered_df['Aggregate rating'] >= min_rating
            ]
            filters_applied.append(f"Min Rating: {min_rating}")
        
        # Filter by city
        if 'city' in user_preferences and user_preferences['city']:
            city = user_preferences['city'].lower()
            filtered_df = filtered_df[
                filtered_df['City_lower'].str.contains(city, na=False)
            ]
            filters_applied.append(f"City: {user_preferences['city']}")
        
        # Filter by online delivery
        if 'has_online_delivery' in user_preferences:
            delivery = user_preferences['has_online_delivery']
            filtered_df = filtered_df[
                filtered_df['Has Online delivery'] == delivery
            ]
            filters_applied.append(f"Online Delivery: {delivery}")
        
        # Filter by table booking
        if 'has_table_booking' in user_preferences:
            booking = user_preferences['has_table_booking']
            filtered_df = filtered_df[
                filtered_df['Has Table booking'] == booking
            ]
            filters_applied.append(f"Table Booking: {booking}")
        
        # Filter by maximum cost
        if 'max_cost' in user_preferences:
            max_cost = user_preferences['max_cost']
            filtered_df = filtered_df[
                filtered_df['Average Cost for two'] <= max_cost
            ]
            filters_applied.append(f"Max Cost: {max_cost}")
        
        # Sort by rating and popularity
        filtered_df = filtered_df.sort_values(
            by=['Aggregate rating', 'popularity_score', 'Votes'],
            ascending=[False, False, False]
        )
        
        # Get top N recommendations
        recommendations = filtered_df.head(top_n)
        
        # Add metadata
        recommendations = recommendations.copy()
        recommendations['match_score'] = self._calculate_match_score(
            recommendations, 
            user_preferences
        )
        
        print(f"\n✓ Found {len(filtered_df)} matching restaurants")
        print(f"  Filters applied: {', '.join(filters_applied) if filters_applied else 'None'}")
        print(f"  Returning top {min(top_n, len(recommendations))} recommendations")
        
        return recommendations
    
    def _calculate_match_score(self, restaurants, preferences):
        """
        Calculate match score for each restaurant
        
        Parameters:
        -----------
        restaurants : pandas DataFrame
            Filtered restaurants
        preferences : dict
            User preferences
            
        Returns:
        --------
        scores : numpy array
            Match scores (0-100)
        """
        scores = np.zeros(len(restaurants))
        
        # Rating contributes 40%
        max_rating = 5.0
        scores += (restaurants['Aggregate rating'].values / max_rating) * 40
        
        # Votes/popularity contributes 30%
        max_votes = restaurants['Votes'].max() if len(restaurants) > 0 else 1
        if max_votes > 0:
            scores += (restaurants['Votes'].values / max_votes) * 30
        
        # Exact price match contributes 20%
        if 'price_range' in preferences:
            price_match = (restaurants['Price range'] == preferences['price_range']).astype(int)
            scores += price_match * 20
        
        # Service options contribute 10%
        if 'has_online_delivery' in preferences:
            delivery_match = (restaurants['Has Online delivery'] == preferences['has_online_delivery']).astype(int)
            scores += delivery_match * 10
        
        return scores
    
    def get_similar_restaurants(self, restaurant_name, top_n=5):
        """
        Find restaurants similar to a given restaurant
        
        Parameters:
        -----------
        restaurant_name : str
            Name of the reference restaurant
        top_n : int
            Number of similar restaurants to return
            
        Returns:
        --------
        similar : pandas DataFrame
            Similar restaurants
        """
        # Find the reference restaurant
        ref_restaurant = self.df[
            self.df['Restaurant Name'].str.contains(restaurant_name, case=False, na=False)
        ]
        
        if len(ref_restaurant) == 0:
            print(f"✗ Restaurant '{restaurant_name}' not found")
            return pd.DataFrame()
        
        ref_restaurant = ref_restaurant.iloc[0]
        
        # Create preferences based on this restaurant
        preferences = {
            'cuisines': ref_restaurant['Cuisines'],
            'price_range': ref_restaurant['Price range'],
            'min_rating': ref_restaurant['Aggregate rating'] - 0.5,
            'city': ref_restaurant['City']
        }
        
        # Get recommendations
        similar = self.get_recommendations(preferences, top_n=top_n+1)
        
        # Exclude the reference restaurant itself
        similar = similar[
            similar['Restaurant Name'] != ref_restaurant['Restaurant Name']
        ].head(top_n)
        
        print(f"\n✓ Found {len(similar)} restaurants similar to '{restaurant_name}'")
        
        return similar
    
    def get_top_rated_by_cuisine(self, cuisine, top_n=10):
        """
        Get top-rated restaurants for a specific cuisine
        
        Parameters:
        -----------
        cuisine : str
            Cuisine type
        top_n : int
            Number of restaurants to return
            
        Returns:
        --------
        top_restaurants : pandas DataFrame
            Top-rated restaurants
        """
        preferences = {
            'cuisines': cuisine,
            'min_rating': 3.5
        }
        
        return self.get_recommendations(preferences, top_n=top_n)
    
    def get_budget_friendly(self, max_cost=500, top_n=10):
        """
        Get budget-friendly restaurant recommendations
        
        Parameters:
        -----------
        max_cost : float
            Maximum cost for two people
        top_n : int
            Number of recommendations
            
        Returns:
        --------
        budget_restaurants : pandas DataFrame
            Budget-friendly restaurants
        """
        preferences = {
            'max_cost': max_cost,
            'min_rating': 3.0,
            'price_range': 1
        }
        
        return self.get_recommendations(preferences, top_n=top_n)
    
    def get_premium_dining(self, top_n=10):
        """
        Get premium/fine dining recommendations
        
        Parameters:
        -----------
        top_n : int
            Number of recommendations
            
        Returns:
        --------
        premium_restaurants : pandas DataFrame
            Premium restaurants
        """
        preferences = {
            'price_range': 4,
            'min_rating': 4.0,
            'has_table_booking': 'Yes'
        }
        
        return self.get_recommendations(preferences, top_n=top_n)