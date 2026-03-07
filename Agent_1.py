"""
AGENT 1: Data Cleaning Agent
Automatically cleans uploaded data files
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List
from datetime import datetime

class DataCleaningAgent:
    """
    Agent 1: Automatically cleans data
    No manual intervention needed!
    """
    
    def __init__(self):
        self.cleaning_report = {
            "steps_performed": [],
            "warnings": [],
            "quality_score": 100,
            "original_shape": None,
            "final_shape": None
        }
    
    def clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Main cleaning function - automatically cleans the entire dataset
        """
        self.cleaning_report["original_shape"] = df.shape
        cleaned_df = df.copy()
        
        # Step 1: Remove duplicates
        cleaned_df, dup_report = self._remove_duplicates(cleaned_df)
        self.cleaning_report["steps_performed"].extend(dup_report)
        
        # Step 2: Handle missing values
        cleaned_df, missing_report = self._handle_missing_values(cleaned_df)
        self.cleaning_report["steps_performed"].extend(missing_report)
        
        # Step 3: Fix data types
        cleaned_df, type_report = self._fix_data_types(cleaned_df)
        self.cleaning_report["steps_performed"].extend(type_report)
        
        # Step 4: Handle outliers
        cleaned_df, outlier_report, warnings = self._handle_outliers(cleaned_df)
        self.cleaning_report["steps_performed"].extend(outlier_report)
        self.cleaning_report["warnings"].extend(warnings)
        
        # Final
        self.cleaning_report["final_shape"] = cleaned_df.shape
        self.cleaning_report["quality_score"] = self._calculate_quality_score(cleaned_df)
        
        return cleaned_df, self.cleaning_report
    
    def _remove_duplicates(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List]:
        """Remove duplicate rows"""
        report = []
        before = len(df)
        df = df.drop_duplicates()
        after = len(df)
        
        if before > after:
            report.append(f"Removed {before - after} duplicate rows")
        
        return df, report
    
    def _handle_missing_values(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List]:
        """Intelligently handle missing values"""
        report = []
        
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                missing_pct = (missing_count / len(df)) * 100
                
                if pd.api.types.is_numeric_dtype(df[col]):
                    if missing_pct < 5:
                        fill_value = df[col].mean()
                        df[col].fillna(fill_value, inplace=True)
                        report.append(f"Filled {missing_count} missing in '{col}' with mean ({fill_value:.2f})")
                    
                    elif missing_pct < 20:
                        fill_value = df[col].median()
                        df[col].fillna(fill_value, inplace=True)
                        report.append(f"Filled {missing_count} missing in '{col}' with median ({fill_value:.2f})")
                    
                    else:
                        df.drop(columns=[col], inplace=True)
                        report.append(f"Dropped column '{col}' due to {missing_pct:.1f}% missing values")
                
                else:
                    if missing_pct < 10:
                        fill_value = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
                        df[col].fillna(fill_value, inplace=True)
                        report.append(f"Filled {missing_count} missing in '{col}' with mode '{fill_value}'")
                    
                    elif missing_pct < 30:
                        df[col].fillna("Missing", inplace=True)
                        report.append(f"Filled {missing_count} missing in '{col}' with 'Missing' label")
                    
                    else:
                        df.drop(columns=[col], inplace=True)
                        report.append(f"Dropped column '{col}' due to {missing_pct:.1f}% missing values")
        
        return df, report
    
    def _fix_data_types(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List]:
        """Automatically detect and fix incorrect data types"""
        report = []
        
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col])
                    df[col] = pd.to_datetime(df[col])
                    report.append(f"Converted '{col}' to datetime")
                    continue
                except:
                    pass
                
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    report.append(f"Converted '{col}' to numeric")
                    continue
                except:
                    pass
                
                if df[col].nunique() < 20:
                    df[col] = df[col].astype('category')
                    report.append(f"Converted '{col}' to category")
        
        return df, report
    
    def _handle_outliers(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List, List]:
        """Detect and handle outliers using IQR method"""
        report = []
        warnings = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if len(df[col].dropna()) > 0:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                outlier_count = len(outliers)
                
                if outlier_count > 0:
                    outlier_pct = (outlier_count / len(df)) * 100
                    
                    if outlier_pct < 5:
                        df[col] = df[col].clip(lower_bound, upper_bound)
                        report.append(f"Capped {outlier_count} outliers in '{col}'")
                    
                    elif outlier_pct < 15:
                        df[col] = df[col].clip(df[col].quantile(0.01), df[col].quantile(0.99))
                        report.append(f"Winsorized {outlier_count} outliers in '{col}'")
                    
                    else:
                        warnings.append(f"'{col}' has {outlier_pct:.1f}% outliers - consider transformation")
        
        return df, report, warnings
    
    def _calculate_quality_score(self, df: pd.DataFrame) -> float:
        """Calculate overall data quality score (0-100)"""
        score = 100
        missing_total = df.isnull().sum().sum()
        missing_pct = missing_total / (df.shape[0] * df.shape[1]) * 100
        score -= missing_pct * 2
        return max(0, min(100, score))