-- =============================================
-- Bank Account Management System
-- Functions and Stored Procedures
-- =============================================

\c bank_management;
SET search_path TO banking, public;

-- =============================================
-- Function: generate_account_number
-- Description: Generates unique account number
-- =============================================
CREATE OR REPLACE FUNCTION generate_account_number(p_customer_id INTEGER)
RETURNS VARCHAR(20) AS $$
DECLARE
    v_account_number VARCHAR(20);
    v_count INTEGER;
BEGIN
    v_count := (SELECT COUNT(*) FROM accounts WHERE customer_id = p_customer_id);
    v_account_number := 'ACC' || LPAD(p_customer_id::TEXT, 4, '0') || LPAD((v_count + 1)::TEXT, 6, '0');
    RETURN v_account_number;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- Function: generate_transaction_number
-- Description: Generates unique transaction number
-- =============================================
CREATE OR REPLACE FUNCTION generate_transaction_number()
RETURNS VARCHAR(30) AS $$
DECLARE
    v_transaction_number VARCHAR(30);
BEGIN
    v_transaction_number := 'TXN' || TO_CHAR(CURRENT_DATE, 'YYYYMMDD') || 
                           LPAD(nextval('transactions_transaction_id_seq')::TEXT, 6, '0');
    RETURN v_transaction_number;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- Function: calculate_account_balance
-- Description: Calculates current account balance
-- =============================================
CREATE OR REPLACE FUNCTION calculate_account_balance(p_account_id INTEGER)
RETURNS DECIMAL(15, 2) AS $$
DECLARE
    v_balance DECIMAL(15, 2);
BEGIN
    SELECT balance INTO v_balance
    FROM accounts
    WHERE account_id = p_account_id;
    
    RETURN COALESCE(v_balance, 0);
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- Procedure: create_customer_account
-- Description: Creates a new customer and account
-- =============================================
CREATE OR REPLACE FUNCTION create_customer_account(
    p_first_name VARCHAR(50),
    p_last_name VARCHAR(50),
    p_email VARCHAR(100),
    p_phone VARCHAR(20),
    p_date_of_birth DATE,
    p_address TEXT,
    p_city VARCHAR(50),
    p_state VARCHAR(50),
    p_zip_code VARCHAR(10),
    p_ssn VARCHAR(11),
    p_account_type_id INTEGER,
    p_initial_deposit DECIMAL(15, 2)
)
RETURNS TABLE(customer_id INTEGER, account_id INTEGER, account_number VARCHAR(20)) AS $$
DECLARE
    v_customer_id INTEGER;
    v_account_id INTEGER;
    v_account_number VARCHAR(20);
BEGIN
    -- Insert customer
    INSERT INTO customers (first_name, last_name, email, phone, date_of_birth, address, city, state, zip_code, ssn)
    VALUES (p_first_name, p_last_name, p_email, p_phone, p_date_of_birth, p_address, p_city, p_state, p_zip_code, p_ssn)
    RETURNING customers.customer_id INTO v_customer_id;
    
    -- Generate account number
    v_account_number := generate_account_number(v_customer_id);
    
    -- Insert account
    INSERT INTO accounts (account_number, customer_id, account_type_id, balance)
    VALUES (v_account_number, v_customer_id, p_account_type_id, p_initial_deposit)
    RETURNING accounts.account_id INTO v_account_id;
    
    -- Record initial deposit transaction
    IF p_initial_deposit > 0 THEN
        INSERT INTO transactions (transaction_number, account_id, transaction_type_id, amount, balance_after, description)
        VALUES (generate_transaction_number(), v_account_id, 1, p_initial_deposit, p_initial_deposit, 'Initial deposit');
    END IF;
    
    RETURN QUERY SELECT v_customer_id, v_account_id, v_account_number;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- Procedure: deposit_money
-- Description: Deposits money into an account
-- =============================================
CREATE OR REPLACE FUNCTION deposit_money(
    p_account_id INTEGER,
    p_amount DECIMAL(15, 2),
    p_description TEXT DEFAULT 'Deposit'
)
RETURNS TABLE(transaction_id INTEGER, new_balance DECIMAL(15, 2)) AS $$
DECLARE
    v_transaction_id INTEGER;
    v_current_balance DECIMAL(15, 2);
    v_new_balance DECIMAL(15, 2);
    v_account_status VARCHAR(20);
BEGIN
    -- Check account status
    SELECT status, balance INTO v_account_status, v_current_balance
    FROM accounts
    WHERE account_id = p_account_id;
    
    IF v_account_status IS NULL THEN
        RAISE EXCEPTION 'Account not found';
    END IF;
    
    IF v_account_status != 'ACTIVE' THEN
        RAISE EXCEPTION 'Account is not active';
    END IF;
    
    -- Calculate new balance
    v_new_balance := v_current_balance + p_amount;
    
    -- Update account balance
    UPDATE accounts
    SET balance = v_new_balance, updated_at = CURRENT_TIMESTAMP
    WHERE account_id = p_account_id;
    
    -- Record transaction
    INSERT INTO transactions (transaction_number, account_id, transaction_type_id, amount, balance_after, description)
    VALUES (generate_transaction_number(), p_account_id, 1, p_amount, v_new_balance, p_description)
    RETURNING transactions.transaction_id INTO v_transaction_id;
    
    RETURN QUERY SELECT v_transaction_id, v_new_balance;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- Procedure: withdraw_money
-- Description: Withdraws money from an account
-- =============================================
CREATE OR REPLACE FUNCTION withdraw_money(
    p_account_id INTEGER,
    p_amount DECIMAL(15, 2),
    p_description TEXT DEFAULT 'Withdrawal'
)
RETURNS TABLE(transaction_id INTEGER, new_balance DECIMAL(15, 2)) AS $$
DECLARE
    v_transaction_id INTEGER;
    v_current_balance DECIMAL(15, 2);
    v_new_balance DECIMAL(15, 2);
    v_account_status VARCHAR(20);
    v_min_balance DECIMAL(15, 2);
BEGIN
    -- Check account status and get minimum balance
    SELECT a.status, a.balance, at.minimum_balance 
    INTO v_account_status, v_current_balance, v_min_balance
    FROM accounts a
    JOIN account_types at ON a.account_type_id = at.account_type_id
    WHERE a.account_id = p_account_id;
    
    IF v_account_status IS NULL THEN
        RAISE EXCEPTION 'Account not found';
    END IF;
    
    IF v_account_status != 'ACTIVE' THEN
        RAISE EXCEPTION 'Account is not active';
    END IF;
    
    -- Calculate new balance
    v_new_balance := v_current_balance - p_amount;
    
    -- Check if sufficient balance
    IF v_new_balance < v_min_balance THEN
        RAISE EXCEPTION 'Insufficient balance. Minimum balance required: %', v_min_balance;
    END IF;
    
    -- Update account balance
    UPDATE accounts
    SET balance = v_new_balance, updated_at = CURRENT_TIMESTAMP
    WHERE account_id = p_account_id;
    
    -- Record transaction
    INSERT INTO transactions (transaction_number, account_id, transaction_type_id, amount, balance_after, description)
    VALUES (generate_transaction_number(), p_account_id, 2, p_amount, v_new_balance, p_description)
    RETURNING transactions.transaction_id INTO v_transaction_id;
    
    RETURN QUERY SELECT v_transaction_id, v_new_balance;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- Procedure: transfer_money
-- Description: Transfers money between accounts
-- =============================================
CREATE OR REPLACE FUNCTION transfer_money(
    p_from_account_id INTEGER,
    p_to_account_id INTEGER,
    p_amount DECIMAL(15, 2),
    p_description TEXT DEFAULT 'Transfer'
)
RETURNS TABLE(transfer_id INTEGER, from_balance DECIMAL(15, 2), to_balance DECIMAL(15, 2)) AS $$
DECLARE
    v_transfer_id INTEGER;
    v_transfer_number VARCHAR(30);
    v_from_balance DECIMAL(15, 2);
    v_to_balance DECIMAL(15, 2);
BEGIN
    -- Validate accounts are different
    IF p_from_account_id = p_to_account_id THEN
        RAISE EXCEPTION 'Cannot transfer to the same account';
    END IF;
    
    -- Withdraw from source account
    SELECT new_balance INTO v_from_balance
    FROM withdraw_money(p_from_account_id, p_amount, 'Transfer out: ' || p_description);
    
    -- Deposit to destination account
    SELECT new_balance INTO v_to_balance
    FROM deposit_money(p_to_account_id, p_amount, 'Transfer in: ' || p_description);
    
    -- Record transfer
    v_transfer_number := 'TRF' || TO_CHAR(CURRENT_DATE, 'YYYYMMDD') || 
                        LPAD(nextval('transfers_transfer_id_seq')::TEXT, 6, '0');
    
    INSERT INTO transfers (transfer_number, from_account_id, to_account_id, amount, description)
    VALUES (v_transfer_number, p_from_account_id, p_to_account_id, p_amount, p_description)
    RETURNING transfers.transfer_id INTO v_transfer_id;
    
    RETURN QUERY SELECT v_transfer_id, v_from_balance, v_to_balance;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- Function: get_customer_total_balance
-- Description: Gets total balance across all accounts
-- =============================================
CREATE OR REPLACE FUNCTION get_customer_total_balance(p_customer_id INTEGER)
RETURNS DECIMAL(15, 2) AS $$
DECLARE
    v_total_balance DECIMAL(15, 2);
BEGIN
    SELECT COALESCE(SUM(balance), 0) INTO v_total_balance
    FROM accounts
    WHERE customer_id = p_customer_id AND status = 'ACTIVE';
    
    RETURN v_total_balance;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- Function: calculate_loan_payment
-- Description: Calculates monthly loan payment
-- =============================================
CREATE OR REPLACE FUNCTION calculate_loan_payment(
    p_principal DECIMAL(15, 2),
    p_annual_rate DECIMAL(5, 2),
    p_term_months INTEGER
)
RETURNS DECIMAL(15, 2) AS $$
DECLARE
    v_monthly_rate DECIMAL(10, 8);
    v_payment DECIMAL(15, 2);
BEGIN
    IF p_annual_rate = 0 THEN
        RETURN p_principal / p_term_months;
    END IF;
    
    v_monthly_rate := p_annual_rate / 100 / 12;
    v_payment := p_principal * (v_monthly_rate * POWER(1 + v_monthly_rate, p_term_months)) / 
                 (POWER(1 + v_monthly_rate, p_term_months) - 1);
    
    RETURN ROUND(v_payment, 2);
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- Procedure: apply_monthly_interest
-- Description: Applies monthly interest to savings accounts
-- =============================================
CREATE OR REPLACE FUNCTION apply_monthly_interest()
RETURNS TABLE(accounts_updated INTEGER, total_interest DECIMAL(15, 2)) AS $$
DECLARE
    v_account RECORD;
    v_interest DECIMAL(15, 2);
    v_count INTEGER := 0;
    v_total DECIMAL(15, 2) := 0;
BEGIN
    FOR v_account IN 
        SELECT a.account_id, a.balance, at.interest_rate
        FROM accounts a
        JOIN account_types at ON a.account_type_id = at.account_type_id
        WHERE a.status = 'ACTIVE' AND at.interest_rate > 0
    LOOP
        -- Calculate monthly interest
        v_interest := v_account.balance * (v_account.interest_rate / 100 / 12);
        
        -- Apply interest
        PERFORM deposit_money(v_account.account_id, v_interest, 'Monthly interest');
        
        v_count := v_count + 1;
        v_total := v_total + v_interest;
    END LOOP;
    
    RETURN QUERY SELECT v_count, v_total;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- Trigger Function: update_timestamp
-- Description: Updates the updated_at timestamp
-- =============================================
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers
CREATE TRIGGER trg_customers_update
    BEFORE UPDATE ON customers
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_accounts_update
    BEFORE UPDATE ON accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_loans_update
    BEFORE UPDATE ON loans
    FOR EACH ROW
    EXECUTE FUNCTION update_timestamp();

-- =============================================
-- Trigger Function: audit_log_trigger
-- Description: Logs all changes to audit_log table
-- =============================================
CREATE OR REPLACE FUNCTION audit_log_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, record_id, new_values, changed_by)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.customer_id, row_to_json(NEW), current_user);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, record_id, old_values, new_values, changed_by)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.customer_id, row_to_json(OLD), row_to_json(NEW), current_user);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, operation, record_id, old_values, changed_by)
        VALUES (TG_TABLE_NAME, TG_OP, OLD.customer_id, row_to_json(OLD), current_user);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Create audit triggers for important tables
CREATE TRIGGER trg_customers_audit
    AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW
    EXECUTE FUNCTION audit_log_trigger();

CREATE TRIGGER trg_accounts_audit
    AFTER INSERT OR UPDATE OR DELETE ON accounts
    FOR EACH ROW
    EXECUTE FUNCTION audit_log_trigger();
