"""
AGENT 2: Feature Engineering Agent
Creates new features automatically from cleaned data
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class FeatureEngineeringAgent:
    """
    Agent 2: Automatically creates relevant features for prediction
    """
    
    def __init__(self):
        self.report = {
            "features_created": [],
            "total_features": 0,
            "warnings": []
        }
        self.label_encoders = {}
    
    def engineer_features(self, df, target_col):
        """
        Main feature engineering function
        """
        enhanced_df = df.copy()
        self.report = {
            "features_created": [],
            "total_features": 0,
            "warnings": []
        }
        
        # STEP 1: Identify date columns
        date_cols = self._find_date_columns(enhanced_df)
        if date_cols:
            enhanced_df, date_features = self._create_time_features(enhanced_df, date_cols[0])
            self.report["features_created"].extend(date_features)
        
        # STEP 2: Create statistical features
        numeric_cols = enhanced_df.select_dtypes(include=[np.number]).columns.tolist()
        if target_col in numeric_cols:
            numeric_cols.remove(target_col)
        
        if numeric_cols:
            enhanced_df, stats_features = self._create_statistical_features(enhanced_df, numeric_cols)
            self.report["features_created"].extend(stats_features)
        
        # STEP 3: Create interaction features
        if len(numeric_cols) >= 2:
            enhanced_df, interaction_features = self._create_interaction_features(enhanced_df, numeric_cols[:3])
            self.report["features_created"].extend(interaction_features)
        
        # STEP 4: Create lag features
        if date_cols and len(enhanced_df) > 10:
            enhanced_df, lag_features = self._create_lag_features(enhanced_df, target_col, numeric_cols[:2])
            self.report["features_created"].extend(lag_features)
        
        # STEP 5: Encode categorical variables
        cat_cols = enhanced_df.select_dtypes(include=['object', 'category']).columns.tolist()
        if cat_cols and target_col in cat_cols:
            cat_cols.remove(target_col)
        
        if cat_cols:
            enhanced_df, encoded_features = self._encode_categorical(enhanced_df, cat_cols)
            self.report["features_created"].extend(encoded_features)
        
        self.report["total_features"] = len(enhanced_df.columns)
        
        return enhanced_df, self.report
    
    def _find_date_columns(self, df):
        """Find columns that contain dates"""
        date_cols = []
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]':
                date_cols.append(col)
            elif 'date' in col.lower() or 'time' in col.lower():
                try:
                    pd.to_datetime(df[col])
                    date_cols.append(col)
                except:
                    pass
        return date_cols
    
    def _create_time_features(self, df, date_col):
        """Extract time-based features"""
        features = []
        
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day'] = df[date_col].dt.day
        df['day_of_week'] = df[date_col].dt.dayofweek
        df['quarter'] = df[date_col].dt.quarter
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['day_of_year'] = df[date_col].dt.dayofyear
        df['week_of_year'] = df[date_col].dt.isocalendar().week
        
        features.extend(['year', 'month', 'day', 'day_of_week', 'quarter', 
                        'is_weekend', 'day_of_year', 'week_of_year'])
        
        return df, features
    
    def _create_statistical_features(self, df, numeric_cols):
        """Create rolling statistics"""
        features = []
        
        for col in numeric_cols[:3]:
            if len(df) > 7:
                df[f'{col}_rolling_mean_7'] = df[col].rolling(window=7, min_periods=1).mean()
                features.append(f'{col}_rolling_mean_7')
                
                df[f'{col}_rolling_std_7'] = df[col].rolling(window=7, min_periods=1).std().fillna(0)
                features.append(f'{col}_rolling_std_7')
                
                df[f'{col}_expanding_mean'] = df[col].expanding(min_periods=1).mean()
                features.append(f'{col}_expanding_mean')
        
        return df, features
    
    def _create_interaction_features(self, df, numeric_cols):
        """Create interaction features"""
        features = []
        
        for i in range(len(numeric_cols)):
            for j in range(i+1, len(numeric_cols)):
                col1, col2 = numeric_cols[i], numeric_cols[j]
                
                df[f'{col1}_x_{col2}'] = df[col1] * df[col2]
                features.append(f'{col1}_x_{col2}')
                
                df[f'{col1}_div_{col2}'] = df[col1] / (df[col2] + 0.001)
                features.append(f'{col1}_div_{col2}')
                
                break
            break
        
        return df, features
    
    def _create_lag_features(self, df, target_col, numeric_cols):
        """Create lag features"""
        features = []
        
        df[f'{target_col}_lag_1'] = df[target_col].shift(1)
        df[f'{target_col}_lag_2'] = df[target_col].shift(2)
        df[f'{target_col}_lag_3'] = df[target_col].shift(3)
        features.extend([f'{target_col}_lag_1', f'{target_col}_lag_2', f'{target_col}_lag_3'])
        
        df.fillna(method='bfill', inplace=True)
        df.fillna(method='ffill', inplace=True)
        
        return df, features
    
    def _encode_categorical(self, df, cat_cols):
        """Encode categorical variables"""
        features = []
        
        for col in cat_cols:
            if df[col].nunique() < 10:
                dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
                df = pd.concat([df, dummies], axis=1)
                df.drop(columns=[col], inplace=True)
                features.extend(dummies.columns.tolist())
            else:
                le = LabelEncoder()
                df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
                features.append(f'{col}_encoded')
                self.label_encoders[col] = le
        
        return df, features