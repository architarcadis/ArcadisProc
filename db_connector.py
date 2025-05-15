import os
import pandas as pd
import streamlit as st

# Try to import psycopg2, but don't fail if it's not available
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

def get_connection():
    """
    Get a connection to the PostgreSQL database.
    Uses environment variables for connection details.
    Returns None if psycopg2 is not available.
    """
    if not PSYCOPG2_AVAILABLE:
        return None
        
    try:
        # Import psycopg2 locally to avoid errors when it's not installed
        import psycopg2
        conn = psycopg2.connect(
            host=os.environ.get("PGHOST", "localhost"),
            database=os.environ.get("PGDATABASE", "postgres"),
            user=os.environ.get("PGUSER", "postgres"),
            password=os.environ.get("PGPASSWORD", ""),
            port=os.environ.get("PGPORT", "5432")
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

def query_data(sql_query):
    """
    Execute a SQL query and return the results as a pandas DataFrame.
    """
    try:
        conn = get_connection()
        if conn:
            df = pd.read_sql_query(sql_query, conn)
            conn.close()
            return df
        return None
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None

def get_suppliers():
    """
    Get all suppliers from the database.
    """
    sql = "SELECT * FROM suppliers ORDER BY name"
    return query_data(sql)

def get_categories():
    """
    Get all categories from the database.
    """
    sql = "SELECT * FROM categories ORDER BY name"
    return query_data(sql)

def get_spend_data(category_id=None, supplier_id=None, start_date=None, end_date=None):
    """
    Get spend data with optional filtering.
    """
    sql = "SELECT sd.*, s.name as supplier_name, c.name as category_name FROM spend_data sd "
    sql += "LEFT JOIN suppliers s ON sd.supplier_id = s.id "
    sql += "LEFT JOIN categories c ON sd.category_id = c.id "
    
    conditions = []
    if category_id:
        conditions.append(f"sd.category_id = {category_id}")
    if supplier_id:
        conditions.append(f"sd.supplier_id = {supplier_id}")
    if start_date:
        conditions.append(f"sd.date >= '{start_date}'")
    if end_date:
        conditions.append(f"sd.date <= '{end_date}'")
    
    if conditions:
        sql += "WHERE " + " AND ".join(conditions)
    
    sql += " ORDER BY sd.date DESC"
    
    return query_data(sql)

def get_risk_assessments(supplier_id=None):
    """
    Get risk assessment data with optional supplier filtering.
    """
    sql = "SELECT ra.*, s.name as supplier_name FROM risk_assessments ra "
    sql += "LEFT JOIN suppliers s ON ra.supplier_id = s.id "
    
    if supplier_id:
        sql += f"WHERE ra.supplier_id = {supplier_id} "
    
    sql += "ORDER BY ra.created_at DESC"
    
    return query_data(sql)

def get_supplier_performance(supplier_id=None):
    """
    Get supplier performance data with optional filtering.
    """
    sql = "SELECT sp.*, s.name as supplier_name FROM supplier_performance sp "
    sql += "LEFT JOIN suppliers s ON sp.supplier_id = s.id "
    
    if supplier_id:
        sql += f"WHERE sp.supplier_id = {supplier_id} "
    
    sql += "ORDER BY sp.created_at DESC"
    
    return query_data(sql)

def get_contracts(supplier_id=None, status=None):
    """
    Get contracts with optional filtering.
    """
    sql = "SELECT c.*, s.name as supplier_name FROM contracts c "
    sql += "LEFT JOIN suppliers s ON c.supplier_id = s.id "
    
    conditions = []
    if supplier_id:
        conditions.append(f"c.supplier_id = {supplier_id}")
    if status:
        conditions.append(f"c.status = '{status}'")
    
    if conditions:
        sql += "WHERE " + " AND ".join(conditions)
    
    sql += " ORDER BY c.end_date ASC"
    
    return query_data(sql)

def get_risk_alerts(supplier_id=None, severity=None, status=None):
    """
    Get risk alerts with optional filtering.
    """
    sql = "SELECT ra.*, s.name as supplier_name FROM risk_alerts ra "
    sql += "LEFT JOIN suppliers s ON ra.supplier_id = s.id "
    
    conditions = []
    if supplier_id:
        conditions.append(f"ra.supplier_id = {supplier_id}")
    if severity:
        conditions.append(f"ra.severity = '{severity}'")
    if status:
        conditions.append(f"ra.status = '{status}'")
    
    if conditions:
        sql += "WHERE " + " AND ".join(conditions)
    
    sql += " ORDER BY ra.created_date DESC"
    
    return query_data(sql)

# Function to check database connection
def check_db_connection():
    """
    Check if we can connect to the database and has required tables.
    Returns a tuple of (connection_successful, error_message)
    """
    # If psycopg2 is not available, return False
    if not PSYCOPG2_AVAILABLE:
        return False, "psycopg2 library not installed - using mock data"
    
    try:
        conn = get_connection()
        if not conn:
            return False, "Could not establish database connection"
        
        # Now we know psycopg2 is available and we have a connection
        from psycopg2.extras import RealDictCursor
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check if required tables exist
        table_check_sql = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_name IN ('suppliers', 'categories', 'spend_data', 'risk_assessments', 
                              'supplier_performance', 'contracts', 'risk_alerts')
        """
        cursor.execute(table_check_sql)
        tables = cursor.fetchall()
        found_tables = [table['table_name'] for table in tables]
        
        required_tables = ['suppliers', 'categories', 'spend_data', 'risk_assessments', 
                          'supplier_performance', 'contracts', 'risk_alerts']
        
        missing_tables = [table for table in required_tables if table not in found_tables]
        
        conn.close()
        
        if missing_tables:
            return False, f"Missing required tables: {', '.join(missing_tables)}"
        
        return True, "Connected to database successfully"
    
    except Exception as e:
        return False, f"Error checking database: {str(e)}"