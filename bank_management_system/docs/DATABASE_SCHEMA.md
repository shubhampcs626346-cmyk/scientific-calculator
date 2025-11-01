# Database Schema Documentation

## Overview

The Bank Account Management System uses a relational database design with 10 main tables, multiple views, stored procedures, and triggers to manage banking operations.

## Entity Relationship Diagram (ERD)

```
┌─────────────┐         ┌──────────────┐         ┌─────────────────┐
│  customers  │────────<│   accounts   │>────────│  account_types  │
└─────────────┘         └──────────────┘         └─────────────────┘
      │                        │
      │                        │
      │                        ├────────<┌──────────────┐
      │                        │         │ transactions │
      │                        │         └──────────────┘
      │                        │                │
      │                        │                │
      │                        │         ┌──────────────────┐
      │                        │         │transaction_types │
      │                        │         └──────────────────┘
      │                        │
      │                        ├────────<┌───────────┐
      │                        │         │  transfers│
      │                        │         └───────────┘
      │                        │
      │                        └────────<┌─────────┐
      │                                  │  cards  │
      │                                  └─────────┘
      │
      └────────<┌─────────┐
                │  loans  │
                └─────────┘
                     │
                     └────────<┌───────────────┐
                               │ loan_payments │
                               └───────────────┘
```

## Table Definitions

### 1. customers

Stores customer personal information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| customer_id | SERIAL | PRIMARY KEY | Unique customer identifier |
| first_name | VARCHAR(50) | NOT NULL | Customer's first name |
| last_name | VARCHAR(50) | NOT NULL | Customer's last name |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Email address |
| phone | VARCHAR(20) | | Phone number |
| date_of_birth | DATE | NOT NULL | Date of birth (must be 18+) |
| address | TEXT | | Street address |
| city | VARCHAR(50) | | City |
| state | VARCHAR(50) | | State |
| zip_code | VARCHAR(10) | | ZIP/Postal code |
| country | VARCHAR(50) | DEFAULT 'USA' | Country |
| ssn | VARCHAR(11) | UNIQUE | Social Security Number |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update time |
| is_active | BOOLEAN | DEFAULT TRUE | Account active status |

**Constraints:**
- Email must be valid format
- Age must be 18 or older

**Indexes:**
- idx_customers_email (email)
- idx_customers_ssn (ssn)

---

### 2. account_types

Defines different types of bank accounts.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| account_type_id | SERIAL | PRIMARY KEY | Unique account type identifier |
| type_name | VARCHAR(50) | UNIQUE, NOT NULL | Account type name |
| description | TEXT | | Account type description |
| minimum_balance | DECIMAL(15,2) | DEFAULT 0.00 | Required minimum balance |
| interest_rate | DECIMAL(5,2) | DEFAULT 0.00 | Annual interest rate (%) |
| monthly_fee | DECIMAL(10,2) | DEFAULT 0.00 | Monthly maintenance fee |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Default Account Types:**
- SAVINGS: Standard savings account
- CHECKING: Standard checking account
- PREMIUM_SAVINGS: High-yield savings
- BUSINESS: Business checking account
- STUDENT: Student account with no fees

---

### 3. accounts

Stores bank account information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| account_id | SERIAL | PRIMARY KEY | Unique account identifier |
| account_number | VARCHAR(20) | UNIQUE, NOT NULL | Account number |
| customer_id | INTEGER | FK → customers, NOT NULL | Account owner |
| account_type_id | INTEGER | FK → account_types, NOT NULL | Type of account |
| balance | DECIMAL(15,2) | DEFAULT 0.00, CHECK >= 0 | Current balance |
| currency | VARCHAR(3) | DEFAULT 'USD' | Currency code |
| status | VARCHAR(20) | DEFAULT 'ACTIVE' | Account status |
| opened_date | DATE | DEFAULT CURRENT_DATE | Account opening date |
| closed_date | DATE | | Account closing date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update time |

**Status Values:**
- ACTIVE: Account is active
- INACTIVE: Account is inactive
- FROZEN: Account is frozen
- CLOSED: Account is closed

**Constraints:**
- Balance must be non-negative
- Closed date must be after opened date

**Indexes:**
- idx_accounts_customer (customer_id)
- idx_accounts_number (account_number)
- idx_accounts_status (status)

---

### 4. transaction_types

Defines different types of transactions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| transaction_type_id | SERIAL | PRIMARY KEY | Unique transaction type identifier |
| type_name | VARCHAR(50) | UNIQUE, NOT NULL | Transaction type name |
| description | TEXT | | Transaction type description |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Default Transaction Types:**
- DEPOSIT: Money deposited
- WITHDRAWAL: Money withdrawn
- TRANSFER_IN: Money transferred in
- TRANSFER_OUT: Money transferred out
- FEE: Bank fee charged
- INTEREST: Interest credited
- ATM_WITHDRAWAL: ATM cash withdrawal
- CHECK_DEPOSIT: Check deposited
- ONLINE_PAYMENT: Online payment
- REFUND: Refund credited

---

### 5. transactions

Records all account transactions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| transaction_id | SERIAL | PRIMARY KEY | Unique transaction identifier |
| transaction_number | VARCHAR(30) | UNIQUE, NOT NULL | Transaction number |
| account_id | INTEGER | FK → accounts, NOT NULL | Account involved |
| transaction_type_id | INTEGER | FK → transaction_types, NOT NULL | Type of transaction |
| amount | DECIMAL(15,2) | NOT NULL, CHECK > 0 | Transaction amount |
| balance_after | DECIMAL(15,2) | NOT NULL | Balance after transaction |
| transaction_date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Transaction date/time |
| description | TEXT | | Transaction description |
| reference_number | VARCHAR(50) | | External reference number |
| status | VARCHAR(20) | DEFAULT 'COMPLETED' | Transaction status |
| created_by | VARCHAR(50) | | User who created transaction |

**Status Values:**
- PENDING: Transaction pending
- COMPLETED: Transaction completed
- FAILED: Transaction failed
- REVERSED: Transaction reversed

**Indexes:**
- idx_transactions_account (account_id)
- idx_transactions_date (transaction_date)
- idx_transactions_type (transaction_type_id)

---

### 6. transfers

Records money transfers between accounts.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| transfer_id | SERIAL | PRIMARY KEY | Unique transfer identifier |
| transfer_number | VARCHAR(30) | UNIQUE, NOT NULL | Transfer number |
| from_account_id | INTEGER | FK → accounts, NOT NULL | Source account |
| to_account_id | INTEGER | FK → accounts, NOT NULL | Destination account |
| amount | DECIMAL(15,2) | NOT NULL, CHECK > 0 | Transfer amount |
| transfer_date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Transfer date/time |
| description | TEXT | | Transfer description |
| status | VARCHAR(20) | DEFAULT 'COMPLETED' | Transfer status |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Constraints:**
- From and to accounts must be different

**Indexes:**
- idx_transfers_from (from_account_id)
- idx_transfers_to (to_account_id)
- idx_transfers_date (transfer_date)

---

### 7. loans

Stores loan information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| loan_id | SERIAL | PRIMARY KEY | Unique loan identifier |
| loan_number | VARCHAR(20) | UNIQUE, NOT NULL | Loan number |
| customer_id | INTEGER | FK → customers, NOT NULL | Loan holder |
| loan_type | VARCHAR(50) | NOT NULL | Type of loan |
| principal_amount | DECIMAL(15,2) | NOT NULL, CHECK > 0 | Original loan amount |
| interest_rate | DECIMAL(5,2) | NOT NULL, CHECK >= 0 | Annual interest rate (%) |
| term_months | INTEGER | NOT NULL, CHECK > 0 | Loan term in months |
| monthly_payment | DECIMAL(15,2) | NOT NULL | Monthly payment amount |
| outstanding_balance | DECIMAL(15,2) | NOT NULL | Remaining balance |
| start_date | DATE | DEFAULT CURRENT_DATE | Loan start date |
| end_date | DATE | | Loan end date |
| status | VARCHAR(20) | DEFAULT 'ACTIVE' | Loan status |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update time |

**Loan Types:**
- PERSONAL: Personal loan
- HOME: Home/mortgage loan
- AUTO: Auto loan
- BUSINESS: Business loan
- EDUCATION: Education loan

**Status Values:**
- PENDING: Loan pending approval
- ACTIVE: Loan is active
- PAID: Loan fully paid
- DEFAULTED: Loan in default
- CLOSED: Loan closed

**Indexes:**
- idx_loans_customer (customer_id)
- idx_loans_status (status)

---

### 8. loan_payments

Records loan payment history.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| payment_id | SERIAL | PRIMARY KEY | Unique payment identifier |
| loan_id | INTEGER | FK → loans, NOT NULL | Associated loan |
| payment_number | VARCHAR(30) | UNIQUE, NOT NULL | Payment number |
| payment_amount | DECIMAL(15,2) | NOT NULL, CHECK > 0 | Total payment amount |
| principal_paid | DECIMAL(15,2) | NOT NULL | Principal portion |
| interest_paid | DECIMAL(15,2) | NOT NULL | Interest portion |
| payment_date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Payment date/time |
| due_date | DATE | NOT NULL | Payment due date |
| status | VARCHAR(20) | DEFAULT 'PAID' | Payment status |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Status Values:**
- PENDING: Payment pending
- PAID: Payment completed
- LATE: Payment late
- MISSED: Payment missed

**Indexes:**
- idx_loan_payments_loan (loan_id)

---

### 9. cards

Stores debit and credit card information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| card_id | SERIAL | PRIMARY KEY | Unique card identifier |
| card_number | VARCHAR(16) | UNIQUE, NOT NULL | Card number |
| account_id | INTEGER | FK → accounts, NOT NULL | Linked account |
| card_type | VARCHAR(20) | NOT NULL | Type of card |
| card_holder_name | VARCHAR(100) | NOT NULL | Name on card |
| expiry_date | DATE | NOT NULL | Card expiry date |
| cvv | VARCHAR(3) | NOT NULL | Card CVV |
| credit_limit | DECIMAL(15,2) | | Credit limit (for credit cards) |
| status | VARCHAR(20) | DEFAULT 'ACTIVE' | Card status |
| issued_date | DATE | DEFAULT CURRENT_DATE | Card issue date |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Card Types:**
- DEBIT: Debit card
- CREDIT: Credit card

**Status Values:**
- ACTIVE: Card is active
- BLOCKED: Card is blocked
- EXPIRED: Card has expired
- CANCELLED: Card is cancelled

**Constraints:**
- Expiry date must be after issue date

**Indexes:**
- idx_cards_account (account_id)

---

### 10. audit_log

Stores audit trail for all database operations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| audit_id | SERIAL | PRIMARY KEY | Unique audit identifier |
| table_name | VARCHAR(50) | NOT NULL | Table that was modified |
| operation | VARCHAR(10) | NOT NULL | Type of operation |
| record_id | INTEGER | NOT NULL | ID of affected record |
| old_values | JSONB | | Previous values (JSON) |
| new_values | JSONB | | New values (JSON) |
| changed_by | VARCHAR(50) | | User who made change |
| changed_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Change timestamp |

**Operation Types:**
- INSERT: New record created
- UPDATE: Record updated
- DELETE: Record deleted

**Indexes:**
- idx_audit_table (table_name, record_id)

---

## Data Types Reference

| Type | Description | Example |
|------|-------------|---------|
| SERIAL | Auto-incrementing integer | 1, 2, 3... |
| VARCHAR(n) | Variable-length string | 'John Smith' |
| TEXT | Unlimited length text | Long descriptions |
| DECIMAL(p,s) | Fixed-point number | 1234.56 |
| DATE | Date only | 2024-01-01 |
| TIMESTAMP | Date and time | 2024-01-01 10:30:00 |
| BOOLEAN | True/false | TRUE, FALSE |
| JSONB | Binary JSON | {"key": "value"} |

---

## Naming Conventions

- **Tables**: Lowercase, plural nouns (customers, accounts)
- **Columns**: Lowercase with underscores (first_name, account_id)
- **Primary Keys**: table_name_id (customer_id, account_id)
- **Foreign Keys**: referenced_table_id (customer_id in accounts table)
- **Indexes**: idx_table_column (idx_customers_email)
- **Views**: descriptive_name (customer_account_summary)
- **Functions**: verb_noun (deposit_money, calculate_loan_payment)

---

## Schema Evolution

To modify the schema:

1. **Adding a column:**
```sql
ALTER TABLE table_name ADD COLUMN column_name TYPE;
```

2. **Modifying a column:**
```sql
ALTER TABLE table_name ALTER COLUMN column_name TYPE new_type;
```

3. **Adding a constraint:**
```sql
ALTER TABLE table_name ADD CONSTRAINT constraint_name CHECK (condition);
```

4. **Creating an index:**
```sql
CREATE INDEX index_name ON table_name(column_name);
```

---

## Best Practices

1. **Always use transactions** for multi-step operations
2. **Use foreign keys** to maintain referential integrity
3. **Add indexes** on frequently queried columns
4. **Use constraints** to enforce business rules
5. **Document changes** in the audit_log table
6. **Regular backups** of the database
7. **Monitor performance** and optimize queries

---

This schema provides a solid foundation for a banking system with room for expansion and customization.
