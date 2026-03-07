# Agent_3.py - ML Trainer Agent
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class MLTrainerAgent:
    def __init__(self):
        self.model = None
        self.predictions = None
        self.report = {}
    
    def train_models(self, df, target_col, days=30):
        """
        Train ML model and generate predictions
        """
        try:
            df_clean = df.copy()
            
            # Convert all columns to proper types
            for col in df_clean.select_dtypes(include=[np.number]).columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            
            # Check target
            if target_col not in df_clean.columns:
                return None, None, {"error": f"Target column '{target_col}' not found"}
            
            # Remove rows with missing target
            df_clean = df_clean.dropna(subset=[target_col])
            
            if len(df_clean) < 5:
                return None, None, {"error": "Insufficient data"}
            
            # Get numeric features
            feature_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
            if target_col in feature_cols:
                feature_cols.remove(target_col)
            
            if len(feature_cols) == 0:
                return None, None, {"error": "No numeric features"}
            
            # Prepare data
            X = df_clean[feature_cols].fillna(0)
            y = df_clean[target_col].fillna(y.mean())
            
            # Train model
            self.model = RandomForestRegressor(n_estimators=50, random_state=42)
            self.model.fit(X, y)
            
            # Calculate accuracy
            y_pred = self.model.predict(X)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            r2 = r2_score(y, y_pred)
            
            # Generate predictions
            self.predictions = []
            last_values = X.iloc[-1:].values
            for i in range(days):
                pred = self.model.predict(last_values)[0]
                self.predictions.append({
                    'day': i + 1,
                    'predicted_value': float(pred)
                })
            
            self.report = {
                'accuracy': float(r2 * 100),
                'rmse': float(rmse),
                'r2_score': float(r2),
                'features_used': feature_cols[:5]
            }
            
            return self.model, self.predictions, self.report
            
        except Exception as e:
            return None, None, {"error": str(e)}