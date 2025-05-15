import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
import base64
from datetime import datetime
from config import RISK_LEVELS, PERFORMANCE_LEVELS, CHART_COLORS

def format_currency(value):
    """Format a number as currency"""
    if pd.isna(value):
        return "$0.00"
    return f"${value:,.2f}"

def format_percentage(value):
    """Format a number as percentage"""
    if pd.isna(value):
        return "0.0%"
    return f"{value:.1f}%"

def format_date(date):
    """Format a date as string"""
    if pd.isna(date):
        return "N/A"
    if isinstance(date, str):
        try:
            date = pd.to_datetime(date)
        except:
            return date
    return date.strftime("%b %d, %Y")

def get_risk_level(score):
    """Get risk level based on score"""
    if score >= 7.5:
        return "critical"
    elif score >= 5.0:
        return "high"
    elif score >= 3.0:
        return "medium"
    else:
        return "low"

def get_performance_level(score):
    """Get performance level based on score"""
    if score >= 8.0:
        return "excellent"
    elif score >= 6.0:
        return "good"
    elif score >= 4.0:
        return "fair"
    else:
        return "poor"

def risk_color(level):
    """Get color for risk level"""
    return RISK_LEVELS[level]["color"]

def performance_color(level):
    """Get color for performance level"""
    return PERFORMANCE_LEVELS[level]["color"]

def create_download_link(df, filename):
    """Create a link to download data as CSV"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def plot_spend_by_category(df):
    """Create a treemap chart of spend by category"""
    if "category" not in df.columns or "amount" not in df.columns:
        # Create dummy data if required columns not present
        data = pd.DataFrame({
            "category": ["Structural Materials", "MEP Systems", "Building Envelope", 
                         "Finishes", "Sitework & Foundations", "Safety Equipment"],
            "amount": [350000, 275000, 180000, 120000, 95000, 55000]
        })
    else:
        # Aggregate data by category
        data = df.groupby("category")["amount"].sum().reset_index()
        data = data.sort_values("amount", ascending=False)
    
    # Create treemap
    fig = px.treemap(
        data,
        path=["category"],
        values="amount",
        color="amount",
        color_continuous_scale="Viridis",
        title="Spend by Category"
    )
    
    # Format the hover text
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Spend: $%{value:,.2f}<extra></extra>'
    )
    
    # Set layout
    fig.update_layout(
        height=450,
        margin=dict(l=10, r=10, t=30, b=10),
        coloraxis_showscale=False
    )
    
    return fig

def plot_spend_trend(df):
    """Create a line chart of spend trend over time"""
    if "date" not in df.columns or "amount" not in df.columns:
        # Create dummy data if required columns not present
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        data = pd.DataFrame({
            "date": dates,
            "amount": [125000, 110000, 135000, 165000, 142000, 158000, 
                      172000, 183000, 167000, 155000, 188000, 210000]
        })
    else:
        # Aggregate data by month
        df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
        data = df.groupby('month').agg({'amount': 'sum'}).reset_index()
        data['date'] = data['month'].dt.to_timestamp()
    
    # Sort by date
    data = data.sort_values('date')
    
    # Calculate moving average
    data['moving_avg'] = data['amount'].rolling(window=3, min_periods=1).mean()
    
    # Create line chart
    fig = go.Figure()
    
    # Add bar chart for monthly spend
    fig.add_trace(go.Bar(
        x=data['date'],
        y=data['amount'],
        name='Monthly Spend',
        marker_color=CHART_COLORS[0],
        opacity=0.7
    ))
    
    # Add line chart for moving average
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['moving_avg'],
        name='3-Month Avg',
        line=dict(color=CHART_COLORS[1], width=3),
        mode='lines'
    ))
    
    # Set layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Spend Amount",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=450,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    # Format y-axis as currency
    fig.update_yaxes(tickprefix="$", tickformat=",")
    
    return fig

def plot_supplier_risk_heatmap(df):
    """Create a heatmap of supplier risk assessments"""
    if len(df) == 0:
        # Create dummy data if no data
        return go.Figure()
    
    # Select top suppliers by overall risk score
    top_suppliers = df.sort_values('overall_risk', ascending=False).head(10)
    
    # Get risk categories
    risk_categories = ['financial_risk', 'operational_risk', 'compliance_risk', 
                       'geopolitical_risk', 'environmental_risk', 'social_risk', 'governance_risk']
    
    # Create heatmap data
    z_data = []
    for _, row in top_suppliers.iterrows():
        supplier_risks = [row[cat] for cat in risk_categories]
        z_data.append(supplier_risks)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=[cat.replace('_risk', '').capitalize() for cat in risk_categories],
        y=top_suppliers['supplier'],
        colorscale=[
            [0, "#4CAF50"],      # Low risk (green)
            [0.3, "#8BC34A"],    # Low-medium
            [0.5, "#FFEB3B"],    # Medium
            [0.7, "#FFC107"],    # Medium-high
            [0.85, "#FF9800"],   # High
            [1, "#F44336"]       # Critical (red)
        ],
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.1f}<extra></extra>',
        colorbar=dict(
            title="Risk Score",
            titleside="top",
            tickmode="array",
            tickvals=[1, 3, 5, 7, 9],
            ticktext=["Very Low", "Low", "Medium", "High", "Critical"],
            ticks="outside"
        )
    ))
    
    # Set layout
    fig.update_layout(
        height=450,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(side="top")
    )
    
    return fig

def plot_risk_radar(supplier_risk, title="Risk Assessment"):
    """Create a radar chart of risk factors"""
    if pd.isna(supplier_risk).all():
        # Create dummy data if no data
        return go.Figure()
    
    # Define risk categories and their values
    categories = [
        'Financial', 'Operational', 'Compliance', 
        'Geopolitical', 'Environmental', 'Social', 'Governance'
    ]
    
    values = [
        supplier_risk['financial_risk'] if 'financial_risk' in supplier_risk else 5,
        supplier_risk['operational_risk'] if 'operational_risk' in supplier_risk else 5,
        supplier_risk['compliance_risk'] if 'compliance_risk' in supplier_risk else 5,
        supplier_risk['geopolitical_risk'] if 'geopolitical_risk' in supplier_risk else 5,
        supplier_risk['environmental_risk'] if 'environmental_risk' in supplier_risk else 5,
        supplier_risk['social_risk'] if 'social_risk' in supplier_risk else 5,
        supplier_risk['governance_risk'] if 'governance_risk' in supplier_risk else 5
    ]
    
    # Create radar chart
    fig = go.Figure()
    
    # Add trace for supplier risk
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=CHART_COLORS[0] + '60',  # Add transparency
        line=dict(color=CHART_COLORS[0], width=2),
        name=title
    ))
    
    # Add benchmark trace (for comparison)
    benchmark_values = [5.2, 4.8, 4.5, 5.0, 5.5, 4.7, 4.9]  # Industry average (mock)
    
    fig.add_trace(go.Scatterpolar(
        r=benchmark_values,
        theta=categories,
        fill='toself',
        fillcolor=CHART_COLORS[1] + '60',  # Add transparency
        line=dict(color=CHART_COLORS[1], width=2, dash='dot'),
        name='Industry Avg'
    ))
    
    # Set layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
        height=450,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    
    return fig

def plot_performance_radar(df, suppliers, max_suppliers=3):
    """Create a radar chart of performance metrics for multiple suppliers"""
    if len(df) == 0 or len(suppliers) == 0:
        # Create dummy data if no data
        return go.Figure()
    
    # Limit to max number of suppliers
    suppliers = suppliers[:max_suppliers]
    
    # Define performance categories
    categories = [
        'Schedule Adherence', 'Work Quality', 'Cost Control', 'Safety Performance',
        'Documentation', 'Communication', 'Problem Resolution'
    ]
    
    # Create radar chart
    fig = go.Figure()
    
    # Add trace for each supplier
    for i, supplier in enumerate(suppliers):
        # Get supplier data
        supplier_data = df[df['supplier'] == supplier]
        
        if len(supplier_data) == 0:
            continue
        
        # Get performance values
        values = [
            supplier_data['schedule_adherence'].values[0],
            supplier_data['work_quality'].values[0],
            supplier_data['cost_control'].values[0],
            supplier_data['safety_performance'].values[0],
            supplier_data['documentation'].values[0],
            supplier_data['communication'].values[0],
            supplier_data['problem_resolution'].values[0]
        ]
        
        # Add trace
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor=CHART_COLORS[i % len(CHART_COLORS)] + '60',  # Add transparency
            line=dict(color=CHART_COLORS[i % len(CHART_COLORS)], width=2),
            name=supplier
        ))
    
    # Set layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
        height=450,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    return fig

def plot_opportunity_matrix(df):
    """Create a bubble chart representing savings opportunities"""
    if len(df) == 0:
        # Create dummy data if no data
        return go.Figure()
    
    # Create bubble chart
    fig = px.scatter(
        df,
        x='complexity',
        y='savings_potential',
        size='annual_spend',
        color='category',
        hover_name='title',
        text='title',
        size_max=60,
        title="Savings Opportunity Matrix"
    )
    
    # Set layout
    fig.update_layout(
        xaxis=dict(
            title="Implementation Complexity",
            tickvals=[1, 2, 3, 4, 5],
            ticktext=["Very Low", "Low", "Medium", "High", "Very High"]
        ),
        yaxis=dict(
            title="Savings Potential (%)",
            ticksuffix="%"
        ),
        height=500,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    return fig

def create_metric_card(title, value, change=None, prefix="", is_currency=False, is_percentage=False):
    """Create a metric card with title, value, and optional change indicator"""
    if is_currency:
        formatted_value = format_currency(value)
    elif is_percentage:
        formatted_value = format_percentage(value)
    else:
        formatted_value = f"{prefix}{value:,}"
    
    st.metric(
        label=title,
        value=formatted_value,
        delta=f"{change:+.1f}%" if change is not None else None
    )

def upload_file_handler(uploaded_file, upload_type):
    """Process uploaded file based on type"""
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Basic validation
        if len(df) == 0:
            return {"success": False, "message": "The uploaded file is empty."}
        
        # Process based on type
        if upload_type == "Spend Data":
            required_cols = ['date', 'supplier', 'category', 'amount']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                return {
                    "success": False, 
                    "message": f"Missing required columns: {', '.join(missing_cols)}.",
                    "detected_type": detect_template_type(uploaded_file)
                }
            
            # Convert date column
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Check for invalid dates
            if df['date'].isna().any():
                return {
                    "success": False, 
                    "message": "The date column contains invalid dates. Please use YYYY-MM-DD format."
                }
            
            # Check for non-numeric amounts
            if not pd.to_numeric(df['amount'], errors='coerce').notna().all():
                return {
                    "success": False, 
                    "message": "The amount column contains non-numeric values."
                }
            
            # Convert amount to numeric
            df['amount'] = pd.to_numeric(df['amount'])
            
        elif upload_type == "Supplier Information":
            required_cols = ['name', 'category']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                return {
                    "success": False, 
                    "message": f"Missing required columns: {', '.join(missing_cols)}.",
                    "detected_type": detect_template_type(uploaded_file)
                }
            
        elif upload_type in ["Risk Assessment", "ESG Risk Assessment"]:
            required_cols = ['supplier', 'assessment_date']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                return {
                    "success": False, 
                    "message": f"Missing required columns: {', '.join(missing_cols)}.",
                    "detected_type": detect_template_type(uploaded_file)
                }
            
            # Convert date column
            df['assessment_date'] = pd.to_datetime(df['assessment_date'], errors='coerce')
            
        elif upload_type == "Supplier Performance":
            required_cols = ['supplier', 'evaluation_date']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                return {
                    "success": False, 
                    "message": f"Missing required columns: {', '.join(missing_cols)}.",
                    "detected_type": detect_template_type(uploaded_file)
                }
            
            # Convert date column
            df['evaluation_date'] = pd.to_datetime(df['evaluation_date'], errors='coerce')
            
        elif upload_type == "Contract Data":
            required_cols = ['name', 'supplier', 'start_date', 'end_date']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                return {
                    "success": False, 
                    "message": f"Missing required columns: {', '.join(missing_cols)}.",
                    "detected_type": detect_template_type(uploaded_file)
                }
            
            # Convert date columns
            df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
            df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
        
        # Return processed data
        return {
            "success": True,
            "data": df,
            "rows_processed": len(df),
            "message": f"Successfully processed {len(df)} rows of {upload_type}."
        }
    
    except Exception as e:
        return {"success": False, "message": f"Error processing file: {str(e)}"}

def detect_template_type(uploaded_file):
    """Attempt to detect the template type based on column names"""
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        columns = set(df.columns.str.lower())
        
        # Check for spend data
        if {'date', 'supplier', 'category', 'amount'}.issubset(columns):
            return "Spend Data"
        
        # Check for supplier information
        if {'name', 'category', 'tier'}.issubset(columns):
            return "Supplier Information"
        
        # Check for risk assessment
        if {'supplier', 'assessment_date', 'overall_risk'}.issubset(columns) or \
           {'financial_risk', 'operational_risk'}.issubset(columns):
            return "Risk Assessment"
        
        # Check for ESG risk assessment
        if {'environmental_risk', 'social_risk', 'governance_risk'}.issubset(columns):
            return "ESG Risk Assessment"
        
        # Check for supplier performance
        if {'supplier', 'evaluation_date', 'overall_score'}.issubset(columns) or \
           {'schedule_adherence', 'work_quality'}.issubset(columns):
            return "Supplier Performance"
        
        # Check for contract data
        if {'name', 'supplier', 'start_date', 'end_date'}.issubset(columns):
            return "Contract Data"
        
        return None
    
    except:
        return None