"""
LOCATION ANALYSIS MODULE
Task 4: Location-based Analysis

This module contains:
- Geographic analysis functions
- City and locality statistics
- Pattern identification
"""

import pandas as pd
import numpy as np

class LocationAnalyzer:
    """
    Comprehensive location-based analysis for restaurants
    """
    
    def __init__(self, dataframe):
        """
        Initialize analyzer with restaurant data
        
        Parameters:
        -----------
        dataframe : pandas DataFrame
            Restaurant data with location information
        """
        self.df = dataframe.copy()
        self.city_stats = None
        self.locality_stats = None
        
    def display_coordinate_statistics(self):
        """Display statistics about coordinates"""
        print("\n📍 COORDINATE STATISTICS")
        print("-"*70)
        
        if self.df['Latitude'].notna().any():
            print(f"Latitude Range:")
            print(f"  Min: {self.df['Latitude'].min():.4f}")
            print(f"  Max: {self.df['Latitude'].max():.4f}")
            print(f"  Mean: {self.df['Latitude'].mean():.4f}")
            print(f"  Median: {self.df['Latitude'].median():.4f}")
        
        if self.df['Longitude'].notna().any():
            print(f"\nLongitude Range:")
            print(f"  Min: {self.df['Longitude'].min():.4f}")
            print(f"  Max: {self.df['Longitude'].max():.4f}")
            print(f"  Mean: {self.df['Longitude'].mean():.4f}")
            print(f"  Median: {self.df['Longitude'].median():.4f}")
        
        # Coverage
        total = len(self.df)
        with_coords = self.df[['Latitude', 'Longitude']].notna().all(axis=1).sum()
        print(f"\nCoverage: {with_coords}/{total} ({with_coords/total*100:.1f}%)")
    
    def analyze_by_city(self, top_n=15):
        """
        Analyze restaurant concentration by city
        
        Parameters:
        -----------
        top_n : int
            Number of top cities to display
        
        Returns:
        --------
        city_stats : pandas DataFrame
            City-wise statistics
        """
        print("\n🏙️  RESTAURANT CONCENTRATION BY CITY")
        print("-"*70)
        
        city_counts = self.df['City'].value_counts().head(top_n)
        
        # Create detailed statistics
        city_data = []
        for city, count in city_counts.items():
            city_df = self.df[self.df['City'] == city]
            
            city_data.append({
                'City': city,
                'Restaurant Count': count,
                'Percentage': f"{count/len(self.df)*100:.2f}%",
                'Avg Rating': city_df['Aggregate rating'].mean(),
                'Avg Cost': city_df['Average Cost for two'].mean()
            })
        
        self.city_stats = pd.DataFrame(city_data)
        
        # Display results
        print(f"\nTop {top_n} Cities by Restaurant Count:")
        print("-"*70)
        for i, row in self.city_stats.iterrows():
            print(f"{i+1:2d}. {row['City']:<25} {row['Restaurant Count']:>4d} restaurants ({row['Percentage']})")
        
        return self.city_stats
    
    def analyze_by_locality(self, top_n=10):
        """
        Analyze restaurant concentration by locality
        
        Parameters:
        -----------
        top_n : int
            Number of top localities to display
        
        Returns:
        --------
        locality_stats : pandas DataFrame
            Locality-wise statistics
        """
        print("\n📌 RESTAURANT CONCENTRATION BY LOCALITY")
        print("-"*70)
        
        locality_counts = self.df['Locality'].value_counts().head(top_n)
        
        # Create detailed statistics
        locality_data = []
        for locality, count in locality_counts.items():
            locality_df = self.df[self.df['Locality'] == locality]
            city = locality_df['City'].iloc[0] if len(locality_df) > 0 else 'Unknown'
            
            locality_data.append({
                'Locality': locality,
                'City': city,
                'Restaurant Count': count,
                'Percentage': f"{count/len(self.df)*100:.2f}%"
            })
        
        self.locality_stats = pd.DataFrame(locality_data)
        
        # Display results
        print(f"\nTop {top_n} Localities by Restaurant Count:")
        print("-"*70)
        for i, row in self.locality_stats.iterrows():
            print(f"{i+1:2d}. {row['Locality']:<30} ({row['City']:<15}) {row['Restaurant Count']:>3d} ({row['Percentage']})")
        
        return self.locality_stats
    
    def calculate_rating_by_city(self, top_n=10):
        """
        Calculate average ratings by city
        
        Parameters:
        -----------
        top_n : int
            Number of cities to analyze
        
        Returns:
        --------
        rating_stats : pandas DataFrame
            Rating statistics by city
        """
        # Get top cities by count
        top_cities = self.df['City'].value_counts().head(top_n).index
        
        rating_data = []
        for city in top_cities:
            city_df = self.df[self.df['City'] == city]
            
            rating_data.append({
                'City': city,
                'Average Rating': city_df['Aggregate rating'].mean(),
                'Median Rating': city_df['Aggregate rating'].median(),
                'Min Rating': city_df['Aggregate rating'].min(),
                'Max Rating': city_df['Aggregate rating'].max(),
                'Count': len(city_df)
            })
        
        rating_stats = pd.DataFrame(rating_data)
        rating_stats = rating_stats.sort_values('Average Rating', ascending=False)
        
        # Display results
        print(f"{'City':<25} {'Avg Rating':<12} {'Median':<10} {'Count':<8}")
        print("-"*70)
        for _, row in rating_stats.iterrows():
            print(f"{row['City']:<25} {row['Average Rating']:<12.2f} {row['Median']:<10.1f} {row['Count']:<8d}")
        
        return rating_stats
    
    def calculate_cost_by_city(self, top_n=10):
        """
        Calculate average cost by city
        
        Parameters:
        -----------
        top_n : int
            Number of cities to analyze
        
        Returns:
        --------
        cost_stats : pandas DataFrame
            Cost statistics by city
        """
        # Get top cities by count
        top_cities = self.df['City'].value_counts().head(top_n).index
        
        cost_data = []
        for city in top_cities:
            city_df = self.df[self.df['City'] == city]
            
            cost_data.append({
                'City': city,
                'Average Cost': city_df['Average Cost for two'].mean(),
                'Median Cost': city_df['Average Cost for two'].median(),
                'Min Cost': city_df['Average Cost for two'].min(),
                'Max Cost': city_df['Average Cost for two'].max(),
                'Currency': city_df['Currency'].mode()[0] if len(city_df) > 0 else 'N/A'
            })
        
        cost_stats = pd.DataFrame(cost_data)
        cost_stats = cost_stats.sort_values('Average Cost', ascending=False)
        
        # Display results
        print(f"{'City':<25} {'Avg Cost':<12} {'Median':<10} {'Currency':<8}")
        print("-"*70)
        for _, row in cost_stats.iterrows():
            print(f"{row['City']:<25} {row['Average Cost']:<12.0f} {row['Median']:<10.0f} {row['Currency']:<8}")
        
        return cost_stats
    
    def analyze_cuisine_diversity(self, top_n=10):
        """
        Analyze cuisine diversity by city
        
        Parameters:
        -----------
        top_n : int
            Number of cities to analyze
        
        Returns:
        --------
        diversity_stats : pandas DataFrame
            Cuisine diversity statistics
        """
        # Get top cities by count
        top_cities = self.df['City'].value_counts().head(top_n).index
        
        diversity_data = []
        for city in top_cities:
            city_df = self.df[self.df['City'] == city]
            unique_cuisines = city_df['Cuisines'].nunique()
            
            diversity_data.append({
                'City': city,
                'Restaurant Count': len(city_df),
                'Unique Cuisines': unique_cuisines,
                'Diversity Score': unique_cuisines / len(city_df) * 100
            })
        
        diversity_stats = pd.DataFrame(diversity_data)
        diversity_stats = diversity_stats.sort_values('Unique Cuisines', ascending=False)
        
        # Display results
        print(f"{'City':<25} {'Restaurants':<12} {'Cuisines':<12} {'Diversity %':<12}")
        print("-"*70)
        for _, row in diversity_stats.iterrows():
            print(f"{row['City']:<25} {row['Restaurant Count']:<12d} {row['Unique Cuisines']:<12d} {row['Diversity Score']:<12.1f}")
        
        return diversity_stats
    
    def analyze_price_range_by_city(self, top_n=5):
        """
        Analyze price range distribution by city
        
        Parameters:
        -----------
        top_n : int
            Number of cities to analyze
        
        Returns:
        --------
        price_stats : pandas DataFrame
            Price range distribution
        """
        # Get top cities by count
        top_cities = self.df['City'].value_counts().head(top_n).index
        
        print(f"{'City':<25} {'Budget %':<12} {'Mid %':<12} {'High %':<12} {'Luxury %':<12}")
        print("-"*70)
        
        price_data = []
        for city in top_cities:
            city_df = self.df[self.df['City'] == city]
            total = len(city_df)
            
            price_dist = city_df['Price range'].value_counts()
            
            price_data.append({
                'City': city,
                'Budget (1)': price_dist.get(1, 0) / total * 100,
                'Mid (2)': price_dist.get(2, 0) / total * 100,
                'High (3)': price_dist.get(3, 0) / total * 100,
                'Luxury (4)': price_dist.get(4, 0) / total * 100
            })
            
            print(f"{city:<25} {price_data[-1]['Budget (1)']:<12.1f} "
                  f"{price_data[-1]['Mid (2)']:<12.1f} "
                  f"{price_data[-1]['High (3)']:<12.1f} "
                  f"{price_data[-1]['Luxury (4)']:<12.1f}")
        
        return pd.DataFrame(price_data)
    
    def find_restaurant_clusters(self):
        """
        Identify geographic clusters of restaurants
        
        Returns:
        --------
        clusters : list
            List of identified clusters
        """
        print("\n🔍 IDENTIFYING GEOGRAPHIC CLUSTERS")
        print("-"*70)
        
        clusters = []
        
        # Simple clustering by city + locality
        city_locality_groups = self.df.groupby(['City', 'Locality']).size()
        high_density = city_locality_groups[city_locality_groups >= 10].sort_values(ascending=False)
        
        print(f"\nHigh-Density Areas (10+ restaurants):")
        print("-"*70)
        for (city, locality), count in high_density.head(10).items():
            cluster_info = f"{city} - {locality}: {count} restaurants"
            clusters.append(cluster_info)
            print(f"  • {cluster_info}")
        
        return clusters
    
    def identify_patterns(self):
        """
        Identify interesting patterns in location data
        
        Returns:
        --------
        patterns : list
            List of identified patterns
        """
        patterns = []
        
        # Pattern 1: City with highest average rating
        city_ratings = self.df.groupby('City')['Aggregate rating'].mean().sort_values(ascending=False)
        if len(city_ratings) > 0:
            top_city = city_ratings.index[0]
            top_rating = city_ratings.iloc[0]
            patterns.append(f"Highest rated city: {top_city} (avg: {top_rating:.2f})")
        
        # Pattern 2: Most expensive city
        city_costs = self.df.groupby('City')['Average Cost for two'].mean().sort_values(ascending=False)
        if len(city_costs) > 0:
            exp_city = city_costs.index[0]
            exp_cost = city_costs.iloc[0]
            patterns.append(f"Most expensive city: {exp_city} (avg: {exp_cost:.0f})")
        
        # Pattern 3: City with most delivery options
        delivery_by_city = self.df[self.df['Has Online delivery'] == 'Yes'].groupby('City').size().sort_values(ascending=False)
        if len(delivery_by_city) > 0:
            del_city = delivery_by_city.index[0]
            del_count = delivery_by_city.iloc[0]
            patterns.append(f"Most delivery options: {del_city} ({del_count} restaurants)")
        
        # Pattern 4: Geographic spread
        if self.df['Latitude'].notna().any():
            lat_range = self.df['Latitude'].max() - self.df['Latitude'].min()
            lon_range = self.df['Longitude'].max() - self.df['Longitude'].min()
            patterns.append(f"Geographic spread: {lat_range:.2f}° latitude × {lon_range:.2f}° longitude")
        
        # Pattern 5: Concentration ratio
        top_city_count = self.df['City'].value_counts().iloc[0]
        concentration = top_city_count / len(self.df) * 100
        patterns.append(f"Top city concentration: {concentration:.1f}% of all restaurants")
        
        return patterns
    
    def save_analysis_results(self, filename='location_analysis_results.txt'):
        """
        Save all analysis results to a file
        
        Parameters:
        -----------
        filename : str
            Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("LOCATION-BASED ANALYSIS RESULTS\n")
            f.write("Task 4: Cognifyz Technologies ML Internship\n")
            f.write("="*70 + "\n\n")
            
            # Summary statistics
            f.write("SUMMARY STATISTICS\n")
            f.write("-"*70 + "\n")
            f.write(f"Total Restaurants: {len(self.df)}\n")
            f.write(f"Unique Cities: {self.df['City'].nunique()}\n")
            f.write(f"Unique Localities: {self.df['Locality'].nunique()}\n")
            f.write(f"With Coordinates: {self.df[['Latitude', 'Longitude']].notna().all(axis=1).sum()}\n\n")
            
            # Top cities
            if self.city_stats is not None:
                f.write("TOP CITIES\n")
                f.write("-"*70 + "\n")
                f.write(self.city_stats.to_string(index=False))
                f.write("\n\n")
            
            # Top localities
            if self.locality_stats is not None:
                f.write("TOP LOCALITIES\n")
                f.write("-"*70 + "\n")
                f.write(self.locality_stats.to_string(index=False))
                f.write("\n\n")
        
        print(f"✓ Analysis results saved to {filename}")