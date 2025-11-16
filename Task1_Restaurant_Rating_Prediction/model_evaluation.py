"""
MODEL EVALUATION MODULE
Task 1: Restaurant Rating Prediction

This module contains:
- Performance metrics calculation
- Results visualization
- Prediction comparison
"""

import numpy as np

def calculate_metrics(y_true, y_pred):
    """
    Calculate regression performance metrics
    
    Parameters:
    -----------
    y_true : numpy array
        Actual values
    y_pred : numpy array
        Predicted values
    
    Returns:
    --------
    metrics : dict
        Dictionary containing MSE, RMSE, MAE, and R²
    """
    # Mean Squared Error
    mse = np.mean((y_true - y_pred) ** 2)
    
    # Root Mean Squared Error
    rmse = np.sqrt(mse)
    
    # Mean Absolute Error
    mae = np.mean(np.abs(y_true - y_pred))
    
    # R-squared (Coefficient of Determination)
    ss_res = np.sum((y_true - y_pred) ** 2)  # Residual sum of squares
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)  # Total sum of squares
    r2 = 1 - (ss_res / ss_tot)
    
    metrics = {
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'r2': r2
    }
    
    return metrics


def evaluate_model(y_true, y_pred):
    """
    Evaluate model performance
    
    Parameters:
    -----------
    y_true : numpy array
        Actual ratings
    y_pred : numpy array
        Predicted ratings
    
    Returns:
    --------
    metrics : dict
        Performance metrics
    """
    metrics = calculate_metrics(y_true, y_pred)
    return metrics


def display_results(y_true, y_pred, metrics):
    """
    Display evaluation results in a formatted way
    
    Parameters:
    -----------
    y_true : numpy array
        Actual values
    y_pred : numpy array
        Predicted values
    metrics : dict
        Performance metrics
    """
    print("\n" + "="*70)
    print("MODEL EVALUATION RESULTS")
    print("="*70)
    
    # Display sample predictions
    print("\nSample Predictions vs Actual Ratings:")
    print("-" * 60)
    print(f"{'Actual':<12} {'Predicted':<12} {'Difference':<12} {'Error %':<12}")
    print("-" * 60)
    
    for i in range(min(10, len(y_true))):
        actual = y_true[i]
        predicted = y_pred[i]
        diff = abs(actual - predicted)
        error_pct = (diff / actual * 100) if actual != 0 else 0
        print(f"{actual:<12.2f} {predicted:<12.2f} {diff:<12.2f} {error_pct:<12.1f}%")
    
    # Display metrics
    print("\n" + "="*70)
    print("PERFORMANCE METRICS")
    print("="*70)
    print(f"Mean Squared Error (MSE):        {metrics['mse']:.4f}")
    print(f"Root Mean Squared Error (RMSE):  {metrics['rmse']:.4f}")
    print(f"Mean Absolute Error (MAE):       {metrics['mae']:.4f}")
    print(f"R-squared (R²):                  {metrics['r2']:.4f}")
    print("-" * 70)
    
    # Interpretation
    print("\n📊 METRICS INTERPRETATION:")
    print("-" * 70)
    print(f"• Average prediction error: {metrics['mae']:.2f} rating points")
    print(f"• Model explains {metrics['r2']*100:.2f}% of rating variance")
    
    # Performance rating
    if metrics['r2'] >= 0.7:
        performance = "EXCELLENT ✓✓✓"
    elif metrics['r2'] >= 0.5:
        performance = "GOOD ✓✓"
    elif metrics['r2'] >= 0.3:
        performance = "MODERATE ✓"
    else:
        performance = "NEEDS IMPROVEMENT ⚠"
    
    print(f"• Model performance: {performance}")
    
    # Additional insights
    print("\n💡 INSIGHTS:")
    print("-" * 70)
    if metrics['mae'] < 0.5:
        print("• Very accurate predictions - excellent for practical use!")
    elif metrics['mae'] < 1.0:
        print("• Good prediction accuracy - suitable for most applications")
    elif metrics['mae'] < 1.5:
        print("• Moderate accuracy - consider adding more features")
    else:
        print("• Lower accuracy - model needs improvement")
    
    if metrics['r2'] < 0.5:
        print("• Consider:")
        print("  - Adding more features (cuisine type, location, reviews)")
        print("  - Using advanced algorithms (Random Forest, Gradient Boosting)")
        print("  - Feature engineering (creating new features)")


def compare_predictions(y_true, y_pred, n_samples=20):
    """
    Create a comparison table of predictions
    
    Parameters:
    -----------
    y_true : numpy array
        Actual values
    y_pred : numpy array
        Predicted values
    n_samples : int
        Number of samples to display
    """
    print(f"\nDetailed Comparison ({n_samples} samples):")
    print("-" * 70)
    print(f"{'Index':<8} {'Actual':<12} {'Predicted':<12} {'Error':<12} {'Status':<12}")
    print("-" * 70)
    
    for i in range(min(n_samples, len(y_true))):
        actual = y_true[i]
        predicted = y_pred[i]
        error = abs(actual - predicted)
        
        if error < 0.5:
            status = "Excellent"
        elif error < 1.0:
            status = "Good"
        elif error < 1.5:
            status = "Fair"
        else:
            status = "Poor"
        
        print(f"{i:<8} {actual:<12.2f} {predicted:<12.2f} {error:<12.2f} {status:<12}")


def save_results(y_true, y_pred, metrics, filename='task1_results.txt'):
    """
    Save evaluation results to a text file
    
    Parameters:
    -----------
    y_true : numpy array
        Actual values
    y_pred : numpy array
        Predicted values
    metrics : dict
        Performance metrics
    filename : str
        Output filename
    """
    with open(filename, 'w') as f:
        f.write("TASK 1: RESTAURANT RATING PREDICTION - RESULTS\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("PERFORMANCE METRICS:\n")
        f.write("-" * 70 + "\n")
        f.write(f"Mean Squared Error (MSE):        {metrics['mse']:.4f}\n")
        f.write(f"Root Mean Squared Error (RMSE):  {metrics['rmse']:.4f}\n")
        f.write(f"Mean Absolute Error (MAE):       {metrics['mae']:.4f}\n")
        f.write(f"R-squared (R²):                  {metrics['r2']:.4f}\n")
        f.write("-" * 70 + "\n\n")
        
        f.write("SAMPLE PREDICTIONS:\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Actual':<12} {'Predicted':<12} {'Difference':<12}\n")
        f.write("-" * 70 + "\n")
        
        for i in range(min(20, len(y_true))):
            actual = y_true[i]
            predicted = y_pred[i]
            diff = abs(actual - predicted)
            f.write(f"{actual:<12.2f} {predicted:<12.2f} {diff:<12.2f}\n")
    
    print(f"\n✓ Results saved to {filename}")