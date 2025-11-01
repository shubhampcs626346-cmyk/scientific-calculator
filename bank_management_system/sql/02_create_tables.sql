-- =============================================
-- Bank Account Management System
-- Table Creation Script
-- =============================================

\c bank_management;
SET search_path TO banking, public;

-- =============================================
-- Table: customers
-- Description: Stores customer information
-- =============================================
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE NOT NULL,
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    country VARCHAR(50) DEFAULT 'USA',
    ssn VARCHAR(11) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT chk_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_age CHECK (date_of_birth <= CURRENT_DATE - INTERVAL '18 years')
);

-- =============================================
-- Table: account_types
-- Description: Defines different types of accounts
-- =============================================
CREATE TABLE account_types (
    account_type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    minimum_balance DECIMAL(15, 2) DEFAULT 0.00,
    interest_rate DECIMAL(5, 2) DEFAULT 0.00,
    monthly_fee DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- Table: accounts
-- Description: Stores account information
-- =============================================
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL,
    account_type_id INTEGER NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00 CHECK (balance >= 0),
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE', 'FROZEN', 'CLOSED')),
    opened_date DATE DEFAULT CURRENT_DATE,
    closed_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    FOREIGN KEY (account_type_id) REFERENCES account_types(account_type_id) ON DELETE RESTRICT,
    CONSTRAINT chk_closed_date CHECK (closed_date IS NULL OR closed_date >= opened_date)
);

-- =============================================
-- Table: transaction_types
-- Description: Defines different types of transactions
-- =============================================
CREATE TABLE transaction_types (
    transaction_type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- Table: transactions
-- Description: Stores all account transactions
-- =============================================
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    transaction_number VARCHAR(30) UNIQUE NOT NULL,
    account_id INTEGER NOT NULL,
    transaction_type_id INTEGER NOT NULL,
    amount DECIMAL(15, 2) NOT NULL CHECK (amount > 0),
    balance_after DECIMAL(15, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    reference_number VARCHAR(50),
    status VARCHAR(20) DEFAULT 'COMPLETED' CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED', 'REVERSED')),
    created_by VARCHAR(50),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE RESTRICT,
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_types(transaction_type_id) ON DELETE RESTRICT
);

-- =============================================
-- Table: transfers
-- Description: Stores transfer transactions between accounts
-- =============================================
CREATE TABLE transfers (
    transfer_id SERIAL PRIMARY KEY,
    transfer_number VARCHAR(30) UNIQUE NOT NULL,
    from_account_id INTEGER NOT NULL,
    to_account_id INTEGER NOT NULL,
    amount DECIMAL(15, 2) NOT NULL CHECK (amount > 0),
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    status VARCHAR(20) DEFAULT 'COMPLETED' CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED', 'REVERSED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_account_id) REFERENCES accounts(account_id) ON DELETE RESTRICT,
    FOREIGN KEY (to_account_id) REFERENCES accounts(account_id) ON DELETE RESTRICT,
    CONSTRAINT chk_different_accounts CHECK (from_account_id != to_account_id)
);

-- =============================================
-- Table: loans
-- Description: Stores loan information
-- =============================================
CREATE TABLE loans (
    loan_id SERIAL PRIMARY KEY,
    loan_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL,
    loan_type VARCHAR(50) NOT NULL CHECK (loan_type IN ('PERSONAL', 'HOME', 'AUTO', 'BUSINESS', 'EDUCATION')),
    principal_amount DECIMAL(15, 2) NOT NULL CHECK (principal_amount > 0),
    interest_rate DECIMAL(5, 2) NOT NULL CHECK (interest_rate >= 0),
    term_months INTEGER NOT NULL CHECK (term_months > 0),
    monthly_payment DECIMAL(15, 2) NOT NULL,
    outstanding_balance DECIMAL(15, 2) NOT NULL,
    start_date DATE DEFAULT CURRENT_DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'ACTIVE' CHECK (status IN ('PENDING', 'ACTIVE', 'PAID', 'DEFAULTED', 'CLOSED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT
);

-- =============================================
-- Table: loan_payments
-- Description: Stores loan payment history
-- =============================================
CREATE TABLE loan_payments (
    payment_id SERIAL PRIMARY KEY,
    loan_id INTEGER NOT NULL,
    payment_number VARCHAR(30) UNIQUE NOT NULL,
    payment_amount DECIMAL(15, 2) NOT NULL CHECK (payment_amount > 0),
    principal_paid DECIMAL(15, 2) NOT NULL,
    interest_paid DECIMAL(15, 2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'PAID' CHECK (status IN ('PENDING', 'PAID', 'LATE', 'MISSED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id) ON DELETE RESTRICT
);

-- =============================================
-- Table: cards
-- Description: Stores debit/credit card information
-- =============================================
CREATE TABLE cards (
    card_id SERIAL PRIMARY KEY,
    card_number VARCHAR(16) UNIQUE NOT NULL,
    account_id INTEGER NOT NULL,
    card_type VARCHAR(20) NOT NULL CHECK (card_type IN ('DEBIT', 'CREDIT')),
    card_holder_name VARCHAR(100) NOT NULL,
    expiry_date DATE NOT NULL,
    cvv VARCHAR(3) NOT NULL,
    credit_limit DECIMAL(15, 2),
    status VARCHAR(20) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'BLOCKED', 'EXPIRED', 'CANCELLED')),
    issued_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE RESTRICT,
    CONSTRAINT chk_expiry CHECK (expiry_date > issued_date)
);

-- =============================================
-- Table: audit_log
-- Description: Stores audit trail for all operations
-- =============================================
CREATE TABLE audit_log (
    audit_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL CHECK (operation IN ('INSERT', 'UPDATE', 'DELETE')),
    record_id INTEGER NOT NULL,
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(50),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_ssn ON customers(ssn);
CREATE INDEX idx_accounts_customer ON accounts(customer_id);
CREATE INDEX idx_accounts_number ON accounts(account_number);
CREATE INDEX idx_accounts_status ON accounts(status);
CREATE INDEX idx_transactions_account ON transactions(account_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_type ON transactions(transaction_type_id);
CREATE INDEX idx_transfers_from ON transfers(from_account_id);
CREATE INDEX idx_transfers_to ON transfers(to_account_id);
CREATE INDEX idx_transfers_date ON transfers(transfer_date);
CREATE INDEX idx_loans_customer ON loans(customer_id);
CREATE INDEX idx_loans_status ON loans(status);
CREATE INDEX idx_loan_payments_loan ON loan_payments(loan_id);
CREATE INDEX idx_cards_account ON cards(account_id);
CREATE INDEX idx_audit_table ON audit_log(table_name, record_id);

-- Add comments to tables
COMMENT ON TABLE customers IS 'Stores customer personal information';
COMMENT ON TABLE account_types IS 'Defines different types of bank accounts';
COMMENT ON TABLE accounts IS 'Stores bank account information';
COMMENT ON TABLE transaction_types IS 'Defines different types of transactions';
COMMENT ON TABLE transactions IS 'Records all account transactions';
COMMENT ON TABLE transfers IS 'Records money transfers between accounts';
COMMENT ON TABLE loans IS 'Stores loan information';
COMMENT ON TABLE loan_payments IS 'Records loan payment history';
COMMENT ON TABLE cards IS 'Stores debit and credit card information';
COMMENT ON TABLE audit_log IS 'Audit trail for all database operations';
