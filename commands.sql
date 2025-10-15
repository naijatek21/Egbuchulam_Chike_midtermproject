SELECT * FROM read_csv_auto('canteen_shop_data.csv') AS Shop;
SELECT Item FROM Shop GROUP BY Date; 
