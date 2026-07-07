CREATE DATABASE financial_analytics;
USE financial_analytics;
-- ==========================================
-- FINANCIAL ANALYTICS ENGINE: DATABASE SETUP
-- ==========================================

-- 1. CREATE CORE TABLES
-- ------------------------------------------
CREATE TABLE chart_of_accounts (
    account_id INT PRIMARY KEY,
    account_name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL
);

CREATE TABLE general_ledger (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_date DATE,
    account_id INT,
    amount DECIMAL(15,2),
    description VARCHAR(225),
    FOREIGN KEY (account_id) REFERENCES chart_of_accounts(account_id)
);

-- 2. SEED THE DICTIONARY (CHART OF ACCOUNTS)
-- ------------------------------------------
-- We need these base accounts to exist before a user uploads a CSV
INSERT INTO chart_of_accounts (account_id, account_name, account_type) VALUES
(101, 'Cash Operating', 'Asset'),
(201, 'Bank Loan', 'Liability'),
(401, 'Sales Revenue', 'Revenue'),
(501, 'Software Cloud Hosting', 'Expense');

-- 3. CREATE VALIDATION ENGINE VIEWS (ANOMALIES)
-- ------------------------------------------
-- View A: Duplicate Transaction Catcher
CREATE VIEW vw_duplicate_transactions AS
WITH DuplicateCheck AS (
    SELECT 
        transaction_id, transaction_date, account_id, amount, description,
        ROW_NUMBER() OVER(PARTITION BY transaction_date, account_id, amount ORDER BY transaction_id ASC) as rank_id
    FROM general_ledger
)
SELECT * FROM DuplicateCheck
WHERE rank_id > 1;

-- View B: The 200% Expense Spike Detector
CREATE VIEW vw_expense_spikes AS
WITH ExpenseHistory AS (
    SELECT
        transaction_date, account_id, amount, 
        LAG(amount, 1) OVER(PARTITION BY account_id ORDER BY transaction_date) AS previous_amount
    FROM general_ledger
    WHERE account_id = 501
)
SELECT 
    transaction_date, account_id, amount, previous_amount,
    (((amount - previous_amount) / previous_amount) * 100) AS spike_percentage
FROM ExpenseHistory
WHERE previous_amount IS NOT NULL 
  AND (((amount - previous_amount) / previous_amount) * 100) > 200;

-- 4. CREATE FINANCIAL REPORT VIEWS
-- ------------------------------------------
-- View C: All-Time Profit & Loss 
CREATE VIEW vw_profit_and_loss AS
SELECT 
    SUM(CASE WHEN a.account_type = 'Revenue' THEN l.amount ELSE 0 END) AS Total_Revenue,
    SUM(CASE WHEN a.account_type = 'Expense' THEN l.amount ELSE 0 END) AS Total_Expense,
    SUM(CASE WHEN a.account_type = 'Revenue' THEN l.amount ELSE 0 END) - 
    SUM(CASE WHEN a.account_type = 'Expense' THEN l.amount ELSE 0 END) AS Net_Profit
FROM general_ledger l
INNER JOIN chart_of_accounts a ON l.account_id = a.account_id;

-- View D: Real-Time Balance Sheet Snapshot
CREATE VIEW vw_balance_sheet AS
SELECT
    SUM(CASE WHEN a.account_type = 'Asset' THEN l.amount ELSE 0 END) AS Total_Assets,
    SUM(CASE WHEN a.account_type = 'Liability' THEN l.amount ELSE 0 END) AS Total_Liabilities,
    SUM(CASE WHEN a.account_type = 'Asset' THEN l.amount ELSE 0 END) - 
    SUM(CASE WHEN a.account_type = 'Liability' THEN l.amount ELSE 0 END) AS Net_Position
FROM general_ledger l
INNER JOIN chart_of_accounts a ON l.account_id = a.account_id;
