SELECT @@VERSION;

CREATE DATABASE TestDB;

USE TestDB;

CREATE TABLE Users (
    ID INT PRIMARY KEY IDENTITY,
    Name NVARCHAR(50),
    Email NVARCHAR(100)
);

INSERT INTO Users (Name, Email)
VALUES ('Alice', 'alice@example.com'), ('Bob', 'bob@example.com');

SELECT * FROM Users;
