USE TestDB;
GO

-- Parameters: change the salt to get a different but repeatable split
DECLARE @salt NVARCHAR(64) = N'seed-001';


-- Safety: ensure source table exists
IF OBJECT_ID('Bakery', 'U') IS NULL
BEGIN
    PRINT 'Error: Table Bakery does not exist in TestDB.';
    RETURN;
END
GO

-- Clean up previous outputs
DROP TABLE IF EXISTS AliceBakery, BobsBreakfast, Charliescafe, Desayuno_de_David, EddiesEats,AggBakery;
GO

DROP TABLE IF EXISTS #Randomized, #AggBakery, #Ordered, AggBakery;
GO

/* 
Create a deterministic order by hashing stable columns with a user-provided salt.
- Using SHA2_256 for a uniform, stable hash.
- ORDER BY hash then a tie-breaker (TransactionNo) ensures a strict total order.
- As long as Bakery content and @salt are unchanged, the split is identical every run.
*/
SELECT 
    TransactionNo,
    STRING_AGG(Items, ', ') AS ItemsPurchased
INTO AggBakery
FROM [Bakery]
GROUP BY TransactionNo,[DateTime]
GO


SELECT  B.*,
        ROW_NUMBER() OVER (
            ORDER BY 
              CONVERT(VARBINARY(32), HASHBYTES('SHA2_256', 
                    @salt +
                    ISNULL(CAST(B.TransactionNo AS NVARCHAR(32)), N'') + N'|' +
                    ISNULL(CONVERT(NVARCHAR(30), B.DateTime, 126), N'') + N'|' +
                    ISNULL(B.Items, N'') + N'|' +
                    ISNULL(B.Daypart, N'') + N'|' +
                    ISNULL(B.DayType, N'')
              )),
              B.TransactionNo
        ) AS rn
INTO #Ordered
FROM AggBakery AS B;
GO

-- Create the five deterministic partitions of exactly 40 rows each
SELECT * INTO AliceBakery FROM #Ordered WHERE rn BETWEEN 1   AND 40;
SELECT * INTO BobsBreakfast FROM #Ordered WHERE rn BETWEEN 41  AND 80;
SELECT * INTO Charliescafe FROM #Ordered WHERE rn BETWEEN 81  AND 120;
SELECT * INTO Desayuno_de_David FROM #Ordered WHERE rn BETWEEN 121 AND 160;
SELECT * INTO EddiesEats FROM #Ordered WHERE rn BETWEEN 161 AND 200;
GO

-- Verify counts
SELECT COUNT(distinct ItemsPurchased), 'AliceBakery' FROM AliceBakery
UNION ALL SELECT COUNT (distinct ItemsPurchased), 'BobsBreakfast' FROM BobsBreakfast
UNION ALL SELECT COUNT(distinct ItemsPurchased), 'CharliesCafe' FROM CharliesCafe
UNION ALL SELECT COUNT(distinct ItemsPurchased), 'Desayuno de David' FROM Desayuno_de_David
UNION ALL SELECT COUNT(distinct ItemsPurchased), 'Eddies Eats' FROM EddiesEats;
GO
