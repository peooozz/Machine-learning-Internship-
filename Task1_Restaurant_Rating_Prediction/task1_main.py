
import warnings
warnings.filterwarnings('ignore')

# Import our custom modules
from data_preprocessing import load_and_preprocess_data
from model_training import train_linear_regression
from model_evaluation import evaluate_model, display_results
from feature_analysis import analyze_feature_importance

def main():
    """Main function to execute the complete Task 1 pipeline"""
    
    print("="*70)
    print("TASK 1: RESTAURANT RATING PREDICTION")
    print("Cognifyz Technologies - Machine Learning Internship")
    print("="*70)
    
    # Step 1: Load and preprocess data
    print("\n[STEP 1] Loading and Preprocessing Data...")
    X_train, X_test, y_train, y_test, feature_names, df = load_and_preprocess_data('Dataset.csv')
    print(f"✓ Data prepared successfully!")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Testing samples: {len(X_test)}")
    print(f"  Features: {len(feature_names)}")
    
    # Step 2: Train the model
    print("\n[STEP 2] Training Linear Regression Model...")
    model = train_linear_regression(X_train, y_train)
    print("✓ Model trained successfully!")
    
    # Step 3: Make predictions
    print("\n[STEP 3] Making Predictions...")
    y_pred = model.predict(X_test)
    print("✓ Predictions completed!")
    
    # Step 4: Evaluate model
    print("\n[STEP 4] Evaluating Model Performance...")
    metrics = evaluate_model(y_test, y_pred)
    display_results(y_test, y_pred, metrics)
    
    # Step 5: Analyze features
    print("\n[STEP 5] Analyzing Feature Importance...")
    analyze_feature_importance(model, feature_names)
    
    # Summary
    print("\n" + "="*70)
    print("TASK 1 COMPLETED SUCCESSFULLY! 🎉")
    print("="*70)
    print(f"\nDataset: {len(df)} restaurants")
    print(f"Model: Linear Regression")
    print(f"R² Score: {metrics['r2']:.4f} ({metrics['r2']*100:.2f}%)")
    print(f"Average Error: {metrics['mae']:.2f} rating points")
    print("\nAll results have been displayed above.")
    print("="*70)

if __name__ == "__main__":
    main()