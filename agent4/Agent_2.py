# Agent_2.py - Feature Engineering Agent
import pandas as pd
import numpy as np

class FeatureEngineerAgent:
    def __init__(self):
        self.featured_df = None
        self.report = {}
    
    def engineer_features(self, df, target_col=None):
        """
        Create new features from existing data
        """
        try:
            enhanced = df.copy()
            report = {}
            
            # Ensure all numeric columns are float
            for col in enhanced.select_dtypes(include=[np.number]).columns:
                enhanced[col] = enhanced[col].astype(float)
            
            # Find date columns
            date_cols = []
            for col in enhanced.columns:
                if 'date' in col.lower() or 'time' in col.lower():
                    try:
                        enhanced[col] = pd.to_datetime(enhanced[col])
                        date_cols.append(col)
                    except:
                        pass
            
            # Create time features if date exists
            if date_cols:
                date_col = date_cols[0]
                enhanced['Year'] = enhanced[date_col].dt.year
                enhanced['Month'] = enhanced[date_col].dt.month
                enhanced['Day'] = enhanced[date_col].dt.day
                enhanced['DayOfWeek'] = enhanced[date_col].dt.dayofweek
                report['time_features'] = "Created Year, Month, Day, DayOfWeek"
            
            # Create age groups if Age column exists
            if 'Age' in enhanced.columns:
                bins = [0, 25, 35, 45, 55, 100]
                labels = ['18-25', '26-35', '36-45', '46-55', '55+']
                enhanced['AgeGroup'] = pd.cut(enhanced['Age'], bins=bins, labels=labels)
                report['age_groups'] = "Created Age Groups"
            
            # Create salary slabs if MonthlyIncome exists
            if 'MonthlyIncome' in enhanced.columns:
                bins = [0, 5000, 10000, 15000, 100000]
                labels = ['Under 5k', '5k-10k', '10k-15k', '15k+']
                enhanced['SalarySlab'] = pd.cut(enhanced['MonthlyIncome'], bins=bins, labels=labels)
                report['salary_slabs'] = "Created Salary Slabs"
            
            # Fill any NaN
            enhanced = enhanced.fillna(0)
            
            self.featured_df = enhanced
            self.report = report
            
            return enhanced, report
            
        except Exception as e:
            return df, {"error": str(e)}