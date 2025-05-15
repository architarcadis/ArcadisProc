# ArcadiaProcure Construction Insights

A powerful data analytics platform for construction procurement professionals that provides strategic insights into material category management, vendor risk assessment, and subcontractor relationship tracking to optimize project costs and mitigate supply chain risks.

## Features

- **Dashboard**: Overview of key procurement metrics for construction materials and services
- **Materials Intelligence**: In-depth analysis of construction material categories, spending trends, and price volatility
- **Vendor Risk**: Comprehensive risk assessment for construction subcontractors and material suppliers
- **Subcontractor Relationship**: Performance tracking and opportunity identification for trade partners
- **Data Upload**: Easy data import functionality with template validation
- **Templates**: Downloadable templates for standardized data collection

## Deployment Instructions

### Option 1: Deploy on Streamlit Cloud

1. Sign up for a free account at [Streamlit Cloud](https://streamlit.io/cloud)
2. Create a new GitHub repository and upload all the files from this package
3. Connect your GitHub repository to Streamlit Cloud
4. Set the main file to `app.py`
5. Add any required secrets in the Streamlit Cloud dashboard (if connecting to a database)

### Option 2: Run Locally

1. Install Python 3.9+ if not already installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Database Configuration

The application works with both mock data (default) and a PostgreSQL database connection.

To use a real database:
1. Set up a PostgreSQL database with the required schema
2. Configure the following environment variables:
   - `PGHOST` - Database host address
   - `PGDATABASE` - Database name
   - `PGUSER` - Database username
   - `PGPASSWORD` - Database password
   - `PGPORT` - Database port (default: 5432)
3. Update the `use_mock_data` setting in `config.py` to `False`

## Customization

- **Branding**: Update the logo in the `assets` folder and modify the app title in `config.py`
- **Colors**: Adjust the color scheme in the `CHART_COLORS` section of `config.py`
- **Categories**: Modify the construction categories in `data_generator.py` for more industry-specific terminology
- **Data Size**: Adjust the mock data generation size in `DATABASE_CONFIG` within `config.py`

## Support

For questions or issues, contact your system administrator or development team.

## License

© 2025 ArcadiaProcure