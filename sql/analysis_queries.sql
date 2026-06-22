
-- Dubai Real Estate Price Intelligence Dashboard
-- SQL Analysis Queries

-- 1. Overall KPIs
SELECT
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(actual_worth), 2) AS total_sales_value,
    ROUND(AVG(actual_worth), 2) AS average_transaction_value,
    ROUND(AVG(meter_sale_price), 2) AS average_price_per_sqm,
    MIN(instance_date) AS start_date,
    MAX(instance_date) AS end_date
FROM transactions;

-- 2. Top 10 areas by transaction count
SELECT
    area_name_en,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(actual_worth), 2) AS total_sales_value,
    ROUND(AVG(actual_worth), 2) AS average_price,
    ROUND(AVG(meter_sale_price), 2) AS average_price_per_sqm
FROM transactions
GROUP BY area_name_en
ORDER BY total_transactions DESC
LIMIT 10;

-- 3. Top 10 areas by total sales value
SELECT
    area_name_en,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(actual_worth), 2) AS total_sales_value,
    ROUND(AVG(actual_worth), 2) AS average_price,
    ROUND(AVG(meter_sale_price), 2) AS average_price_per_sqm
FROM transactions
GROUP BY area_name_en
ORDER BY total_sales_value DESC
LIMIT 10;

-- 4. Property type performance
SELECT
    property_type_en,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(actual_worth), 2) AS total_sales_value,
    ROUND(AVG(actual_worth), 2) AS average_price,
    ROUND(AVG(meter_sale_price), 2) AS average_price_per_sqm
FROM transactions
GROUP BY property_type_en
ORDER BY total_transactions DESC;

-- 5. Yearly market trend
SELECT
    transaction_year,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(actual_worth), 2) AS total_sales_value,
    ROUND(AVG(actual_worth), 2) AS average_price,
    ROUND(AVG(meter_sale_price), 2) AS average_price_per_sqm
FROM transactions
GROUP BY transaction_year
ORDER BY transaction_year;

-- 6. Monthly market trend
SELECT
    transaction_year_month,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(actual_worth), 2) AS total_sales_value,
    ROUND(AVG(actual_worth), 2) AS average_price,
    ROUND(AVG(meter_sale_price), 2) AS average_price_per_sqm
FROM transactions
GROUP BY transaction_year_month
ORDER BY transaction_year_month;

-- 7. Top 10 areas by price per sqm
SELECT
    area_name_en,
    COUNT(transaction_id) AS total_transactions,
    ROUND(AVG(actual_worth), 2) AS average_price,
    ROUND(AVG(meter_sale_price), 2) AS average_price_per_sqm
FROM transactions
GROUP BY area_name_en
HAVING COUNT(transaction_id) >= 500
ORDER BY average_price_per_sqm DESC
LIMIT 10;

-- 8. Registration type analysis
SELECT
    reg_type_en,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(actual_worth), 2) AS total_sales_value,
    ROUND(AVG(actual_worth), 2) AS average_price,
    ROUND(AVG(meter_sale_price), 2) AS average_price_per_sqm
FROM transactions
GROUP BY reg_type_en
ORDER BY total_transactions DESC;

-- 9. Area and property type combination
SELECT
    area_name_en,
    property_type_en,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(actual_worth), 2) AS total_sales_value,
    ROUND(AVG(actual_worth), 2) AS average_price,
    ROUND(AVG(meter_sale_price), 2) AS average_price_per_sqm
FROM transactions
GROUP BY area_name_en, property_type_en
ORDER BY total_transactions DESC
LIMIT 20;
