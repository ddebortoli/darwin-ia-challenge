-- Database Schema
-- PostgreSQL database schema for the Telegram Expense Bot

-- Users table for whitelisted Telegram users
CREATE TABLE users (
    "id" SERIAL PRIMARY KEY,
    "telegram_id" text UNIQUE NOT NULL,
    "created_at" timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Expenses table for storing user expenses
CREATE TABLE expenses (
    "id" SERIAL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES users("id") ON DELETE CASCADE,
    "description" text NOT NULL,
    "amount" money NOT NULL,
    "category" text NOT NULL,
    "added_at" timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster lookups
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_expenses_user_id ON expenses(user_id);
CREATE INDEX idx_expenses_category ON expenses(category);
CREATE INDEX idx_expenses_added_at ON expenses(added_at);

-- Insert some sample users for testing
-- Replace these with actual Telegram IDs
INSERT INTO users (telegram_id) VALUES 
    ('123456789'),  -- Replace with actual Telegram ID
    ('987654321');  -- Replace with actual Telegram ID

-- Create a view for expense statistics
CREATE VIEW expense_stats AS
SELECT 
    u.telegram_id,
    e.category,
    COUNT(*) as expense_count,
    SUM(e.amount::numeric) as total_amount
FROM expenses e
JOIN users u ON e.user_id = u.id
GROUP BY u.telegram_id, e.category
ORDER BY u.telegram_id, total_amount DESC; 