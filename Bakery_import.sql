IF DB_ID('TestDB') IS NULL
    CREATE DATABASE [TestDB];
GO
USE [TestDB];
GO

IF OBJECT_ID('Bakery', 'U') IS NOT NULL
    DROP TABLE [Bakery];
GO

CREATE TABLE [Bakery] (
    [TransactionNo] INT,
    [Items] NVARCHAR(50),
    [DateTime] DATETIME2,
    [Daypart] NVARCHAR(50),
    [DayType] NVARCHAR(50)
);
GO

-- Copy or mount the CSV into the SQL Server container at /tmp/Bakery.csv
-- Example copy: docker cp /path/to/Bakery.csv sqlserver:/tmp/Bakery.csv

BULK INSERT [Bakery]
FROM '/tmp/Bakery.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);


-- SELECT * FROM [Bakery];
SELECT 
    TransactionNo,
    STRING_AGG(Items, ', ') AS ItemsPurchased
INTO #AggBakery
FROM [Bakery]
GROUP BY TransactionNo
GO





-- Drop previous parts if they exist
DROP TABLE IF EXISTS AliceBakery, BobsBreakfast, Charliescafe, Desayuno_de_David, EddiesEats, AggBakery;
GO

DROP TABLE IF EXISTS #Randomized, #AggBakery;
GO

SELECT 
    TransactionNo,
    STRING_AGG(Items, ', ') AS ItemsPurchased,[DateTime]
INTO AggBakery
FROM [Bakery]
GROUP BY TransactionNo,[DateTime]
GO
-- Create randomized temp table
SELECT *, ROW_NUMBER() OVER (ORDER BY NEWID()) AS rn
INTO #Randomized
FROM AggBakery;
GO


-- Create 5 random partitions of 40 rows each
SELECT * INTO AliceBakery FROM #Randomized WHERE rn BETWEEN 1 AND 40;
SELECT * INTO BobsBreakfast FROM #Randomized WHERE rn BETWEEN 41 AND 80;
SELECT * INTO Charliescafe FROM #Randomized WHERE rn BETWEEN 81 AND 120;
SELECT * INTO Desayuno_de_David FROM #Randomized WHERE rn BETWEEN 121 AND 160;
SELECT * INTO EddiesEats FROM #Randomized WHERE rn BETWEEN 161 AND 200;
GO

-- Verify
-- SELECT COUNT(*)  FROM AliceBakery
-- UNION ALL
-- SELECT COUNT(*) FROM BobsBreakfast 
-- UNION ALL
-- SELECT COUNT(*)  FROM Charliescafe
-- UNION ALL
-- SELECT COUNT(Distinct ItemsPurchaes) FROM Desayuno_de_David
-- UNION ALL
-- SELECT COUNT(ItemsPurchsed) FROM EddiesEats;
-- GO


SELECT * FROM AggBakery;
-- SELECT * FROM BobsBreakfast;
-- SELECT * FROM Charliescafe;
-- SELECT * FROM Desayuno_de_David;
-- SELECT * FROM EddiesEats;
GO