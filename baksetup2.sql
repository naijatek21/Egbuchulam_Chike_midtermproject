USE TestDB;
GO

/* ================================================
   STEP 1: Identify the Top 30 Most Frequent Items
   ================================================ */
DROP TABLE IF EXISTS #TopItems;

WITH ItemFrequency AS (
    SELECT 
        LTRIM(RTRIM(value)) AS Item,
        COUNT(*) AS PurchaseCount
    FROM Bakery
        CROSS APPLY STRING_SPLIT(Items, ',')
    GROUP BY LTRIM(RTRIM(value))
)
SELECT TOP 30 Item
INTO #TopItems
FROM ItemFrequency
ORDER BY PurchaseCount DESC;

/* ================================================
   STEP 2: Create AggBakery_Frequent (Filtered Dataset)
   ================================================ */
DROP TABLE IF EXISTS AggBakery_Frequent;

SELECT 
    TransactionNo,
    [DateTime],
    STRING_AGG(Items, ', ') AS ItemsPurchased
INTO AggBakery_Frequent
FROM Bakery
WHERE EXISTS (
    SELECT 1
    FROM STRING_SPLIT(Items, ',') AS s
    WHERE LTRIM(RTRIM(s.value)) IN (SELECT Item FROM #TopItems)
)
GROUP BY TransactionNo, [DateTime];
GO

/* ================================================
   STEP 3: Materialize a Deterministically Ordered Table
   ================================================ */
DROP TABLE IF EXISTS #Numbered;

SELECT 
    *,
    ROW_NUMBER() OVER (ORDER BY TransactionNo, [DateTime]) AS rn
INTO #Numbered
FROM AggBakery_Frequent;
GO

/* ================================================
   STEP 4: Split into 5 Labeled Tables (60 Rows Each)
   ================================================ */
DROP TABLE IF EXISTS AliceBakery, BobsBreakfast, CharliesCafe, Desayuno_de_David, EddiesEats;

SELECT * INTO AliceBakery        FROM #Numbered WHERE rn BETWEEN 1   AND 40;
SELECT * INTO BobsBreakfast      FROM #Numbered WHERE rn BETWEEN 41  AND 80;
SELECT * INTO CharliesCafe       FROM #Numbered WHERE rn BETWEEN 81 AND 120;
SELECT * INTO Desayuno_de_David  FROM #Numbered WHERE rn BETWEEN 121 AND 160;
SELECT * INTO EddiesEats         FROM #Numbered WHERE rn BETWEEN 161 AND 200;
GO

/* ================================================
   STEP 5: Verify Split Summary
   ================================================ */
-- SELECT COUNT(*) AS Rows, 'AliceBakery'       AS TableName FROM AliceBakery
-- UNION ALL SELECT COUNT(*), 'BobsBreakfast'      FROM BobsBreakfast
-- UNION ALL SELECT COUNT(*), 'CharliesCafe'       FROM CharliesCafe
-- UNION ALL SELECT COUNT(*), 'Desayuno_de_David'  FROM Desayuno_de_David
-- UNION ALL SELECT COUNT(*), 'EddiesEats'         FROM EddiesEats;
-- GO

SELECT TransactionNo,ItemsPurchased FROM EddiesEats ORDER BY TransactionNo