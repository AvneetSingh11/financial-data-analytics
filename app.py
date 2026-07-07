import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ==========================================
# 1. PAGE SETUP & UI HEADER
# ==========================================
st.set_page_config(page_title="Financial Analytics Engine", layout="wide")
st.title("📊 Financial Data Analytics & Anomaly Detection")
st.markdown("Upload your general ledger CSV below to process financial reports and flag anomalies.")

# ==========================================
# 2. SECURE DATABASE CONNECTION (SIDEBAR)
# ==========================================
# THIS is the section that creates the sidebar!
st.sidebar.header("⚙️ Database Connection")
db_user = st.sidebar.text_input("MySQL Username", value="root")
db_password = st.sidebar.text_input("MySQL Password", type="password")
db_host = st.sidebar.text_input("Host", value="localhost")
db_name = st.sidebar.text_input("Database Name", value="financial_analytics")

def create_connection():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return connection
    except Error as e:
        st.sidebar.error(f"Connection failed: {e}")
        return None

# ==========================================
# 3. DATA INSERTION LOGIC
# ==========================================
def insert_ledger_data(df, connection):
    """Inserts Pandas DataFrame rows into the MySQL general_ledger table."""
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO general_ledger (transaction_date, account_id, amount, description)
    VALUES (%s, %s, %s, %s)
    """
    
    # Convert DataFrame to a list of tuples for insertion
    data_tuples = list(df.itertuples(index=False, name=None))
    
    try:
        # executemany is much faster than running a loop for bulk inserts
        cursor.executemany(insert_query, data_tuples)
        connection.commit()
        return cursor.rowcount
    except Error as e:
        st.error(f"Failed to insert data: {e}")
        return 0
    finally:
        cursor.close()

# ==========================================
# 4. MAIN APPLICATION FLOW
# ==========================================
st.divider()

# --- Template Download ---
st.subheader("1. Format Your Data")
template_data = {
    "transaction_date": ["2026-07-01", "2026-07-02"],
    "account_id": [101, 501],
    "amount": [1000.00, 100.00],
    "description": ["Initial Funding", "AWS Monthly Bill"]
}
template_df = pd.DataFrame(template_data)
csv_template = template_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download CSV Template",
    data=csv_template,
    file_name="ledger_upload_template.csv",
    mime="text/csv"
)

st.divider()

# --- File Upload & Processing ---
st.subheader("2. Upload Your Ledger")
uploaded_file = st.file_uploader("Drop your formatted CSV here", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # We only process if the user has entered their DB password
    if st.button("🚀 Process Financial Data"):
        if not db_password:
            st.warning("Please enter your MySQL Password in the sidebar on the left first.")
        else:
            conn = create_connection()
            if conn and conn.is_connected():
                with st.spinner("Injecting data into SQL database..."):
                    rows_inserted = insert_ledger_data(df, conn)
                
                if rows_inserted > 0:
                    st.success(f"Successfully processed {rows_inserted} transactions!")
                    
                    # ==========================================
                    # 5. THE DASHBOARD (READING FROM SQL VIEWS)
                    # ==========================================
                    st.markdown("## 📈 Financial Intelligence Dashboard")
                    
                    # Fetching the core reports using Pandas read_sql
                    pl_df = pd.read_sql("SELECT * FROM vw_profit_and_loss", conn)
                    bs_df = pd.read_sql("SELECT * FROM vw_balance_sheet", conn)
                    
                    # Layout: Create 3 columns for Top-Level Metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(label="Net Profit (All-Time)", value=f"${pl_df['Net_Profit'].iloc[0]:,.2f}")
                    with col2:
                        st.metric(label="Total Assets", value=f"${bs_df['Total_Assets'].iloc[0]:,.2f}")
                    with col3:
                        st.metric(label="Total Liabilities", value=f"${bs_df['Total_Liabilities'].iloc[0]:,.2f}")
                    
                    st.divider()
                    
                    # Fetching and displaying the Anomalies
                    st.markdown("## 🚨 Anomaly Detection Engine")
                    
                    dup_df = pd.read_sql("SELECT * FROM vw_duplicate_transactions", conn)
                    spike_df = pd.read_sql("SELECT * FROM vw_expense_spikes", conn)
                    
                    col_anom1, col_anom2 = st.columns(2)
                    
                    with col_anom1:
                        st.error(f"Duplicate Transactions Found: {len(dup_df)}")
                        if not dup_df.empty:
                            st.dataframe(dup_df, hide_index=True)
                            
                    with col_anom2:
                        st.warning(f"Expense Spikes (>200%) Found: {len(spike_df)}")
                        if not spike_df.empty:
                            st.dataframe(spike_df, hide_index=True)
                            
                    conn.close()