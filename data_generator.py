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
] # This list has 46 suppliers

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
    df_cols = [ 
        'date', 'invoice_number', 'supplier', 'category', 'subcategory',
        'project', 'amount', 'payment_terms', 'fiscal_year', 'fiscal_quarter', 'description'
    ]
    if n == 0:
        return pd.DataFrame(columns=df_cols)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=1095) 
    dates_data = pd.date_range(start=start_date, end=end_date, periods=n) # Renamed

    # Use current constants or provide defaults if they are empty
    current_categories_list = CONSTRUCTION_CATEGORIES if CONSTRUCTION_CATEGORIES else ["Default Category"]
    category_weights = [0.30, 0.25, 0.20, 0.15, 0.08, 0.02] if len(current_categories_list) == 6 else None
    categories_generated_data = np.random.choice(current_categories_list, size=n, p=category_weights) # Renamed

    subcategories_generated_data = [] # Renamed
    current_subcat_dict = CONSTRUCTION_SUBCATEGORIES if CONSTRUCTION_SUBCATEGORIES else {"Default Category": ["Default Subcategory"]}
    for cat_item_spend in categories_generated_data: # Renamed cat to cat_item_spend
        subcats_for_cat_spend = current_subcat_dict.get(cat_item_spend, ["Default Subcategory"]) # Renamed subcats
        subcategories_generated_data.append(np.random.choice(subcats_for_cat_spend if subcats_for_cat_spend else ["Default Subcategory"]))

    suppliers_generated_data = np.array([]) # Renamed suppliers
    if CONSTRUCTION_SUPPLIERS: 
        num_top_tier_suppliers = min(10, len(CONSTRUCTION_SUPPLIERS)) 
        top_suppliers_list_spend = CONSTRUCTION_SUPPLIERS[:num_top_tier_suppliers] # Renamed
        other_suppliers_list_spend = CONSTRUCTION_SUPPLIERS[num_top_tier_suppliers:] # Renamed

        size_for_top_tier_spend = int(n * 0.8) # Renamed
        size_for_other_tier_spend = n - size_for_top_tier_spend # Renamed

        chosen_top_suppliers_arr_spend = np.array([]) # Renamed
        if size_for_top_tier_spend > 0 and top_suppliers_list_spend: 
            chosen_top_suppliers_arr_spend = np.random.choice(top_suppliers_list_spend, size=size_for_top_tier_spend, replace=True)

        chosen_other_suppliers_arr_spend = np.array([]) # Renamed
        if size_for_other_tier_spend > 0 :
            if other_suppliers_list_spend: 
                 chosen_other_suppliers_arr_spend = np.random.choice(other_suppliers_list_spend, size=size_for_other_tier_spend, replace=True)
            elif top_suppliers_list_spend: 
                 chosen_other_suppliers_arr_spend = np.random.choice(top_suppliers_list_spend, size=size_for_other_tier_spend, replace=True)
        
        temp_suppliers_list_spend = [] # Renamed
        if len(chosen_top_suppliers_arr_spend) > 0:
            temp_suppliers_list_spend.extend(list(chosen_top_suppliers_arr_spend))
        if len(chosen_other_suppliers_arr_spend) > 0:
            temp_suppliers_list_spend.extend(list(chosen_other_suppliers_arr_spend))
        
        if temp_suppliers_list_spend:
            suppliers_generated_data = np.array(temp_suppliers_list_spend)
            if suppliers_generated_data.size > 0: # Shuffle only if array is not empty
                 np.random.shuffle(suppliers_generated_data)
        
        if len(suppliers_generated_data) < n and CONSTRUCTION_SUPPLIERS: 
            padding_needed_spend = n - len(suppliers_generated_data) # Renamed
            padding_suppliers_arr_spend = np.random.choice(CONSTRUCTION_SUPPLIERS, size=padding_needed_spend, replace=True) # Renamed
            if suppliers_generated_data.size > 0:
                suppliers_generated_data = np.concatenate([suppliers_generated_data, padding_suppliers_arr_spend])
            else:
                suppliers_generated_data = padding_suppliers_arr_spend
    
    if len(suppliers_generated_data) < n : 
        default_supplier_list = ["Default Supplier"] * n if not CONSTRUCTION_SUPPLIERS else CONSTRUCTION_SUPPLIERS
        suppliers_generated_data = np.random.choice(default_supplier_list, size=n, replace=True)


    supplier_project_map_spend = {} # Renamed
    unique_map_suppliers_list_spend = list(set(CONSTRUCTION_SUPPLIERS)) if CONSTRUCTION_SUPPLIERS else ["Default Supplier"] # Renamed

    for sup_key_item_spend in unique_map_suppliers_list_spend: # Renamed sup_key
        num_projects_for_supplier_spend = np.random.randint(1, 4) # Renamed
        current_projects_list_spend = CONSTRUCTION_PROJECTS if CONSTRUCTION_PROJECTS else ["Default Project"] # Renamed
        if current_projects_list_spend: 
             supplier_project_map_spend[sup_key_item_spend] = np.random.choice(current_projects_list_spend, size=num_projects_for_supplier_spend, replace=True)
        else:
             supplier_project_map_spend[sup_key_item_spend] = ["Default Project"]

    projects_generated_data = [] # Renamed projects
    default_project_choice_list_spend = ["Default Project"] # Renamed
    if CONSTRUCTION_PROJECTS: 
        default_project_choice_list_spend = list(np.random.choice(CONSTRUCTION_PROJECTS, size=1)) 

    for sup_data_item_spend in suppliers_generated_data: # Renamed sup_item
        project_choices_for_supplier_spend = supplier_project_map_spend.get(sup_data_item_spend, default_project_choice_list_spend) # Renamed
        if project_choices_for_supplier_spend is not None and len(project_choices_for_supplier_spend) > 0:
            projects_generated_data.append(np.random.choice(project_choices_for_supplier_spend))
        else: 
            projects_generated_data.append(default_project_choice_list_spend[0])
            
    amounts_generated_data = [] # Renamed amounts
    for i, cat_data_item_spend in enumerate(categories_generated_data): # Renamed category to cat_data_item_spend
        if cat_data_item_spend == "Structural Materials": amount_val_spend = np.random.lognormal(mean=10.5, sigma=1.2) # Renamed amount
        elif cat_data_item_spend == "MEP Systems": amount_val_spend = np.random.lognormal(mean=10.2, sigma=1.0)
        elif cat_data_item_spend == "Building Envelope": amount_val_spend = np.random.lognormal(mean=9.8, sigma=0.9)
        elif cat_data_item_spend == "Finishes": amount_val_spend = np.random.lognormal(mean=9.2, sigma=1.1)
        elif cat_data_item_spend == "Sitework & Foundations": amount_val_spend = np.random.lognormal(mean=10.3, sigma=1.3)
        else: amount_val_spend = np.random.lognormal(mean=8.5, sigma=0.8)

        if CONSTRUCTION_SUPPLIERS and suppliers_generated_data.size > i and suppliers_generated_data[i] in CONSTRUCTION_SUPPLIERS[:min(5, len(CONSTRUCTION_SUPPLIERS))]:
            amount_val_spend *= np.random.uniform(0.9, 1.3)
        amounts_generated_data.append(amount_val_spend)

    current_invoice_prefixes_spend = CONSTRUCTION_INVOICE_PREFIXES if CONSTRUCTION_INVOICE_PREFIXES else ["INV"] # Renamed
    invoice_numbers_generated_data = [f"{np.random.choice(current_invoice_prefixes_spend)}-{np.random.randint(10000, 100000)}" for _ in range(n)] # Renamed
    payment_terms_generated_data = np.random.choice(["Net 30", "Net 45", "Net 60"], size=n) # Renamed

    final_suppliers_spend = suppliers_generated_data[:n] if len(suppliers_generated_data) >= n else np.random.choice(["Default Supplier"]*n if not CONSTRUCTION_SUPPLIERS else CONSTRUCTION_SUPPLIERS, size=n, replace=True) # Renamed
    final_projects_spend = projects_generated_data[:n] if len(projects_generated_data) >= n else np.random.choice(["Default Project"]*n if not CONSTRUCTION_PROJECTS else CONSTRUCTION_PROJECTS, size=n, replace=True) # Renamed

    df_dict_spend = { # Renamed
        'date': dates_data[:n], 
        'invoice_number': invoice_numbers_generated_data[:n], 
        'supplier': final_suppliers_spend[:n],
        'category': categories_generated_data[:n], 
        'subcategory': subcategories_generated_data[:n], 
        'project': final_projects_spend[:n],
        'amount': amounts_generated_data[:n], 
        'payment_terms': payment_terms_generated_data[:n],
    }
    if n > 0: 
        df_dict_spend['fiscal_year'] = pd.DatetimeIndex(dates_data[:n]).year
        df_dict_spend['fiscal_quarter'] = pd.DatetimeIndex(dates_data[:n]).quarter
    else: 
        df_dict_spend['fiscal_year'] = []
        df_dict_spend['fiscal_quarter'] = []

    df = pd.DataFrame(df_dict_spend)
    
    descriptions_generated_data = [] # Renamed descriptions
    if n > 0 and not df.empty: 
        for _, row_item_spend_desc in df.iterrows(): # Renamed row to row_item_spend_desc
            descriptions_generated_data.append(f"{row_item_spend_desc.get('subcategory', 'N/A')} for {row_item_spend_desc.get('project', 'N/A')}")
        df['description'] = descriptions_generated_data
    else: 
        df['description'] = [] 
        
    return df

def generate_risk_data(n=20): # n will be 40 from config.py
    """Generate construction-specific risk assessment data"""
    df_cols = [
        'supplier', 'assessment_date', 'tier', 'financial_risk', 'operational_risk',
        'compliance_risk', 'geopolitical_risk', 'environmental_risk', 'social_risk',
        'governance_risk', 'overall_risk', 'material_delay_probability',
        'schedule_impact', 'quality_consistency', 'financial_stability',
        'safety_compliance', 'notes'
    ]
    if n == 0: return pd.DataFrame(columns=df_cols)
    if not CONSTRUCTION_SUPPLIERS: return pd.DataFrame(columns=df_cols)

    num_to_select_risk = min(n, len(CONSTRUCTION_SUPPLIERS)) # Renamed
    if num_to_select_risk == 0 : return pd.DataFrame(columns=df_cols)

    suppliers_list_risk_data = np.random.choice(CONSTRUCTION_SUPPLIERS, size=num_to_select_risk, replace=False) # Renamed

    end_date_risk = datetime.now() # Renamed
    start_date_risk = end_date_risk - timedelta(days=180) # Renamed
    assessment_dates_risk_data = [start_date_risk + timedelta(days=np.random.randint(0, 180)) for _ in range(num_to_select_risk)] # Renamed

    financial_risks_data = np.clip(np.random.normal(loc=5.2, scale=1.8, size=num_to_select_risk), 1, 10) # Renamed
    operational_risks_data = np.clip(np.random.normal(loc=4.8, scale=1.5, size=num_to_select_risk), 1, 10) # Renamed
    # ... (rename other risk variables similarly for consistency if desired, or leave as is if clear)
    compliance_risks = np.clip(np.random.normal(loc=4.5, scale=1.7, size=num_to_select_risk), 1, 10)
    geopolitical_risks = np.clip(np.random.normal(loc=4.2, scale=1.3, size=num_to_select_risk), 1, 10)
    environmental_risks = np.clip(np.random.normal(loc=4.0, scale=1.6, size=num_to_select_risk), 1, 10)
    social_risks = np.clip(np.random.normal(loc=3.8, scale=1.4, size=num_to_select_risk), 1, 10)
    governance_risks = np.clip(np.random.normal(loc=3.5, scale=1.5, size=num_to_select_risk), 1, 10)
    material_delay_probability = np.clip(np.random.normal(loc=6.2, scale=1.7, size=num_to_select_risk), 1, 10)
    schedule_impact = np.clip(np.random.normal(loc=5.8, scale=1.8, size=num_to_select_risk), 1, 10)
    quality_consistency = np.clip(np.random.normal(loc=4.9, scale=1.5, size=num_to_select_risk), 1, 10)
    financial_stability = np.clip(np.random.normal(loc=5.5, scale=1.6, size=num_to_select_risk), 1, 10)
    safety_compliance = np.clip(np.random.normal(loc=4.2, scale=1.9, size=num_to_select_risk), 1, 10)


    overall_risks_calc_risk = np.round(0.20 * financial_risks_data + 0.20 * operational_risks_data + 0.15 * compliance_risks +
                           0.10 * geopolitical_risks + 0.10 * environmental_risks + 0.10 * social_risks +
                           0.15 * governance_risks, 1) # Renamed

    tiers_list_risk_data = [] # Renamed
    len_construction_suppliers_risk = len(CONSTRUCTION_SUPPLIERS) # Renamed
    for sup_item_risk_data in suppliers_list_risk_data: # Renamed supplier
        if len_construction_suppliers_risk > 0 and sup_item_risk_data in CONSTRUCTION_SUPPLIERS[:min(5, len_construction_suppliers_risk)]: 
            tiers_list_risk_data.append("Tier 1 (Prime)")
        elif len_construction_suppliers_risk > 5 and sup_item_risk_data in CONSTRUCTION_SUPPLIERS[min(5, len_construction_suppliers_risk):min(15, len_construction_suppliers_risk)]: 
            tiers_list_risk_data.append("Tier 2 (Major Sub)")
        else: 
            tiers_list_risk_data.append("Tier 3 (Specialty)")

    df = pd.DataFrame({
        'supplier': suppliers_list_risk_data, 'assessment_date': assessment_dates_risk_data, 'tier': tiers_list_risk_data,
        'financial_risk': np.round(financial_risks_data, 1), 'operational_risk': np.round(operational_risks_data, 1),
        'compliance_risk': np.round(compliance_risks, 1), 'geopolitical_risk': np.round(geopolitical_risks, 1),
        'environmental_risk': np.round(environmental_risks, 1), 'social_risk': np.round(social_risks, 1),
        'governance_risk': np.round(governance_risks, 1), 'overall_risk': overall_risks_calc_risk,
        'material_delay_probability': np.round(material_delay_probability, 1),
        'schedule_impact': np.round(schedule_impact, 1), 'quality_consistency': np.round(quality_consistency, 1),
        'financial_stability': np.round(financial_stability, 1), 'safety_compliance': np.round(safety_compliance, 1)
    })

    risk_notes_list_generated = [] # Renamed
    if not df.empty:
        for _, row_item_risk_notes in df.iterrows(): # Renamed row
            notes_parts_risk = [] # Renamed notes
            if row_item_risk_notes['financial_risk'] > 7: notes_parts_risk.append("Financial stability concerns.")
            if row_item_risk_notes['operational_risk'] > 7: notes_parts_risk.append("Materials delivery delays.")
            if row_item_risk_notes['compliance_risk'] > 7: notes_parts_risk.append("Permit compliance issues.")
            if row_item_risk_notes['safety_compliance'] > 7: notes_parts_risk.append("Multiple safety incidents.")
            if not notes_parts_risk: notes_parts_risk.append("Monitor general risk indicators.")
            risk_notes_list_generated.append(" ".join(notes_parts_risk))
    df['notes'] = risk_notes_list_generated if risk_notes_list_generated else [""] * len(df)

    return df

def generate_performance_data(n=20): # n will be 40 from config.py
    """Generate construction-specific supplier performance data"""
    df_cols = [
        'supplier', 'supplier_type', 'category', 'evaluation_date',
        'schedule_adherence', 'work_quality', 'cost_control', 'safety_performance',
        'documentation', 'communication', 'problem_resolution', 'overall_score',
        'relationship_length', 'annual_spend', 'active_projects', 'comments', 'evaluator'
    ]
    if n == 0: return pd.DataFrame(columns=df_cols)
    if not CONSTRUCTION_SUPPLIERS: return pd.DataFrame(columns=df_cols)
        
    num_to_select_perf = min(n, len(CONSTRUCTION_SUPPLIERS)) # Renamed
    if num_to_select_perf == 0 : return pd.DataFrame(columns=df_cols)

    suppliers_list_perf_data = np.random.choice(CONSTRUCTION_SUPPLIERS, size=num_to_select_perf, replace=False) # Renamed

    end_date_perf = datetime.now() # Renamed
    start_date_perf = end_date_perf - timedelta(days=365) # Renamed
    evaluation_dates_perf_data = [start_date_perf + timedelta(days=np.random.randint(0, 365)) for _ in range(num_to_select_perf)] # Renamed

    schedule_adherence_perf = np.clip(np.random.normal(loc=7.2, scale=1.5, size=num_to_select_perf), 1, 10) # Renamed
    work_quality_perf = np.clip(np.random.normal(loc=7.5, scale=1.3, size=num_to_select_perf), 1, 10) # Renamed
    # ... (rename other performance variables similarly)
    cost_control = np.clip(np.random.normal(loc=6.8, scale=1.7, size=num_to_select_perf), 1, 10)
    safety_performance = np.clip(np.random.normal(loc=7.8, scale=1.6, size=num_to_select_perf), 1, 10)
    documentation = np.clip(np.random.normal(loc=6.5, scale=1.4, size=num_to_select_perf), 1, 10)
    communication = np.clip(np.random.normal(loc=7.0, scale=1.5, size=num_to_select_perf), 1, 10)
    problem_resolution = np.clip(np.random.normal(loc=6.9, scale=1.6, size=num_to_select_perf), 1, 10)

    overall_scores_calc_perf = np.round(0.20 * schedule_adherence_perf + 0.20 * work_quality_perf + 0.15 * cost_control +
                            0.15 * safety_performance + 0.10 * documentation + 0.10 * communication +
                            0.10 * problem_resolution, 1) # Renamed

    supplier_types_list_perf_data = [] # Renamed 
    categories_list_perf_gen = [] # Renamed to avoid conflict with module name
    relationship_lengths_list_perf_data = [] # Renamed 
    annual_spends_list_perf_data = [] # Renamed 
    active_projects_list_perf_gen = [] # Renamed

    current_construction_categories_list_perf = CONSTRUCTION_CATEGORIES if CONSTRUCTION_CATEGORIES else ["Default Category"] # Renamed
    category_weights_perf_gen = [0.3, 0.25, 0.2, 0.15, 0.08, 0.02] if len(current_construction_categories_list_perf) == 6 else None # Renamed
    len_construction_suppliers_for_perf = len(CONSTRUCTION_SUPPLIERS) # Renamed

    for sup_item_perf_data in suppliers_list_perf_data: # Renamed supplier
        if len_construction_suppliers_for_perf > 0 and sup_item_perf_data in CONSTRUCTION_SUPPLIERS[:min(10, len_construction_suppliers_for_perf)]:
            supplier_types_list_perf_data.append("General Contractor")
            relationship_lengths_list_perf_data.append(np.random.choice(["5+ years", "3-5 years", "1-3 years"], p=[0.6, 0.3, 0.1]))
            annual_spends_list_perf_data.append(np.random.uniform(1000000, 5000000))
            active_projects_list_perf_gen.append(np.random.randint(2, 6))
        elif len_construction_suppliers_for_perf > 10 and sup_item_perf_data in CONSTRUCTION_SUPPLIERS[min(10,len_construction_suppliers_for_perf):min(25,len_construction_suppliers_for_perf)]:
            supplier_types_list_perf_data.append("Specialty Contractor")
            relationship_lengths_list_perf_data.append(np.random.choice(["5+ years", "3-5 years", "1-3 years", "<1 year"], p=[0.3, 0.4, 0.2, 0.1]))
            annual_spends_list_perf_data.append(np.random.uniform(500000, 2000000))
            active_projects_list_perf_gen.append(np.random.randint(1, 4))
        else:
            supplier_types_list_perf_data.append("Material Supplier")
            relationship_lengths_list_perf_data.append(np.random.choice(["5+ years", "3-5 years", "1-3 years", "<1 year"], p=[0.2, 0.3, 0.4, 0.1]))
            annual_spends_list_perf_data.append(np.random.uniform(100000, 1000000))
            active_projects_list_perf_gen.append(np.random.randint(1, 3))
        categories_list_perf_gen.append(np.random.choice(current_construction_categories_list_perf, p=category_weights_perf_gen))

    df = pd.DataFrame({
        'supplier': suppliers_list_perf_data, 'supplier_type': supplier_types_list_perf_data, 'category': categories_list_perf_gen,
        'evaluation_date': evaluation_dates_perf_data, 'schedule_adherence': np.round(schedule_adherence_perf, 1),
        'work_quality': np.round(work_quality_perf, 1), 'cost_control': np.round(cost_control, 1),
        'safety_performance': np.round(safety_performance, 1), 'documentation': np.round(documentation, 1),
        'communication': np.round(communication, 1), 'problem_resolution': np.round(problem_resolution, 1),
        'overall_score': overall_scores_calc_perf, 'relationship_length': relationship_lengths_list_perf_data,
        'annual_spend': annual_spends_list_perf_data, 'active_projects': active_projects_list_perf_gen
    })

    comments_list_perf_data = [] # Renamed
    if not df.empty:
        for _, row_item_perf_data in df.iterrows(): # Renamed row
            comment_parts_perf_data = [] # Renamed
            if row_item_perf_data['overall_score'] >= 8.5: comment_parts_perf_data.append("Exceptional performer.")
            elif row_item_perf_data['overall_score'] >= 7.5: comment_parts_perf_data.append("Strong performance.")
            elif row_item_perf_data['overall_score'] >= 6.0: comment_parts_perf_data.append("Meets expectations.")
            elif row_item_perf_data['overall_score'] >= 4.0: comment_parts_perf_data.append("Performance issues identified.")
            else: comment_parts_perf_data.append("Significant performance concerns.")
            if row_item_perf_data['schedule_adherence'] < 5.0: comment_parts_perf_data.append("Schedule delays noted.")
            if row_item_perf_data['work_quality'] < 5.0: comment_parts_perf_data.append("Quality issues documented.")
            comments_list_perf_data.append(" ".join(comment_parts_perf_data))
    df['comments'] = comments_list_perf_data if comments_list_perf_data else [""] * len(df)
    df['evaluator'] = np.random.choice(["Project Manager", "Construction Director", "Procurement Lead"], size=num_to_select_perf) if num_to_select_perf > 0 else []
    return df

def generate_contract_data(n=30): # n will be 50 from config.py
    """Generate construction-specific contract data"""
    df_cols = [
        'name', 'supplier', 'type', 'start_date', 'end_date', 'value',
        'status', 'category', 'auto_renewal', 'notice_period_days', 'description'
    ]
    if n == 0: return pd.DataFrame(columns=df_cols)
    if not CONSTRUCTION_SUPPLIERS: return pd.DataFrame(columns=df_cols)

    allow_replacement_contract = n > len(CONSTRUCTION_SUPPLIERS) # Renamed
    suppliers_list_contract_data = np.random.choice(CONSTRUCTION_SUPPLIERS, size=n, replace=allow_replacement_contract) # Renamed

    contract_types_list_gen = ["Fixed Price", "Unit Price", "Cost Plus", "GMP", "Time & Materials", "Design-Build", "Design-Bid-Build", "CMAR", "IDIQ"] # Renamed
    contract_names_list_gen = [] # Renamed
    current_projects_list_contract_gen = CONSTRUCTION_PROJECTS if CONSTRUCTION_PROJECTS else ["Default Project"] # Renamed

    for sup_item_contract_gen in suppliers_list_contract_data: # Renamed supplier
        supplier_short_name_gen = sup_item_contract_gen.split()[0] if sup_item_contract_gen else "Supplier" # Renamed
        project_choice_contract_gen = np.random.choice(current_projects_list_contract_gen) # Renamed
        project_short_name_gen = " ".join(project_choice_contract_gen.split()[:2]) if project_choice_contract_gen else "Project" # Renamed
        contract_names_list_gen.append(f"{project_short_name_gen} - {supplier_short_name_gen} Agreement")

    current_date_contract = datetime.now() # Renamed
    start_dates_list_contract_gen = [] # Renamed
    end_dates_list_contract_gen = [] # Renamed
    for _ in range(n):
        start_dt_val_contract = current_date_contract - timedelta(days=np.random.randint(0, 1095)) # Renamed
        duration_days_val_contract = np.random.randint(180, 1095) # Renamed
        end_dt_val_contract = start_dt_val_contract + timedelta(days=duration_days_val_contract) # Renamed
        start_dates_list_contract_gen.append(start_dt_val_contract)
        end_dates_list_contract_gen.append(end_dt_val_contract)

    log_values_contract_data = np.random.lognormal(mean=13, sigma=1.2, size=n) # Renamed
    len_construction_suppliers_for_contract = len(CONSTRUCTION_SUPPLIERS) # Renamed
    for i, sup_item_contract_val_gen in enumerate(suppliers_list_contract_data): # Renamed
        if len_construction_suppliers_for_contract > 0 and sup_item_contract_val_gen in CONSTRUCTION_SUPPLIERS[:min(5, len_construction_suppliers_for_contract)]: 
            log_values_contract_data[i] *= np.random.uniform(1.5, 2.5)
        elif len_construction_suppliers_for_contract > 5 and sup_item_contract_val_gen in CONSTRUCTION_SUPPLIERS[min(5, len_construction_suppliers_for_contract):min(15, len_construction_suppliers_for_contract)]: 
            log_values_contract_data[i] *= np.random.uniform(0.8, 1.4)

    statuses_list_contract_gen = [] # Renamed
    for i in range(n):
        if end_dates_list_contract_gen[i] < current_date_contract: statuses_list_contract_gen.append("Expired")
        elif start_dates_list_contract_gen[i] > current_date_contract: statuses_list_contract_gen.append("Pending")
        else: statuses_list_contract_gen.append("Active")

    categories_list_contract_gen_data = [] # Renamed
    for sup_item_contract_gen_data in suppliers_list_contract_data: # Renamed
        if sup_item_contract_gen_data and ("Construction" in sup_item_contract_gen_data or "Building" in sup_item_contract_gen_data): 
            categories_list_contract_gen_data.append(np.random.choice(["General Construction", "Design-Build", "Construction Management"]))
        elif sup_item_contract_gen_data and any(term_contract_gen in sup_item_contract_gen_data for term_contract_gen in ["Steel", "Concrete", "Materials"]): 
            categories_list_contract_gen_data.append("Material Supply")
        elif sup_item_contract_gen_data and any(term_contract_gen in sup_item_contract_gen_data for term_contract_gen in ["Electric", "Plumbing", "Mechanical"]): 
            categories_list_contract_gen_data.append("MEP Services")
        else: 
            categories_list_contract_gen_data.append(np.random.choice(["Specialty Services", "Consulting", "Equipment Rental"]))

    df = pd.DataFrame({
        'name': contract_names_list_gen, 'supplier': suppliers_list_contract_data,
        'type': np.random.choice(contract_types_list_gen if contract_types_list_gen else ["Default Type"], size=n),
        'start_date': start_dates_list_contract_gen, 'end_date': end_dates_list_contract_gen, 'value': log_values_contract_data,
        'status': statuses_list_contract_gen, 'category': categories_list_contract_gen_data,
        'auto_renewal': np.random.choice([True, False], size=n, p=[0.3, 0.7]),
        'notice_period_days': np.random.choice([30, 60, 90], size=n)
    })

    descriptions_list_contract_gen = [] # Renamed
    if not df.empty:
        for _, row_item_contract_gen in df.iterrows(): # Renamed
            row_type_contract_gen = row_item_contract_gen['type'] # Renamed 
            row_cat_contract_gen = row_item_contract_gen['category'] # Renamed 
            if row_type_contract_gen == "Fixed Price": descriptions_list_contract_gen.append(f"Fixed price for {row_cat_contract_gen}.")
            elif row_type_contract_gen == "GMP": descriptions_list_contract_gen.append(f"GMP for {row_cat_contract_gen}.")
            else: descriptions_list_contract_gen.append(f"Standard {row_type_contract_gen} for {row_cat_contract_gen}.")
    df['description'] = descriptions_list_contract_gen if descriptions_list_contract_gen else [""] * len(df)
    return df

def generate_risk_alerts(n=50):
    """Generate construction-specific risk alerts"""
    df_cols = ['supplier', 'date', 'alert_type', 'description', 'severity', 'status', 'project', 'project_impact']
    if n == 0: return pd.DataFrame(columns=df_cols)
    if not CONSTRUCTION_SUPPLIERS: return pd.DataFrame(columns=df_cols)

    suppliers_list_alerts_data = np.random.choice(CONSTRUCTION_SUPPLIERS, size=n, replace=True) # Renamed

    end_date_alerts = datetime.now() # Renamed
    start_date_alerts = end_date_alerts - timedelta(days=90) # Renamed
    dates_list_alerts_data = [start_date_alerts + timedelta(days=np.random.randint(0, 90)) for _ in range(n)] # Renamed

    alert_types_list_gen_data = [] # Renamed 
    descriptions_list_gen_data = [] # Renamed 
    projects_list_gen_data = [] # Renamed 

    current_alert_types_list_gen = CONSTRUCTION_ALERT_TYPES if CONSTRUCTION_ALERT_TYPES else ["Default Alert Type"] # Renamed
    current_projects_list_alerts_gen = CONSTRUCTION_PROJECTS if CONSTRUCTION_PROJECTS else ["Default Project"] # Renamed
    current_categories_list_alerts_gen = CONSTRUCTION_CATEGORIES if CONSTRUCTION_CATEGORIES else ["Default Category"] # Renamed
    current_subcat_dict_alerts_gen = CONSTRUCTION_SUBCATEGORIES if CONSTRUCTION_SUBCATEGORIES else {"Default Category": ["Default Subcategory"]} # Renamed

    for i in range(n):
        alert_type_choice_val_gen = np.random.choice(current_alert_types_list_gen) # Renamed
        alert_types_list_gen_data.append(alert_type_choice_val_gen)
        projects_list_gen_data.append(np.random.choice(current_projects_list_alerts_gen))
        cat_choice_val_gen = np.random.choice(current_categories_list_alerts_gen) # Renamed
        subcat_options_gen = current_subcat_dict_alerts_gen.get(cat_choice_val_gen, ["Default Subcategory"]) # Renamed
        subcat_choice_val_gen = np.random.choice(subcat_options_gen if subcat_options_gen else ["Default Subcategory"]) # Renamed

        if alert_type_choice_val_gen == "Material Price Increase": descriptions_list_gen_data.append(f"{subcat_choice_val_gen} prices up {np.random.randint(5,30)}%.")
        elif alert_type_choice_val_gen == "Delivery Delay": descriptions_list_gen_data.append(f"{subcat_choice_val_gen} delivery delayed {np.random.randint(5,45)} days.")
        elif alert_type_choice_val_gen == "Labor Shortage": descriptions_list_gen_data.append(f"{np.random.choice(['Skilled', 'General'])} labor shortage impacting progress.")
        else: descriptions_list_gen_data.append(f"{alert_type_choice_val_gen}: Check details for {suppliers_list_alerts_data[i] if i < len(suppliers_list_alerts_data) else 'N/A'}.")


    severities_list_alerts_data = np.random.choice(["Low", "Medium", "High", "Critical"], size=n, p=[0.2, 0.4, 0.3, 0.1]) # Renamed
    statuses_list_alerts_gen_data = [] # Renamed
    for dt_item_alerts_gen in dates_list_alerts_data: # Renamed date
        days_ago_alerts_gen = (end_date_alerts - dt_item_alerts_gen).days # Renamed
        if days_ago_alerts_gen < 7: statuses_list_alerts_gen_data.append(np.random.choice(["Open", "Acknowledged"], p=[0.8, 0.2]))
        elif days_ago_alerts_gen < 21: statuses_list_alerts_gen_data.append(np.random.choice(["Open", "Acknowledged", "Resolved"], p=[0.3, 0.5, 0.2]))
        else: statuses_list_alerts_gen_data.append(np.random.choice(["Resolved", "Acknowledged"], p=[0.6,0.4])) 

    project_impacts_list_alerts_data = [] # Renamed
    for sev_item_alerts_gen in severities_list_alerts_data: # Renamed severity
        if sev_item_alerts_gen == "Critical": project_impacts_list_alerts_data.append(np.random.choice(["Major", "Severe"], p=[0.3, 0.7]))
        elif sev_item_alerts_gen == "High": project_impacts_list_alerts_data.append(np.random.choice(["Moderate", "Major"], p=[0.4, 0.6]))
        elif sev_item_alerts_gen == "Medium": project_impacts_list_alerts_data.append(np.random.choice(["Minor", "Moderate"], p=[0.5,0.5]))
        else: project_impacts_list_alerts_data.append(np.random.choice(["Minimal", "Minor"], p=[0.7, 0.3]))

    df = pd.DataFrame({
        'supplier': suppliers_list_alerts_data, 'date': dates_list_alerts_data, 'alert_type': alert_types_list_gen_data,
        'description': descriptions_list_gen_data, 'severity': severities_list_alerts_data, 'status': statuses_list_alerts_gen_data,
        'project': projects_list_gen_data, 'project_impact': project_impacts_list_alerts_data
    })
    return df

def generate_opportunity_data():
    """Generate construction-specific opportunity analysis data"""
    opportunities = [
        {"title": "Bundle Structural Material Orders", "description": "Consolidate structural steel and concrete orders across multiple projects to achieve volume discounts.", "savings_potential": 8.5, "complexity": 2, "annual_spend": 3800000, "category": "Structural Materials", "implementation_time": "1-3 months", "steps": ["Identify upcoming projects requiring similar materials", "Develop consolidated order schedule", "Negotiate volume-based pricing with suppliers", "Implement shared storage and logistics"]},
        {"title": "Standardize MEP System Specifications", "description": "Implement standard specifications for mechanical, electrical, and plumbing systems to reduce customization costs.", "savings_potential": 6.2, "complexity": 3, "annual_spend": 2900000, "category": "MEP Systems", "implementation_time": "3-6 months", "steps": ["Audit current MEP specifications across projects", "Identify standardization opportunities with minimal impact", "Develop standard specification library", "Train design and procurement teams on new standards"]},
        {"title": "Early Procurement of Long-Lead Items", "description": "Implement early procurement strategy for long-lead construction items to avoid expedite fees and market price increases.", "savings_potential": 5.8, "complexity": 2, "annual_spend": 1500000, "category": "Building Envelope", "implementation_time": "1-2 months", "steps": ["Identify critical long-lead items across projects", "Create early procurement schedule aligned with project timelines", "Negotiate early commitment discounts", "Secure storage arrangements for early deliveries"]},
        {"title": "Regional Supplier Development", "description": "Develop local/regional supplier relationships to reduce logistics costs and lead times.", "savings_potential": 4.5, "complexity": 4, "annual_spend": 2200000, "category": "Finishes", "implementation_time": "6-12 months", "steps": ["Map current supply chain geography", "Identify potential regional suppliers", "Qualify suppliers through assessment process", "Develop phased transition plan to regional sources"]},
        {"title": "Construction Equipment Pooling", "description": "Implement equipment pooling across multiple projects to increase utilization and reduce rental costs.", "savings_potential": 12.5, "complexity": 3, "annual_spend": 1800000, "category": "Sitework & Foundations", "implementation_time": "2-4 months", "steps": ["Audit current equipment utilization and costs", "Develop cross-project equipment scheduling system", "Negotiate revised rental terms with providers", "Implement tracking and logistics for equipment movement"]},
        {"title": "Safety Equipment Standardization", "description": "Standardize safety equipment across projects and negotiate enterprise pricing.", "savings_potential": 7.2, "complexity": 1, "annual_spend": 780000, "category": "Safety Equipment", "implementation_time": "1-2 months", "steps": ["Review current safety equipment specifications", "Develop standard safety equipment catalog", "Negotiate enterprise pricing with suppliers", "Implement inspection and replacement program"]},
        {"title": "Value Engineering for Sitework", "description": "Implement systematic value engineering process for sitework and foundation design to reduce material and labor costs.", "savings_potential": 9.5, "complexity": 3, "annual_spend": 3100000, "category": "Sitework & Foundations", "implementation_time": "3-6 months", "steps": ["Establish value engineering team with design and construction expertise", "Develop VE review process for all projects over $5M", "Create database of successful VE solutions", "Implement tracking system for VE savings"]},
        {"title": "Bulk Purchase of Finishing Materials", "description": "Establish annual bulk purchase agreements for high-volume finishing materials like paint, flooring, and drywall.", "savings_potential": 6.8, "complexity": 2, "annual_spend": 1650000, "category": "Finishes", "implementation_time": "2-3 months", "steps": ["Analyze annual usage quantities for finishing materials", "Identify storage and logistics requirements", "Negotiate annual supply agreements with tiered pricing", "Develop material allocation system for projects"]},
        {"title": "Prefabrication Strategy", "description": "Implement prefabrication approach for repetitive building elements to reduce on-site labor and improve quality.", "savings_potential": 11.2, "complexity": 4, "annual_spend": 4200000, "category": "Structural Materials", "implementation_time": "6-12 months", "steps": ["Identify high-potential prefabrication opportunities", "Engage design team for prefab-friendly design modifications", "Develop logistics plan for prefab components", "Establish quality control process for prefabricated elements"]},
        {"title": "Design Standardization Program", "description": "Implement design standardization for repeatable building elements across projects to reduce engineering and material costs.", "savings_potential": 8.7, "complexity": 5, "annual_spend": 2800000, "category": "MEP Systems", "implementation_time": "9-18 months", "steps": ["Conduct portfolio analysis of recent projects", "Identify common design elements with standardization potential", "Develop standard design library and specification guides", "Create training program for design and procurement teams"]}
    ]
    return pd.DataFrame(opportunities)

def generate_improvement_data():
    """Generate construction-specific performance improvement data"""
    improvements = [
        {"supplier": "Turner Construction", "title": "Schedule Compliance Improvement", "description": "Implement detailed milestone tracking and weekly progress reviews to improve schedule adherence.", "category": "Schedule Performance", "impact": "High", "effort": "Medium", "savings": 425000, "steps": ["Establish detailed milestone tracking system", "Implement weekly progress reviews with accountability", "Develop early warning indicators for schedule risks", "Create incentive program tied to milestone achievement"]},
        {"supplier": "Bechtel Corp", "title": "Quality Control Enhancement", "description": "Develop standardized QC protocols and inspection checklists to reduce rework and improve first-time quality.", "category": "Quality Management", "impact": "Medium", "effort": "Medium", "savings": 320000, "steps": ["Audit current quality performance and issues", "Develop standardized inspection checklists by trade", "Implement phased inspection process", "Train field supervisors on quality standards"]},
        {"supplier": "Suffolk Construction", "title": "Cost Reporting Improvement", "description": "Implement real-time cost reporting and variance analysis to improve cost control performance.", "category": "Cost Control", "impact": "High", "effort": "High", "savings": 580000, "steps": ["Evaluate current cost reporting practices", "Implement digital cost tracking system", "Develop variance analysis protocol", "Train project teams on cost control methods"]},
        {"supplier": "Clark Construction Group", "title": "Safety Program Enhancement", "description": "Develop comprehensive safety training and monitoring program to improve safety performance metrics.", "category": "Safety Performance", "impact": "High", "effort": "Medium", "savings": 275000, "steps": ["Conduct safety performance assessment", "Develop targeted training for high-risk activities", "Implement daily safety briefings and inspections", "Create near-miss reporting system"]},
        {"supplier": "DPR Construction", "title": "Documentation Standardization", "description": "Standardize project documentation processes and templates to improve completeness and timeliness.", "category": "Documentation", "impact": "Medium", "effort": "Low", "savings": 180000, "steps": ["Audit current documentation practices", "Develop standardized document templates", "Implement digital document management system", "Train teams on documentation requirements"]},
        {"supplier": "Skanska USA", "title": "Communication Protocol Implementation", "description": "Establish formal communication protocols and escalation paths to improve responsiveness and clarity.", "category": "Communication", "impact": "Medium", "effort": "Low", "savings": 150000, "steps": ["Define communication requirements by project role", "Establish response time standards", "Implement communication plan template", "Create escalation path for critical issues"]},
        {"supplier": "Whiting-Turner", "title": "Issue Resolution Process", "description": "Implement structured issue tracking and resolution process to improve problem-solving efficiency.", "category": "Problem Resolution", "impact": "High", "effort": "Medium", "savings": 340000, "steps": ["Develop issue categorization system", "Implement issue tracking database", "Establish resolution timeframes by issue type", "Create weekly issue review process"]},
        {"supplier": "Fluor Corp", "title": "BIM Implementation", "description": "Expand use of Building Information Modeling to improve coordination and reduce field conflicts.", "category": "Quality Management", "impact": "High", "effort": "High", "savings": 650000, "steps": ["Assess current BIM capabilities", "Develop BIM execution plan template", "Train project teams on clash detection", "Implement model-based coordination meetings"]},
        {"supplier": "Gilbane Building", "title": "Lean Construction Methods", "description": "Implement lean construction methodologies to reduce waste and improve production efficiency.", "category": "Schedule Performance", "impact": "High", "effort": "High", "savings": 520000, "steps": ["Analyze workflow and identify waste sources", "Implement pull planning for project scheduling", "Develop last planner system for field operations", "Create continuous improvement process"]},
        {"supplier": "Kiewit Corporation", "title": "Procurement Planning Enhancement", "description": "Improve procurement planning and tracking to prevent material-related delays and cost overruns.", "category": "Cost Control", "impact": "Medium", "effort": "Medium", "savings": 380000, "steps": ["Develop comprehensive procurement schedule template", "Implement submittal tracking system", "Create material expediting process", "Establish early warning system for procurement risks"]}
    ]
    return pd.DataFrame(improvements)

def generate_timeline_data(supplier=None):
    """Generate relationship timeline data for a specific supplier or random supplier"""
    df_cols_timeline = ['date', 'title', 'description', 'category', 'impact', 'supplier'] # Renamed
    if not CONSTRUCTION_SUPPLIERS: 
        return pd.DataFrame(columns=df_cols_timeline)

    supplier_choice_for_timeline = supplier if supplier and supplier in CONSTRUCTION_SUPPLIERS else np.random.choice(CONSTRUCTION_SUPPLIERS) # Renamed


    current_date_timeline = datetime.now() # Renamed
    timeline_start_date_for_timeline = current_date_timeline - timedelta(days=np.random.randint(1095, 1825)) # Renamed
    milestones_list_for_timeline = [] # Renamed

    onboarding_dt_for_timeline = timeline_start_date_for_timeline # Renamed
    milestones_list_for_timeline.append({"date": onboarding_dt_for_timeline, "title": "Initial Qualification", "description": f"Completed supplier qualification process for {supplier_choice_for_timeline}", "category": "Relationship", "impact": "Positive"})

    first_award_dt_for_timeline = onboarding_dt_for_timeline + timedelta(days=np.random.randint(30, 90)) # Renamed
    current_projects_list_for_timeline_gen = CONSTRUCTION_PROJECTS if CONSTRUCTION_PROJECTS else ["Default Project"] # Renamed
    project_choice_for_timeline_gen = np.random.choice(current_projects_list_for_timeline_gen) # Renamed
    milestones_list_for_timeline.append({"date": first_award_dt_for_timeline, "title": "First Project Award", "description": f"Awarded {project_choice_for_timeline_gen} project with estimated value of ${np.random.randint(5, 50)/10:.1f}M", "category": "Contract", "impact": "Positive"})

    num_events_for_timeline_gen = np.random.randint(5, 15) # Renamed
    event_dates_list_for_timeline_gen = [] # Renamed
    
    range_start_date_timeline = first_award_dt_for_timeline + timedelta(days=30) # Renamed
    range_end_date_timeline = current_date_timeline - timedelta(days=7) # Renamed

    if range_start_date_timeline < range_end_date_timeline :
        days_in_event_range_timeline = (range_end_date_timeline - range_start_date_timeline).days # Renamed
        # Ensure periods is at least 1 if days_in_event_range_timeline is small or 0.
        periods_for_event_range_timeline = max(1, days_in_event_range_timeline // 30 if days_in_event_range_timeline > 0 else 1) # Renamed

        possible_dates_list_for_timeline_gen = pd.date_range(start=range_start_date_timeline, end=range_end_date_timeline, periods=periods_for_event_range_timeline ) # Renamed
        if not possible_dates_list_for_timeline_gen.empty:
             event_dates_list_for_timeline_gen = np.random.choice(possible_dates_list_for_timeline_gen, size=min(num_events_for_timeline_gen, len(possible_dates_list_for_timeline_gen)), replace=False)
             event_dates_list_for_timeline_gen = sorted(event_dates_list_for_timeline_gen)

    event_types_for_timeline_gen = [ # Renamed
        ("Performance Review", "Completed quarterly performance review", "Performance", ["Positive", "Neutral", "Negative"], [0.6, 0.3, 0.1]),
        ("Contract Renewal", "Renewed master agreement for additional term", "Contract", ["Positive"], [1.0]),
        ("Contract Amendment", "Amended contract terms for scope adjustment", "Contract", ["Neutral", "Positive", "Negative"], [0.5, 0.3, 0.2]),
        ("Price Negotiation", "Completed price negotiation for upcoming projects", "Contract", ["Positive", "Neutral", "Negative"], [0.5, 0.3, 0.2]),
        ("Project Completion", "Successfully completed project on schedule", "Project", ["Positive", "Neutral"], [0.8, 0.2]),
        ("Schedule Issue", "Addressed schedule delay on active project", "Project", ["Negative", "Neutral"], [0.7, 0.3]),
        ("Quality Review", "Conducted quality review of completed work", "Project", ["Positive", "Neutral", "Negative"], [0.5, 0.3, 0.2]),
        ("Change Order", "Processed change order for scope modification", "Project", ["Neutral", "Negative", "Positive"], [0.6, 0.3, 0.1]),
        ("Risk Assessment", "Updated supplier risk assessment", "Risk", ["Neutral", "Negative", "Positive"], [0.6, 0.3, 0.1]),
        ("Safety Incident", "Addressed safety incident on project site", "Risk", ["Negative", "Neutral"], [0.8, 0.2]),
        ("Financial Review", "Completed financial stability review", "Risk", ["Positive", "Neutral", "Negative"], [0.5, 0.3, 0.2])
    ]

    for evt_date_val_timeline_gen in event_dates_list_for_timeline_gen: # Renamed
        if not event_types_for_timeline_gen: continue 
        evt_type_choice_timeline_gen = event_types_for_timeline_gen[np.random.choice(len(event_types_for_timeline_gen))] # Renamed
        title_val_timeline_gen = evt_type_choice_timeline_gen[0] # Renamed
        description_val_timeline_gen = evt_type_choice_timeline_gen[1] # Renamed
        category_val_timeline_gen = evt_type_choice_timeline_gen[2] # Renamed
        impact_val_timeline_gen = np.random.choice(evt_type_choice_timeline_gen[3], p=evt_type_choice_timeline_gen[4]) # Renamed

        if title_val_timeline_gen == "Performance Review":
            score_val_timeline_gen = np.random.randint(60, 95) # Renamed
            description_val_timeline_gen = f"Quarterly performance review completed with score of {score_val_timeline_gen}/100"
            if score_val_timeline_gen >= 85: impact_val_timeline_gen = "Positive"
            elif score_val_timeline_gen >= 70: impact_val_timeline_gen = "Neutral"
            else: impact_val_timeline_gen = "Negative"
        elif title_val_timeline_gen == "Project Completion":
            project_comp_name_timeline_gen = np.random.choice(current_projects_list_for_timeline_gen) # Renamed
            on_time_val_timeline_gen = np.random.choice([True, False], p=[0.7, 0.3]) # Renamed
            on_budget_val_timeline_gen = np.random.choice([True, False], p=[0.7, 0.3]) # Renamed
            if on_time_val_timeline_gen and on_budget_val_timeline_gen: description_val_timeline_gen = f"Completed {project_comp_name_timeline_gen} on time and within budget"; impact_val_timeline_gen = "Positive"
            elif on_time_val_timeline_gen: description_val_timeline_gen = f"Completed {project_comp_name_timeline_gen} on time but over budget"; impact_val_timeline_gen = "Neutral"
            elif on_budget_val_timeline_gen: description_val_timeline_gen = f"Completed {project_comp_name_timeline_gen} within budget but delayed"; impact_val_timeline_gen = "Neutral"
            else: description_val_timeline_gen = f"Completed {project_comp_name_timeline_gen} with delays and budget overruns"; impact_val_timeline_gen = "Negative"
        elif title_val_timeline_gen == "Risk Assessment":
            risk_level_val_timeline_gen = np.random.choice(["Low", "Medium", "High", "Critical"]) # Renamed
            description_val_timeline_gen = f"Updated risk assessment - current level: {risk_level_val_timeline_gen}"
            if risk_level_val_timeline_gen == "Low": impact_val_timeline_gen = "Positive"
            elif risk_level_val_timeline_gen == "Medium": impact_val_timeline_gen = "Neutral"
            else: impact_val_timeline_gen = "Negative"
        milestones_list_for_timeline.append({"date": evt_date_val_timeline_gen, "title": title_val_timeline_gen, "description": description_val_timeline_gen, "category": category_val_timeline_gen, "impact": impact_val_timeline_gen})

    recent_date_val_for_timeline_gen = current_date_timeline - timedelta(days=np.random.randint(1, 7)) # Renamed
    recent_event_choices_list_timeline_gen = [  # Renamed
        {"date": recent_date_val_for_timeline_gen, "title": "Strategy Discussion", "description": f"Met with {supplier_choice_for_timeline} leadership to discuss future partnership opportunities", "category": "Relationship", "impact": "Positive"},
        {"date": recent_date_val_for_timeline_gen, "title": "Performance Improvement Plan", "description": f"Initiated performance improvement plan for {supplier_choice_for_timeline} in response to recent issues", "category": "Performance", "impact": "Neutral"},
        {"date": recent_date_val_for_timeline_gen, "title": "Contract Renewal Discussion", "description": f"Began contract renewal discussions with {supplier_choice_for_timeline} for upcoming term", "category": "Contract", "impact": "Neutral"}
    ]
    if recent_event_choices_list_timeline_gen: 
        milestones_list_for_timeline.append(recent_event_choices_list_timeline_gen[np.random.choice(len(recent_event_choices_list_timeline_gen))])

    df = pd.DataFrame(milestones_list_for_timeline)
    if not df.empty:
        df = df.sort_values("date")
    df["supplier"] = supplier_choice_for_timeline 
    return df
