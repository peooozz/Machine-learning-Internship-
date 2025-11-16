"""
MODEL TRAINING MODULE
Task 1: Restaurant Rating Prediction

This module contains:
- Linear Regression implementation
- Model training function
"""

import numpy as np

class LinearRegressionModel:
    """
    Simple Linear Regression implementation using Normal Equation
    
    The model learns weights that minimize prediction error.
    Formula: y = X @ weights
    Normal Equation: weights = (X^T X)^(-1) X^T y
    """
    
    def __init__(self):
        """Initialize the model"""
        self.weights = None
        self.feature_count = None
    
    def fit(self, X, y):
        """
        Train the model using training data
        
        Parameters:
        -----------
        X : numpy array
            Training features (n_samples, n_features)
        y : numpy array
            Training targets (n_samples,)
        """
        # Add bias term (column of ones) to X
        X_with_bias = np.c_[np.ones(X.shape[0]), X]
        
        # Normal Equation: w = (X^T X)^(-1) X^T y
        # Using pseudo-inverse for numerical stability
        try:
            XtX = X_with_bias.T @ X_with_bias
            Xty = X_with_bias.T @ y
            self.weights = np.linalg.pinv(XtX) @ Xty
            self.feature_count = X.shape[1]
            print(f"✓ Model trained with {self.feature_count} features")
        except Exception as e:
            print(f"✗ Error during training: {e}")
            raise
    
    def predict(self, X):
        """
        Make predictions on new data
        
        Parameters:
        -----------
        X : numpy array
            Features to predict (n_samples, n_features)
        
        Returns:
        --------
        predictions : numpy array
            Predicted values (n_samples,)
        """
        if self.weights is None:
            raise ValueError("Model not trained yet! Call fit() first.")
        
        # Add bias term
        X_with_bias = np.c_[np.ones(X.shape[0]), X]
        
        # Make predictions
        predictions = X_with_bias @ self.weights
        
        return predictions
    
    def get_weights(self):
        """
        Get the learned weights
        
        Returns:
        --------
        weights : numpy array
            Model weights (first element is bias)
        """
        if self.weights is None:
            raise ValueError("Model not trained yet!")
        return self.weights
    
    def get_feature_weights(self):
        """
        Get feature weights (excluding bias)
        
        Returns:
        --------
        feature_weights : numpy array
            Weights for each feature
        """
        if self.weights is None:
            raise ValueError("Model not trained yet!")
        return self.weights[1:]  # Exclude bias (first element)


def train_linear_regression(X_train, y_train):
    """
    Train a Linear Regression model
    
    Parameters:
    -----------
    X_train : numpy array
        Training features
    y_train : numpy array
        Training targets
    
    Returns:
    --------
    model : LinearRegressionModel
        Trained model
    """
    model = LinearRegressionModel()
    model.fit(X_train, y_train)
    
    # Display training information
    print(f"  Bias term: {model.weights[0]:.4f}")
    print(f"  Feature weights shape: {model.get_feature_weights().shape}")
    
    return model


def save_model_weights(model, filename='model_weights.txt'):
    """
    Save model weights to a text file
    
    Parameters:
    -----------
    model : LinearRegressionModel
        Trained model
    filename : str
        Output filename
    """
    weights = model.get_weights()
    np.savetxt(filename, weights)
    print(f"✓ Model weights saved to {filename}")


def load_model_weights(filename='model_weights.txt'):
    """
    Load model weights from a text file
    
    Parameters:
    -----------
    filename : str
        Input filename
    
    Returns:
    --------
    model : LinearRegressionModel
        Model with loaded weights
    """
    model = LinearRegressionModel()
    model.weights = np.loadtxt(filename)
    print(f"✓ Model weights loaded from {filename}")
    return model