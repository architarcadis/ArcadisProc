"""
Template Library for ArcadisProcure Insights
Provides downloadable template files for various data imports
"""

import streamlit as st
import pandas as pd
import numpy as np
import base64
import io
from datetime import datetime, timedelta

def get_binary_file_downloader_html(file_path, file_label):
    """
    Generate HTML for a file download link
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_path}">Download {file_label}</a>'
        return href
    except Exception as e:
        # Generate file on the fly if it doesn't exist
        if "spend_data" in file_path:
            return generate_spend_template(file_path, file_label)
        elif "supplier" in file_path:
            return generate_supplier_template(file_path, file_label)
        elif "risk_assessment" in file_path:
            return generate_risk_template(file_path, file_label)
        elif "performance" in file_path:
            return generate_performance_template(file_path, file_label)
        elif "contract" in file_path:
            return generate_contract_template(file_path, file_label)
        else:
            return f"Error: {str(e)}"

def generate_spend_template(file_path, file_label):
    """Generate spend data template"""
    df = pd.DataFrame({
        'date': ['YYYY-MM-DD'],
        'supplier': ['Supplier Name'],
        'category': ['Material Category'],
        'subcategory': ['Material Subcategory'],
        'project': ['Project Name'],
        'amount': [1000.00],
        'invoice_number': ['INV-12345'],
        'payment_terms': ['Net 30'],
        'description': ['Material description']
    })
    csv = df.to_csv(index=False)
    bin_str = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{bin_str}" download="{file_path}">Download {file_label}</a>'
    return href

def generate_supplier_template(file_path, file_label):
    """Generate supplier template"""
    df = pd.DataFrame({
        'name': ['Supplier Name'],
        'category': ['Primary Category'],
        'tier': ['Tier 1 (Prime)'],
        'status': ['active'],
        'segment': ['strategic'],
        'annual_spend': [1000000],
        'relationship_start': ['YYYY-MM-DD'],
        'contact_name': ['Contact Name'],
        'contact_email': ['email@example.com'],
        'location': ['City, State']
    })
    csv = df.to_csv(index=False)
    bin_str = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{bin_str}" download="{file_path}">Download {file_label}</a>'
    return href

def generate_risk_template(file_path, file_label):
    """Generate risk assessment template"""
    df = pd.DataFrame({
        'supplier': ['Supplier Name'],
        'assessment_date': ['YYYY-MM-DD'],
        'financial_risk': [5.0],
        'operational_risk': [5.0],
        'compliance_risk': [5.0],
        'geopolitical_risk': [5.0],
        'environmental_risk': [5.0],
        'social_risk': [5.0],
        'governance_risk': [5.0],
        'overall_risk': [5.0],
        'notes': ['Assessment notes']
    })
    csv = df.to_csv(index=False)
    bin_str = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{bin_str}" download="{file_path}">Download {file_label}</a>'
    return href

def generate_performance_template(file_path, file_label):
    """Generate performance template"""
    df = pd.DataFrame({
        'supplier': ['Supplier Name'],
        'evaluation_date': ['YYYY-MM-DD'],
        'schedule_adherence': [7.0],
        'work_quality': [7.0],
        'cost_control': [7.0],
        'safety_performance': [7.0],
        'documentation': [7.0],
        'communication': [7.0],
        'problem_resolution': [7.0],
        'overall_score': [7.0],
        'evaluator': ['Evaluator Name'],
        'comments': ['Evaluation comments']
    })
    csv = df.to_csv(index=False)
    bin_str = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{bin_str}" download="{file_path}">Download {file_label}</a>'
    return href

def generate_contract_template(file_path, file_label):
    """Generate contract template"""
    df = pd.DataFrame({
        'name': ['Contract Name'],
        'supplier': ['Supplier Name'],
        'type': ['Fixed Price'],
        'start_date': ['YYYY-MM-DD'],
        'end_date': ['YYYY-MM-DD'],
        'value': [1000000],
        'status': ['active'],
        'description': ['Contract description'],
        'category': ['Contract category'],
        'auto_renewal': [False],
        'notice_period_days': [30]
    })
    csv = df.to_csv(index=False)
    bin_str = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{bin_str}" download="{file_path}">Download {file_label}</a>'
    return href

def generate_risk_alert_template(file_path, file_label):
    """Generate risk alert template"""
    df = pd.DataFrame({
        'supplier': ['Supplier Name'],
        'date': ['YYYY-MM-DD'],
        'alert_type': ['Alert Type'],
        'description': ['Alert description'],
        'severity': ['Medium'],
        'status': ['Open'],
        'project': ['Project Name'],
        'project_impact': ['Medium']
    })
    csv = df.to_csv(index=False)
    bin_str = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{bin_str}" download="{file_path}">Download {file_label}</a>'
    return href

def generate_category_mapping_template(file_path, file_label):
    """Generate category mapping template"""
    df = pd.DataFrame({
        'category_code': ['CAT001'],
        'category_name': ['Category Name'],
        'parent_category': [''],
        'description': ['Category description'],
        'industry': ['Construction']
    })
    csv = df.to_csv(index=False)
    bin_str = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{bin_str}" download="{file_path}">Download {file_label}</a>'
    return href

def generate_price_index_template(file_path, file_label):
    """Generate price index template"""
    dates = [(datetime.now() - timedelta(days=30*i)).strftime('%Y-%m-%d') for i in range(12)]
    df = pd.DataFrame({
        'date': dates,
        'material': ['Concrete'] * 12,
        'index_value': [100 + i for i in range(12)],
        'category': ['Structural Materials'] * 12,
        'region': ['National'] * 12,
        'source': ['PPI'] * 12
    })
    csv = df.to_csv(index=False)
    bin_str = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{bin_str}" download="{file_path}">Download {file_label}</a>'
    return href

def generate_market_intelligence_template(file_path, file_label):
    """Generate market intelligence template"""
    df = pd.DataFrame({
        'date': ['YYYY-MM-DD'],
        'category': ['Category Name'],
        'subcategory': ['Subcategory Name'],
        'insight_type': ['Market Trend'],
        'title': ['Insight Title'],
        'description': ['Detailed description of market insight'],
        'source': ['Source name'],
        'impact_level': ['Medium'],
        'tags': ['tag1, tag2']
    })
    csv = df.to_csv(index=False)
    bin_str = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{bin_str}" download="{file_path}">Download {file_label}</a>'
    return href

def generate_esg_risk_template(file_path, file_label):
    """Generate ESG risk assessment template"""
    df = pd.DataFrame({
        'supplier': ['Supplier Name'],
        'assessment_date': ['YYYY-MM-DD'],
        'environmental_score': [7.0],
        'carbon_footprint': [6.5],
        'water_usage': [7.5],
        'waste_management': [7.0],
        'social_score': [7.0],
        'labor_practices': [7.0],
        'community_impact': [6.5],
        'health_safety': [7.5],
        'governance_score': [7.0],
        'ethics_compliance': [7.0],
        'transparency': [7.5],
        'overall_esg_score': [7.0],
        'notes': ['Assessment notes']
    })
    csv = df.to_csv(index=False)
    bin_str = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{bin_str}" download="{file_path}">Download {file_label}</a>'
    return href

def template_library():
    """
    Display and provide downloads for available templates
    """
    st.markdown('<h2 class="module-header">Construction Data Templates</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <p>Download template files for standardized data collection and import.</p>
        <p>Fill in the templates with your construction procurement data and upload through the Data Upload section.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Template categories
    template_category = st.selectbox(
        "Select Template Category",
        ["Spend & Cost Data", "Supplier Management", "Risk Management", "Contract Management", "Market Intelligence"]
    )
    
    if template_category == "Spend & Cost Data":
        st.markdown("### Spend Data Templates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Spend Data Template")
            st.markdown("Import historical construction spend data with this template.")
            st.markdown(generate_spend_template("spend_data_template.csv", "Spend Data Template"), unsafe_allow_html=True)
            
            st.markdown("##### Required Fields:")
            st.markdown("""
            - `date` - Transaction date
            - `supplier` - Supplier name
            - `category` - Construction material category
            - `amount` - Transaction amount
            """)
        
        with col2:
            st.markdown("#### Category Mapping Template")
            st.markdown("Define your custom construction material category hierarchy.")
            st.markdown(generate_category_mapping_template("category_mapping_template.csv", "Category Mapping Template"), unsafe_allow_html=True)
            
            st.markdown("##### Required Fields:")
            st.markdown("""
            - `category_code` - Unique category identifier
            - `category_name` - Category display name
            - `parent_category` - Parent category (if applicable)
            """)
        
        st.markdown("### Price Indices")
        st.markdown("Import material price index data for forecasting and benchmarking.")
        st.markdown(generate_price_index_template("price_index_template.csv", "Price Index Template"), unsafe_allow_html=True)
    
    elif template_category == "Supplier Management":
        st.markdown("### Supplier Management Templates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Supplier Information Template")
            st.markdown("Import construction supplier/vendor master data.")
            st.markdown(generate_supplier_template("supplier_template.csv", "Supplier Template"), unsafe_allow_html=True)
            
            st.markdown("##### Required Fields:")
            st.markdown("""
            - `name` - Supplier company name
            - `category` - Primary construction category
            - `tier` - Supplier tier (Tier 1, 2, 3)
            - `status` - Status (active, inactive, pending)
            """)
        
        with col2:
            st.markdown("#### Supplier Performance Template")
            st.markdown("Import construction subcontractor performance evaluations.")
            st.markdown(generate_performance_template("supplier_performance_template.csv", "Performance Template"), unsafe_allow_html=True)
            
            st.markdown("##### Required Fields:")
            st.markdown("""
            - `supplier` - Supplier name
            - `evaluation_date` - Date of performance evaluation
            - Performance metrics (0-10 scale)
            - `evaluator` - Person conducting evaluation
            """)
    
    elif template_category == "Risk Management":
        st.markdown("### Risk Management Templates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Risk Assessment Template")
            st.markdown("Import construction-specific supplier risk assessments.")
            st.markdown(generate_risk_template("risk_assessment_template.csv", "Risk Assessment Template"), unsafe_allow_html=True)
            
            st.markdown("##### Required Fields:")
            st.markdown("""
            - `supplier` - Supplier name
            - `assessment_date` - Assessment date
            - Risk category scores (0-10 scale)
            """)
            
            st.markdown("#### Risk Alert Template")
            st.markdown("Import construction risk alerts and notifications.")
            st.markdown(generate_risk_alert_template("risk_alert_template.csv", "Risk Alert Template"), unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### ESG Risk Assessment Template")
            st.markdown("Import construction supplier ESG (Environmental, Social, Governance) risk data.")
            st.markdown(generate_esg_risk_template("esg_risk_assessment_template.csv", "ESG Risk Template"), unsafe_allow_html=True)
            
            st.markdown("##### Required Fields:")
            st.markdown("""
            - `supplier` - Supplier name
            - `assessment_date` - Assessment date
            - Environmental, Social, and Governance scores (0-10 scale)
            """)
    
    elif template_category == "Contract Management":
        st.markdown("### Contract Management Templates")
        
        st.markdown("#### Contract Template")
        st.markdown("Import construction contract data for suppliers and subcontractors.")
        st.markdown(generate_contract_template("contract_template.csv", "Contract Template"), unsafe_allow_html=True)
        
        st.markdown("##### Required Fields:")
        st.markdown("""
        - `name` - Contract name
        - `supplier` - Supplier name
        - `type` - Contract type (e.g., Fixed Price, GMP, etc.)
        - `start_date` - Start date
        - `end_date` - End date
        - `value` - Contract value
        - `status` - Status (active, expired, pending)
        """)
    
    elif template_category == "Market Intelligence":
        st.markdown("### Market Intelligence Templates")
        
        st.markdown("#### Market Intelligence Template")
        st.markdown("Import construction market insights and intelligence.")
        st.markdown(generate_market_intelligence_template("market_intelligence_template.csv", "Market Intelligence Template"), unsafe_allow_html=True)
        
        st.markdown("##### Required Fields:")
        st.markdown("""
        - `date` - Date of insight
        - `category` - Construction category
        - `insight_type` - Type of intelligence (Market Trend, Price Change, Supply Issue, etc.)
        - `title` - Brief title
        - `description` - Detailed description
        """)
    
    st.markdown("### Template Usage Instructions")
    
    with st.expander("How to Use Templates"):
        st.markdown("""
        1. **Download Template**: Click the download link for the desired template.
        
        2. **Fill in Data**: Open the CSV file in Excel or another spreadsheet application and fill in your construction data.
            - Required fields are marked above for each template
            - Follow the format of the example row
            - Dates should be in YYYY-MM-DD format
            - Don't change column names
        
        3. **Save and Upload**: Save the file and upload it through the Data Upload section of the application.
        
        4. **Verify Import**: Review the data preview after upload to ensure it was imported correctly.
        """)
        
    with st.expander("Date Formatting"):
        st.markdown("""
        All dates should be in ISO format: `YYYY-MM-DD`
        
        Examples:
        - May 15, 2023 should be entered as `2023-05-15`
        - December 31, 2022 should be entered as `2022-12-31`
        """)
        
    with st.expander("Numeric Scoring"):
        st.markdown("""
        Risk and performance scores use a 0-10 scale:
        
        - **Risk Scores**:
            - 1-3: Low risk
            - 3-5: Medium risk
            - 5-7.5: High risk
            - 7.5-10: Critical risk
            
        - **Performance Scores**:
            - 1-4: Poor
            - 4-6: Fair
            - 6-8: Good
            - 8-10: Excellent
        """)