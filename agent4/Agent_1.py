# Agent_1.py - Data Cleaning Agent
import pandas as pd
import numpy as np

class DataCleaningAgent:
    def __init__(self):
        self.cleaned_df = None
        self.report = {}
    
    def clean_data(self, df):
        """
        Clean the dataset by handling missing values, outliers, and fixing data types
        """
        try:
            # Make a copy
            cleaned = df.copy()
            report = {}
            
            # Convert all columns to proper types
            for col in cleaned.columns:
                # Try to convert to numeric
                try:
                    cleaned[col] = pd.to_numeric(cleaned[col], errors='ignore')
                except:
                    pass
                
                # Try to convert to datetime
                try:
                    cleaned[col] = pd.to_datetime(cleaned[col], errors='ignore')
                except:
                    pass
            
            # Handle missing values
            missing_before = cleaned.isnull().sum().sum()
            missing_report = {}
            
            for col in cleaned.columns:
                missing_count = cleaned[col].isnull().sum()
                if missing_count > 0:
                    if cleaned[col].dtype in ['int64', 'float64']:
                        cleaned[col].fillna(cleaned[col].mean(), inplace=True)
                        missing_report[col] = f"Filled {missing_count} missing with mean"
                    else:
                        cleaned[col].fillna('Unknown', inplace=True)
                        missing_report[col] = f"Filled {missing_count} missing with Unknown"
            
            # Remove duplicates
            cleaned.drop_duplicates(inplace=True)
            
            report['missing_values'] = {
                'before': int(missing_before),
                'after': int(cleaned.isnull().sum().sum())
            }
            
            report['rows'] = len(cleaned)
            report['columns'] = len(cleaned.columns)
            
            self.cleaned_df = cleaned
            self.report = report
            
            return cleaned, report
            
        except Exception as e:
            return df, {"error": str(e)}