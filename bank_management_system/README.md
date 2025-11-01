# Bank Account Management System - PostgreSQL Project

A comprehensive PostgreSQL database system for managing bank accounts, customers, transactions, loans, and cards. This project demonstrates advanced SQL concepts including stored procedures, functions, triggers, views, and complex queries.

## 📋 Table of Contents

- [Features](#features)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Usage](#usage)
- [Database Objects](#database-objects)
- [Example Queries](#example-queries)
- [Security Considerations](#security-considerations)

## ✨ Features

### Core Functionality
- **Customer Management**: Store and manage customer information with validation
- **Account Management**: Multiple account types (Savings, Checking, Premium, Business, Student)
- **Transaction Processing**: Deposits, withdrawals, transfers with full audit trail
- **Loan Management**: Track loans with payment schedules and interest calculations
- **Card Management**: Debit and credit card tracking with expiry monitoring
- **Audit Logging**: Complete audit trail for all database operations

### Advanced Features
- Automated interest calculation and application
- Balance validation and minimum balance enforcement
- Transaction history and reporting
- Customer financial overview
- Monthly transaction summaries
- Loan payment calculations
- Card expiry notifications

## 🗄️ Database Schema

### Main Tables

1. **customers** - Customer personal information
2. **account_types** - Different types of bank accounts
3. **accounts** - Bank account details
4. **transaction_types** - Types of transactions
5. **transactions** - All account transactions
6. **transfers** - Money transfers between accounts
7. **loans** - Loan information
8. **loan_payments** - Loan payment history
9. **cards** - Debit and credit cards
10. **audit_log** - Audit trail for all operations

### Entity Relationships

```
customers (1) ----< (N) accounts
accounts (1) ----< (N) transactions
accounts (1) ----< (N) cards
customers (1) ----< (N) loans
loans (1) ----< (N) loan_payments
account_types (1) ----< (N) accounts
transaction_types (1) ----< (N) transactions
```

## 🚀 Installation

### Prerequisites
- PostgreSQL 12 or higher
- psql command-line tool
- Appropriate database permissions

### Setup Steps

1. **Clone or download the project**
```bash
cd bank_management_system
```

2. **Create the database**
```bash
psql -U postgres -f sql/01_create_database.sql
```

3. **Create tables**
```bash
psql -U postgres -d bank_management -f sql/02_create_tables.sql
```

4. **Insert sample data**
```bash
psql -U postgres -d bank_management -f sql/03_insert_sample_data.sql
```

5. **Create functions and procedures**
```bash
psql -U postgres -d bank_management -f sql/04_functions_procedures.sql
```

6. **Create views**
```bash
psql -U postgres -d bank_management -f sql/05_views_queries.sql
```

### All-in-One Installation
```bash
psql -U postgres -f sql/01_create_database.sql && \
psql -U postgres -d bank_management -f sql/02_create_tables.sql && \
psql -U postgres -d bank_management -f sql/03_insert_sample_data.sql && \
psql -U postgres -d bank_management -f sql/04_functions_procedures.sql && \
psql -U postgres -d bank_management -f sql/05_views_queries.sql
```

## 💻 Usage

### Connect to Database
```bash
psql -U postgres -d bank_management
```

### Set Schema
```sql
SET search_path TO banking, public;
```

## 🔧 Database Objects

### Stored Functions

#### 1. **create_customer_account**
Creates a new customer with an initial account.

```sql
SELECT * FROM create_customer_account(
    'John', 'Doe', 'john.doe@email.com', '555-1234',
    '1990-01-01', '123 Main St', 'New York', 'NY', '10001',
    '123-45-6789', 1, 5000.00
);
```

#### 2. **deposit_money**
Deposits money into an account.

```sql
SELECT * FROM deposit_money(1, 1000.00, 'Salary deposit');
```

#### 3. **withdraw_money**
Withdraws money from an account with balance validation.

```sql
SELECT * FROM withdraw_money(1, 500.00, 'ATM withdrawal');
```

#### 4. **transfer_money**
Transfers money between two accounts.

```sql
SELECT * FROM transfer_money(1, 2, 250.00, 'Monthly transfer');
```

#### 5. **get_customer_total_balance**
Gets total balance across all customer accounts.

```sql
SELECT get_customer_total_balance(1);
```

#### 6. **calculate_loan_payment**
Calculates monthly loan payment amount.

```sql
SELECT calculate_loan_payment(50000.00, 5.5, 60);
```

#### 7. **apply_monthly_interest**
Applies monthly interest to all eligible accounts.

```sql
SELECT * FROM apply_monthly_interest();
```

### Views

#### 1. **customer_account_summary**
Summary of all customer accounts with total balances.

```sql
SELECT * FROM customer_account_summary ORDER BY total_balance DESC;
```

#### 2. **account_details**
Detailed account information with customer data.

```sql
SELECT * FROM account_details WHERE status = 'ACTIVE';
```

#### 3. **recent_transactions**
Recent transactions with full details.

```sql
SELECT * FROM recent_transactions LIMIT 20;
```

#### 4. **transfer_history**
Complete transfer history between accounts.

```sql
SELECT * FROM transfer_history WHERE transfer_date >= CURRENT_DATE - INTERVAL '30 days';
```

#### 5. **loan_summary**
Comprehensive loan information with payment progress.

```sql
SELECT * FROM loan_summary WHERE status = 'ACTIVE';
```

#### 6. **card_details**
Card information with expiry status.

```sql
SELECT * FROM card_details WHERE expiry_status = 'Expiring Soon';
```

#### 7. **monthly_transaction_summary**
Monthly transaction summaries by account.

```sql
SELECT * FROM monthly_transaction_summary 
WHERE month >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '6 months');
```

#### 8. **customer_financial_overview**
Complete financial overview per customer.

```sql
SELECT * FROM customer_financial_overview ORDER BY net_worth DESC;
```

## 📊 Example Queries

### 1. Find Accounts Below Minimum Balance
```sql
SELECT account_number, customer_name, balance, minimum_balance
FROM account_details
WHERE balance < minimum_balance;
```

### 2. Get Top 10 Customers by Balance
```sql
SELECT customer_name, total_balance, total_accounts
FROM customer_account_summary
ORDER BY total_balance DESC
LIMIT 10;
```

### 3. Get Transaction History for Account
```sql
SELECT transaction_date, transaction_type, amount, balance_after, description
FROM recent_transactions
WHERE account_number = 'ACC1001000001'
ORDER BY transaction_date DESC;
```

### 4. Find High-Value Transactions
```sql
SELECT transaction_number, customer_name, amount, transaction_date
FROM recent_transactions
WHERE amount > 10000 AND status = 'COMPLETED'
ORDER BY amount DESC;
```

### 5. Get Customer Activity Report
```sql
SELECT customer_name, total_accounts, total_balance, 
       total_loans, net_worth
FROM customer_financial_overview
ORDER BY net_worth DESC;
```

### 6. Find Cards Expiring Soon
```sql
SELECT card_number, card_holder_name, expiry_date, account_number
FROM card_details
WHERE expiry_status = 'Expiring Soon'
ORDER BY expiry_date;
```

### 7. Get Loan Payment History
```sql
SELECT l.loan_number, c.first_name || ' ' || c.last_name AS customer_name,
       lp.payment_date, lp.payment_amount, lp.principal_paid, lp.interest_paid
FROM loan_payments lp
JOIN loans l ON lp.loan_id = l.loan_id
JOIN customers c ON l.customer_id = c.customer_id
WHERE l.loan_number = 'LOAN1001001'
ORDER BY lp.payment_date DESC;
```

### 8. Get Monthly Transaction Summary
```sql
SELECT month, customer_name, transaction_count, 
       total_credits, total_debits, net_change
FROM monthly_transaction_summary
WHERE month >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '3 months')
ORDER BY month DESC;
```

## 🔒 Security Considerations

### Implemented Security Features

1. **Data Validation**
   - Email format validation
   - Age verification (minimum 18 years)
   - Balance constraints
   - Date validations

2. **Referential Integrity**
   - Foreign key constraints
   - Cascade rules for deletions
   - Unique constraints on critical fields

3. **Audit Trail**
   - Complete audit logging
   - Timestamp tracking
   - User tracking for changes

4. **Business Rules**
   - Minimum balance enforcement
   - Account status checks
   - Transaction validation

### Recommended Additional Security

1. **Encryption**
   - Encrypt sensitive data (SSN, card numbers)
   - Use PostgreSQL pgcrypto extension

2. **Access Control**
   - Implement role-based access control (RBAC)
   - Create separate roles for different operations
   - Use row-level security (RLS)

3. **Password Protection**
   - Add user authentication table
   - Hash passwords using bcrypt
   - Implement password policies

4. **Monitoring**
   - Set up query logging
   - Monitor failed login attempts
   - Alert on suspicious activities

## 📁 Project Structure

```
bank_management_system/
├── sql/
│   ├── 01_create_database.sql      # Database creation
│   ├── 02_create_tables.sql        # Table definitions
│   ├── 03_insert_sample_data.sql   # Sample data
│   ├── 04_functions_procedures.sql # Functions and procedures
│   ├── 05_views_queries.sql        # Views and queries
│   └── 06_example_usage.sql        # Usage examples
├── docs/
│   └── (additional documentation)
└── README.md                        # This file
```

## 🧪 Testing

Run the example usage script to test all functionality:

```bash
psql -U postgres -d bank_management -f sql/06_example_usage.sql
```

## 📝 Sample Data

The database includes sample data for:
- 10 customers
- 15 accounts across different types
- Multiple transactions
- 5 loans with payment history
- 7 debit and credit cards
- Transfer history

## 🔄 Maintenance Tasks

### Regular Maintenance

1. **Apply Monthly Interest**
```sql
SELECT * FROM apply_monthly_interest();
```

2. **Check Accounts Below Minimum**
```sql
SELECT * FROM account_details WHERE balance < minimum_balance;
```

3. **Monitor Card Expiry**
```sql
SELECT * FROM card_details WHERE expiry_status IN ('Expiring Soon', 'Expired');
```

4. **Review Audit Logs**
```sql
SELECT * FROM audit_log WHERE changed_at >= CURRENT_DATE - INTERVAL '7 days';
```

## 🤝 Contributing

This is an educational project. Feel free to:
- Add new features
- Improve existing queries
- Enhance security measures
- Add more comprehensive test cases

## 📄 License

This project is created for educational purposes.

## 👥 Author

Created as a PostgreSQL mini project for Bank Account Management System.

## 📞 Support

For questions or issues:
1. Review the example usage file
2. Check the inline SQL comments
3. Refer to PostgreSQL documentation

---

**Note**: This is a demonstration project. For production use, implement additional security measures, encryption, and compliance with banking regulations.
