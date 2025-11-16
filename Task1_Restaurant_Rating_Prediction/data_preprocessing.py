"""
DATA PREPROCESSING MODULE
Task 1: Restaurant Rating Prediction

This module handles:
- Loading CSV data
- Handling missing values
- Feature selection
- Encoding categorical variables
- Train-test splitting
"""

import pandas as pd
import numpy as np

def load_and_preprocess_data(csv_file, test_size=0.2, random_state=42):
    """
    Load and preprocess restaurant data
    
    Parameters:
    -----------
    csv_file : str
        Path to the CSV file
    test_size : float
        Proportion of data for testing (default: 0.2 = 20%)
    random_state : int
        Random seed for reproducibility
    
    Returns:
    --------
    X_train, X_test, y_train, y_test : numpy arrays
        Training and testing features and targets
    feature_names : list
        Names of the features used
    df : pandas DataFrame
        Original dataframe (for reference)
    """
    
    # Load the dataset
    df = pd.read_csv(csv_file)
    print(f"✓ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Display first few rows
    print("\nFirst 3 rows:")
    print(df.head(3))
    
    # Check missing values
    print("\nChecking missing values...")
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    
    if len(missing_cols) > 0:
        print("Missing values found:")
        for col, count in missing_cols.items():
            print(f"  {col}: {count} ({count/len(df)*100:.2f}%)")
    else:
        print("✓ No missing values!")
    
    # Handle missing values
    if 'Cuisines' in df.columns and df['Cuisines'].isnull().sum() > 0:
        df['Cuisines'] = df['Cuisines'].fillna('Unknown')
        print("✓ Filled missing Cuisines with 'Unknown'")
    
    # Define features
    numerical_features = ['Average Cost for two', 'Price range', 'Votes']
    categorical_features = ['Country Code', 'Has Table booking', 'Has Online delivery']
    target = 'Aggregate rating'
    
    print(f"\nFeatures selected:")
    print(f"  Numerical: {numerical_features}")
    print(f"  Categorical: {categorical_features}")
    print(f"  Target: {target}")
    
    # Handle missing values in numerical features
    for col in numerical_features:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"  Filled {col} with median: {median_val}")
    
    # Encode categorical variables (Yes/No to 1/0)
    for col in ['Has Table booking', 'Has Online delivery']:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0})
    
    # Handle any remaining NaN in categorical columns
    df[categorical_features] = df[categorical_features].fillna(0)
    
    # Create feature matrix X and target y
    all_features = numerical_features + categorical_features
    X = df[all_features].copy().values
    y = df[target].copy().values
    
    print(f"\n✓ Feature matrix created: {X.shape}")
    print(f"✓ Target vector created: {y.shape}")
    
    # Train-test split
    np.random.seed(random_state)
    indices = np.random.permutation(len(X))
    split_idx = int((1 - test_size) * len(X))
    
    train_indices = indices[:split_idx]
    test_indices = indices[split_idx:]
    
    X_train = X[train_indices]
    X_test = X[test_indices]
    y_train = y[train_indices]
    y_test = y[test_indices]
    
    print(f"\n✓ Data split complete:")
    print(f"  Training: {len(X_train)} samples ({(1-test_size)*100:.0f}%)")
    print(f"  Testing: {len(X_test)} samples ({test_size*100:.0f}%)")
    
    return X_train, X_test, y_train, y_test, all_features, df


def get_feature_statistics(X, feature_names):
    """
    Calculate and display statistics for features
    
    Parameters:
    -----------
    X : numpy array
        Feature matrix
    feature_names : list
        Names of features
    """
    df_stats = pd.DataFrame(X, columns=feature_names)
    print("\nFeature Statistics:")
    print(df_stats.describe())
    return df_stats.describe()