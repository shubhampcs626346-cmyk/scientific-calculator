-- =============================================
-- Bank Account Management System
-- Sample Data Insertion Script
-- =============================================

\c bank_management;
SET search_path TO banking, public;

-- =============================================
-- Insert Account Types
-- =============================================
INSERT INTO account_types (type_name, description, minimum_balance, interest_rate, monthly_fee) VALUES
('SAVINGS', 'Standard savings account with interest', 500.00, 2.50, 0.00),
('CHECKING', 'Standard checking account for daily transactions', 100.00, 0.10, 5.00),
('PREMIUM_SAVINGS', 'High-yield savings account', 5000.00, 4.00, 0.00),
('BUSINESS', 'Business checking account', 1000.00, 0.50, 15.00),
('STUDENT', 'Student checking account with no fees', 0.00, 0.25, 0.00);

-- =============================================
-- Insert Transaction Types
-- =============================================
INSERT INTO transaction_types (type_name, description) VALUES
('DEPOSIT', 'Money deposited into account'),
('WITHDRAWAL', 'Money withdrawn from account'),
('TRANSFER_IN', 'Money transferred into account'),
('TRANSFER_OUT', 'Money transferred out of account'),
('FEE', 'Bank fee charged'),
('INTEREST', 'Interest credited to account'),
('ATM_WITHDRAWAL', 'Cash withdrawn from ATM'),
('CHECK_DEPOSIT', 'Check deposited into account'),
('ONLINE_PAYMENT', 'Online payment made'),
('REFUND', 'Refund credited to account');

-- =============================================
-- Insert Sample Customers
-- =============================================
INSERT INTO customers (first_name, last_name, email, phone, date_of_birth, address, city, state, zip_code, ssn) VALUES
('John', 'Smith', 'john.smith@email.com', '555-0101', '1985-03-15', '123 Main St', 'New York', 'NY', '10001', '123-45-6789'),
('Sarah', 'Johnson', 'sarah.johnson@email.com', '555-0102', '1990-07-22', '456 Oak Ave', 'Los Angeles', 'CA', '90001', '234-56-7890'),
('Michael', 'Williams', 'michael.williams@email.com', '555-0103', '1982-11-08', '789 Pine Rd', 'Chicago', 'IL', '60601', '345-67-8901'),
('Emily', 'Brown', 'emily.brown@email.com', '555-0104', '1995-01-30', '321 Elm St', 'Houston', 'TX', '77001', '456-78-9012'),
('David', 'Jones', 'david.jones@email.com', '555-0105', '1988-05-17', '654 Maple Dr', 'Phoenix', 'AZ', '85001', '567-89-0123'),
('Jessica', 'Garcia', 'jessica.garcia@email.com', '555-0106', '1992-09-25', '987 Cedar Ln', 'Philadelphia', 'PA', '19101', '678-90-1234'),
('Robert', 'Martinez', 'robert.martinez@email.com', '555-0107', '1980-12-03', '147 Birch Ct', 'San Antonio', 'TX', '78201', '789-01-2345'),
('Amanda', 'Rodriguez', 'amanda.rodriguez@email.com', '555-0108', '1993-04-19', '258 Spruce Way', 'San Diego', 'CA', '92101', '890-12-3456'),
('James', 'Wilson', 'james.wilson@email.com', '555-0109', '1987-08-11', '369 Willow Pl', 'Dallas', 'TX', '75201', '901-23-4567'),
('Lisa', 'Anderson', 'lisa.anderson@email.com', '555-0110', '1991-02-28', '741 Ash Blvd', 'San Jose', 'CA', '95101', '012-34-5678');

-- =============================================
-- Insert Sample Accounts
-- =============================================
INSERT INTO accounts (account_number, customer_id, account_type_id, balance, status) VALUES
('ACC1001000001', 1, 1, 15000.00, 'ACTIVE'),
('ACC1001000002', 1, 2, 3500.50, 'ACTIVE'),
('ACC1002000001', 2, 1, 25000.75, 'ACTIVE'),
('ACC1002000002', 2, 3, 50000.00, 'ACTIVE'),
('ACC1003000001', 3, 2, 8750.25, 'ACTIVE'),
('ACC1003000002', 3, 4, 125000.00, 'ACTIVE'),
('ACC1004000001', 4, 5, 2500.00, 'ACTIVE'),
('ACC1005000001', 5, 1, 18500.00, 'ACTIVE'),
('ACC1005000002', 5, 2, 4200.00, 'ACTIVE'),
('ACC1006000001', 6, 1, 32000.00, 'ACTIVE'),
('ACC1007000001', 7, 2, 6800.00, 'ACTIVE'),
('ACC1007000002', 7, 3, 75000.00, 'ACTIVE'),
('ACC1008000001', 8, 5, 1800.00, 'ACTIVE'),
('ACC1009000001', 9, 1, 22000.00, 'ACTIVE'),
('ACC1010000001', 10, 2, 5500.00, 'ACTIVE');

-- =============================================
-- Insert Sample Transactions
-- =============================================
INSERT INTO transactions (transaction_number, account_id, transaction_type_id, amount, balance_after, description, status) VALUES
('TXN20240101001', 1, 1, 5000.00, 15000.00, 'Initial deposit', 'COMPLETED'),
('TXN20240102001', 1, 1, 10000.00, 15000.00, 'Salary deposit', 'COMPLETED'),
('TXN20240103001', 2, 1, 3500.50, 3500.50, 'Initial deposit', 'COMPLETED'),
('TXN20240104001', 3, 1, 25000.75, 25000.75, 'Initial deposit', 'COMPLETED'),
('TXN20240105001', 4, 1, 50000.00, 50000.00, 'Investment transfer', 'COMPLETED'),
('TXN20240106001', 5, 1, 10000.00, 10000.00, 'Initial deposit', 'COMPLETED'),
('TXN20240107001', 5, 2, 1249.75, 8750.25, 'ATM withdrawal', 'COMPLETED'),
('TXN20240108001', 6, 1, 125000.00, 125000.00, 'Business capital', 'COMPLETED'),
('TXN20240109001', 7, 1, 2500.00, 2500.00, 'Student account opening', 'COMPLETED'),
('TXN20240110001', 8, 1, 18500.00, 18500.00, 'Salary deposit', 'COMPLETED');

-- =============================================
-- Insert Sample Transfers
-- =============================================
INSERT INTO transfers (transfer_number, from_account_id, to_account_id, amount, description, status) VALUES
('TRF20240201001', 1, 2, 500.00, 'Transfer to checking', 'COMPLETED'),
('TRF20240202001', 3, 4, 1000.00, 'Investment transfer', 'COMPLETED'),
('TRF20240203001', 8, 9, 300.00, 'Emergency fund transfer', 'COMPLETED');

-- =============================================
-- Insert Sample Loans
-- =============================================
INSERT INTO loans (loan_number, customer_id, loan_type, principal_amount, interest_rate, term_months, monthly_payment, outstanding_balance, status) VALUES
('LOAN1001001', 1, 'AUTO', 25000.00, 5.50, 60, 475.00, 25000.00, 'ACTIVE'),
('LOAN1002001', 2, 'HOME', 250000.00, 3.75, 360, 1157.79, 250000.00, 'ACTIVE'),
('LOAN1003001', 3, 'BUSINESS', 100000.00, 6.00, 120, 1110.21, 100000.00, 'ACTIVE'),
('LOAN1004001', 4, 'EDUCATION', 35000.00, 4.50, 120, 363.00, 35000.00, 'ACTIVE'),
('LOAN1005001', 5, 'PERSONAL', 15000.00, 7.00, 36, 463.16, 15000.00, 'ACTIVE');

-- =============================================
-- Insert Sample Loan Payments
-- =============================================
INSERT INTO loan_payments (loan_id, payment_number, payment_amount, principal_paid, interest_paid, due_date, status) VALUES
(1, 'PAY1001001001', 475.00, 360.42, 114.58, '2024-02-01', 'PAID'),
(1, 'PAY1001001002', 475.00, 362.07, 112.93, '2024-03-01', 'PAID'),
(2, 'PAY1002001001', 1157.79, 376.04, 781.75, '2024-02-01', 'PAID'),
(3, 'PAY1003001001', 1110.21, 610.21, 500.00, '2024-02-01', 'PAID'),
(4, 'PAY1004001001', 363.00, 231.75, 131.25, '2024-02-01', 'PAID'),
(5, 'PAY1005001001', 463.16, 375.66, 87.50, '2024-02-01', 'PAID');

-- =============================================
-- Insert Sample Cards
-- =============================================
INSERT INTO cards (card_number, account_id, card_type, card_holder_name, expiry_date, cvv, credit_limit, status) VALUES
('4532123456789012', 2, 'DEBIT', 'JOHN SMITH', '2027-12-31', '123', NULL, 'ACTIVE'),
('5412345678901234', 3, 'DEBIT', 'SARAH JOHNSON', '2028-06-30', '456', NULL, 'ACTIVE'),
('4916123456789012', 5, 'DEBIT', 'MICHAEL WILLIAMS', '2027-09-30', '789', NULL, 'ACTIVE'),
('5512345678901234', 7, 'DEBIT', 'EMILY BROWN', '2028-03-31', '234', NULL, 'ACTIVE'),
('4024007156789012', 9, 'DEBIT', 'DAVID JONES', '2027-11-30', '567', NULL, 'ACTIVE'),
('5105105105105100', 2, 'CREDIT', 'JOHN SMITH', '2028-12-31', '890', 10000.00, 'ACTIVE'),
('4111111111111111', 4, 'CREDIT', 'SARAH JOHNSON', '2029-06-30', '321', 25000.00, 'ACTIVE');

-- Update sequences to avoid conflicts
SELECT setval('customers_customer_id_seq', (SELECT MAX(customer_id) FROM customers));
SELECT setval('accounts_account_id_seq', (SELECT MAX(account_id) FROM accounts));
SELECT setval('transactions_transaction_id_seq', (SELECT MAX(transaction_id) FROM transactions));
SELECT setval('transfers_transfer_id_seq', (SELECT MAX(transfer_id) FROM transfers));
SELECT setval('loans_loan_id_seq', (SELECT MAX(loan_id) FROM loans));
SELECT setval('loan_payments_payment_id_seq', (SELECT MAX(payment_id) FROM loan_payments));
SELECT setval('cards_card_id_seq', (SELECT MAX(card_id) FROM cards));
