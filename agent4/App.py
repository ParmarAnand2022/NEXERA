# App.py - AutoDS Universal Dashboard Generator (FIXED)
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import base64
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go

# Import agents
from Agent_1 import DataCleaningAgent
from Agent_2 import FeatureEngineerAgent
from Agent_3 import MLTrainerAgent
from Agent_4 import DashboardCreatorAgent

# Page config
st.set_page_config(
    page_title="AutoDS - AI Dashboard Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive design
st.markdown("""
<style>
    /* Main container */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Cards */
    .dashboard-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
        border: 1px solid #f0f0f0;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Metrics */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* File uploader */
    .uploadfile {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Success message */
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        color: #0c5460;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196F3;
        margin: 0.5rem 0;
    }
    
    /* Feature tags */
    .feature-tag {
        display: inline-block;
        background: #f0f0f0;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.85rem;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'username' not in st.session_state:
    st.session_state.username = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None
if 'featured_df' not in st.session_state:
    st.session_state.featured_df = None
if 'predictions' not in st.session_state:
    st.session_state.predictions = None
if 'report' not in st.session_state:
    st.session_state.report = None
if 'dashboard_file' not in st.session_state:
    st.session_state.dashboard_file = None
if 'data_summary' not in st.session_state:
    st.session_state.data_summary = None

# Initialize agents
if 'agent1' not in st.session_state:
    st.session_state.agent1 = DataCleaningAgent()
if 'agent2' not in st.session_state:
    st.session_state.agent2 = FeatureEngineerAgent()
if 'agent3' not in st.session_state:
    st.session_state.agent3 = MLTrainerAgent()
if 'agent4' not in st.session_state:
    st.session_state.agent4 = DashboardCreatorAgent()

# ==================== LOGIN PAGE ====================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>🤖 AutoDS</h1>
            <p style="font-size: 1.2rem;">AI-Powered Universal Dashboard Generator</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""
            <div class="dashboard-card">
                <h3 style="color: #667eea;">Welcome Back!</h3>
                <p style="color: #666;">Login to create stunning dashboards from your data</p>
            </div>
            """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
            
            with tab1:
                with st.form("login_form"):
                    username = st.text_input("Username", placeholder="Enter your username")
                    password = st.text_input("Password", type="password", placeholder="Enter your password")
                    
                    if st.form_submit_button("Login", use_container_width=True):
                        if username:
                            st.session_state.username = username
                            st.session_state.page = 'intro'
                            st.rerun()
                        else:
                            st.error("Please enter username")
            
            with tab2:
                with st.form("register_form"):
                    new_username = st.text_input("Choose Username", placeholder="Enter username")
                    new_email = st.text_input("Email", placeholder="Enter email")
                    new_password = st.text_input("Password", type="password", placeholder="Create password")
                    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
                    
                    if st.form_submit_button("Create Account", use_container_width=True):
                        if new_password == confirm_password:
                            st.success("Account created! Please login.")
                            st.session_state.page = 'login'
                            st.rerun()
                        else:
                            st.error("Passwords don't match")

# ==================== INTRO PAGE ====================
def intro_page():
    st.markdown(f"""
    <div class="main-header">
        <h1>Welcome, {st.session_state.username}! 👋</h1>
        <p style="font-size: 1.2rem;">Let's create something amazing with your data</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #667eea;">🧹 Agent 1</h3>
            <h4 style="color: #667eea;">Data Cleaner</h4>
            <p style="color: black;">Automatically handles missing values, outliers, and fixes data types</p>
            <div class="feature-tag">Missing Values</div>
            <div class="feature-tag">Outliers</div>
            <div class="feature-tag">Data Types</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #667eea;">🔧 Agent 2</h3>
            <h4 style="color: #667eea;">Feature Engineer</h4>
            <p style="color: black;">Creates new features, detects patterns, and optimizes data for ML</p>
            <div class="feature-tag">Time Features</div>
            <div class="feature-tag">Aggregations</div>
            <div class="feature-tag">Interactions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #667eea;">📊 Agent 3</h3>
            <h4 style="color: #667eea;">ML Trainer</h4>
            <p style="color: black;">Trains multiple models and generates accurate predictions</p>
            <div class="feature-tag">Random Forest</div>
            <div class="feature-tag">XGBoost</div>
            <div class="feature-tag">Predictions</div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="dashboard-card" style="text-align: center;">
            <h3 style="color: #667eea;">📈 Agent 4</h3>
            <h4 style="color: #667eea;">Dashboard Creator</h4>
            <p style="color: black;">Generates beautiful PowerBI-ready dashboards from any data</p>
            <div class="feature-tag">PowerBI Export</div>
            <div class="feature-tag">DAX Measures</div>
            <div class="feature-tag">HTML Preview</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Your Journey", use_container_width=True):
            st.session_state.page = 'upload'
            st.rerun()

# ==================== UPLOAD PAGE ====================
def upload_page():
    st.markdown("""
    <div class="main-header">
        <h1>📤 Upload Your Data</h1>
        <p style="font-size: 1.2rem;">Supporting CSV, Excel, and more</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #667eea;">Choose File</h3>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Drag and drop or click to browse",
            type=['csv', 'xlsx', 'xls'],
            help="Upload your dataset (CSV or Excel format)"
        )
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state.df = df
                
                # Calculate summary
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                
                st.session_state.data_summary = {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'numeric': len(numeric_cols),
                    'categorical': len(categorical_cols),
                    'missing': df.isnull().sum().sum()
                }
                
                st.success(f"✅ Successfully loaded: {uploaded_file.name}")
                
            except Exception as e:
                st.error(f"Error loading file: {e}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        if st.session_state.df is not None:
            st.markdown("""
            <div class="dashboard-card">
                <h3 style="color: #667eea;">📊 Data Summary</h3>
            """, unsafe_allow_html=True)
            
            summary = st.session_state.data_summary
            st.metric("Total Rows", summary['rows'])
            st.metric("Total Columns", summary['columns'])
            st.metric("Numeric Features", summary['numeric'])
            st.metric("Categorical Features", summary['categorical'])
            st.metric("Missing Values", summary['missing'])
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.df is not None:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #667eea;">👁️ Data Preview</h3>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            st.session_state.df.head(10),
            use_container_width=True,
            height=300
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Next: Select Target", use_container_width=True):
                st.session_state.page = 'features'
                st.rerun()

# ==================== FEATURES PAGE ====================
def features_page():
    if st.session_state.df is None:
        st.warning("Please upload data first")
        st.session_state.page = 'upload'
        st.rerun()
    
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Configure Your Dashboard</h1>
        <p style="font-size: 1.2rem;">Tell us what to predict and analyze</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.df
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #667eea;">📌 Target Variable</h3>
        """, unsafe_allow_html=True)
        
        target = st.selectbox(
            "What do you want to predict?",
            options=df.columns,
            help="Select the column you want to analyze and predict"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #667eea;">⏱️ Prediction Settings</h3>
        """, unsafe_allow_html=True)
        
        days = st.slider(
            "How many days to predict?",
            min_value=7,
            max_value=90,
            value=30,
            step=1,
            help="Number of future predictions to generate"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Feature selection
    st.markdown("""
    <div class="dashboard-card">
        <h3 style="color: #667eea;">🔍 Feature Selection (Optional)</h3>
    """, unsafe_allow_html=True)
    
    feature_options = [col for col in df.columns if col != target]
    
    if feature_options:
        selected_features = st.multiselect(
            "Choose features to include in analysis",
            options=feature_options,
            default=feature_options[:min(5, len(feature_options))],
            help="Select the columns you want to use for analysis"
        )
    else:
        st.info("No additional features available")
        selected_features = []
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Data visualization
    st.markdown("""
    <div class="dashboard-card">
        <h3 style="color: #667eea;">📈 Quick Data Visualization</h3>
    """, unsafe_allow_html=True)
    
    viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Distribution", "Correlation", "Summary"])
    
    with viz_tab1:
        if target in df.columns and df[target].dtype in ['int64', 'float64']:
            fig = px.histogram(df, x=target, title=f"Distribution of {target}", 
                               color_discrete_sequence=['#667eea'])
            st.plotly_chart(fig, use_container_width=True)
    
    with viz_tab2:
        numeric_cols = df.select_dtypes(include=[np.number]).columns[:6]
        if len(numeric_cols) >= 2:
            fig = px.scatter_matrix(df[numeric_cols], title="Correlation Matrix")
            st.plotly_chart(fig, use_container_width=True)
    
    with viz_tab3:
        st.dataframe(df.describe(), use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Dashboard", use_container_width=True):
            with st.spinner("🤖 AI Agents are working their magic..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Agent 1: Clean
                status_text.text("🧹 Agent 1: Cleaning data...")
                progress_bar.progress(25)
                cleaned_df, clean_report = st.session_state.agent1.clean_data(df)
                st.session_state.cleaned_df = cleaned_df
                
                # Agent 2: Feature Engineering
                status_text.text("🔧 Agent 2: Engineering features...")
                progress_bar.progress(50)
                featured_df, feature_report = st.session_state.agent2.engineer_features(cleaned_df, target)
                st.session_state.featured_df = featured_df
                
                # Agent 3: Train
                status_text.text("📊 Agent 3: Training ML model...")
                progress_bar.progress(75)
                model, predictions, ml_report = st.session_state.agent3.train_models(featured_df, target, days)
                st.session_state.predictions = predictions
                st.session_state.report = ml_report
                
                # Agent 4: Dashboard
                status_text.text("📈 Agent 4: Creating dashboard...")
                progress_bar.progress(100)
                result = st.session_state.agent4.create_dashboard(
                    cleaned_df, predictions, target, st.session_state.username
                )
                
                if result['success']:
                    st.session_state.dashboard_file = result['zip_file']
                    st.session_state.page = 'results'
                    st.rerun()
                else:
                    st.error(f"Dashboard creation failed: {result.get('error', 'Unknown error')}")

# ==================== RESULTS PAGE ====================
def results_page():
    st.markdown("""
    <div class="main-header">
        <h1>🎉 Your Dashboard is Ready!</h1>
        <p style="font-size: 1.2rem;">Download your complete PowerBI-ready package</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #667eea;">📊 Model Performance</h3>
        """, unsafe_allow_html=True)
        
        if st.session_state.report:
            metrics = st.session_state.report
            
            st.metric("Model Accuracy", f"{metrics.get('accuracy', 0):.1f}%")
            st.metric("R² Score", f"{metrics.get('r2_score', 0):.3f}")
            st.metric("RMSE", f"{metrics.get('rmse', 0):.2f}")
            
            if metrics.get('features_used'):
                st.markdown("**Features Used:**")
                for f in metrics['features_used'][:5]:
                    st.markdown(f"• {f}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h3 style="color: #667eea;">📈 Predictions Preview</h3>
        """, unsafe_allow_html=True)
        
        if st.session_state.predictions:
            pred_df = pd.DataFrame(st.session_state.predictions)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=pred_df['day'],
                y=pred_df['predicted_value'],
                mode='lines+markers',
                name='Predictions',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="Future Predictions",
                xaxis_title="Days Ahead",
                yaxis_title="Predicted Value",
                template="plotly_white",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(pred_df.head(10), use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Dashboard preview
    st.markdown("""
    <div class="dashboard-card">
        <h3 style="color: #667eea;">📦 Dashboard Package Contents</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4>📊 Cleaned_Data.csv</h4>
            <p style="color: #666;">Processed dataset ready for PowerBI</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4>📈 Predictions.csv</h4>
            <p style="color: #666;">Future predictions in CSV format</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4>⚙️ Dashboard_Config.json</h4>
            <p style="color: #666;">Auto-detected dashboard configuration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h4>📄 DAX_Measures.txt</h4>
            <p style="color: #666;">Ready-to-use DAX formulas</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Download button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.dashboard_file and os.path.exists(st.session_state.dashboard_file):
            with open(st.session_state.dashboard_file, 'rb') as f:
                st.download_button(
                    label="📥 Download Complete Dashboard Package",
                    data=f,
                    file_name=st.session_state.dashboard_file,
                    mime="application/zip",
                    use_container_width=True
                )
            
            st.markdown("""
            <div class="info-box">
                <h4>📋 Next Steps:</h4>
                <ol>
                    <li>Extract the ZIP file</li>
                    <li>Open PowerBI Desktop</li>
                    <li>Import the CSV files</li>
                    <li>Copy DAX measures from DAX_Measures.txt</li>
                    <li>Create visualizations using Dashboard_Config.json</li>
                    <li>Save as .pbix file</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
    
    # New analysis button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Start New Analysis", use_container_width=True):
            st.session_state.page = 'upload'
            st.rerun()

# ==================== NAVIGATION ====================
def main():
    if st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'intro':
        intro_page()
    elif st.session_state.page == 'upload':
        upload_page()
    elif st.session_state.page == 'features':
        features_page()
    elif st.session_state.page == 'results':
        results_page()

if __name__ == "__main__":
    main()