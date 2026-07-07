# 📊 Financial Data Analytics & Anomaly Detection Engine

## 📖 What This Project Is

This project is a full-stack data pipeline and interactive web dashboard designed to automate core accounting reports and detect financial anomalies using advanced SQL Window Functions. 

It allows users to upload raw general ledger data (CSV) via a secure web interface, automatically injects the data into a relational database, and instantly generates real-time business intelligence metrics and fraud/anomaly alerts.

---

## 🚀 Key Features

* **Automated Anomaly Detection Engine:** Utilizes advanced SQL (`LAG()`, `ROW_NUMBER()`, `PARTITION BY`) to automatically flag duplicate ledger entries and sudden month-over-month expense spikes.
* **Real-Time Financial Reporting:** Uses conditional aggregation pipelines to instantly calculate All-Time Profit & Loss (P&L) and Balance Sheet metrics.
* **Interactive Python Frontend:** Built with Streamlit, providing a code-free, drag-and-drop user interface for end-users.
* **Secure Database Connection:** Dynamic authentication sidebar ensures database credentials remain secure and are never hardcoded into the repository.
* **Data Validation:** Includes a downloadable CSV template to ensure strict schema adherence before data ingestion.

---

## 🛠️ Technology Used

* **Database:** MySQL (Relational Schema, Complex Views, CTEs, Window Functions)
* **Backend Logic:** Python 3.x
* **Data Processing:** Pandas
* **Database Driver:** `mysql-connector-python`
* **Frontend UI:** Streamlit

---

## 📂 Project Structure

```text
financial-data-analytics/
├── app.py                   # Main Streamlit application and Python backend
├── database_setup.sql       # SQL script to initialize tables and analytical views
├── requirements.txt         # Python library dependencies
├── .gitignore               # Ignored system and cache files
└── README.md                # Project documentation
```

---

## 🏃‍♂️ How to Run

### 1. Setup the Repository

First, clone the code to your machine and navigate into the project folder:

```bash
git clone https://github.com/AvneetSingh11/financial-data-analytics.git
cd financial-data-analytics
```

### 2. Database Initialization

Before running the Python application, you must build the SQL architecture:

* Open MySQL Workbench (or your preferred SQL client).
* Create a new, blank database schema by running:
  ```sql
  CREATE DATABASE financial_analytics;
  ```
* Open the `database_setup.sql` file provided in this repository and execute the entire script. This will instantly build the `chart_of_accounts`, the `general_ledger`, and all required analytical VIEWS.

### 3. Install Python Dependencies

Install the required Python libraries using the provided text file:

```bash
pip install -r requirements.txt
```

### 4. Launch the Application

Start the Streamlit server to open the web dashboard:

```bash
streamlit run app.py
```

---

## 💡 How to Use

Once the application is running, follow these exact steps to process a ledger:

### 1. Authenticate the Database
* Open the **gear icon (⚙️) sidebar** on the left side of the screen.
* Enter your local MySQL username (usually `root`) and password. *(Your credentials are used purely for local connection and are never stored).*

### 2. Format Your Financial Data
* Click the **📥 Download CSV Template** button.
* Open the downloaded `ledger_upload_template.csv` file.
* Ensure your data matches the exact column headers: `transaction_date`, `account_id`, `amount`, and `description`.
* **Pro-Tip:** To test the Anomaly Engine, intentionally add a duplicate row, or add a massive, sudden expense spike for account `501`!

### 3. Process the Ledger
* Drag and drop your completed CSV file into the upload zone.
* Click **🚀 Process Financial Data**.
* The Python backend will automatically establish the MySQL connection and execute a bulk `INSERT` into the `general_ledger` table.

### 4. Review the Dashboard
Once processing is complete, the SQL engine calculates the metrics and instantly returns:
* **Top-Level Metrics:** Real-time Net Profit, Total Assets, and Total Liabilities.
* **Anomaly Alerts:** Red and yellow warning tables will immediately flag any duplicate entries or 200%+ expense spikes.

---