import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import os

# Import local modules
from utils import (
    format_currency, format_percentage, format_date,
    get_risk_level, get_performance_level,
    risk_color, performance_color,
    create_download_link, plot_spend_by_category, plot_spend_trend,
    plot_supplier_risk_heatmap, plot_risk_radar, plot_performance_radar,
    plot_opportunity_matrix, create_metric_card, upload_file_handler,
    detect_template_type
)
from data_generator import (
    generate_spend_data, generate_risk_data, generate_performance_data,
    generate_contract_data, generate_risk_alerts, generate_opportunity_data,
    generate_improvement_data, generate_timeline_data
)
from db_connector import (
    check_db_connection, get_suppliers, get_categories, get_spend_data,
    get_risk_assessments, get_supplier_performance, get_contracts, get_risk_alerts
)
from config import (
    APP_NAME, APP_VERSION, APP_DESCRIPTION, DASHBOARD_CONFIG,
    DATABASE_CONFIG, RISK_LEVELS, PERFORMANCE_LEVELS, CHART_COLORS
)
from template_library import template_library

# Set up page configuration
st.set_page_config(
    page_title=f"{APP_NAME} v{APP_VERSION}",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #FF5722;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        margin-top: 0;
    }
    .module-header {
        font-size: 1.5rem;
        color: #2196F3;
        border-bottom: 2px solid #FF5722;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f8f9fa;
        border-left: 4px solid #FF5722;
        padding: 1rem;
        border-radius: 0.3rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F8F9FA;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF5722 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Application header
st.markdown(f'<h1 class="main-header">{APP_NAME}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">v{APP_VERSION} - {APP_DESCRIPTION}</p>', unsafe_allow_html=True)

# Data connection check
db_connected, db_message = check_db_connection()

# Sidebar configuration
# Use local logo file if exists, otherwise try to display a default icon
logo_path = "assets/arcadisprocure_logo.svg"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=200)
else:
    st.sidebar.title("ArcadiaProcure")
    st.sidebar.markdown("🏗️ **Construction Insights**")

st.sidebar.title("Navigation")

# Main navigation
app_mode = st.sidebar.radio(
    "Select Module:",
    ["Dashboard", "Materials Intelligence", "Vendor Risk", "Subcontractor Relationship", "Data Upload", "Templates"]
)

# Initial data loading or generation
@st.cache_data(ttl=3600)
def load_data():
    if db_connected and not DATABASE_CONFIG["use_mock_data"]:
        # Use database connection to load data
        try:
            suppliers_df = get_suppliers()
            categories_df = get_categories()
            spend_df = get_spend_data()
            risk_df = get_risk_assessments()
            performance_df = get_supplier_performance()
            contracts_df = get_contracts()
            risk_alerts_df = get_risk_alerts()
            
            # Generate additional data for modules that don't have DB tables yet
            opportunity_df = generate_opportunity_data()
            improvement_df = generate_improvement_data()
            timeline_df = generate_timeline_data()
            
            return {
                "suppliers": suppliers_df,
                "categories": categories_df,
                "spend_data": spend_df,
                "risk_data": risk_df,
                "performance_data": performance_df,
                "contracts": contracts_df,
                "risk_alerts": risk_alerts_df,
                "opportunity_data": opportunity_df,
                "improvement_data": improvement_df,
                "timeline_data": timeline_df
            }
        except Exception as e:
            st.sidebar.error(f"Error loading data: {str(e)}")
            # Fall back to generated data
            return generate_all_mock_data()
    else:
        # Use generated mock data
        return generate_all_mock_data()

def generate_all_mock_data():
    return {
        "spend_data": generate_spend_data(DATABASE_CONFIG["mock_data_size"]["spend_data"]),
        "risk_data": generate_risk_data(DATABASE_CONFIG["mock_data_size"]["suppliers"]),
        "performance_data": generate_performance_data(DATABASE_CONFIG["mock_data_size"]["suppliers"]),
        "contracts": generate_contract_data(DATABASE_CONFIG["mock_data_size"]["contracts"]),
        "risk_alerts": generate_risk_alerts(DATABASE_CONFIG["mock_data_size"]["risk_alerts"]),
        "opportunity_data": generate_opportunity_data(),
        "improvement_data": generate_improvement_data(),
        "timeline_data": generate_timeline_data()
    }

# Load or generate data
data = load_data()

# Status indicator in sidebar
if db_connected:
    st.sidebar.success("✅ Connected to database")
else:
    if DATABASE_CONFIG["use_mock_data"]:
        st.sidebar.info("ℹ️ Using simulated data (mock mode)")
    else:
        st.sidebar.warning(f"⚠️ {db_message}. Using simulated data.")

# Display date and application info in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Today's Date:** {datetime.now().strftime('%B %d, %Y')}")
st.sidebar.markdown(f"**Last Data Update:** {(datetime.now() - timedelta(days=1)).strftime('%B %d, %Y')}")
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    f"{APP_NAME} provides construction procurement professionals with powerful insights "
    f"for material category management, subcontractor risk assessment, and vendor relationship tracking "
    f"to optimize project costs and mitigate supply chain risks."
)

# Main application content
if app_mode == "Dashboard":
    st.markdown('<h2 class="module-header">Construction Procurement Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_spend = data["spend_data"]["amount"].sum()
        create_metric_card("Total Construction Materials Spend", total_spend, change=3.2, is_currency=True)
    
    with col2:
        avg_risk = data["risk_data"]["overall_risk"].mean()
        create_metric_card("Construction Vendor Risk Index", round(avg_risk, 1), change=-0.5)
    
    with col3:
        avg_performance = data["performance_data"]["overall_score"].mean()
        create_metric_card("Construction Subcontractor Performance", round(avg_performance, 1), change=1.2)
    
    with col4:
        contracts_expiring = len(data["contracts"][data["contracts"]["end_date"] <= datetime.now() + timedelta(days=90)])
        create_metric_card("Subcontract Agreements Expiring (90d)", contracts_expiring, prefix="")
    
    # Charts and insights
    st.markdown("### Construction Material Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Project Materials by CSI Division")
        st.plotly_chart(plot_spend_by_category(data["spend_data"]), use_container_width=True)
    
    with col2:
        st.subheader("Materials Cost Trend Analysis")
        st.plotly_chart(plot_spend_trend(data["spend_data"]), use_container_width=True)
    
    # Risk and Performance Overview
    st.markdown("### Subcontractor Risk & Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Trade Contractor Risk Assessment")
        st.plotly_chart(plot_supplier_risk_heatmap(data["risk_data"]), use_container_width=True)
    
    with col2:
        # Get top 3 suppliers by spend
        top_suppliers = data["spend_data"].groupby('supplier')['amount'].sum().nlargest(3).index.tolist()
        st.subheader("Key Vendor Performance Metrics")
        st.plotly_chart(plot_performance_radar(data["performance_data"], top_suppliers), use_container_width=True)
    
    # Alerts and notifications
    st.markdown("### Construction Project Alerts")
    
    alerts = data["risk_alerts"].sort_values("date", ascending=False).head(5)
    for _, alert in alerts.iterrows():
        severity_color = {
            "High": "#F44336",
            "Medium": "#FF9800",
            "Low": "#4CAF50"
        }.get(alert["severity"], "#808080")
        
        st.markdown(f"""
        <div style="border-left: 4px solid {severity_color}; padding: 0.5rem 1rem; margin-bottom: 0.5rem; background-color: #f8f9fa;">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-weight: bold;">{alert["alert_type"]} Alert - {alert["supplier"]}</span>
                <span style="color: {severity_color}; font-weight: bold;">{alert["severity"]}</span>
            </div>
            <div>{alert["description"]}</div>
            <div style="font-size: 0.8rem; color: #666;">Project Impact: {alert.get("project_impact", "Medium")} | {format_date(alert["date"])}</div>
        </div>
        """, unsafe_allow_html=True)

elif app_mode == "Materials Intelligence":
    st.markdown('<h2 class="module-header">Construction Materials & Equipment Intelligence</h2>', unsafe_allow_html=True)
    
    # Filters
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Get unique categories from the data
        categories = sorted(data["spend_data"]["category"].unique())
        selected_category = st.selectbox("Select Category", categories)
        
        # Date range selector
        date_range = st.date_input(
            "Date Range",
            value=[
                datetime.now() - timedelta(days=365),
                datetime.now()
            ]
        )
        
        # Apply filters
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_spend = data["spend_data"][
                (data["spend_data"]["category"] == selected_category) &
                (data["spend_data"]["date"] >= pd.Timestamp(start_date)) &
                (data["spend_data"]["date"] <= pd.Timestamp(end_date))
            ]
        else:
            filtered_spend = data["spend_data"][data["spend_data"]["category"] == selected_category]
    
    # Main content area
    with col2:
        # Key metrics for the selected category
        category_spend = filtered_spend["amount"].sum()
        category_count = len(filtered_spend)
        avg_invoice = category_spend / category_count if category_count > 0 else 0
        
        cols = st.columns(3)
        with cols[0]:
            create_metric_card(f"{selected_category} Total Spend", category_spend, is_currency=True)
        
        with cols[1]:
            category_pct = (category_spend / data["spend_data"]["amount"].sum()) * 100
            create_metric_card(f"% of Total Spend", category_pct, is_percentage=True)
        
        with cols[2]:
            create_metric_card("Avg. Invoice Value", avg_invoice, is_currency=True)
        
        # Spend analysis
        st.markdown("#### Spend Analysis")
        
        tabs = st.tabs(["Time Trend", "Vendor Distribution", "Invoice Analysis"])
        
        with tabs[0]:
            st.plotly_chart(plot_spend_trend(filtered_spend), use_container_width=True)
        
        with tabs[1]:
            supplier_spend = filtered_spend.groupby('supplier')['amount'].sum().reset_index()
            supplier_spend = supplier_spend.sort_values('amount', ascending=False)
            
            fig = px.bar(
                supplier_spend, 
                x='supplier', 
                y='amount',
                color='amount',
                color_continuous_scale="Viridis",
                title=f"Spend by Supplier for {selected_category}"
            )
            fig.update_layout(xaxis_title="Supplier", yaxis_title="Spend Amount")
            st.plotly_chart(fig, use_container_width=True)
        
        with tabs[2]:
            # Create a histogram of invoice amounts
            fig = px.histogram(
                filtered_spend, 
                x="amount", 
                nbins=20,
                title=f"Invoice Amount Distribution for {selected_category}"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show the top 10 invoices
            st.markdown("##### Top Invoices")
            top_invoices = filtered_spend.sort_values("amount", ascending=False).head(10)
            
            for _, invoice in top_invoices.iterrows():
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span><strong>Invoice {invoice.get('invoice_number', 'N/A')}</strong> - {invoice['supplier']}</span>
                        <span style="color: #FF5722; font-weight: bold;">{format_currency(invoice['amount'])}</span>
                    </div>
                    <div style="font-size: 0.9rem; color: #666;">{format_date(invoice['date'])}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Download data option
        st.markdown("#### Export Data")
        st.markdown(create_download_link(filtered_spend, f"{selected_category}_spend_data.csv"), unsafe_allow_html=True)

elif app_mode == "Vendor Risk":
    st.markdown('<h2 class="module-header">Construction Vendor Risk Assessment</h2>', unsafe_allow_html=True)
    
    # Vendor selection
    suppliers = sorted(data["risk_data"]["supplier"].unique())
    selected_supplier = st.selectbox("Select Vendor", suppliers)
    
    # Get supplier data
    supplier_risk = data["risk_data"][data["risk_data"]["supplier"] == selected_supplier].iloc[0]
    
    # Risk rating and summary
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Overall risk score display
        overall_score = supplier_risk["overall_risk"]
        risk_level = get_risk_level(overall_score)
        risk_color_hex = risk_color(risk_level)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 20px;">
            <div style="font-size: 4rem; font-weight: 700; color: {risk_color_hex};">{overall_score:.1f}</div>
            <div style="font-size: 1.5rem; text-transform: uppercase; font-weight: 600; color: {risk_color_hex};">
                {RISK_LEVELS[risk_level]["label"]} RISK
            </div>
            <div style="font-size: 1rem; color: #666;">Overall Risk Score</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk category scores
        categories = [
            {"name": "Financial", "score": supplier_risk["financial_risk"]},
            {"name": "Operational", "score": supplier_risk["operational_risk"]},
            {"name": "Compliance", "score": supplier_risk["compliance_risk"]},
            {"name": "Geopolitical", "score": supplier_risk["geopolitical_risk"]},
            {"name": "Environmental", "score": supplier_risk["environmental_risk"]},
            {"name": "Social", "score": supplier_risk["social_risk"]},
            {"name": "Governance", "score": supplier_risk["governance_risk"]}
        ]
        
        st.markdown("### Risk Categories")
        
        for category in categories:
            cat_risk_level = get_risk_level(category["score"])
            cat_color = risk_color(cat_risk_level)
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>{category["name"]}</span>
                <span style="font-weight: bold; color: {cat_color};">{category["score"]:.1f}</span>
            </div>
            <div style="height: 6px; background-color: #e0e0e0; border-radius: 3px; margin-bottom: 15px;">
                <div style="width: {category["score"]*10}%; height: 6px; background-color: {cat_color}; border-radius: 3px;"></div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Tabs for different risk aspects
        tabs = st.tabs(["Risk Breakdown", "Alerts", "Mitigation Actions"])
        
        with tabs[0]:
            st.plotly_chart(plot_risk_radar(supplier_risk), use_container_width=True)
            
            # Risk factors
            st.markdown("#### Key Risk Factors")
            
            risk_factors = [
                {
                    "name": "Material Delay Probability",
                    "score": supplier_risk.get("material_delay_probability", 6.8),
                    "description": "Likelihood of construction material delivery delays based on historical performance and current supply chain conditions."
                },
                {
                    "name": "Schedule Impact",
                    "score": supplier_risk.get("schedule_impact", 7.2),
                    "description": "Potential impact on construction schedule if this vendor fails to deliver on time or encounters disruptions."
                },
                {
                    "name": "Quality Consistency",
                    "score": supplier_risk.get("quality_consistency", 4.5),
                    "description": "Consistency of material/service quality based on inspections, defect rates, and field performance."
                },
                {
                    "name": "Financial Stability",
                    "score": supplier_risk.get("financial_stability", 5.9),
                    "description": "Vendor's financial health including liquidity, profitability, and debt metrics that could affect operations."
                },
                {
                    "name": "Safety Compliance",
                    "score": supplier_risk.get("safety_compliance", 3.8),
                    "description": "Adherence to safety protocols, incident rates, and compliance with construction safety regulations."
                }
            ]
            
            for factor in risk_factors:
                risk_lvl = get_risk_level(factor["score"])
                factor_color = risk_color(risk_lvl)
                
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="font-weight: bold;">{factor["name"]}</span>
                        <span style="font-weight: bold; color: {factor_color};">{factor["score"]:.1f}</span>
                    </div>
                    <div style="height: 6px; background-color: #e0e0e0; border-radius: 3px; margin-bottom: 10px;">
                        <div style="width: {factor["score"]*10}%; height: 6px; background-color: {factor_color}; border-radius: 3px;"></div>
                    </div>
                    <div style="font-size: 0.9rem; color: #666;">{factor["description"]}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with tabs[1]:
            # Get alerts for this supplier
            supplier_alerts = data["risk_alerts"][data["risk_alerts"]["supplier"] == selected_supplier]
            supplier_alerts = supplier_alerts.sort_values("date", ascending=False)
            
            if len(supplier_alerts) > 0:
                for _, alert in supplier_alerts.iterrows():
                    severity_color = {
                        "High": "#F44336",
                        "Medium": "#FF9800",
                        "Low": "#4CAF50"
                    }.get(alert["severity"], "#808080")
                    
                    st.markdown(f"""
                    <div style="border-left: 4px solid {severity_color}; padding: 1rem; margin-bottom: 1rem; background-color: #f8f9fa;">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="font-weight: bold;">{alert["alert_type"]} Alert</span>
                            <span style="color: {severity_color}; font-weight: bold;">{alert["severity"]}</span>
                        </div>
                        <div style="margin: 0.5rem 0;">{alert["description"]}</div>
                        <div style="font-size: 0.8rem; color: #666;">
                            Detected: {format_date(alert["date"])} | 
                            Status: {alert.get("status", "Open")}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No alerts found for this vendor.")
        
        with tabs[2]:
            # Mitigation actions - this would typically come from a database
            # Using mock data for demonstration
            mitigation_actions = [
                {
                    "action": "Implement Dual Sourcing Strategy",
                    "status": "In Progress",
                    "description": "Identify and onboard backup suppliers for critical construction materials to reduce dependency risks.",
                    "priority": "High",
                    "owner": "Procurement Team",
                    "due_date": datetime.now() + timedelta(days=30)
                },
                {
                    "action": "Increase Safety Audit Frequency",
                    "status": "Scheduled",
                    "description": "Double the frequency of on-site safety audits for this vendor's work and document improvements.",
                    "priority": "Medium",
                    "owner": "Safety Department",
                    "due_date": datetime.now() + timedelta(days=14)
                },
                {
                    "action": "Require Weekly Schedule Updates",
                    "status": "Active",
                    "description": "Implement mandatory weekly schedule updates and progress reports to identify potential delays early.",
                    "priority": "High",
                    "owner": "Project Manager",
                    "due_date": datetime.now() + timedelta(days=7)
                },
                {
                    "action": "Review Contract Terms",
                    "status": "Not Started",
                    "description": "Review and potentially renegotiate contract terms to include stricter performance guarantees and penalties.",
                    "priority": "Medium",
                    "owner": "Legal Department",
                    "due_date": datetime.now() + timedelta(days=45)
                }
            ]
            
            for action in mitigation_actions:
                status_color = {
                    "Active": "#4CAF50",
                    "In Progress": "#2196F3",
                    "Scheduled": "#FFC107",
                    "Not Started": "#9E9E9E",
                    "Completed": "#673AB7"
                }.get(action["status"], "#9E9E9E")
                
                priority_color = {
                    "High": "#F44336",
                    "Medium": "#FF9800",
                    "Low": "#4CAF50"
                }.get(action["priority"], "#9E9E9E")
                
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="font-weight: bold;">{action["action"]}</span>
                        <span style="background-color: {status_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;">
                            {action["status"]}
                        </span>
                    </div>
                    <div style="margin: 10px 0; color: #333;">{action["description"]}</div>
                    <div style="display: flex; flex-wrap: wrap; gap: 15px; font-size: 0.9rem; color: #666;">
                        <div>
                            <span style="font-weight: bold;">Priority:</span> 
                            <span style="color: {priority_color};">{action["priority"]}</span>
                        </div>
                        <div>
                            <span style="font-weight: bold;">Owner:</span> {action["owner"]}
                        </div>
                        <div>
                            <span style="font-weight: bold;">Due:</span> {format_date(action["due_date"])}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

elif app_mode == "Subcontractor Relationship":
    st.markdown('<h2 class="module-header">Construction Subcontractor Relationship Management</h2>', unsafe_allow_html=True)
    
    # Supplier selection
    suppliers = sorted(data["performance_data"]["supplier"].unique())
    selected_supplier = st.selectbox("Select Subcontractor", suppliers)
    
    # Get supplier data
    supplier_performance = data["performance_data"][data["performance_data"]["supplier"] == selected_supplier].iloc[0]
    
    # Performance rating and summary
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Overall performance score display
        overall_score = supplier_performance["overall_score"]
        performance_level = get_performance_level(overall_score)
        perf_color_hex = performance_color(performance_level)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 20px;">
            <div style="font-size: 4rem; font-weight: 700; color: {perf_color_hex};">{overall_score:.1f}</div>
            <div style="font-size: 1.5rem; text-transform: uppercase; font-weight: 600; color: {perf_color_hex};">
                {PERFORMANCE_LEVELS[performance_level]["label"]}
            </div>
            <div style="font-size: 1rem; color: #666;">Overall Performance Score</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Supplier info card
        st.markdown(f"""
        <div style="background-color: #f8f9fa; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
            <h3 style="margin-top: 0;">Vendor Information</h3>
            <div style="margin: 10px 0;"><strong>Type:</strong> {supplier_performance.get("supplier_type", "General Contractor")}</div>
            <div style="margin: 10px 0;"><strong>Category:</strong> {supplier_performance.get("category", "Construction Services")}</div>
            <div style="margin: 10px 0;"><strong>Active Projects:</strong> {supplier_performance.get("active_projects", 3)}</div>
            <div style="margin: 10px 0;"><strong>Relationship:</strong> {supplier_performance.get("relationship_length", "3-5 years")}</div>
            <div style="margin: 10px 0;"><strong>Annual Spend:</strong> {format_currency(supplier_performance.get("annual_spend", 1200000))}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Tabs for different performance aspects
        tabs = st.tabs(["Performance Metrics", "Contracts", "Improvement Opportunities"])
        
        with tabs[0]:
            st.plotly_chart(plot_performance_radar(data["performance_data"], [selected_supplier]), use_container_width=True)
            
            # Performance categories
            categories = [
                {"name": "Schedule Adherence", "score": supplier_performance["schedule_adherence"]},
                {"name": "Work Quality", "score": supplier_performance["work_quality"]},
                {"name": "Cost Control", "score": supplier_performance["cost_control"]},
                {"name": "Safety Performance", "score": supplier_performance["safety_performance"]},
                {"name": "Documentation", "score": supplier_performance["documentation"]},
                {"name": "Communication", "score": supplier_performance["communication"]},
                {"name": "Problem Resolution", "score": supplier_performance["problem_resolution"]}
            ]
            
            st.markdown("#### Performance Categories")
            
            col1, col2 = st.columns(2)
            
            for i, category in enumerate(categories):
                perf_level = get_performance_level(category["score"])
                cat_color = performance_color(perf_level)
                
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                    <div style="margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span>{category["name"]}</span>
                            <span style="font-weight: bold; color: {cat_color};">{category["score"]:.1f}</span>
                        </div>
                        <div style="height: 6px; background-color: #e0e0e0; border-radius: 3px;">
                            <div style="width: {category["score"]*10}%; height: 6px; background-color: {cat_color}; border-radius: 3px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tabs[1]:
            # Get contracts for this supplier - would typically come from database
            # Mocking for demonstration
            supplier_contracts = data["contracts"][data["contracts"]["supplier"] == selected_supplier]
            
            if len(supplier_contracts) > 0:
                for _, contract in supplier_contracts.iterrows():
                    status = contract.get("status", "Active")
                    status_color = {
                        "Active": "#4CAF50",
                        "Expired": "#F44336", 
                        "Pending": "#FFC107"
                    }.get(status, "#9E9E9E")
                    
                    expiry_date = contract.get("end_date", datetime.now() + timedelta(days=180))
                    days_to_expiry = (expiry_date - datetime.now()).days
                    expiry_class = ""
                    
                    if days_to_expiry < 0:
                        expiry_text = "Expired"
                        expiry_class = "color: #F44336; font-weight: bold;"
                    elif days_to_expiry < 30:
                        expiry_text = f"Expires in {days_to_expiry} days"
                        expiry_class = "color: #F44336; font-weight: bold;"
                    elif days_to_expiry < 90:
                        expiry_text = f"Expires in {days_to_expiry} days"
                        expiry_class = "color: #FF9800; font-weight: bold;"
                    else:
                        expiry_text = f"Expires in {days_to_expiry} days"
                    
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: bold; font-size: 1.1rem;">{contract.get("name", "Construction Services Agreement")}</span>
                            <span style="background-color: {status_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;">
                                {status}
                            </span>
                        </div>
                        <div style="display: flex; flex-wrap: wrap; gap: 20px; margin: 10px 0; color: #666;">
                            <div>
                                <div style="font-weight: bold;">Contract Value</div>
                                <div>{format_currency(contract.get("value", 750000))}</div>
                            </div>
                            <div>
                                <div style="font-weight: bold;">Start Date</div>
                                <div>{format_date(contract.get("start_date", datetime.now() - timedelta(days=180)))}</div>
                            </div>
                            <div>
                                <div style="font-weight: bold;">End Date</div>
                                <div style="{expiry_class}">{format_date(expiry_date)} <br/> {expiry_text}</div>
                            </div>
                            <div>
                                <div style="font-weight: bold;">Type</div>
                                <div>{contract.get("type", "Fixed Price")}</div>
                            </div>
                        </div>
                        <div style="margin: 10px 0;">
                            <div style="font-weight: bold;">Description</div>
                            <div style="color: #333;">{contract.get("description", "General construction services for commercial projects.")}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No contracts found for this vendor.")
        
        with tabs[2]:
            # Improvement opportunities - would typically come from analytics
            # Mocking for demonstration
            improvement_data = data.get("improvement_data", [])
            supplier_improvements = [item for item in improvement_data if item.get("supplier") == selected_supplier]
            
            if supplier_improvements:
                for improvement in supplier_improvements:
                    impact_level = improvement.get("impact", "Medium")
                    impact_color = {
                        "High": "#F44336",
                        "Medium": "#FF9800",
                        "Low": "#4CAF50"
                    }.get(impact_level, "#9E9E9E")
                    
                    effort_level = improvement.get("effort", "Medium")
                    effort_color = {
                        "High": "#F44336", 
                        "Medium": "#FF9800",
                        "Low": "#4CAF50"
                    }.get(effort_level, "#9E9E9E")
                    
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: bold; font-size: 1.1rem;">{improvement.get("title", "Improvement Opportunity")}</span>
                        </div>
                        <div style="margin: 10px 0; color: #333;">{improvement.get("description", "No description provided")}</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 20px; margin: 10px 0; font-size: 0.9rem;">
                            <div>
                                <span style="font-weight: bold;">Category:</span> {improvement.get("category", "Performance")}
                            </div>
                            <div>
                                <span style="font-weight: bold;">Impact:</span> 
                                <span style="color: {impact_color};">{impact_level}</span>
                            </div>
                            <div>
                                <span style="font-weight: bold;">Implementation Effort:</span> 
                                <span style="color: {effort_color};">{effort_level}</span>
                            </div>
                            <div>
                                <span style="font-weight: bold;">Estimated Savings:</span> 
                                {format_currency(improvement.get("savings", 50000))}
                            </div>
                        </div>
                        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; margin-top: 10px;">
                            <div style="font-weight: bold;">Implementation Steps:</div>
                            <ol style="margin: 5px 0 0 20px; padding: 0;">
                                {' '.join(['<li>' + step + '</li>' for step in improvement.get("steps", ["No steps defined"])])}
                            </ol>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No improvement opportunities identified for this vendor.")

elif app_mode == "Data Upload":
    st.markdown('<h2 class="module-header">Upload Construction Procurement Data</h2>', unsafe_allow_html=True)
    
    # Instructions
    st.markdown("""
    <div class="info-box">
        <p>Upload your construction procurement and supply chain data files to analyze and visualize insights.</p>
        <p>Supported file formats: CSV, Excel (.xlsx, .xls)</p>
        <p>For best results, use the template files available in the Templates section.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload options
    upload_type = st.selectbox(
        "Select Data Type",
        [
            "Spend Data", 
            "Supplier Information", 
            "Risk Assessment",
            "Supplier Performance", 
            "Contract Data"
        ]
    )
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            # Process the uploaded file
            result = upload_file_handler(uploaded_file, upload_type)
            
            if result["success"]:
                st.success(f"File processed successfully! Imported {result['rows_processed']} rows of data.")
                
                # Display preview of the data
                st.subheader("Data Preview")
                st.dataframe(result["data"].head(10))
                
                # Show summary statistics
                if upload_type == "Spend Data":
                    st.subheader("Summary Statistics")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        total_spend = result["data"]["amount"].sum()
                        create_metric_card("Total Spend", total_spend, is_currency=True)
                    
                    with col2:
                        avg_spend = result["data"]["amount"].mean()
                        create_metric_card("Average Transaction", avg_spend, is_currency=True)
                    
                    with col3:
                        supplier_count = result["data"]["supplier"].nunique()
                        create_metric_card("Unique Suppliers", supplier_count)
                    
                    # Show a quick chart
                    if len(result["data"]) > 0:
                        st.subheader("Quick Visualization")
                        
                        chart_type = st.selectbox(
                            "Select Chart Type",
                            ["Category Breakdown", "Supplier Breakdown", "Time Trend"]
                        )
                        
                        if chart_type == "Category Breakdown":
                            st.plotly_chart(plot_spend_by_category(result["data"]), use_container_width=True)
                        elif chart_type == "Supplier Breakdown":
                            supplier_spend = result["data"].groupby('supplier')['amount'].sum().reset_index()
                            supplier_spend = supplier_spend.sort_values('amount', ascending=False)
                            
                            fig = px.bar(
                                supplier_spend, 
                                x='supplier', 
                                y='amount',
                                color='amount',
                                title="Spend by Supplier"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.plotly_chart(plot_spend_trend(result["data"]), use_container_width=True)
            else:
                st.error(f"Error processing file: {result['message']}")
                
                if "detected_type" in result:
                    st.warning(f"The file appears to be a {result['detected_type']} template. Please select the correct data type.")
                
                # Show template recommendation
                template_type = detect_template_type(uploaded_file)
                if template_type:
                    st.info(f"This looks like a {template_type} file. Try selecting '{template_type}' as the data type.")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # File instructions based on type
    with st.expander("File Format Instructions"):
        if upload_type == "Spend Data":
            st.markdown("""
            ### Spend Data Format
            Your file should include the following columns:
            - `date` - Transaction date (YYYY-MM-DD)
            - `supplier` - Supplier/vendor name
            - `category` - Spend category
            - `subcategory` - Subcategory (optional)
            - `project` - Project ID or name
            - `amount` - Transaction amount
            - `invoice_number` - Invoice reference (optional)
            - `description` - Transaction description (optional)
            """)
            
        elif upload_type == "Supplier Information":
            st.markdown("""
            ### Supplier Information Format
            Your file should include the following columns:
            - `name` - Supplier company name
            - `category` - Primary category
            - `tier` - Supplier tier (1, 2, 3)
            - `status` - Status (active, inactive, pending)
            - `segment` - Segment (strategic, tactical, transactional)
            - `annual_spend` - Annual spend with supplier
            - `relationship_start` - Relationship start date (YYYY-MM-DD)
            - `contact_name` - Primary contact name (optional)
            - `contact_email` - Primary contact email (optional)
            - `location` - Primary location/address (optional)
            """)
            
        elif upload_type == "Risk Assessment":
            st.markdown("""
            ### Risk Assessment Format
            Your file should include the following columns:
            - `supplier` - Supplier name
            - `assessment_date` - Assessment date (YYYY-MM-DD)
            - `financial_risk` - Financial risk score (0-10)
            - `operational_risk` - Operational risk score (0-10)
            - `compliance_risk` - Compliance risk score (0-10)
            - `geopolitical_risk` - Geopolitical risk score (0-10)
            - `environmental_risk` - Environmental risk score (0-10)
            - `social_risk` - Social risk score (0-10)
            - `governance_risk` - Governance risk score (0-10)
            - `overall_risk` - Overall risk score (0-10) or leave blank to calculate
            - `notes` - Assessment notes (optional)
            """)
            
        elif upload_type == "Supplier Performance":
            st.markdown("""
            ### Supplier Performance Format
            Your file should include the following columns:
            - `supplier` - Supplier name
            - `evaluation_date` - Evaluation date (YYYY-MM-DD)
            - `schedule_adherence` - Schedule score (0-10)
            - `work_quality` - Quality score (0-10)
            - `cost_control` - Cost control score (0-10)
            - `safety_performance` - Safety score (0-10)
            - `documentation` - Documentation score (0-10)
            - `communication` - Communication score (0-10)
            - `problem_resolution` - Problem resolution score (0-10)
            - `overall_score` - Overall score (0-10) or leave blank to calculate
            - `evaluator` - Evaluator name (optional)
            - `comments` - Evaluation comments (optional)
            """)
            
        elif upload_type == "Contract Data":
            st.markdown("""
            ### Contract Data Format
            Your file should include the following columns:
            - `name` - Contract name
            - `supplier` - Supplier name
            - `type` - Contract type (e.g., fixed price, unit price, etc.)
            - `start_date` - Start date (YYYY-MM-DD)
            - `end_date` - End date (YYYY-MM-DD)
            - `value` - Contract value
            - `status` - Status (active, expired, pending)
            - `description` - Contract description (optional)
            - `category` - Contract category (optional)
            - `auto_renewal` - Auto-renewal flag (true/false, optional)
            - `notice_period_days` - Notice period in days (optional)
            """)

elif app_mode == "Templates":
    template_library()

# Define a function to help with project impact (referenced in Dashboard section)
def get_project_impact(alert):
    """Get project impact from alert data"""
    return alert.get("project_impact", "Medium")