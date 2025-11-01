-- =============================================
-- Bank Account Management System
-- Views and Common Queries
-- =============================================

\c bank_management;
SET search_path TO banking, public;

-- =============================================
-- View: customer_account_summary
-- Description: Summary of all customer accounts
-- =============================================
CREATE OR REPLACE VIEW customer_account_summary AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.phone,
    COUNT(a.account_id) AS total_accounts,
    SUM(a.balance) AS total_balance,
    STRING_AGG(DISTINCT at.type_name, ', ') AS account_types,
    c.created_at AS customer_since
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id AND a.status = 'ACTIVE'
LEFT JOIN account_types at ON a.account_type_id = at.account_type_id
WHERE c.is_active = TRUE
GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.phone, c.created_at;

-- =============================================
-- View: account_details
-- Description: Detailed account information
-- =============================================
CREATE OR REPLACE VIEW account_details AS
SELECT 
    a.account_id,
    a.account_number,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    at.type_name AS account_type,
    a.balance,
    a.currency,
    a.status,
    a.opened_date,
    at.minimum_balance,
    at.interest_rate,
    at.monthly_fee,
    CASE 
        WHEN a.balance < at.minimum_balance THEN 'Below Minimum'
        ELSE 'OK'
    END AS balance_status
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id
JOIN account_types at ON a.account_type_id = at.account_type_id;

-- =============================================
-- View: recent_transactions
-- Description: Recent transactions with details
-- =============================================
CREATE OR REPLACE VIEW recent_transactions AS
SELECT 
    t.transaction_id,
    t.transaction_number,
    a.account_number,
    c.first_name || ' ' || c.last_name AS customer_name,
    tt.type_name AS transaction_type,
    t.amount,
    t.balance_after,
    t.transaction_date,
    t.description,
    t.status
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
ORDER BY t.transaction_date DESC;

-- =============================================
-- View: transfer_history
-- Description: Transfer history between accounts
-- =============================================
CREATE OR REPLACE VIEW transfer_history AS
SELECT 
    tr.transfer_id,
    tr.transfer_number,
    a1.account_number AS from_account,
    c1.first_name || ' ' || c1.last_name AS from_customer,
    a2.account_number AS to_account,
    c2.first_name || ' ' || c2.last_name AS to_customer,
    tr.amount,
    tr.transfer_date,
    tr.description,
    tr.status
FROM transfers tr
JOIN accounts a1 ON tr.from_account_id = a1.account_id
JOIN customers c1 ON a1.customer_id = c1.customer_id
JOIN accounts a2 ON tr.to_account_id = a2.account_id
JOIN customers c2 ON a2.customer_id = c2.customer_id
ORDER BY tr.transfer_date DESC;

-- =============================================
-- View: loan_summary
-- Description: Summary of all loans
-- =============================================
CREATE OR REPLACE VIEW loan_summary AS
SELECT 
    l.loan_id,
    l.loan_number,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    l.loan_type,
    l.principal_amount,
    l.interest_rate,
    l.term_months,
    l.monthly_payment,
    l.outstanding_balance,
    l.principal_amount - l.outstanding_balance AS amount_paid,
    ROUND((l.principal_amount - l.outstanding_balance) / l.principal_amount * 100, 2) AS percent_paid,
    l.start_date,
    l.end_date,
    l.status,
    COUNT(lp.payment_id) AS payments_made
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
LEFT JOIN loan_payments lp ON l.loan_id = lp.loan_id AND lp.status = 'PAID'
GROUP BY l.loan_id, l.loan_number, c.customer_id, c.first_name, c.last_name, 
         c.email, l.loan_type, l.principal_amount, l.interest_rate, l.term_months,
         l.monthly_payment, l.outstanding_balance, l.start_date, l.end_date, l.status;

-- =============================================
-- View: card_details
-- Description: Card information with account details
-- =============================================
CREATE OR REPLACE VIEW card_details AS
SELECT 
    cd.card_id,
    cd.card_number,
    cd.card_type,
    cd.card_holder_name,
    cd.expiry_date,
    cd.status AS card_status,
    a.account_number,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    cd.credit_limit,
    cd.issued_date,
    CASE 
        WHEN cd.expiry_date < CURRENT_DATE THEN 'Expired'
        WHEN cd.expiry_date < CURRENT_DATE + INTERVAL '3 months' THEN 'Expiring Soon'
        ELSE 'Valid'
    END AS expiry_status
FROM cards cd
JOIN accounts a ON cd.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id;

-- =============================================
-- View: monthly_transaction_summary
-- Description: Monthly transaction summary by account
-- =============================================
CREATE OR REPLACE VIEW monthly_transaction_summary AS
SELECT 
    a.account_id,
    a.account_number,
    c.first_name || ' ' || c.last_name AS customer_name,
    DATE_TRUNC('month', t.transaction_date) AS month,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(CASE WHEN tt.type_name IN ('DEPOSIT', 'TRANSFER_IN', 'INTEREST', 'REFUND') 
             THEN t.amount ELSE 0 END) AS total_credits,
    SUM(CASE WHEN tt.type_name IN ('WITHDRAWAL', 'TRANSFER_OUT', 'FEE', 'ATM_WITHDRAWAL', 'ONLINE_PAYMENT') 
             THEN t.amount ELSE 0 END) AS total_debits,
    SUM(CASE WHEN tt.type_name IN ('DEPOSIT', 'TRANSFER_IN', 'INTEREST', 'REFUND') 
             THEN t.amount ELSE -t.amount END) AS net_change
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
WHERE t.status = 'COMPLETED'
GROUP BY a.account_id, a.account_number, c.first_name, c.last_name, DATE_TRUNC('month', t.transaction_date)
ORDER BY month DESC, a.account_number;

-- =============================================
-- View: customer_financial_overview
-- Description: Complete financial overview per customer
-- =============================================
CREATE OR REPLACE VIEW customer_financial_overview AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.phone,
    COALESCE(SUM(a.balance), 0) AS total_account_balance,
    COALESCE(SUM(l.outstanding_balance), 0) AS total_loan_balance,
    COALESCE(SUM(a.balance), 0) - COALESCE(SUM(l.outstanding_balance), 0) AS net_worth,
    COUNT(DISTINCT a.account_id) AS total_accounts,
    COUNT(DISTINCT l.loan_id) AS total_loans,
    COUNT(DISTINCT cd.card_id) AS total_cards
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id AND a.status = 'ACTIVE'
LEFT JOIN loans l ON c.customer_id = l.customer_id AND l.status IN ('ACTIVE', 'PENDING')
LEFT JOIN cards cd ON a.account_id = cd.account_id AND cd.status = 'ACTIVE'
WHERE c.is_active = TRUE
GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.phone;

-- =============================================
-- Common Queries
-- =============================================

-- Query 1: Get all accounts with balance below minimum
COMMENT ON VIEW account_details IS 'Use this query to find accounts below minimum balance:
SELECT * FROM account_details WHERE balance < minimum_balance;';

-- Query 2: Get top 10 customers by total balance
COMMENT ON VIEW customer_account_summary IS 'Use this query to find top customers:
SELECT * FROM customer_account_summary ORDER BY total_balance DESC LIMIT 10;';

-- Query 3: Get all transactions for a specific account in date range
-- SELECT * FROM recent_transactions 
-- WHERE account_number = 'ACC1001000001' 
-- AND transaction_date BETWEEN '2024-01-01' AND '2024-12-31';

-- Query 4: Get all overdue loan payments
-- SELECT l.loan_number, c.first_name || ' ' || c.last_name AS customer_name,
--        lp.due_date, lp.payment_amount, lp.status
-- FROM loan_payments lp
-- JOIN loans l ON lp.loan_id = l.loan_id
-- JOIN customers c ON l.customer_id = c.customer_id
-- WHERE lp.status = 'PENDING' AND lp.due_date < CURRENT_DATE;

-- Query 5: Get monthly account activity
-- SELECT * FROM monthly_transaction_summary 
-- WHERE month = DATE_TRUNC('month', CURRENT_DATE);

-- Query 6: Get all inactive customers with accounts
-- SELECT c.customer_id, c.first_name || ' ' || c.last_name AS customer_name,
--        c.email, COUNT(a.account_id) AS account_count, SUM(a.balance) AS total_balance
-- FROM customers c
-- JOIN accounts a ON c.customer_id = a.customer_id
-- WHERE c.is_active = FALSE
-- GROUP BY c.customer_id, c.first_name, c.last_name, c.email;

-- Query 7: Get cards expiring in next 3 months
-- SELECT * FROM card_details 
-- WHERE expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '3 months'
-- AND card_status = 'ACTIVE';

-- Query 8: Get customer transaction history
-- SELECT t.transaction_date, t.transaction_number, tt.type_name, 
--        t.amount, t.balance_after, t.description
-- FROM transactions t
-- JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
-- JOIN accounts a ON t.account_id = a.account_id
-- WHERE a.customer_id = 1
-- ORDER BY t.transaction_date DESC;

-- Query 9: Get account balance history
-- SELECT transaction_date, transaction_number, amount, balance_after
-- FROM transactions
-- WHERE account_id = 1
-- ORDER BY transaction_date;

-- Query 10: Get total deposits and withdrawals by customer
-- SELECT c.customer_id, c.first_name || ' ' || c.last_name AS customer_name,
--        SUM(CASE WHEN tt.type_name = 'DEPOSIT' THEN t.amount ELSE 0 END) AS total_deposits,
--        SUM(CASE WHEN tt.type_name = 'WITHDRAWAL' THEN t.amount ELSE 0 END) AS total_withdrawals
-- FROM customers c
-- JOIN accounts a ON c.customer_id = a.customer_id
-- JOIN transactions t ON a.account_id = t.account_id
-- JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
-- GROUP BY c.customer_id, c.first_name, c.last_name;
