"""
AGENT 1: Data Cleaning Agent - Complete Implementation
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
import os

# ==================== AGENT 1 CLASS ====================

class DataCleaningAgent:
    """
    Agent 1: Automatically cleans uploaded data files
    No manual intervention needed!
    """
    
    def __init__(self):
        self.report = {
            "steps": [],
            "warnings": [],
            "quality_score": 100,
            "original_shape": None,
            "final_shape": None
        }
    
    def clean(self, df):
        """Main cleaning function - call this only once!"""
        
        self.report["original_shape"] = df.shape
        cleaned_df = df.copy()
        
        # STEP 1: Remove duplicates
        cleaned_df, steps = self._remove_duplicates(cleaned_df)
        self.report["steps"].extend(steps)
        
        # STEP 2: Handle missing values
        cleaned_df, steps = self._handle_missing(cleaned_df)
        self.report["steps"].extend(steps)
        
        # STEP 3: Fix data types
        cleaned_df, steps = self._fix_types(cleaned_df)
        self.report["steps"].extend(steps)
        
        # STEP 4: Handle outliers
        cleaned_df, steps, warnings = self._handle_outliers(cleaned_df)
        self.report["steps"].extend(steps)
        self.report["warnings"].extend(warnings)
        
        # Final
        self.report["final_shape"] = cleaned_df.shape
        self.report["quality_score"] = self._calculate_score(cleaned_df)
        
        return cleaned_df, self.report
    
    def _remove_duplicates(self, df):
        """Remove duplicate rows"""
        before = len(df)
        df = df.drop_duplicates()
        after = len(df)
        steps = []
        if before > after:
            steps.append(f"✅ Removed {before - after} duplicate rows")
        return df, steps
    
    def _handle_missing(self, df):
        """Handle missing values intelligently"""
        steps = []
        
        for col in df.columns:
            missing = df[col].isnull().sum()
            if missing > 0:
                missing_pct = (missing / len(df)) * 100
                
                if pd.api.types.is_numeric_dtype(df[col]):
                    if missing_pct < 5:
                        val = df[col].mean()
                        df[col].fillna(val, inplace=True)
                        steps.append(f"✅ Filled {missing} missing in '{col}' with mean ({val:.2f})")
                    elif missing_pct < 20:
                        val = df[col].median()
                        df[col].fillna(val, inplace=True)
                        steps.append(f"✅ Filled {missing} missing in '{col}' with median ({val:.2f})")
                    else:
                        df.drop(columns=[col], inplace=True)
                        steps.append(f"⚠️ Dropped '{col}' - {missing_pct:.1f}% missing")
                else:
                    if missing_pct < 10:
                        val = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
                        df[col].fillna(val, inplace=True)
                        steps.append(f"✅ Filled {missing} missing in '{col}' with '{val}'")
                    elif missing_pct < 30:
                        df[col].fillna("Missing", inplace=True)
                        steps.append(f"✅ Filled {missing} missing in '{col}' with 'Missing'")
                    else:
                        df.drop(columns=[col], inplace=True)
                        steps.append(f"⚠️ Dropped '{col}' - {missing_pct:.1f}% missing")
        
        return df, steps
    
    def _fix_types(self, df):
        """Fix incorrect data types"""
        steps = []
        
        for col in df.columns:
            # Try datetime
            if df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col])
                    df[col] = pd.to_datetime(df[col])
                    steps.append(f"✅ Converted '{col}' to datetime")
                    continue
                except:
                    pass
                
                # Try numeric
                try:
                    df[col] = pd.to_numeric(df[col])
                    steps.append(f"✅ Converted '{col}' to number")
                    continue
                except:
                    pass
                
                # To category if few unique
                if df[col].nunique() < 20:
                    df[col] = df[col].astype('category')
                    steps.append(f"✅ Converted '{col}' to category")
        
        return df, steps
    
    def _handle_outliers(self, df):
        """Detect and handle outliers"""
        steps = []
        warnings = []
        
        for col in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower) | (df[col] > upper)]
            if len(outliers) > 0:
                pct = (len(outliers) / len(df)) * 100
                if pct < 5:
                    df[col] = df[col].clip(lower, upper)
                    steps.append(f"✅ Capped {len(outliers)} outliers in '{col}'")
                else:
                    warnings.append(f"⚠️ '{col}' has {pct:.1f}% outliers")
        
        return df, steps, warnings
    
    def _calculate_score(self, df):
        """Calculate data quality score"""
        score = 100
        # Deduct for remaining issues
        missing = df.isnull().sum().sum()
        score -= missing * 2
        return max(0, min(100, score))

# ==================== STREAMLIT UI ====================

st.set_page_config(
    page_title="Agent 1 - Data Cleaner",
    page_icon="🧹",
    layout="wide"
)

# Title
st.title("🧹 Agent 1: Automatic Data Cleaning")
st.markdown("Upload any CSV or Excel file - Agent will clean it automatically!")

# Initialize agent in session state (runs only once)
if 'agent' not in st.session_state:
    st.session_state.agent = DataCleaningAgent()
    st.session_state.cleaned_df = None
    st.session_state.report = None

# File upload
uploaded_file = st.file_uploader(
    "📁 Choose a file",
    type=['csv', 'xlsx', 'xls'],
    help="Upload your business data"
)

if uploaded_file is not None:
    
    # Read file
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ Loaded: {uploaded_file.name}")
        
        # Show original data
        with st.expander("👁️ View Original Data", expanded=False):
            st.dataframe(df.head(10))
            st.caption(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Clean button
        if st.button("🚀 RUN AGENT 1", type="primary", use_container_width=True):
            
            with st.spinner("🤖 Agent 1 is cleaning your data..."):
                # Run cleaning (only once!)
                cleaned_df, report = st.session_state.agent.clean(df)
                
                # Store in session
                st.session_state.cleaned_df = cleaned_df
                st.session_state.report = report
            
            st.success("✅ Agent 1 completed!")
            st.balloons()
    
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Show results if available
if st.session_state.cleaned_df is not None:
    
    st.divider()
    st.subheader("📊 Results")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Quality Score", f"{st.session_state.report['quality_score']:.1f}%")
    with col2:
        st.metric("Original Rows", st.session_state.report['original_shape'][0])
    with col3:
        st.metric("Final Rows", st.session_state.report['final_shape'][0])
    with col4:
        st.metric("Changes", len(st.session_state.report['steps']))
    
    # Two tabs
    tab1, tab2, tab3 = st.tabs(["✅ Cleaned Data", "📋 Cleaning Steps", "⚠️ Warnings"])
    
    with tab1:
        st.dataframe(st.session_state.cleaned_df)
        
        # Download button
        csv = st.session_state.cleaned_df.to_csv(index=False)
        st.download_button(
            "📥 Download Cleaned CSV",
            csv,
            f"cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "text/csv"
        )
    
    with tab2:
        for step in st.session_state.report['steps']:
            st.write(step)
    
    with tab3:
        if st.session_state.report['warnings']:
            for w in st.session_state.report['warnings']:
                st.warning(w)
        else:
            st.success("No warnings! Data looks good.")

# Footer
st.divider()
st.caption("🤖 Agent 1: Data Cleaning Agent | One agent at a time")