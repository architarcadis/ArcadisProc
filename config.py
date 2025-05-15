"""
Configuration settings for the ArcadiaProcure Construction Insights Streamlit application.
"""

# Application Info
APP_NAME = "ArcadiaProcure Insights"
APP_VERSION = "1.2.0"
APP_DESCRIPTION = "Construction Procurement Analytics Platform"

# Dashboard Configuration
DASHBOARD_CONFIG = {
    "refresh_interval": 3600,  # Data refresh interval in seconds
    "default_date_range": 365,  # Default date range in days
    "chart_height": 450        # Default chart height in pixels
}

# Database Configuration
DATABASE_CONFIG = {
    "use_mock_data": True,     # Set to False to use database connection
    "mock_data_size": {
        "spend_data": 1000,    # Number of spend records
        "suppliers": 40,       # Number of suppliers
        "contracts": 100,      # Number of contracts
        "risk_alerts": 50      # Number of risk alerts
    }
}

# Chart Colors
CHART_COLORS = [
    "#3366CC",  # Primary blue
    "#FF5722",  # Primary orange
    "#4CAF50",  # Green
    "#9C27B0",  # Purple
    "#FFC107",  # Amber
    "#00BCD4",  # Cyan
    "#FF9800",  # Orange
    "#795548",  # Brown
    "#607D8B",  # Blue Grey
    "#E91E63"   # Pink
]

# Risk Levels
RISK_LEVELS = {
    "low": {
        "label": "Low",
        "color": "#4CAF50",
        "description": "Minimal risk with little to no impact on procurement/construction operations"
    },
    "medium": {
        "label": "Medium",
        "color": "#FFC107",
        "description": "Moderate risk with potential for project delays or minor cost increases"
    },
    "high": {
        "label": "High",
        "color": "#FF9800",
        "description": "Significant risk with likely impact on project timeline, cost, or quality"
    },
    "critical": {
        "label": "Critical",
        "color": "#F44336",
        "description": "Severe risk requiring immediate attention to avoid major project disruption"
    }
}

# Performance Levels
PERFORMANCE_LEVELS = {
    "poor": {
        "label": "Poor",
        "color": "#F44336",
        "description": "Consistently below expectations, requires significant improvement"
    },
    "fair": {
        "label": "Fair",
        "color": "#FF9800",
        "description": "Meets some expectations but has substantial room for improvement"
    },
    "good": {
        "label": "Good",
        "color": "#4CAF50",
        "description": "Consistently meets expectations with minor areas for improvement"
    },
    "excellent": {
        "label": "Excellent",
        "color": "#2196F3",
        "description": "Consistently exceeds expectations and sets industry benchmarks"
    }
}

# Construction-specific categories
CONSTRUCTION_CATEGORIES = [
    "Structural Materials",
    "MEP Systems",
    "Building Envelope",
    "Finishes",
    "Sitework & Foundations",
    "Safety Equipment"
]

# Construction-specific supplier segments
CONSTRUCTION_SUPPLIER_SEGMENTS = [
    "Prime Contractors",
    "Major Subcontractors",
    "Specialty Contractors/Suppliers",
    "Material Manufacturers",
    "Equipment Providers",
    "Labor Providers"
]

# Construction risk factors
CONSTRUCTION_RISK_FACTORS = [
    "Material Price Volatility",
    "Labor Availability",
    "Regulatory Compliance",
    "Weather Impacts",
    "Safety Performance",
    "Quality Control",
    "Lead Time Reliability",
    "Financial Stability"
]