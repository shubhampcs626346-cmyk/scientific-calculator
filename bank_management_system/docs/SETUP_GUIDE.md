# Bank Account Management System - Setup Guide

## Quick Start Guide

This guide will help you set up the Bank Account Management System database from scratch.

## Prerequisites

Before you begin, ensure you have:

1. **PostgreSQL installed** (version 12 or higher)
   - Download from: https://www.postgresql.org/download/
   - Verify installation: `psql --version`

2. **Database access credentials**
   - Username (default: postgres)
   - Password
   - Appropriate permissions to create databases

3. **Command-line access**
   - Terminal (Linux/Mac)
   - Command Prompt or PowerShell (Windows)

## Installation Methods

### Method 1: Step-by-Step Installation (Recommended for Learning)

#### Step 1: Create Database
```bash
psql -U postgres -f sql/01_create_database.sql
```

**What this does:**
- Creates a new database named `bank_management`
- Creates a schema named `banking`
- Sets up the basic database structure

**Expected output:**
```
DROP DATABASE
CREATE DATABASE
You are now connected to database "bank_management" as user "postgres".
CREATE SCHEMA
SET
```

#### Step 2: Create Tables
```bash
psql -U postgres -d bank_management -f sql/02_create_tables.sql
```

**What this does:**
- Creates all database tables
- Sets up foreign key relationships
- Creates indexes for performance
- Adds constraints for data validation

**Expected output:**
```
CREATE TABLE (repeated for each table)
CREATE INDEX (repeated for each index)
COMMENT (repeated for each comment)
```

#### Step 3: Insert Sample Data
```bash
psql -U postgres -d bank_management -f sql/03_insert_sample_data.sql
```

**What this does:**
- Inserts account types (Savings, Checking, etc.)
- Inserts transaction types (Deposit, Withdrawal, etc.)
- Creates 10 sample customers
- Creates 15 sample accounts
- Adds sample transactions, transfers, loans, and cards

**Expected output:**
```
INSERT 0 5
INSERT 0 10
INSERT 0 10
...
```

#### Step 4: Create Functions and Procedures
```bash
psql -U postgres -d bank_management -f sql/04_functions_procedures.sql
```

**What this does:**
- Creates utility functions (generate account numbers, etc.)
- Creates business logic functions (deposit, withdraw, transfer)
- Sets up triggers for automatic updates
- Creates audit logging functionality

**Expected output:**
```
CREATE FUNCTION (repeated for each function)
CREATE TRIGGER (repeated for each trigger)
```

#### Step 5: Create Views
```bash
psql -U postgres -d bank_management -f sql/05_views_queries.sql
```

**What this does:**
- Creates views for common queries
- Sets up reporting views
- Creates summary views for analytics

**Expected output:**
```
CREATE VIEW (repeated for each view)
COMMENT (repeated for each comment)
```

### Method 2: One-Command Installation (Quick Setup)

For experienced users who want to set up everything at once:

```bash
psql -U postgres -f sql/01_create_database.sql && \
psql -U postgres -d bank_management -f sql/02_create_tables.sql && \
psql -U postgres -d bank_management -f sql/03_insert_sample_data.sql && \
psql -U postgres -d bank_management -f sql/04_functions_procedures.sql && \
psql -U postgres -d bank_management -f sql/05_views_queries.sql
```

## Verification

After installation, verify the setup:

### 1. Connect to Database
```bash
psql -U postgres -d bank_management
```

### 2. Set Schema
```sql
SET search_path TO banking, public;
```

### 3. Check Tables
```sql
\dt
```

**Expected output:** List of all tables (customers, accounts, transactions, etc.)

### 4. Check Views
```sql
\dv
```

**Expected output:** List of all views

### 5. Check Functions
```sql
\df
```

**Expected output:** List of all functions

### 6. Verify Sample Data
```sql
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM accounts;
SELECT COUNT(*) FROM transactions;
```

**Expected output:**
```
 count 
-------
    10
(1 row)

 count 
-------
    15
(1 row)

 count 
-------
    10
(1 row)
```

## Testing the Installation

Run some test queries to ensure everything works:

### Test 1: View Customer Summary
```sql
SELECT * FROM customer_account_summary LIMIT 5;
```

### Test 2: View Recent Transactions
```sql
SELECT * FROM recent_transactions LIMIT 5;
```

### Test 3: Test Deposit Function
```sql
SELECT * FROM deposit_money(1, 100.00, 'Test deposit');
```

### Test 4: View Account Details
```sql
SELECT * FROM account_details WHERE account_id = 1;
```

## Troubleshooting

### Issue 1: Permission Denied
**Error:** `ERROR: permission denied to create database`

**Solution:**
```bash
# Login as superuser
sudo -u postgres psql

# Or specify superuser credentials
psql -U postgres -W
```

### Issue 2: Database Already Exists
**Error:** `ERROR: database "bank_management" already exists`

**Solution:**
```sql
-- Drop existing database (WARNING: This deletes all data)
DROP DATABASE bank_management;

-- Then run the installation again
```

### Issue 3: Connection Refused
**Error:** `psql: error: could not connect to server: Connection refused`

**Solution:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if not running
sudo systemctl start postgresql
```

### Issue 4: Schema Not Found
**Error:** `ERROR: schema "banking" does not exist`

**Solution:**
```sql
-- Always set the search path after connecting
SET search_path TO banking, public;

-- Or add to your .psqlrc file for automatic setup
echo "SET search_path TO banking, public;" >> ~/.psqlrc
```

## Configuration Options

### Change Database Name

Edit `sql/01_create_database.sql`:
```sql
-- Change this line
CREATE DATABASE your_database_name;
```

### Change Schema Name

Edit `sql/01_create_database.sql`:
```sql
-- Change this line
CREATE SCHEMA IF NOT EXISTS your_schema_name;
```

Then update all other files to use the new schema name.

### Customize Sample Data

Edit `sql/03_insert_sample_data.sql` to add your own sample data or modify existing data.

## Next Steps

After successful installation:

1. **Explore the Data**
   - Review sample customers, accounts, and transactions
   - Understand the relationships between tables

2. **Try Example Queries**
   - Run queries from `sql/06_example_usage.sql`
   - Experiment with different parameters

3. **Test Functions**
   - Create new customers and accounts
   - Perform deposits, withdrawals, and transfers
   - Apply monthly interest

4. **Review Documentation**
   - Read the main README.md
   - Study the SQL comments in each file
   - Understand the business logic

5. **Customize for Your Needs**
   - Add new tables or fields
   - Create additional functions
   - Modify business rules

## Uninstallation

To completely remove the database:

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Drop the database
DROP DATABASE bank_management;

-- Exit
\q
```

## Additional Resources

- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **SQL Tutorial**: https://www.postgresql.org/docs/current/tutorial.html
- **PL/pgSQL Guide**: https://www.postgresql.org/docs/current/plpgsql.html

## Support

If you encounter issues not covered in this guide:

1. Check PostgreSQL logs: `/var/log/postgresql/`
2. Review error messages carefully
3. Verify PostgreSQL version compatibility
4. Ensure all prerequisites are met

---

**Happy Banking! 🏦**
