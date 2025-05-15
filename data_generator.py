"""
Data generator functions for ArcadiaProcure Construction Insights.
This module provides functions to generate construction-specific mock data 
for various aspects of the procurement and supply chain analytics platform.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config import CONSTRUCTION_CATEGORIES, CONSTRUCTION_SUPPLIER_SEGMENTS, CONSTRUCTION_RISK_FACTORS

# Seed for reproducibility
np.random.seed(42)

# Constants for construction data generation
CONSTRUCTION_SUPPLIERS = [
    "Turner Construction", "Bechtel Corp", "Fluor Corp", "Kiewit Corporation", 
    "Suffolk Construction", "McCarthy Building", "Skanska USA", "Clark Construction Group",
    "Whiting-Turner", "DPR Construction", "Gilbane Building", "JE Dunn Construction",
    "AECOM", "Hensel Phelps", "PCL Construction", "Swinerton", "Holder Construction",
    "Mortenson", "Hathaway Dinwiddie", "Walsh Group", "Clayco", "Ryan Companies",
    "Balfour Beatty US", "Lendlease", "Brasfield & Gorrie", "Granite Construction",
    "Webcor Builders", "Robins & Morton", "CBG Building Company", "Structure Tone",
    "Hunt Construction", "Barton Malow", "HITT Contracting", "Hoffman Construction",
    "Sundt Construction", "Adolfson & Peterson", "W. M. Jordan", "Shawmut Design and Construction",
    "Messer Construction", "Gray Construction", "The Beck Group", "JLG Architects",
    "Alberici Constructors", "Yates Construction", "Consigli Construction", "Layton Construction"
]

CONSTRUCTION_PROJECTS = [
    "Downtown Highrise Tower", "Metro Transit Hub", "Waterfront Plaza", "Medical Center Expansion",
    "University Science Building", "Municipal Water Treatment", "Highway 101 Widening", 
    "Airport Terminal Expansion", "Office Park Development", "Shopping Center Renovation",
    "Resort Hotel Construction", "Public Library Complex", "Industrial Park Warehouses",
    "Residential Tower", "Suburban Hospital", "School District Modernization", 
    "Data Center Complex", "Sports Stadium Upgrade", "Civic Center Renovation",
    "Mixed-Use Development", "Affordable Housing Project", "Retirement Community",
    "Manufacturing Plant", "Corporate Campus", "Utility Infrastructure"
]

CONSTRUCTION_SUBCATEGORIES = {
    "Structural Materials": ["Concrete", "Rebar", "Structural Steel", "Lumber", "Pre-Cast Elements", "Bridge Components"],
    "MEP Systems": ["HVAC Units", "Electrical Equipment", "Plumbing Fixtures", "Fire Suppression", "Building Automation"],
    "Building Envelope": ["Curtain Wall", "Roofing Systems", "Windows", "Doors", "Insulation", "Waterproofing"],
    "Finishes": ["Flooring", "Drywall", "Ceiling Systems", "Paint", "Millwork", "Tile", "Carpet"],
    "Sitework & Foundations": ["Earthwork", "Paving", "Utilities", "Landscaping", "Foundations", "Retaining Walls"],
    "Safety Equipment": ["Fall Protection", "PPE", "Traffic Safety", "Confined Space", "Fire Safety"]
}

CONSTRUCTION_INVOICE_PREFIXES = ["INV", "CI", "BLD", "CNST", "PROJ"]

CONSTRUCTION_ALERT_TYPES = [
    "Material Price Increase", "Delivery Delay", "Labor Shortage", "Permit Issue", 
    "Weather Impact", "Safety Incident", "Quality Defect", "Contract Dispute", 
    "Design Change", "Regulatory Compliance", "Financial Stability", 
    "Environmental Issue", "Supply Chain Disruption"
]

def generate_spend_data(n=1000):
    """Generate robust mock spend data for construction industry"""
    # Date range (past 3 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1095)  # ~3 years
    dates = pd.date_range(start=start_date, end=end_date, periods=n)
    
    # Random selection with weighted probabilities
    categories = np.random.choice(
        CONSTRUCTION_CATEGORIES, 
        size=n, 
        p=[0.30, 0.25, 0.20, 0.15, 0.08, 0.02]  # Weights based on typical construction spend
    )
    
    # Generate subcategories based on main category
    subcategories = []
    for cat in categories:
        subcats = CONSTRUCTION_SUBCATEGORIES[cat]
        subcategories.append(np.random.choice(subcats))
    
    # Generate suppliers with some concentration (80/20 rule)
    top_suppliers = np.random.choice(CONSTRUCTION_SUPPLIERS[:10], size=int(n*0.8))
    other_suppliers = np.random.choice(CONSTRUCTION_SUPPLIERS[10:], size=n - int(n*0.8))
    suppliers = np.concatenate([top_suppliers, other_suppliers])
    np.random.shuffle(suppliers)
    
    # Generate projects with association to suppliers
    # Create consistent supplier-project mappings
    supplier_project_map = {}
    for supplier in set(suppliers):
        # Each supplier works on 1-3 projects
        num_projects = np.random.randint(1, 4)
        supplier_project_map[supplier] = np.random.choice(CONSTRUCTION_PROJECTS, size=num_projects, replace=False)
    
    projects = []
    for supplier in suppliers:
        projects.append(np.random.choice(supplier_project_map[supplier]))
    
    # Generate realistic construction spend amounts
    # Use lognormal distribution for more realistic spend patterns
    # Different scales based on category
    amounts = []
    for i, category in enumerate(categories):
        if category == "Structural Materials":
            amount = np.random.lognormal(mean=10.5, sigma=1.2)
        elif category == "MEP Systems":
            amount = np.random.lognormal(mean=10.2, sigma=1.0)
        elif category == "Building Envelope":
            amount = np.random.lognormal(mean=9.8, sigma=0.9)
        elif category == "Finishes":
            amount = np.random.lognormal(mean=9.2, sigma=1.1)
        elif category == "Sitework & Foundations":
            amount = np.random.lognormal(mean=10.3, sigma=1.3)
        else:  # Safety Equipment
            amount = np.random.lognormal(mean=8.5, sigma=0.8)
        
        # Add some variability based on supplier tier
        if suppliers[i] in CONSTRUCTION_SUPPLIERS[:5]:  # Top tier
            amount *= np.random.uniform(0.9, 1.3)
        
        amounts.append(amount)
    
    # Generate invoice numbers
    invoice_numbers = []
    for i in range(n):
        prefix = np.random.choice(CONSTRUCTION_INVOICE_PREFIXES)
        number = np.random.randint(10000, 100000)
        invoice_numbers.append(f"{prefix}-{number}")
    
    # Create payment terms
    payment_terms = np.random.choice(["Net 30", "Net 45", "Net 60"], size=n)
    
    # Create dataframe
    df = pd.DataFrame({
        'date': dates,
        'invoice_number': invoice_numbers,
        'supplier': suppliers,
        'category': categories,
        'subcategory': subcategories,
        'project': projects,
        'amount': amounts,
        'payment_terms': payment_terms,
        'fiscal_year': pd.DatetimeIndex(dates).year,
        'fiscal_quarter': pd.DatetimeIndex(dates).quarter
    })
    
    # Add some description text
    descriptions = []
    for i, row in df.iterrows():
        descriptions.append(f"{row['subcategory']} for {row['project']}")
    
    df['description'] = descriptions
    
    return df

def generate_risk_data(n=20):
    """Generate construction-specific risk assessment data"""
    # Use top suppliers
    suppliers = np.random.choice(CONSTRUCTION_SUPPLIERS, size=n, replace=False)
    
    # Generate assessment dates (within past 6 months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    assessment_dates = [start_date + timedelta(days=np.random.randint(0, 180)) for _ in range(n)]
    
    # Risk factors - use realistic distributions for construction
    # Financial stability is a key factor in construction
    financial_risks = np.random.normal(loc=5.2, scale=1.8, size=n)
    financial_risks = np.clip(financial_risks, 1, 10)
    
    # Operational risks (delivery, capacity, etc.)
    operational_risks = np.random.normal(loc=4.8, scale=1.5, size=n)
    operational_risks = np.clip(operational_risks, 1, 10)
    
    # Compliance risks (permits, codes, regulations)
    compliance_risks = np.random.normal(loc=4.5, scale=1.7, size=n)
    compliance_risks = np.clip(compliance_risks, 1, 10)
    
    # Geopolitical risks (materials sourcing, tariffs)
    geopolitical_risks = np.random.normal(loc=4.2, scale=1.3, size=n)
    geopolitical_risks = np.clip(geopolitical_risks, 1, 10)
    
    # Environmental risks
    environmental_risks = np.random.normal(loc=4.0, scale=1.6, size=n)
    environmental_risks = np.clip(environmental_risks, 1, 10)
    
    # Social risks (labor practices, community impact)
    social_risks = np.random.normal(loc=3.8, scale=1.4, size=n)
    social_risks = np.clip(social_risks, 1, 10)
    
    # Governance risks
    governance_risks = np.random.normal(loc=3.5, scale=1.5, size=n)
    governance_risks = np.clip(governance_risks, 1, 10)
    
    # Construction-specific risk factors
    material_delay_probability = np.random.normal(loc=6.2, scale=1.7, size=n)
    material_delay_probability = np.clip(material_delay_probability, 1, 10)
    
    schedule_impact = np.random.normal(loc=5.8, scale=1.8, size=n)
    schedule_impact = np.clip(schedule_impact, 1, 10)
    
    quality_consistency = np.random.normal(loc=4.9, scale=1.5, size=n)
    quality_consistency = np.clip(quality_consistency, 1, 10)
    
    financial_stability = np.random.normal(loc=5.5, scale=1.6, size=n)
    financial_stability = np.clip(financial_stability, 1, 10)
    
    safety_compliance = np.random.normal(loc=4.2, scale=1.9, size=n)
    safety_compliance = np.clip(safety_compliance, 1, 10)
    
    # Calculate overall risk (weighted average)
    overall_risks = (
        0.20 * financial_risks + 
        0.20 * operational_risks + 
        0.15 * compliance_risks + 
        0.10 * geopolitical_risks + 
        0.10 * environmental_risks + 
        0.10 * social_risks + 
        0.15 * governance_risks
    )
    
    # Round to 1 decimal place
    overall_risks = np.round(overall_risks, 1)
    financial_risks = np.round(financial_risks, 1)
    operational_risks = np.round(operational_risks, 1)
    compliance_risks = np.round(compliance_risks, 1)
    geopolitical_risks = np.round(geopolitical_risks, 1)
    environmental_risks = np.round(environmental_risks, 1)
    social_risks = np.round(social_risks, 1)
    governance_risks = np.round(governance_risks, 1)
    material_delay_probability = np.round(material_delay_probability, 1)
    schedule_impact = np.round(schedule_impact, 1)
    quality_consistency = np.round(quality_consistency, 1)
    financial_stability = np.round(financial_stability, 1)
    safety_compliance = np.round(safety_compliance, 1)
    
    # Generate tier information
    tiers = []
    for supplier in suppliers:
        if supplier in CONSTRUCTION_SUPPLIERS[:5]:
            tiers.append("Tier 1 (Prime)")
        elif supplier in CONSTRUCTION_SUPPLIERS[5:15]:
            tiers.append("Tier 2 (Major Sub)")
        else:
            tiers.append("Tier 3 (Specialty)")
    
    # Create dataframe
    df = pd.DataFrame({
        'supplier': suppliers,
        'assessment_date': assessment_dates,
        'tier': tiers,
        'financial_risk': financial_risks,
        'operational_risk': operational_risks,
        'compliance_risk': compliance_risks,
        'geopolitical_risk': geopolitical_risks,
        'environmental_risk': environmental_risks,
        'social_risk': social_risks,
        'governance_risk': governance_risks,
        'overall_risk': overall_risks,
        'material_delay_probability': material_delay_probability,
        'schedule_impact': schedule_impact,
        'quality_consistency': quality_consistency,
        'financial_stability': financial_stability,
        'safety_compliance': safety_compliance
    })
    
    # Add risk notes
    risk_notes = []
    for i, row in df.iterrows():
        notes = []
        if row['financial_risk'] > 7:
            notes.append("Financial stability concerns due to overextended project commitments.")
        if row['operational_risk'] > 7:
            notes.append("History of materials delivery delays affecting project timelines.")
        if row['compliance_risk'] > 7:
            notes.append("Previous permit compliance issues identified in regulatory reviews.")
        if row['safety_compliance'] > 7:
            notes.append("Multiple safety incidents reported in past 12 months.")
        
        if not notes:
            top_risk = max(
                row['financial_risk'], 
                row['operational_risk'], 
                row['compliance_risk'],
                row['geopolitical_risk'],
                row['environmental_risk']
            )
            risk_type = ""
            if top_risk == row['financial_risk']:
                risk_type = "financial"
            elif top_risk == row['operational_risk']:
                risk_type = "operational"
            elif top_risk == row['compliance_risk']:
                risk_type = "compliance"
            elif top_risk == row['geopolitical_risk']:
                risk_type = "geopolitical"
            else:
                risk_type = "environmental"
            
            notes.append(f"Monitor {risk_type} risk indicators for potential changes.")
        
        risk_notes.append(" ".join(notes))
    
    df['notes'] = risk_notes
    
    return df

def generate_performance_data(n=20):
    """Generate construction-specific supplier performance data"""
    # Use the same suppliers as in risk data for consistency
    suppliers = np.random.choice(CONSTRUCTION_SUPPLIERS, size=n, replace=False)
    
    # Generate evaluation dates (within past year)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    evaluation_dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(n)]
    
    # Generate construction-specific performance metrics
    # Schedule adherence (meeting timeline commitments)
    schedule_adherence = np.random.normal(loc=7.2, scale=1.5, size=n)
    schedule_adherence = np.clip(schedule_adherence, 1, 10)
    
    # Work quality (construction quality)
    work_quality = np.random.normal(loc=7.5, scale=1.3, size=n)
    work_quality = np.clip(work_quality, 1, 10)
    
    # Cost control (budget adherence)
    cost_control = np.random.normal(loc=6.8, scale=1.7, size=n)
    cost_control = np.clip(cost_control, 1, 10)
    
    # Safety performance (job site safety)
    safety_performance = np.random.normal(loc=7.8, scale=1.6, size=n)
    safety_performance = np.clip(safety_performance, 1, 10)
    
    # Documentation (submittals, RFIs, etc.)
    documentation = np.random.normal(loc=6.5, scale=1.4, size=n)
    documentation = np.clip(documentation, 1, 10)
    
    # Communication (responsiveness, clarity)
    communication = np.random.normal(loc=7.0, scale=1.5, size=n)
    communication = np.clip(communication, 1, 10)
    
    # Problem resolution (issue management)
    problem_resolution = np.random.normal(loc=6.9, scale=1.6, size=n)
    problem_resolution = np.clip(problem_resolution, 1, 10)
    
    # Calculate overall score (weighted average)
    overall_scores = (
        0.20 * schedule_adherence + 
        0.20 * work_quality + 
        0.15 * cost_control + 
        0.15 * safety_performance + 
        0.10 * documentation + 
        0.10 * communication + 
        0.10 * problem_resolution
    )
    
    # Round to 1 decimal place
    overall_scores = np.round(overall_scores, 1)
    schedule_adherence = np.round(schedule_adherence, 1)
    work_quality = np.round(work_quality, 1)
    cost_control = np.round(cost_control, 1)
    safety_performance = np.round(safety_performance, 1)
    documentation = np.round(documentation, 1)
    communication = np.round(communication, 1)
    problem_resolution = np.round(problem_resolution, 1)
    
    # Assign supplier types and categories based on supplier
    supplier_types = []
    categories = []
    relationship_lengths = []
    annual_spends = []
    active_projects = []
    
    for supplier in suppliers:
        # Supplier type
        if supplier in CONSTRUCTION_SUPPLIERS[:10]:
            supplier_types.append("General Contractor")
            relationship_lengths.append(np.random.choice(["5+ years", "3-5 years", "1-3 years"], p=[0.6, 0.3, 0.1]))
            annual_spends.append(np.random.uniform(1000000, 5000000))
            active_projects.append(np.random.randint(2, 6))
        elif supplier in CONSTRUCTION_SUPPLIERS[10:25]:
            supplier_types.append("Specialty Contractor")
            relationship_lengths.append(np.random.choice(["5+ years", "3-5 years", "1-3 years", "<1 year"], p=[0.3, 0.4, 0.2, 0.1]))
            annual_spends.append(np.random.uniform(500000, 2000000))
            active_projects.append(np.random.randint(1, 4))
        else:
            supplier_types.append("Material Supplier")
            relationship_lengths.append(np.random.choice(["5+ years", "3-5 years", "1-3 years", "<1 year"], p=[0.2, 0.3, 0.4, 0.1]))
            annual_spends.append(np.random.uniform(100000, 1000000))
            active_projects.append(np.random.randint(1, 3))
        
        # Category
        categories.append(np.random.choice(CONSTRUCTION_CATEGORIES, p=[0.3, 0.25, 0.2, 0.15, 0.08, 0.02]))
    
    # Create dataframe
    df = pd.DataFrame({
        'supplier': suppliers,
        'supplier_type': supplier_types,
        'category': categories,
        'evaluation_date': evaluation_dates,
        'schedule_adherence': schedule_adherence,
        'work_quality': work_quality,
        'cost_control': cost_control,
        'safety_performance': safety_performance,
        'documentation': documentation,
        'communication': communication,
        'problem_resolution': problem_resolution,
        'overall_score': overall_scores,
        'relationship_length': relationship_lengths,
        'annual_spend': annual_spends,
        'active_projects': active_projects
    })
    
    # Add evaluation comments
    comments = []
    for i, row in df.iterrows():
        comment_parts = []
        
        if row['overall_score'] >= 8.5:
            comment_parts.append("Exceptional performer across all categories.")
        elif row['overall_score'] >= 7.5:
            comment_parts.append("Strong performance with consistent quality.")
        elif row['overall_score'] >= 6.0:
            comment_parts.append("Meets expectations with some areas for improvement.")
        elif row['overall_score'] >= 4.0:
            comment_parts.append("Several performance issues identified requiring attention.")
        else:
            comment_parts.append("Significant performance concerns across multiple areas.")
        
        # Add metric-specific comments
        if row['schedule_adherence'] < 5.0:
            comment_parts.append("Persistent schedule delays affecting project timeline.")
        elif row['work_quality'] < 5.0:
            comment_parts.append("Quality issues requiring rework have been documented.")
        elif row['cost_control'] < 5.0:
            comment_parts.append("Budget overruns on multiple work packages.")
        elif row['safety_performance'] < 5.0:
            comment_parts.append("Safety protocol compliance needs immediate improvement.")
        
        comments.append(" ".join(comment_parts))
    
    df['comments'] = comments
    df['evaluator'] = np.random.choice(["Project Manager", "Construction Director", "Procurement Lead"], size=n)
    
    return df

def generate_contract_data(n=30):
    """Generate construction-specific contract data"""
    # Use the same suppliers for consistency
    suppliers = np.random.choice(CONSTRUCTION_SUPPLIERS, size=n, replace=True)
    
    # Contract types
    contract_types = [
        "Fixed Price", "Unit Price", "Cost Plus", "GMP", "Time & Materials", 
        "Design-Build", "Design-Bid-Build", "CMAR", "IDIQ"
    ]
    
    # Contract names
    contract_names = []
    for i, supplier in enumerate(suppliers):
        supplier_short = supplier.split()[0]
        project = np.random.choice(CONSTRUCTION_PROJECTS)
        project_short = " ".join(project.split()[:2])
        contract_names.append(f"{project_short} - {supplier_short} Agreement")
    
    # Contract dates
    # More realistic construction timelines (6 months to 3 years)
    current_date = datetime.now()
    start_dates = []
    end_dates = []
    
    for i in range(n):
        # Start date from 3 years ago to now
        start_date = current_date - timedelta(days=np.random.randint(0, 1095))
        
        # Contract duration between 6 months and 3 years
        duration_days = np.random.randint(180, 1095)
        end_date = start_date + timedelta(days=duration_days)
        
        start_dates.append(start_date)
        end_dates.append(end_date)
    
    # Contract values - use lognormal for more realistic distribution
    log_values = np.random.lognormal(mean=13, sigma=1.2, size=n)
    
    # Adjust values based on supplier tier
    for i, supplier in enumerate(suppliers):
        if supplier in CONSTRUCTION_SUPPLIERS[:5]:  # Top tier
            log_values[i] *= np.random.uniform(1.5, 2.5)
        elif supplier in CONSTRUCTION_SUPPLIERS[5:15]:  # Mid tier
            log_values[i] *= np.random.uniform(0.8, 1.4)
    
    # Contract statuses
    statuses = []
    for i in range(n):
        if end_dates[i] < current_date:
            statuses.append("Expired")
        elif start_dates[i] > current_date:
            statuses.append("Pending")
        else:
            statuses.append("Active")
    
    # Generate categories based on supplier
    categories = []
    for supplier in suppliers:
        if "Construction" in supplier or "Building" in supplier:
            categories.append(np.random.choice(["General Construction", "Design-Build", "Construction Management"]))
        elif any(term in supplier for term in ["Steel", "Concrete", "Materials"]):
            categories.append("Material Supply")
        elif any(term in supplier for term in ["Electric", "Plumbing", "Mechanical"]):
            categories.append("MEP Services")
        else:
            categories.append(np.random.choice(["Specialty Services", "Consulting", "Equipment Rental"]))
    
    # Create dataframe
    df = pd.DataFrame({
        'name': contract_names,
        'supplier': suppliers,
        'type': np.random.choice(contract_types, size=n),
        'start_date': start_dates,
        'end_date': end_dates,
        'value': log_values,
        'status': statuses,
        'category': categories,
        'auto_renewal': np.random.choice([True, False], size=n, p=[0.3, 0.7]),
        'notice_period_days': np.random.choice([30, 60, 90], size=n)
    })
    
    # Add contract descriptions
    descriptions = []
    for i, row in df.iterrows():
        if row['type'] == "Fixed Price":
            descriptions.append(f"Fixed price contract for {row['category']} services on project.")
        elif row['type'] == "GMP":
            descriptions.append(f"Guaranteed Maximum Price contract with shared savings for {row['category']}.")
        elif row['type'] == "Cost Plus":
            descriptions.append(f"Cost Plus Fixed Fee contract for {row['category']} with escalation clauses.")
        elif row['type'] == "Design-Build":
            descriptions.append(f"Design-Build contract covering all design and construction services.")
        elif row['type'] == "Time & Materials":
            descriptions.append(f"Time and Materials contract for {row['category']} with not-to-exceed amount.")
        else:
            descriptions.append(f"Standard {row['type']} agreement for {row['category']} services.")
    
    df['description'] = descriptions
    
    return df

def generate_risk_alerts(n=50):
    """Generate construction-specific risk alerts"""
    # Use suppliers from suppliers list
    suppliers = np.random.choice(CONSTRUCTION_SUPPLIERS, size=n)
    
    # Generate dates (past 90 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    dates = [start_date + timedelta(days=np.random.randint(0, 90)) for _ in range(n)]
    
    # Alert types and descriptions
    alert_types = []
    descriptions = []
    projects = []
    
    for i in range(n):
        alert_type = np.random.choice(CONSTRUCTION_ALERT_TYPES)
        alert_types.append(alert_type)
        project = np.random.choice(CONSTRUCTION_PROJECTS)
        projects.append(project)
        
        if alert_type == "Material Price Increase":
            category = np.random.choice(CONSTRUCTION_CATEGORIES)
            subcategory = np.random.choice(CONSTRUCTION_SUBCATEGORIES[category])
            percent = np.random.randint(5, 30)
            descriptions.append(f"{subcategory} prices have increased by {percent}% due to market conditions, affecting project budget.")
        
        elif alert_type == "Delivery Delay":
            category = np.random.choice(CONSTRUCTION_CATEGORIES)
            subcategory = np.random.choice(CONSTRUCTION_SUBCATEGORIES[category])
            days = np.random.randint(5, 45)
            descriptions.append(f"{subcategory} delivery delayed by {days} days, potentially impacting project schedule.")
        
        elif alert_type == "Labor Shortage":
            trade = np.random.choice(["Electrical", "Plumbing", "Carpentry", "Masonry", "Steel", "Concrete"])
            descriptions.append(f"Shortage of {trade} workers reported, may cause schedule delays and increased labor costs.")
        
        elif alert_type == "Permit Issue":
            permit_type = np.random.choice(["Building", "Electrical", "Plumbing", "Environmental", "Occupancy"])
            descriptions.append(f"{permit_type} permit approval delayed due to regulatory requirements, affecting project timeline.")
        
        elif alert_type == "Weather Impact":
            weather = np.random.choice(["Heavy rain", "Snow", "High winds", "Extreme temperatures", "Flooding"])
            days = np.random.randint(2, 10)
            descriptions.append(f"{weather} forecast for next {days} days, may impact outdoor construction activities.")
        
        elif alert_type == "Safety Incident":
            incident = np.random.choice(["Fall", "Struck-by", "Electrical", "Equipment", "Material handling"])
            descriptions.append(f"{incident} incident reported on site, triggering safety review and potential work stoppage.")
        
        elif alert_type == "Quality Defect":
            item = np.random.choice(["Concrete placement", "Steel connections", "MEP installation", "Finishes", "Building envelope"])
            descriptions.append(f"Quality issues identified with {item}, requiring rework and potentially delaying subsequent activities.")
        
        elif alert_type == "Contract Dispute":
            issue = np.random.choice(["Change order pricing", "Schedule extension", "Scope interpretation", "Payment timing"])
            descriptions.append(f"Contractual disagreement regarding {issue} requires resolution to avoid project impacts.")
        
        elif alert_type == "Design Change":
            element = np.random.choice(["Structural", "Architectural", "MEP", "Site", "Interior"])
            descriptions.append(f"Late {element} design modifications requested, requiring schedule adjustment and cost evaluation.")
        
        elif alert_type == "Financial Stability":
            descriptions.append(f"Financial monitoring indicates potential liquidity concerns for {suppliers[i]}, increasing performance risk.")
        
        elif alert_type == "Supply Chain Disruption":
            material = np.random.choice(["Steel", "Lumber", "Concrete", "HVAC equipment", "Electrical components", "Glass"])
            descriptions.append(f"Global supply chain issues affecting {material} availability, requiring sourcing alternatives.")
        
        else:
            descriptions.append(f"Alert: {alert_type} requires attention for project risk management.")
    
    # Alert severity
    severities = np.random.choice(["Low", "Medium", "High", "Critical"], size=n, p=[0.2, 0.4, 0.3, 0.1])
    
    # Alert status
    statuses = []
    for i, date in enumerate(dates):
        days_ago = (end_date - date).days
        if days_ago < 7:
            statuses.append(np.random.choice(["Open", "Acknowledged"], p=[0.8, 0.2]))
        elif days_ago < 21:
            statuses.append(np.random.choice(["Open", "Acknowledged", "Resolved"], p=[0.3, 0.5, 0.2]))
        else:
            statuses.append(np.random.choice(["Open", "Acknowledged", "Resolved"], p=[0.1, 0.3, 0.6]))
    
    # Project impacts
    project_impacts = []
    for severity in severities:
        if severity == "Critical":
            project_impacts.append(np.random.choice(["Major", "Severe"], p=[0.3, 0.7]))
        elif severity == "High":
            project_impacts.append(np.random.choice(["Moderate", "Major"], p=[0.4, 0.6]))
        elif severity == "Medium":
            project_impacts.append(np.random.choice(["Minor", "Moderate"], p=[0.5, 0.5]))
        else:
            project_impacts.append(np.random.choice(["Minimal", "Minor"], p=[0.7, 0.3]))
    
    # Create dataframe
    df = pd.DataFrame({
        'supplier': suppliers,
        'date': dates,
        'alert_type': alert_types,
        'description': descriptions,
        'severity': severities,
        'status': statuses,
        'project': projects,
        'project_impact': project_impacts
    })
    
    return df

def generate_opportunity_data():
    """Generate construction-specific opportunity analysis data"""
    # Create a list of opportunities
    opportunities = [
        {
            "title": "Bundle Structural Material Orders",
            "description": "Consolidate structural steel and concrete orders across multiple projects to achieve volume discounts.",
            "savings_potential": 8.5,
            "complexity": 2,
            "annual_spend": 3800000,
            "category": "Structural Materials",
            "implementation_time": "1-3 months",
            "steps": [
                "Identify upcoming projects requiring similar materials",
                "Develop consolidated order schedule",
                "Negotiate volume-based pricing with suppliers",
                "Implement shared storage and logistics"
            ]
        },
        {
            "title": "Standardize MEP System Specifications",
            "description": "Implement standard specifications for mechanical, electrical, and plumbing systems to reduce customization costs.",
            "savings_potential": 6.2,
            "complexity": 3,
            "annual_spend": 2900000,
            "category": "MEP Systems",
            "implementation_time": "3-6 months",
            "steps": [
                "Audit current MEP specifications across projects",
                "Identify standardization opportunities with minimal impact",
                "Develop standard specification library",
                "Train design and procurement teams on new standards"
            ]
        },
        {
            "title": "Early Procurement of Long-Lead Items",
            "description": "Implement early procurement strategy for long-lead construction items to avoid expedite fees and market price increases.",
            "savings_potential": 5.8,
            "complexity": 2,
            "annual_spend": 1500000,
            "category": "Building Envelope",
            "implementation_time": "1-2 months",
            "steps": [
                "Identify critical long-lead items across projects",
                "Create early procurement schedule aligned with project timelines",
                "Negotiate early commitment discounts",
                "Secure storage arrangements for early deliveries"
            ]
        },
        {
            "title": "Regional Supplier Development",
            "description": "Develop local/regional supplier relationships to reduce logistics costs and lead times.",
            "savings_potential": 4.5,
            "complexity": 4,
            "annual_spend": 2200000,
            "category": "Finishes",
            "implementation_time": "6-12 months",
            "steps": [
                "Map current supply chain geography",
                "Identify potential regional suppliers",
                "Qualify suppliers through assessment process",
                "Develop phased transition plan to regional sources"
            ]
        },
        {
            "title": "Construction Equipment Pooling",
            "description": "Implement equipment pooling across multiple projects to increase utilization and reduce rental costs.",
            "savings_potential": 12.5,
            "complexity": 3,
            "annual_spend": 1800000,
            "category": "Sitework & Foundations",
            "implementation_time": "2-4 months",
            "steps": [
                "Audit current equipment utilization and costs",
                "Develop cross-project equipment scheduling system",
                "Negotiate revised rental terms with providers",
                "Implement tracking and logistics for equipment movement"
            ]
        },
        {
            "title": "Safety Equipment Standardization",
            "description": "Standardize safety equipment across projects and negotiate enterprise pricing.",
            "savings_potential": 7.2,
            "complexity": 1,
            "annual_spend": 780000,
            "category": "Safety Equipment",
            "implementation_time": "1-2 months",
            "steps": [
                "Review current safety equipment specifications",
                "Develop standard safety equipment catalog",
                "Negotiate enterprise pricing with suppliers",
                "Implement inspection and replacement program"
            ]
        },
        {
            "title": "Value Engineering for Sitework",
            "description": "Implement systematic value engineering process for sitework and foundation design to reduce material and labor costs.",
            "savings_potential": 9.5,
            "complexity": 3,
            "annual_spend": 3100000,
            "category": "Sitework & Foundations",
            "implementation_time": "3-6 months",
            "steps": [
                "Establish value engineering team with design and construction expertise",
                "Develop VE review process for all projects over $5M",
                "Create database of successful VE solutions",
                "Implement tracking system for VE savings"
            ]
        },
        {
            "title": "Bulk Purchase of Finishing Materials",
            "description": "Establish annual bulk purchase agreements for high-volume finishing materials like paint, flooring, and drywall.",
            "savings_potential": 6.8,
            "complexity": 2,
            "annual_spend": 1650000,
            "category": "Finishes",
            "implementation_time": "2-3 months",
            "steps": [
                "Analyze annual usage quantities for finishing materials",
                "Identify storage and logistics requirements",
                "Negotiate annual supply agreements with tiered pricing",
                "Develop material allocation system for projects"
            ]
        },
        {
            "title": "Prefabrication Strategy",
            "description": "Implement prefabrication approach for repetitive building elements to reduce on-site labor and improve quality.",
            "savings_potential": 11.2,
            "complexity": 4,
            "annual_spend": 4200000,
            "category": "Structural Materials",
            "implementation_time": "6-12 months",
            "steps": [
                "Identify high-potential prefabrication opportunities",
                "Engage design team for prefab-friendly design modifications",
                "Develop logistics plan for prefab components",
                "Establish quality control process for prefabricated elements"
            ]
        },
        {
            "title": "Design Standardization Program",
            "description": "Implement design standardization for repeatable building elements across projects to reduce engineering and material costs.",
            "savings_potential": 8.7,
            "complexity": 5,
            "annual_spend": 2800000,
            "category": "MEP Systems",
            "implementation_time": "9-18 months",
            "steps": [
                "Conduct portfolio analysis of recent projects",
                "Identify common design elements with standardization potential",
                "Develop standard design library and specification guides",
                "Create training program for design and procurement teams"
            ]
        }
    ]
    
    # Convert to dataframe
    df = pd.DataFrame(opportunities)
    
    return df

def generate_improvement_data():
    """Generate construction-specific performance improvement data"""
    # Create a list of improvement opportunities
    improvements = [
        {
            "supplier": "Turner Construction",
            "title": "Schedule Compliance Improvement",
            "description": "Implement detailed milestone tracking and weekly progress reviews to improve schedule adherence.",
            "category": "Schedule Performance",
            "impact": "High",
            "effort": "Medium",
            "savings": 425000,
            "steps": [
                "Establish detailed milestone tracking system",
                "Implement weekly progress reviews with accountability",
                "Develop early warning indicators for schedule risks",
                "Create incentive program tied to milestone achievement"
            ]
        },
        {
            "supplier": "Bechtel Corp",
            "title": "Quality Control Enhancement",
            "description": "Develop standardized QC protocols and inspection checklists to reduce rework and improve first-time quality.",
            "category": "Quality Management",
            "impact": "Medium",
            "effort": "Medium",
            "savings": 320000,
            "steps": [
                "Audit current quality performance and issues",
                "Develop standardized inspection checklists by trade",
                "Implement phased inspection process",
                "Train field supervisors on quality standards"
            ]
        },
        {
            "supplier": "Suffolk Construction",
            "title": "Cost Reporting Improvement",
            "description": "Implement real-time cost reporting and variance analysis to improve cost control performance.",
            "category": "Cost Control",
            "impact": "High",
            "effort": "High",
            "savings": 580000,
            "steps": [
                "Evaluate current cost reporting practices",
                "Implement digital cost tracking system",
                "Develop variance analysis protocol",
                "Train project teams on cost control methods"
            ]
        },
        {
            "supplier": "Clark Construction Group",
            "title": "Safety Program Enhancement",
            "description": "Develop comprehensive safety training and monitoring program to improve safety performance metrics.",
            "category": "Safety Performance",
            "impact": "High",
            "effort": "Medium",
            "savings": 275000,
            "steps": [
                "Conduct safety performance assessment",
                "Develop targeted training for high-risk activities",
                "Implement daily safety briefings and inspections",
                "Create near-miss reporting system"
            ]
        },
        {
            "supplier": "DPR Construction",
            "title": "Documentation Standardization",
            "description": "Standardize project documentation processes and templates to improve completeness and timeliness.",
            "category": "Documentation",
            "impact": "Medium",
            "effort": "Low",
            "savings": 180000,
            "steps": [
                "Audit current documentation practices",
                "Develop standardized document templates",
                "Implement digital document management system",
                "Train teams on documentation requirements"
            ]
        },
        {
            "supplier": "Skanska USA",
            "title": "Communication Protocol Implementation",
            "description": "Establish formal communication protocols and escalation paths to improve responsiveness and clarity.",
            "category": "Communication",
            "impact": "Medium",
            "effort": "Low",
            "savings": 150000,
            "steps": [
                "Define communication requirements by project role",
                "Establish response time standards",
                "Implement communication plan template",
                "Create escalation path for critical issues"
            ]
        },
        {
            "supplier": "Whiting-Turner",
            "title": "Issue Resolution Process",
            "description": "Implement structured issue tracking and resolution process to improve problem-solving efficiency.",
            "category": "Problem Resolution",
            "impact": "High",
            "effort": "Medium",
            "savings": 340000,
            "steps": [
                "Develop issue categorization system",
                "Implement issue tracking database",
                "Establish resolution timeframes by issue type",
                "Create weekly issue review process"
            ]
        },
        {
            "supplier": "Fluor Corp",
            "title": "BIM Implementation",
            "description": "Expand use of Building Information Modeling to improve coordination and reduce field conflicts.",
            "category": "Quality Management",
            "impact": "High",
            "effort": "High",
            "savings": 650000,
            "steps": [
                "Assess current BIM capabilities",
                "Develop BIM execution plan template",
                "Train project teams on clash detection",
                "Implement model-based coordination meetings"
            ]
        },
        {
            "supplier": "Gilbane Building",
            "title": "Lean Construction Methods",
            "description": "Implement lean construction methodologies to reduce waste and improve production efficiency.",
            "category": "Schedule Performance",
            "impact": "High",
            "effort": "High",
            "savings": 520000,
            "steps": [
                "Analyze workflow and identify waste sources",
                "Implement pull planning for project scheduling",
                "Develop last planner system for field operations",
                "Create continuous improvement process"
            ]
        },
        {
            "supplier": "Kiewit Corporation",
            "title": "Procurement Planning Enhancement",
            "description": "Improve procurement planning and tracking to prevent material-related delays and cost overruns.",
            "category": "Cost Control",
            "impact": "Medium",
            "effort": "Medium",
            "savings": 380000,
            "steps": [
                "Develop comprehensive procurement schedule template",
                "Implement submittal tracking system",
                "Create material expediting process",
                "Establish early warning system for procurement risks"
            ]
        }
    ]
    
    return improvements

def generate_timeline_data(supplier=None):
    """Generate relationship timeline data for a specific supplier or random supplier"""
    if not supplier:
        supplier = np.random.choice(CONSTRUCTION_SUPPLIERS)
    
    # Generate random timeline events
    current_date = datetime.now()
    timeline_start = current_date - timedelta(days=np.random.randint(1095, 1825))  # 3-5 years ago
    
    # Create milestones
    milestones = []
    
    # Initial qualification/onboarding
    onboarding_date = timeline_start
    milestones.append({
        "date": onboarding_date,
        "title": "Initial Qualification",
        "description": f"Completed supplier qualification process for {supplier}",
        "category": "Relationship",
        "impact": "Positive"
    })
    
    # First project award
    first_award_date = onboarding_date + timedelta(days=np.random.randint(30, 90))
    project = np.random.choice(CONSTRUCTION_PROJECTS)
    milestones.append({
        "date": first_award_date,
        "title": "First Project Award",
        "description": f"Awarded {project} project with estimated value of ${np.random.randint(5, 50)/10}M",
        "category": "Contract",
        "impact": "Positive"
    })
    
    # Generate 5-15 random events over the timeline
    num_events = np.random.randint(5, 15)
    possible_dates = pd.date_range(first_award_date + timedelta(days=30), current_date - timedelta(days=7), periods=30)
    event_dates = np.random.choice(possible_dates, size=num_events, replace=False)
    event_dates = sorted(event_dates)
    
    # Event types
    event_types = [
        # Performance events
        ("Performance Review", "Completed quarterly performance review", "Performance", 
            ["Positive", "Neutral", "Negative"], [0.6, 0.3, 0.1]),
        
        # Contract events
        ("Contract Renewal", "Renewed master agreement for additional term", "Contract", 
            ["Positive"], [1.0]),
        ("Contract Amendment", "Amended contract terms for scope adjustment", "Contract", 
            ["Neutral", "Positive", "Negative"], [0.5, 0.3, 0.2]),
        ("Price Negotiation", "Completed price negotiation for upcoming projects", "Contract", 
            ["Positive", "Neutral", "Negative"], [0.5, 0.3, 0.2]),
        
        # Project events
        ("Project Completion", "Successfully completed project on schedule", "Project", 
            ["Positive", "Neutral"], [0.8, 0.2]),
        ("Schedule Issue", "Addressed schedule delay on active project", "Project", 
            ["Negative", "Neutral"], [0.7, 0.3]),
        ("Quality Review", "Conducted quality review of completed work", "Project", 
            ["Positive", "Neutral", "Negative"], [0.5, 0.3, 0.2]),
        ("Change Order", "Processed change order for scope modification", "Project", 
            ["Neutral", "Negative", "Positive"], [0.6, 0.3, 0.1]),
        
        # Risk events
        ("Risk Assessment", "Updated supplier risk assessment", "Risk", 
            ["Neutral", "Negative", "Positive"], [0.6, 0.3, 0.1]),
        ("Safety Incident", "Addressed safety incident on project site", "Risk", 
            ["Negative", "Neutral"], [0.8, 0.2]),
        ("Financial Review", "Completed financial stability review", "Risk", 
            ["Positive", "Neutral", "Negative"], [0.5, 0.3, 0.2])
    ]
    
    for event_date in event_dates:
        event_type = np.random.choice(event_types)
        title = event_type[0]
        description = event_type[1]
        category = event_type[2]
        impact = np.random.choice(event_type[3], p=event_type[4])
        
        # Add some variety to descriptions
        if title == "Performance Review":
            score = np.random.randint(60, 95)
            description = f"Quarterly performance review completed with score of {score}/100"
            if score >= 85:
                impact = "Positive"
            elif score >= 70:
                impact = "Neutral"
            else:
                impact = "Negative"
        
        elif title == "Project Completion":
            project = np.random.choice(CONSTRUCTION_PROJECTS)
            on_time = np.random.choice([True, False], p=[0.7, 0.3])
            on_budget = np.random.choice([True, False], p=[0.7, 0.3])
            
            if on_time and on_budget:
                description = f"Completed {project} on time and within budget"
                impact = "Positive"
            elif on_time:
                description = f"Completed {project} on time but over budget"
                impact = "Neutral"
            elif on_budget:
                description = f"Completed {project} within budget but delayed"
                impact = "Neutral"
            else:
                description = f"Completed {project} with delays and budget overruns"
                impact = "Negative"
        
        elif title == "Risk Assessment":
            risk_level = np.random.choice(["Low", "Medium", "High", "Critical"])
            description = f"Updated risk assessment - current level: {risk_level}"
            if risk_level == "Low":
                impact = "Positive"
            elif risk_level == "Medium":
                impact = "Neutral"
            else:
                impact = "Negative"
        
        milestones.append({
            "date": event_date,
            "title": title,
            "description": description,
            "category": category,
            "impact": impact
        })
    
    # Add most recent event
    recent_date = current_date - timedelta(days=np.random.randint(1, 7))
    recent_events = [
        {
            "date": recent_date,
            "title": "Strategy Discussion",
            "description": f"Met with {supplier} leadership to discuss future partnership opportunities",
            "category": "Relationship",
            "impact": "Positive"
        },
        {
            "date": recent_date,
            "title": "Performance Improvement Plan",
            "description": f"Initiated performance improvement plan for {supplier} in response to recent issues",
            "category": "Performance",
            "impact": "Neutral"
        },
        {
            "date": recent_date,
            "title": "Contract Renewal Discussion",
            "description": f"Began contract renewal discussions with {supplier} for upcoming term",
            "category": "Contract",
            "impact": "Neutral"
        }
    ]
    
    milestones.append(np.random.choice(recent_events))
    
    # Convert to dataframe and sort by date
    df = pd.DataFrame(milestones)
    df = df.sort_values("date")
    
    # Add supplier column
    df["supplier"] = supplier
    
    return df
