# Agent_4.py - FIXED (NO ARROWS, NO SPECIAL CHARACTERS)
import pandas as pd
import json
import zipfile
import os
from datetime import datetime
import numpy as np

class DashboardCreatorAgent:
    def __init__(self):
        self.files_created = []
        self.zip_path = None
    
    def create_dashboard(self, df, predictions, target_col, username="user"):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            files = []
            output_dir = f"AutoDS_Dashboard_{timestamp}"
            os.makedirs(output_dir, exist_ok=True)
            
            cleaned_path = f"{output_dir}/Cleaned_Data.csv"
            df.to_csv(cleaned_path, index=False)
            files.append(cleaned_path)
            
            pred_path = f"{output_dir}/Predictions.csv"
            if predictions and len(predictions) > 0:
                pred_df = pd.DataFrame(predictions)
            else:
                if target_col in df.columns and df[target_col].dtype in ['int64', 'float64']:
                    mean_val = df[target_col].mean()
                    pred_df = pd.DataFrame([{'day': i, 'predicted_value': mean_val * (1 + i*0.01)} for i in range(1, 31)])
                else:
                    pred_df = pd.DataFrame([{'day': i, 'predicted_value': 100} for i in range(1, 31)])
            pred_df.to_csv(pred_path, index=False)
            files.append(pred_path)
            
            config = self._create_universal_config(df, target_col, predictions)
            config_path = f"{output_dir}/Dashboard_Config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            files.append(config_path)
            
            pbix_path = f"{output_dir}/PowerBI_Instructions.txt"
            self._create_pbix_instructions(pbix_path, df, target_col, config)
            files.append(pbix_path)
            
            dax_path = f"{output_dir}/DAX_Measures.txt"
            self._create_dax_measures(dax_path, df, target_col)
            files.append(dax_path)
            
            html_path = f"{output_dir}/Dashboard_Preview.html"
            self._create_html_preview(html_path, df, predictions, target_col)
            files.append(html_path)
            
            readme_path = f"{output_dir}/README.txt"
            self._create_readme(readme_path, df, target_col)
            files.append(readme_path)
            
            zip_filename = f"AutoDS_Dashboard_{username}_{timestamp}.zip"
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for file in files:
                    zipf.write(file, arcname=os.path.basename(file))
            
            self.zip_path = zip_filename
            return {'success': True, 'zip_file': zip_filename, 'files': files, 'message': "AutoDS Dashboard created successfully!"}
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e), 'message': f"Error: {str(e)}"}
    
    def _create_universal_config(self, df, target_col, predictions):
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    pd.to_datetime(df[col].head(5))
                    date_cols.append(col)
                except:
                    pass
        date_cols = list(set(date_cols))
        total_rows = len(df)
        total_cols = len(df.columns)
        
        if 'salary' in str(df.columns).lower() or 'income' in str(df.columns).lower() or 'hr' in str(df.columns).lower():
            dashboard_type = 'HR Analytics'
            theme = {'name': 'HR Analytics', 'primary_color': '#2C3E50', 'secondary_color': '#3498DB', 'accent_color': '#E74C3C', 'background_color': '#ECF0F1'}
        elif 'sales' in str(df.columns).lower() or 'revenue' in str(df.columns).lower() or 'profit' in str(df.columns).lower():
            dashboard_type = 'Sales Analytics'
            theme = {'name': 'Sales Dashboard', 'primary_color': '#27AE60', 'secondary_color': '#2980B9', 'accent_color': '#F39C12', 'background_color': '#F5F5F5'}
        elif 'customer' in str(df.columns).lower() or 'client' in str(df.columns).lower():
            dashboard_type = 'Customer Analytics'
            theme = {'name': 'Customer Dashboard', 'primary_color': '#8E44AD', 'secondary_color': '#3498DB', 'accent_color': '#E67E22', 'background_color': '#F8F9F9'}
        else:
            dashboard_type = 'Data Analytics'
            theme = {'name': 'Universal Dashboard', 'primary_color': '#34495E', 'secondary_color': '#3498DB', 'accent_color': '#E74C3C', 'background_color': '#FFFFFF'}
        
        kpis = []
        if target_col in numeric_cols:
            kpis.append({'title': f'Total {target_col}', 'value': float(df[target_col].sum()), 'format': '0.00', 'color': theme['secondary_color']})
            kpis.append({'title': f'Average {target_col}', 'value': float(df[target_col].mean()), 'format': '0.00', 'color': theme['accent_color']})
        kpis.append({'title': 'Total Records', 'value': total_rows, 'format': '0', 'color': theme['primary_color']})
        
        charts = []
        chart_position = 1
        if target_col in numeric_cols:
            charts.append({'id': chart_position, 'type': 'histogram', 'title': f'{target_col} Distribution', 'column': target_col, 'color': theme['secondary_color'], 'position': {'row': 1, 'col': 1}})
            chart_position += 1
        
        for i, col in enumerate(categorical_cols[:3]):
            if i < 3:
                value_counts = df[col].value_counts().head(5).to_dict()
                clean_counts = {}
                for k, v in value_counts.items():
                    try:
                        json.dumps({str(k): v})
                        clean_counts[str(k)] = int(v)
                    except:
                        clean_counts[str(k)] = int(v)
                charts.append({'id': chart_position, 'type': 'bar', 'title': f'{col} Distribution', 'data': clean_counts, 'color': theme['secondary_color'], 'position': {'row': 1 if i < 3 else 2, 'col': i+1}})
                chart_position += 1
        
        if date_cols and numeric_cols:
            charts.append({'id': chart_position, 'type': 'line', 'title': f'{numeric_cols[0]} over Time', 'date_column': date_cols[0], 'value_column': numeric_cols[0], 'color': theme['accent_color'], 'position': {'row': 2, 'col': 1, 'colspan': 2}})
            chart_position += 1
        
        if len(numeric_cols) >= 2:
            charts.append({'id': chart_position, 'type': 'scatter', 'title': f'{numeric_cols[0]} vs {numeric_cols[1]}', 'x_column': numeric_cols[0], 'y_column': numeric_cols[1], 'color': theme['secondary_color'], 'position': {'row': 2, 'col': 3}})
            chart_position += 1
        
        if categorical_cols:
            top_cats = {}
            for col in categorical_cols[:3]:
                top_cats[col] = df[col].value_counts().head(3).to_dict()
            charts.append({'id': chart_position, 'type': 'table', 'title': 'Top Categories', 'data': top_cats, 'position': {'row': 3, 'col': 1, 'colspan': 3}})
        
        config = {
            'dashboard_title': f'{dashboard_type} Dashboard',
            'dashboard_type': dashboard_type,
            'created_at': datetime.now().isoformat(),
            'dataset_info': {'name': 'Uploaded Dataset', 'rows': total_rows, 'columns': total_cols, 'numeric_features': len(numeric_cols), 'categorical_features': len(categorical_cols), 'date_features': len(date_cols)},
            'theme': theme,
            'kpis': kpis,
            'charts': charts,
            'filters': [{'field': col, 'type': 'dropdown'} for col in categorical_cols[:3] if col != target_col],
            'target_variable': target_col,
            'predictions': {'days': len(predictions) if predictions else 30, 'available': bool(predictions)}
        }
        return config
    
    def _create_pbix_instructions(self, path, df, target_col, config):
        instructions = f"""
POWERBI DASHBOARD CREATION INSTRUCTIONS
========================================
Dashboard Type: {config['dashboard_title']}
Generated: {datetime.now()}

STEP 1: IMPORT DATA
-------------------
1. Open PowerBI Desktop
2. Click "Get Data" then "CSV"
3. Select "Cleaned_Data.csv" and click "Load"
4. Click "Get Data" then "CSV" again
5. Select "Predictions.csv" and click "Load"

STEP 2: CREATE MEASURES
-----------------------
Copy these DAX formulas into PowerBI:

-- Basic Measures
Total Records = COUNTROWS('Cleaned_Data')

-- Target Measures (if applicable)
Target Average = AVERAGE('Cleaned_Data'[{target_col}])
Target Total = SUM('Cleaned_Data'[{target_col}])
Target Max = MAX('Cleaned_Data'[{target_col}])
Target Min = MIN('Cleaned_Data'[{target_col}])

STEP 3: CREATE VISUALIZATIONS
------------------------------
Based on your data, create these visualizations:

{self._get_visualization_instructions(config)}

STEP 4: APPLY THEME
-------------------
Primary Color: {config['theme']['primary_color']}
Secondary Color: {config['theme']['secondary_color']}
Accent Color: {config['theme']['accent_color']}
Background: {config['theme']['background_color']}

STEP 5: ARRANGE DASHBOARD
-------------------------
Layout your dashboard in this grid pattern:

+-----------------------------------------------------+
|  [KPI 1]    [KPI 2]    [KPI 3]                    |
+-----------------------------------------------------+
|  +---------+  +---------+  +---------+            |
|  | Chart 1 |  | Chart 2 |  | Chart 3 |            |
|  +---------+  +---------+  +---------+            |
+-----------------------------------------------------+
|  +---------------------+  +---------------------+  |
|  |     Chart 4         |  |     Chart 5         |  |
|  +---------------------+  +---------------------+  |
+-----------------------------------------------------+
|  +-----------------------------------------------+ |
|  |              Chart 6 (Table)                  | |
|  +-----------------------------------------------+ |
+-----------------------------------------------------+

STEP 6: SAVE AND PUBLISH
------------------------
1. Click File then Save As -> "AutoDS_Dashboard.pbix"
2. Click "Publish" to share online (optional)

Your dashboard is ready!
"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(instructions)
    
    def _get_visualization_instructions(self, config):
        instructions = ""
        for i, chart in enumerate(config['charts'][:6]):
            instructions += f"\nChart {i+1}: {chart['title']}\n"
            instructions += f"  Type: {chart['type']}\n"
            if chart['type'] == 'bar':
                instructions += f"  Create a bar chart showing distribution\n"
            elif chart['type'] == 'line':
                instructions += f"  Create a line chart showing trend over time\n"
            elif chart['type'] == 'histogram':
                instructions += f"  Create a histogram showing data distribution\n"
            elif chart['type'] == 'scatter':
                instructions += f"  Create a scatter plot showing correlation\n"
            elif chart['type'] == 'table':
                instructions += f"  Create a table showing top values\n"
        return instructions
    
    def _create_dax_measures(self, path, df, target_col):
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        dax = f"""
// AUTODS DASHBOARD - DAX MEASURES
// Copy these into PowerBI 'New Measure'

// ========================================
// BASIC MEASURES
// ========================================

Total Records = COUNTROWS('Cleaned_Data')

"""
        if numeric_cols:
            dax += f"""
// ========================================
// NUMERIC MEASURES
// ========================================
"""
            for col in numeric_cols[:5]:
                dax += f"""
{col} Average = AVERAGE('Cleaned_Data'[{col}])
{col} Total = SUM('Cleaned_Data'[{col}])
{col} Max = MAX('Cleaned_Data'[{col}])
{col} Min = MIN('Cleaned_Data'[{col}])
"""
        if categorical_cols:
            dax += f"""
// ========================================
// CATEGORICAL MEASURES
// ========================================
"""
            for col in categorical_cols[:3]:
                dax += f"""
Distinct {col} = DISTINCTCOUNT('Cleaned_Data'[{col}])
"""
        if target_col in df.columns:
            dax += f"""
// ========================================
// TARGET MEASURES
// ========================================

Target Average = AVERAGE('Cleaned_Data'[{target_col}])
Target Total = SUM('Cleaned_Data'[{target_col}])
Target Max = MAX('Cleaned_Data'[{target_col}])
Target Min = MIN('Cleaned_Data'[{target_col}])

// Percentage of Total
Target Percent of Total = DIVIDE([Target Total], CALCULATE([Target Total], ALL('Cleaned_Data')), 0)
"""
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        if date_cols:
            dax += f"""
// ========================================
// TIME INTELLIGENCE MEASURES
// ========================================

Previous Period = CALCULATE([Target Total], DATEADD('Cleaned_Data'[{date_cols[0]}], -1, MONTH))
Growth Percent = DIVIDE([Target Total] - [Previous Period], [Previous Period], 0)
"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(dax)
    
    def _create_readme(self, path, df, target_col):
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        with open(path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("AUTODS - UNIVERSAL DATA SCIENCE DASHBOARD\n")
            f.write("="*60 + "\n\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns\n")
            f.write(f"Target Variable: {target_col}\n\n")
            f.write("DATASET OVERVIEW:\n")
            f.write("-"*40 + "\n")
            f.write(f"Numeric Columns: {len(numeric_cols)}\n")
            f.write(f"Categorical Columns: {len(categorical_cols)}\n")
            if numeric_cols:
                f.write(f"Sample Numeric: {', '.join(numeric_cols[:5])}\n")
            if categorical_cols:
                f.write(f"Sample Categories: {', '.join(categorical_cols[:5])}\n\n")
            f.write("FILES INCLUDED:\n")
            f.write("-"*40 + "\n")
            f.write("1. Cleaned_Data.csv - Your processed dataset\n")
            f.write("2. Predictions.csv - Future predictions\n")
            f.write("3. Dashboard_Config.json - Auto-detected dashboard config\n")
            f.write("4. PowerBI_Instructions.txt - Step-by-step PowerBI guide\n")
            f.write("5. DAX_Measures.txt - DAX formulas\n")
            f.write("6. Dashboard_Preview.html - HTML preview\n")
            f.write("7. README.txt - This file\n\n")
            f.write("HOW TO CREATE POWERBI DASHBOARD:\n")
            f.write("-"*40 + "\n")
            f.write("1. Read PowerBI_Instructions.txt\n")
            f.write("2. Import both CSV files into PowerBI\n")
            f.write("3. Copy DAX measures from DAX_Measures.txt\n")
            f.write("4. Create visualizations as suggested\n")
            f.write("5. Apply the theme colors\n")
            f.write("6. Save as .pbix file\n\n")
            f.write("COLOR THEME:\n")
            f.write("-"*40 + "\n")
            f.write("Primary: #34495E (Dark Blue-Gray)\n")
            f.write("Secondary: #3498DB (Bright Blue)\n")
            f.write("Accent: #E74C3C (Red)\n")
            f.write("Background: #FFFFFF (White)\n\n")
            f.write("TIPS FOR BEAUTIFUL DASHBOARD:\n")
            f.write("-"*40 + "\n")
            f.write("Use consistent colors\n")
            f.write("Add clear titles\n")
            f.write("Use white space effectively\n")
            f.write("Add filters for interactivity\n")
            f.write("Include your company logo\n\n")
            f.write("Your AutoDS dashboard is ready!\n")
    
    def _create_html_preview(self, path, df, predictions, target_col):
        total_rows = len(df)
        total_cols = len(df.columns)
        preview_rows = df.head(5).to_dict('records')
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AutoDS Dashboard Preview</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background-color: #34495E;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #3498DB;
        }}
        .stat-label {{
            color: #7F8C8D;
            font-size: 14px;
        }}
        .section {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section-title {{
            color: #34495E;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            border-bottom: 2px solid #3498DB;
            padding-bottom: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background-color: #34495E;
            color: white;
            padding: 10px;
            text-align: left;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ecf0f1;
        }}
        tr:hover {{
            background-color: #f8f9f9;
        }}
        .predictions {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .prediction-card {{
            background: linear-gradient(135deg, #3498DB, #2980B9);
            color: white;
            padding: 15px;
            border-radius: 8px;
            min-width: 150px;
        }}
        .footer {{
            text-align: center;
            color: #7F8C8D;
            margin-top: 30px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AutoDS Dashboard Preview</h1>
            <p>Universal Data Science Dashboard Generator</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-value">{total_rows}</div><div class="stat-label">Total Rows</div></div>
            <div class="stat-card"><div class="stat-value">{total_cols}</div><div class="stat-label">Total Columns</div></div>
            <div class="stat-card"><div class="stat-value">{len(df.select_dtypes(include=[np.number]).columns)}</div><div class="stat-label">Numeric Features</div></div>
            <div class="stat-card"><div class="stat-value">{len(df.select_dtypes(include=['object']).columns)}</div><div class="stat-label">Categorical Features</div></div>
        </div>
        
        <div class="section">
            <div class="section-title">Data Preview (First 5 Rows)</div>
            <table><thead><tr>{''.join([f'<th>{col}</th>' for col in df.columns[:6]])}</tr></thead><tbody>"""
        for row in preview_rows:
            html += "<tr>"
            for col in df.columns[:6]:
                val = row.get(col, '')
                if isinstance(val, float):
                    html += f"<td>{val:.2f}</td>"
                else:
                    html += f"<td>{str(val)[:30]}</td>"
            html += "</tr>"
        html += "</tbody></table></div>"
        
        html += '<div class="section"><div class="section-title">Quick Statistics</div>'
        numeric_cols = df.select_dtypes(include=[np.number]).columns[:4]
        if len(numeric_cols) > 0:
            html += "<table><tr><th>Column</th><th>Mean</th><th>Min</th><th>Max</th></tr>"
            for col in numeric_cols:
                html += f"<tr><td>{col}</td><td>{df[col].mean():.2f}</td><td>{df[col].min():.2f}</td><td>{df[col].max():.2f}</td></tr>"
            html += "</table>"
        html += "</div>"
        
        html += '<div class="section"><div class="section-title">Predictions Preview</div><div class="predictions">'
        if predictions and len(predictions) > 0:
            for i, pred in enumerate(predictions[:5]):
                html += f'<div class="prediction-card"><div>Day {pred.get("day", i+1)}</div><div style="font-size:20px;font-weight:bold;">{pred.get("predicted_value", 100):.2f}</div></div>'
        else:
            html += "<p>No predictions available</p>"
        html += f"""</div></div>
        <div class="footer">
            <p>AutoDS - Universal Data Science Dashboard Agent</p>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Target Column: {target_col}</p>
        </div>
    </div>
</body>
</html>"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)