SELECT *
FROM dirty_cafe_sales;

CREATE TABLE test.dirty_cafe
LIKE dirty_cafe_sales;

INSERT dirty_cafe
SELECT * FROM dirty_cafe_sales;

SELECT *
FROM dirty_cafe;

-- DATA CLEANING

-- 1

SELECT *
FROM dirty_cafe
WHERE Item = "";

DELETE FROM dirty_cafe
WHERE Item IN ("", "UNKNOWN", "ERROR");

-- 2. Quantity * Price Per Unit

SELECT *
FROM dirty_cafe
WHERE `Total Spent` = "";

UPDATE dirty_cafe
SET `Total Spent` = Quantity * `Price Per Unit`;

ALTER TABLE dirty_cafe
MODIFY `Total Spent` FLOAT;

-- 3

SELECT DISTINCT `Payment Method`
FROM dirty_cafe;

SELECT DISTINCT Location
FROM dirty_cafe;

DELETE FROM dirty_cafe
WHERE `Payment Method` IN ('', ERROR, UNKNOWN);

DELETE FROM dirty_cafe
WHERE Location IN ('', "ERROR", "UNKNOWN");

-- 4

SELECT DISTINCT `Transaction Date`
FROM dirty_cafe;

DELETE FROM dirty_cafe
WHERE `Transaction Date` IN ('', "ERROR", "UNKNOWN");

ALTER TABLE dirty_cafe
MODIFY `Transaction Date` DATE;

-- DATA EXPLORATORY

SELECT *
FROM dirty_cafe;

SELECT DISTINCT Item
FROM dirty_cafe;

SELECT Item, SUM(Quantity) AS "Quantity Sold", SUM(`Total Spent`) AS "Sales"
FROM dirty_cafe
GROUP BY Item;

SELECT `Payment Method`, COUNT(*) AS Total
FROM dirty_cafe
GROUP BY `Payment Method`
ORDER BY Total DESC;

SELECT 
    MONTH(`Transaction Date`) as "No", MONTHNAME(`Transaction Date`) as "Month",
    COUNT(*) AS "Total Transactions", SUM(Quantity) AS "Quantity Sold", SUM(`Total Spent`) AS "Total Sales" 
FROM dirty_cafe
GROUP BY MONTH(`Transaction Date`), MONTHNAME(`Transaction Date`)
ORDER BY MONTH(`Transaction Date`);

SELECT 
    DAYNAME(`Transaction Date`) as "Day",
    COUNT(*) AS "Total Transactions", SUM(Quantity) AS "Quantity Sold", SUM(`Total Spent`) AS "Total Sales" 
FROM dirty_cafe
GROUP BY DAYNAME(`Transaction Date`)
ORDER BY DAYNAME(`Transaction Date`);

SELECT Item, AVG(`Price Per Unit`) AS Price, SUM(Quantity) As "Quantity Sold", SUM(Quantity)/9790*100 AS "Portion Of Quantity (%)"
FROM dirty_cafe
GROUP BY Item
ORDER BY SUM(Quantity) DESC;

SELECT SUM(Quantity)
FROM dirty_cafe