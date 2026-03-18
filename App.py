"""
Main App with Agent 1 + Agent 2
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Import both agents
from Agent_1 import DataCleaningAgent
from Agent_2 import FeatureEngineeringAgent

# Page config
st.set_page_config(
    page_title="AI Business Predictor - Agents 1 & 2",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'agent1' not in st.session_state:
    st.session_state.agent1 = DataCleaningAgent()
    st.session_state.agent2 = FeatureEngineeringAgent()
    st.session_state.df = None
    st.session_state.cleaned_df = None
    st.session_state.featured_df = None
    st.session_state.report1 = None
    st.session_state.report2 = None

# Header
st.title("🤖 AI Business Predictor")
st.markdown("""
| Agent | Role | Status |
|-------|------|--------|
| 🧹 Agent 1 | Data Cleaning | ✅ Ready |
| 🔧 Agent 2 | Feature Engineering | ✅ Ready |
""")

# Sidebar
with st.sidebar:
    st.header("📊 Progress")
    
    if st.session_state.df is not None:
        st.success("✅ Step 1: Data Uploaded")
    else:
        st.info("⏳ Step 1: Upload Data")
    
    if st.session_state.cleaned_df is not None:
        st.success("✅ Step 2: Data Cleaned")
    else:
        st.info("⏳ Step 2: Run Agent 1")
    
    if st.session_state.featured_df is not None:
        st.success("✅ Step 3: Features Created")
    else:
        st.info("⏳ Step 3: Run Agent 2")
    
    st.divider()
    
    if st.session_state.df is not None:
        st.metric("Original Data", f"{st.session_state.df.shape[0]} rows, {st.session_state.df.shape[1]} cols")
    if st.session_state.cleaned_df is not None:
        st.metric("After Cleaning", f"{st.session_state.cleaned_df.shape[0]} rows, {st.session_state.cleaned_df.shape[1]} cols")
    if st.session_state.featured_df is not None:
        st.metric("After Features", f"{st.session_state.featured_df.shape[0]} rows, {st.session_state.featured_df.shape[1]} cols")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Step 1: Upload Data")
    
    uploaded_file = st.file_uploader(
        "Choose CSV or Excel file",
        type=['csv', 'xlsx', 'xls']
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.session_state.df = df
            st.success(f"✅ Loaded: {uploaded_file.name}")
            
            with st.expander("👁️ Preview Original Data"):
                st.dataframe(df.head())
                st.caption(f"Shape: {df.shape}")
        
        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    if st.session_state.df is not None:
        st.subheader("🧹 Step 2: Agent 1 - Data Cleaning")
        
        if st.button("🚀 Run Agent 1", type="primary", use_container_width=True):
            with st.spinner("Agent 1 cleaning data..."):
                cleaned_df, report = st.session_state.agent1.clean(st.session_state.df)
                st.session_state.cleaned_df = cleaned_df
                st.session_state.report1 = report
            st.success("✅ Agent 1 Complete!")
            st.balloons()
        
        if st.session_state.cleaned_df is not None:
            st.subheader("🔧 Step 3: Agent 2 - Feature Engineering")
            
            target = st.selectbox(
                "🎯 Select target column to predict",
                st.session_state.cleaned_df.columns
            )
            
            if st.button("🚀 Run Agent 2", type="primary", use_container_width=True):
                with st.spinner("Agent 2 creating features..."):
                    featured_df, report = st.session_state.agent2.engineer_features(
                        st.session_state.cleaned_df,
                        target
                    )
                    st.session_state.featured_df = featured_df
                    st.session_state.report2 = report
                st.success("✅ Agent 2 Complete!")

# Results section
if st.session_state.cleaned_df is not None or st.session_state.featured_df is not None:
    st.divider()
    st.subheader("📊 Results")
    
    tab1, tab2, tab3 = st.tabs(["🧹 Agent 1 Report", "🔧 Agent 2 Report", "📈 Data Preview"])
    
    with tab1:
        if st.session_state.report1:
            st.metric("Quality Score", f"{st.session_state.report1['quality_score']:.1f}%")
            
            st.write("**Steps Performed:**")
            for step in st.session_state.report1['steps_performed']:
                st.write(f"✅ {step}")
            
            if st.session_state.report1['warnings']:
                st.write("**Warnings:**")
                for w in st.session_state.report1['warnings']:
                    st.warning(w)
    
    with tab2:
        if st.session_state.report2:
            st.metric("New Features Created", len(st.session_state.report2['features_created']))
            st.metric("Total Features", st.session_state.report2['total_features'])
            
            st.write("**New Features:**")
            for f in st.session_state.report2['features_created'][:15]:
                st.write(f"✅ {f}")
    
    with tab3:
        if st.session_state.featured_df is not None:
            st.dataframe(st.session_state.featured_df.head())
            st.caption(f"Final Shape: {st.session_state.featured_df.shape}")
            
            # Download button
            csv = st.session_state.featured_df.to_csv(index=False)
            st.download_button(
                "📥 Download Enhanced Data",
                csv,
                f"enhanced_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv"
            )

# Footer
st.divider()
st.caption("🤖 Agents 1 & 2: Data Cleaning + Feature Engineering | Built for Hackathon")