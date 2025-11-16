"""
LOCATION ANALYSIS MODULE
Task 4: Location-based Analysis

This module contains the LocationAnalyzer class for statistical analysis
of geographical restaurant data.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import warnings

# Suppress KMeans warnings for simplicity in the report
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

class LocationAnalyzer:
    """
    Analyzes restaurant data based on location features (city, coordinates, locality).
    """
    def __init__(self, df):
        self.df = df
        self.analysis_report = []

    def _log_analysis(self, title, data):
        """Internal helper to format and log analysis results."""
        self.analysis_report.append(f"\n--- {title} ---\n")
        self.analysis_report.append(data.to_string())
        print(data)

    def display_coordinate_statistics(self):
        """Displays statistics related to geographic coordinates."""
        coords = self.df[['Latitude', 'Longitude']].dropna()
        if len(coords) == 0:
            print("No valid coordinates available for statistics.")
            return

        print(f"Total restaurants with coordinates: {len(coords)}")
        print(f"Mean Latitude: {coords['Latitude'].mean():.4f}")
        print(f"Mean Longitude: {coords['Longitude'].mean():.4f}")
        print(f"Spread (Lat/Lon range): ({coords['Latitude'].max() - coords['Latitude'].min():.2f}°/{coords['Longitude'].max() - coords['Longitude'].min():.2f}°)")
    
    def analyze_by_city(self, top_n=10):
        """Analyzes restaurant concentration by city."""
        city_counts = self.df['City'].value_counts().reset_index()
        city_counts.columns = ['City', 'Restaurant Count']
        city_counts['City Concentration (%)'] = (city_counts['Restaurant Count'] / len(self.df) * 100).round(1)
        
        title = f"City Restaurant Concentration (Top {top_n})"
        self._log_analysis(title, city_counts.head(top_n))
        return city_counts

    def analyze_by_locality(self, top_n=10):
        """Analyzes restaurant concentration by locality."""
        locality_counts = self.df['Locality'].value_counts().reset_index()
        locality_counts.columns = ['Locality', 'Restaurant Count']
        
        title = f"Locality Restaurant Concentration (Top {top_n})"
        self._log_analysis(title, locality_counts.head(top_n))
        return locality_counts

    def calculate_rating_by_city(self, top_n=10):
        """
        Calculates average rating and count by city.
        """
        rating_stats = self.df.groupby('City').agg(
            {'Aggregate rating': ['mean', 'count']}
        )
        rating_stats.columns = ['Average Rating', 'Count']
        rating_stats = rating_stats.sort_values(by='Average Rating', ascending=False)
        
        # --- FIX: Reset index to make 'City' a column for visualization ---
        rating_stats = rating_stats.reset_index()
        # ------------------------------------------------------------------

        title = f"Average Rating by City (Top {top_n})"
        self._log_analysis(title, rating_stats.head(top_n).round(2))
        return rating_stats

    def calculate_cost_by_city(self, top_n=10):
        """Calculates average cost for two by city."""
        cost_stats = self.df.groupby('City')['Average Cost for two'].mean().reset_index()
        cost_stats.columns = ['City', 'Average Cost']
        cost_stats = cost_stats.sort_values(by='Average Cost', ascending=False)
        
        title = f"Average Cost for Two by City (Top {top_n})"
        self._log_analysis(title, cost_stats.head(top_n).round(0))
        return cost_stats

    def analyze_cuisine_diversity(self, top_n=10):
        """Analyzes unique cuisine count by city."""
        def count_unique_cuisines(series):
            cuisines = series.str.split(', ').explode().str.strip().dropna()
            return cuisines.nunique()

        diversity = self.df.groupby('City')['Cuisines'].apply(count_unique_cuisines).reset_index()
        diversity.columns = ['City', 'Unique Cuisines']
        diversity = diversity.sort_values(by='Unique Cuisines', ascending=False)
        
        title = f"Cuisine Diversity by City (Top {top_n})"
        self._log_analysis(title, diversity.head(top_n))
        return diversity

    def analyze_price_range_by_city(self, top_n=5):
        """Analyzes the dominant price range in top cities."""
        city_price_dist = self.df.groupby('City')['Price range'].value_counts(normalize=True).mul(100).rename('Percentage').reset_index()
        
        top_cities = self.df['City'].value_counts().head(top_n).index
        city_price_dist = city_price_dist[city_price_dist['City'].isin(top_cities)]
        
        # Get dominant price range for each of the top cities
        idx = city_price_dist.groupby(['City'])['Percentage'].transform(max) == city_price_dist['Percentage']
        dominant_price = city_price_dist[idx].sort_values(by=['City', 'Price range'])
        dominant_price.columns = ['City', 'Dominant Price Range', 'Percentage']
        
        title = f"Dominant Price Range in Top {top_n} Cities"
        self._log_analysis(title, dominant_price)
        return dominant_price

    def identify_patterns(self):
        """Identifies key location-based patterns."""
        patterns = []
        
        if self.df.empty or 'City' not in self.df.columns or 'Aggregate rating' not in self.df.columns:
            return ["Insufficient data to identify patterns."]

        # 1. High Concentration
        if not self.df['City'].value_counts().empty:
            top_city = self.df['City'].value_counts().index[0]
            top_city_count = self.df['City'].value_counts().iloc[0]
            concentration = top_city_count / len(self.df) * 100
            patterns.append(f"High Concentration: **{top_city}** accounts for {concentration:.1f}% of all restaurants, indicating a primary market focus.")
        
        # 2. Rating-Concentration (Inverse relationship)
        rating_stats = self.calculate_rating_by_city().set_index('City') 
        if not rating_stats.empty:
            high_rating_city = rating_stats['Average Rating'].idxmax()
            high_rating_score = rating_stats.loc[high_rating_city, 'Average Rating']
            
            if high_rating_city != top_city:
                patterns.append(f"Quality Anomaly: The city with the highest average rating (**{high_rating_city}**, Avg Rating: {high_rating_score:.2f}) is not the most concentrated market, suggesting high quality in niche/smaller cities.")
            else:
                 patterns.append(f"Quality Correlation: The most concentrated city (**{top_city}**) is also the highest-rated city, indicating strong market leadership in both volume and quality.")

        # 3. Delivery Gap
        delivery_pct = self.df['Has Online delivery'].value_counts(normalize=True).get('Yes', 0) * 100
        patterns.append(f"Service Gap: Only **{delivery_pct:.1f}%** of all restaurants offer online delivery, highlighting a major expansion opportunity.")
        
        self.analysis_report.append("\n--- Identified Patterns ---")
        self.analysis_report.extend(patterns)
        return patterns

    def find_restaurant_clusters(self, k=5):
        """Uses K-Means to find major geographic clusters of restaurants."""
        coords = self.df[['Latitude', 'Longitude']].dropna()
        
        if len(coords) < k:
            return []
        
        try:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
            coords['Cluster'] = kmeans.fit_predict(coords[['Latitude', 'Longitude']])
            
            cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=['Lat', 'Lon'])
            print(f"Found {k} major geographic clusters. Centers are:")
            print(cluster_centers.round(4))
            
            self.analysis_report.append("\n--- Geographic Cluster Centers (K-Means) ---")
            self.analysis_report.append(cluster_centers.round(4).to_string())
            
            return cluster_centers.to_dict('records')
        except Exception as e:
            print(f"Clustering failed: {e}")
            return []


    def save_analysis_results(self, filename):
        """Saves the entire analysis log to a text file."""
        import os
        output_dir = os.path.dirname(filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("TASK 4: LOCATION-BASED ANALYSIS REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Total Restaurants Analyzed: {len(self.df)}\n")
            f.write(f"Total Unique Cities: {self.df['City'].nunique() if 'City' in self.df.columns else 'N/A'}\n")
            f.write("="*70 + "\n")
            f.write("\n".join(self.analysis_report))