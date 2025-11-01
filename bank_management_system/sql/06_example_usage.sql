-- =============================================
-- Bank Account Management System
-- Example Usage and Test Queries
-- =============================================

\c bank_management;
SET search_path TO banking, public;

-- =============================================
-- Example 1: Create a new customer with account
-- =============================================
SELECT * FROM create_customer_account(
    'Alice',                    -- first_name
    'Cooper',                   -- last_name
    'alice.cooper@email.com',   -- email
    '555-0201',                 -- phone
    '1994-06-15',              -- date_of_birth
    '999 Rock Ave',            -- address
    'Seattle',                 -- city
    'WA',                      -- state
    '98101',                   -- zip_code
    '111-22-3333',             -- ssn
    1,                         -- account_type_id (SAVINGS)
    5000.00                    -- initial_deposit
);

-- =============================================
-- Example 2: Deposit money into an account
-- =============================================
SELECT * FROM deposit_money(
    1,                         -- account_id
    1000.00,                   -- amount
    'Salary deposit'           -- description
);

-- =============================================
-- Example 3: Withdraw money from an account
-- =============================================
SELECT * FROM withdraw_money(
    1,                         -- account_id
    500.00,                    -- amount
    'ATM withdrawal'           -- description
);

-- =============================================
-- Example 4: Transfer money between accounts
-- =============================================
SELECT * FROM transfer_money(
    1,                         -- from_account_id
    2,                         -- to_account_id
    250.00,                    -- amount
    'Monthly transfer'         -- description
);

-- =============================================
-- Example 5: Get customer total balance
-- =============================================
SELECT get_customer_total_balance(1) AS total_balance;

-- =============================================
-- Example 6: Calculate loan payment
-- =============================================
SELECT calculate_loan_payment(
    50000.00,                  -- principal
    5.5,                       -- annual_rate
    60                         -- term_months
) AS monthly_payment;

-- =============================================
-- Example 7: Apply monthly interest to all accounts
-- =============================================
SELECT * FROM apply_monthly_interest();

-- =============================================
-- Example 8: View customer account summary
-- =============================================
SELECT * FROM customer_account_summary
ORDER BY total_balance DESC;

-- =============================================
-- Example 9: View recent transactions
-- =============================================
SELECT * FROM recent_transactions
LIMIT 20;

-- =============================================
-- Example 10: View account details
-- =============================================
SELECT * FROM account_details
WHERE customer_name LIKE '%Smith%';

-- =============================================
-- Example 11: View transfer history
-- =============================================
SELECT * FROM transfer_history
WHERE transfer_date >= CURRENT_DATE - INTERVAL '30 days';

-- =============================================
-- Example 12: View loan summary
-- =============================================
SELECT * FROM loan_summary
WHERE status = 'ACTIVE';

-- =============================================
-- Example 13: View customer financial overview
-- =============================================
SELECT * FROM customer_financial_overview
ORDER BY net_worth DESC;

-- =============================================
-- Example 14: Find accounts below minimum balance
-- =============================================
SELECT 
    account_number,
    customer_name,
    account_type,
    balance,
    minimum_balance,
    minimum_balance - balance AS shortfall
FROM account_details
WHERE balance < minimum_balance;

-- =============================================
-- Example 15: Get transaction history for specific account
-- =============================================
SELECT 
    transaction_date,
    transaction_number,
    transaction_type,
    amount,
    balance_after,
    description,
    status
FROM recent_transactions
WHERE account_number = 'ACC1001000001'
ORDER BY transaction_date DESC;

-- =============================================
-- Example 16: Get monthly transaction summary
-- =============================================
SELECT 
    month,
    customer_name,
    transaction_count,
    total_credits,
    total_debits,
    net_change
FROM monthly_transaction_summary
WHERE month >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '6 months')
ORDER BY month DESC, customer_name;

-- =============================================
-- Example 17: Find customers with multiple accounts
-- =============================================
SELECT 
    customer_name,
    email,
    total_accounts,
    total_balance,
    account_types
FROM customer_account_summary
WHERE total_accounts > 1
ORDER BY total_accounts DESC;

-- =============================================
-- Example 18: Get cards expiring soon
-- =============================================
SELECT 
    card_number,
    card_type,
    card_holder_name,
    expiry_date,
    expiry_status,
    account_number
FROM card_details
WHERE expiry_status IN ('Expiring Soon', 'Expired')
ORDER BY expiry_date;

-- =============================================
-- Example 19: Get loan payment history
-- =============================================
SELECT 
    l.loan_number,
    c.first_name || ' ' || c.last_name AS customer_name,
    lp.payment_date,
    lp.payment_amount,
    lp.principal_paid,
    lp.interest_paid,
    lp.status
FROM loan_payments lp
JOIN loans l ON lp.loan_id = l.loan_id
JOIN customers c ON l.customer_id = c.customer_id
WHERE l.loan_number = 'LOAN1001001'
ORDER BY lp.payment_date DESC;

-- =============================================
-- Example 20: Get audit log for specific customer
-- =============================================
SELECT 
    audit_id,
    table_name,
    operation,
    changed_at,
    changed_by,
    new_values->>'first_name' AS first_name,
    new_values->>'last_name' AS last_name,
    new_values->>'email' AS email
FROM audit_log
WHERE table_name = 'customers' 
  AND record_id = 1
ORDER BY changed_at DESC;

-- =============================================
-- Example 21: Get total transactions by type
-- =============================================
SELECT 
    tt.type_name,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount) AS total_amount,
    AVG(t.amount) AS average_amount,
    MIN(t.amount) AS min_amount,
    MAX(t.amount) AS max_amount
FROM transactions t
JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
WHERE t.status = 'COMPLETED'
GROUP BY tt.type_name
ORDER BY total_amount DESC;

-- =============================================
-- Example 22: Get customer activity report
-- =============================================
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(DISTINCT a.account_id) AS accounts,
    COUNT(DISTINCT t.transaction_id) AS transactions,
    COUNT(DISTINCT tr.transfer_id) AS transfers,
    COUNT(DISTINCT l.loan_id) AS loans,
    MAX(t.transaction_date) AS last_transaction_date
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN transactions t ON a.account_id = t.account_id
LEFT JOIN transfers tr ON a.account_id IN (tr.from_account_id, tr.to_account_id)
LEFT JOIN loans l ON c.customer_id = l.customer_id
WHERE c.is_active = TRUE
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY transactions DESC;

-- =============================================
-- Example 23: Get account balance trends
-- =============================================
SELECT 
    a.account_number,
    c.first_name || ' ' || c.last_name AS customer_name,
    DATE_TRUNC('day', t.transaction_date) AS date,
    MIN(t.balance_after) AS min_balance,
    MAX(t.balance_after) AS max_balance,
    (SELECT balance_after FROM transactions 
     WHERE account_id = a.account_id 
     AND DATE_TRUNC('day', transaction_date) = DATE_TRUNC('day', t.transaction_date)
     ORDER BY transaction_date DESC LIMIT 1) AS closing_balance
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id
JOIN transactions t ON a.account_id = t.account_id
WHERE a.account_number = 'ACC1001000001'
GROUP BY a.account_number, c.first_name, c.last_name, DATE_TRUNC('day', t.transaction_date), a.account_id
ORDER BY date DESC
LIMIT 30;

-- =============================================
-- Example 24: Get high-value transactions
-- =============================================
SELECT 
    t.transaction_number,
    a.account_number,
    c.first_name || ' ' || c.last_name AS customer_name,
    tt.type_name,
    t.amount,
    t.transaction_date,
    t.description
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
WHERE t.amount > 10000 AND t.status = 'COMPLETED'
ORDER BY t.amount DESC;

-- =============================================
-- Example 25: Get customer retention metrics
-- =============================================
SELECT 
    DATE_TRUNC('month', created_at) AS signup_month,
    COUNT(*) AS new_customers,
    SUM(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at)) AS cumulative_customers
FROM customers
WHERE is_active = TRUE
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY signup_month DESC;
