
-- 1. Total number of sales records
SELECT COUNT(*) AS total_sales_rows
FROM sales;

-- 2. Total revenue
SELECT ROUND(SUM("TotalAmount")::numeric, 2) AS total_revenue
FROM sales;

-- 3. Top 10 products by revenue
SELECT
    "Description",
    ROUND(SUM("TotalAmount")::numeric, 2) AS revenue
FROM sales
GROUP BY "Description"
ORDER BY revenue DESC
LIMIT 10;

-- 4. Monthly revenue
SELECT
    DATE_TRUNC('month', "InvoiceDate"::timestamp) AS month,
    ROUND(SUM("TotalAmount")::numeric, 2) AS revenue
FROM sales
GROUP BY month
ORDER BY month;
