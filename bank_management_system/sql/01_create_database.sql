-- =============================================
-- Bank Account Management System
-- Database Creation Script
-- =============================================

-- Drop database if exists (use with caution in production)
DROP DATABASE IF EXISTS bank_management;

-- Create database
CREATE DATABASE bank_management;

-- Connect to the database
\c bank_management;

-- Create schema
CREATE SCHEMA IF NOT EXISTS banking;

-- Set search path
SET search_path TO banking, public;

COMMENT ON DATABASE bank_management IS 'Bank Account Management System Database';
COMMENT ON SCHEMA banking IS 'Main schema for banking operations';
