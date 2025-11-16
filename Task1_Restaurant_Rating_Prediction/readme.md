# Task 1: Predict Restaurant Ratings

**Machine Learning Internship - Cognifyz Technologies**

---

## 📋 Project Overview

This project builds a machine learning model to predict restaurant ratings (0-5 scale) based on various features such as price range, delivery options, location, and customer engagement.

### Objective
Build a Linear Regression model that can accurately predict aggregate restaurant ratings using available features.

---

## 📁 Project Structure

```
task1/
├── task1_main.py              # Main execution file
├── data_preprocessing.py      # Data loading and cleaning
├── model_training.py          # Linear Regression model
├── model_evaluation.py        # Performance metrics
├── feature_analysis.py        # Feature importance analysis
├── Dataset.csv               # Restaurant dataset (9,551 records)
├── README.md                 # This file
└── requirements.txt          # Required libraries
```

---

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas numpy
```

### Execution
```bash
python task1_main.py
```

The script will:
1. Load and preprocess the dataset
2. Split data into training (80%) and testing (20%)
3. Train a Linear Regression model
4. Make predictions on test data
5. Evaluate model performance
6. Analyze feature importance

---

## 📊 Dataset Information

- **Total Records**: 9,551 restaurants
- **Features Used**: 6 features
  - Average Cost for two (numerical)
  - Price range (numerical: 1-4)
  - Votes (numerical)
  - Country Code (categorical)
  - Has Table booking (binary: 0/1)
  - Has Online delivery (binary: 0/1)
- **Target Variable**: Aggregate rating (0-5 scale)

---

## 🎯 Model Performance

### Results Summary
- **Algorithm**: Linear Regression (Normal Equation)
- **Training Samples**: 7,640 (80%)
- **Testing Samples**: 1,911 (20%)

### Performance Metrics
- **R² Score**: 0.3073 (30.73%)
- **Mean Absolute Error (MAE)**: 1.08 rating points
- **Root Mean Squared Error (RMSE)**: 1.30
- **Mean Squared Error (MSE)**: 1.68

### Interpretation
- The model explains **30.73%** of rating variance
- Average prediction error: **±1.08 stars**
- Performance: **MODERATE** (acceptable baseline)

---

## 🔍 Feature Importance

### Top Features (by impact)

1. **Has Online Delivery** (Weight: +0.7559)
   - Strongest positive impact
   - Restaurants with delivery get ~0.76 higher ratings

2. **Price Range** (Weight: +0.5266)
   - Higher-priced restaurants tend to have better ratings
   - Each price level increase adds ~0.53 to rating

3. **Votes** (Weight: +0.0006)
   - More popular restaurants have better ratings
   - Each additional vote adds 0.0006 to rating

4. **Has Table Booking** (Weight: -0.0599)
   - Slight negative impact
   - May indicate casual dining preference

5. **Country Code** (Weight: +0.0055)
   - Minimal impact on ratings

6. **Average Cost** (Weight: ~0.0000)
   - No significant direct impact

---

## 💡 Key Insights

### What Affects Ratings?

✅ **Positive Factors:**
- Online delivery availability
- Higher price positioning
- Customer engagement (votes)

⚠️ **Negative Factors:**
- Table booking requirement (slight)

### Business Recommendations

1. **Implement Online Delivery**
   - Biggest impact on ratings (+0.76)
   - Critical for improving customer satisfaction

2. **Premium Positioning**
   - Higher price ranges correlate with better ratings
   - Quality perception matters

3. **Increase Customer Engagement**
   - More reviews/votes lead to better ratings
   - Encourage customer feedback

---

## 🛠️ Technical Details

### Algorithm: Linear Regression

**Formula:**
```
Rating = w₁·Cost + w₂·Price + w₃·Votes + w₄·Country + w₅·Booking + w₆·Delivery + bias
```

**Training Method:**
- Normal Equation: `w = (XᵀX)⁻¹Xᵀy`
- Closed-form solution (no iterations needed)
- Finds optimal weights that minimize MSE

### Data Preprocessing Steps

1. **Missing Value Handling**
   - Cuisines: Filled with 'Unknown'
   - Numerical features: Filled with median

2. **Feature Encoding**
   - Binary features (Yes/No) → (1/0)
   - Kept numerical features as-is

3. **Train-Test Split**
   - Random 80-20 split
   - Seed: 42 (for reproducibility)

---

## 📈 Potential Improvements

### To Increase Model Performance:

1. **Add More Features**
   - Cuisine type
   - Location details (city, locality)
   - Restaurant type (casual/fine dining)
   - Customer reviews text

2. **Try Advanced Algorithms**
   - Random Forest
   - Gradient Boosting (XGBoost, LightGBM)
   - Neural Networks

3. **Feature Engineering**
   - Create interaction features
   - Polynomial features
   - Cuisine popularity scores

4. **Handle Outliers**
   - Remove extreme values
   - Cap very high/low costs

---

## 📝 Files Description

### 1. `task1_main.py`
Main orchestration file that executes the entire pipeline.

### 2. `data_preprocessing.py`
- Loads CSV data
- Handles missing values
- Encodes categorical variables
- Splits into train/test sets

### 3. `model_training.py`
- Implements Linear Regression from scratch
- Trains using Normal Equation
- Provides prediction functionality

### 4. `model_evaluation.py`
- Calculates performance metrics (MSE, RMSE, MAE, R²)
- Displays results in formatted tables
- Saves results to file

### 5. `feature_analysis.py`
- Analyzes feature importance
- Interprets model weights
- Provides business insights

---

## 🎓 Learning Outcomes

From this task, I learned:

1. **Data Preprocessing**
   - Handling missing values
   - Encoding categorical variables
   - Feature selection

2. **Model Training**
   - Linear Regression implementation
   - Normal Equation method
   - Train-test splitting

3. **Model Evaluation**
   - Regression metrics (MSE, RMSE, MAE, R²)
   - Performance interpretation
   - Result analysis

4. **Feature Analysis**
   - Understanding feature importance
   - Business interpretation of weights
   - Actionable insights

---

## 👤 Author

**Your Name**  
Machine Learning Intern  
Cognifyz Technologies  
November 2025

---

## 📧 Contact

For questions or feedback:
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn Profile]
- GitHub: [Your GitHub Profile]

---

## 🙏 Acknowledgments

Special thanks to **Cognifyz Technologies** for providing this learning opportunity and the restaurant dataset for analysis.

---

## 📄 License

This project is part of an internship program at Cognifyz Technologies.

---

**Last Updated**: November 17, 2025