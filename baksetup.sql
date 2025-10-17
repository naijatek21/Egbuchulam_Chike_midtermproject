USE TestDB;
GO

/* 1) Ensure AggBakery exists with your exact definition (no DateTime in SELECT) */
IF OBJECT_ID('AggBakery', 'U') IS NULL
BEGIN
    SELECT 
        TransactionNo,
        STRING_AGG(Items, ', ') AS ItemsPurchased
    INTO AggBakery
    FROM Bakery
    GROUP BY TransactionNo, [DateTime];
END

/* 2) Deterministic split into 5 x 40-row tables with your custom names */
DECLARE @salt NVARCHAR(64) = N'seed-001'; -- change to reshuffle deterministically

-- Clean up prior runs
DROP TABLE IF EXISTS AliceBakery, BobsBreakfast, CharliesCafe, Desayuno_de_David, EddiesEats;
IF OBJECT_ID('tempdb..#Ordered') IS NOT NULL DROP TABLE #Ordered;

-- Deterministic order using a salted SHA-256 over AggBakery columns
SELECT  A.*,
        ROW_NUMBER() OVER (
            ORDER BY 
              CONVERT(VARBINARY(32), HASHBYTES('SHA2_256',
                    @salt +
                    ISNULL(CAST(A.TransactionNo AS NVARCHAR(32)), N'') + N'|' +
                    ISNULL(A.ItemsPurchased, N'')
              )),
              A.TransactionNo
        ) AS rn
INTO #Ordered
FROM AggBakery AS A;

-- Create the 5 labeled tables (exactly 40 rows each)
SELECT * INTO AliceBakery        FROM #Ordered WHERE rn BETWEEN 1   AND 40;
SELECT * INTO BobsBreakfast      FROM #Ordered WHERE rn BETWEEN 41  AND 80;
SELECT * INTO CharliesCafe       FROM #Ordered WHERE rn BETWEEN 81  AND 120;
SELECT * INTO Desayuno_de_David  FROM #Ordered WHERE rn BETWEEN 121 AND 160;
SELECT * INTO EddiesEats         FROM #Ordered WHERE rn BETWEEN 161 AND 200;

--Verify the splits
SELECT 'AliceBakery'AS TableName , COUNT(*) AS NumRows, COUNT(Distinct ItemsPurchased) AS Unique_Items FROM AliceBakery
UNION ALL SELECT 'BobsBreakfast',COUNT(*) , COUNT(Distinct ItemsPurchased) FROM BobsBreakfast
UNION ALL SELECT  'CharliesCafe',Count(*),COUNT(Distinct ItemsPurchased) AS Unique_Items FROM CharliesCafe
UNION ALL SELECT  'Desayuno_de_David',COUNT(*) ,COUNT(Distinct ItemsPurchased) AS Unique_Items FROM Desayuno_de_David
UNION ALL SELECT 'EddiesEats',COUNT(*),COUNT(Distinct ItemsPurchased) AS Unique_Items FROM EddiesEats;


