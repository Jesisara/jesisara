
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'OmniBusReservation') 
BEGIN 
CREATE DATABASE OmniBusReservation; 
END; 
GO

USE OmniBusReservation; 
GO

CREATE TABLE Buses ( 
BusID INT IDENTITY(1,1) PRIMARY KEY, 
BusNumber NVARCHAR(20), 
BusType NVARCHAR(50), 
TotalSeats INT ); 

CREATE TABLE Routes ( 
RouteID INT IDENTITY(1,1) PRIMARY KEY, 
Source NVARCHAR(100), 
Destination NVARCHAR(100), 
Distance INT ); 

CREATE TABLE Customers ( 
CustomerID INT IDENTITY(1,1) PRIMARY KEY, 
CustomerName NVARCHAR(255), 
Email NVARCHAR(255), 
Phone NVARCHAR(20) ); 

CREATE TABLE Bookings ( 
BookingID INT IDENTITY(1,1) PRIMARY KEY, 
CustomerID INT, 
RouteID INT, 
BookingDate DATE, 
FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID), 
FOREIGN KEY (RouteID) REFERENCES Routes(RouteID) ); 

CREATE TABLE BookingDetails ( 
BookingDetailID INT IDENTITY(1,1) PRIMARY KEY, 
BookingID INT, 
BusID INT, 
SeatsBooked INT, 
FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID), 
FOREIGN KEY (BusID) REFERENCES Buses(BusID) ); 
GO

INSERT INTO Buses (BusNumber, BusType, TotalSeats) VALUES 
('AB123', 'Luxury', 40), 
('CD456', 'Standard', 50), 
('EF789', 'Economy', 30); 
GO

INSERT INTO Routes (Source, Destination, Distance) VALUES 
('New York', 'Boston', 215), 
('Los Angeles', 'San Francisco', 380), 
('Chicago', 'Detroit', 280); 
GO

INSERT INTO Customers (CustomerName, Email, Phone) VALUES 
('Alice Johnson', 'alice.johnson@example.com', '555-1234'), 
('Bob Smith', 'bob.smith@example.com', '555-5678'); 
GO

INSERT INTO Bookings (CustomerID, RouteID, BookingDate) VALUES 
(1, 1, '2024-08-01'), 
(2, 2, '2024-08-02'); 
GO

INSERT INTO BookingDetails (BookingID, BusID, SeatsBooked) VALUES 
(1, 1, 2), 
(2, 2, 3); 
GO

CREATE INDEX idx_customer_id ON Bookings(CustomerID); 
CREATE INDEX idx_route_id ON Bookings(RouteID); 
CREATE INDEX idx_bus_id ON BookingDetails(BusID); 
GO

SELECT b.BookingID, c.CustomerName, r.Source, r.Destination, b.BookingDate, bd.SeatsBooked, bu.BusNumber 
FROM Bookings b 
JOIN Customers c ON b.CustomerID = c.CustomerID 
JOIN Routes r ON b.RouteID = r.RouteID 
JOIN BookingDetails bd ON b.BookingID = bd.BookingID 
JOIN Buses bu ON bd.BusID = bu.BusID; 
GO

SELECT bu.BusNumber, SUM(bd.SeatsBooked) AS TotalSeatsBooked 
FROM BookingDetails bd 
JOIN Buses bu ON bd.BusID = bu.BusID 
GROUP BY bu.BusNumber; 
GO

CREATE PROCEDURE ApplyBookingReduction @CustomerID INT, @ReductionAmount DECIMAL(10, 2) 
AS 
BEGIN 
DECLARE @BookingCount INT; 
SELECT @BookingCount = COUNT(*) FROM Bookings WHERE CustomerID = @CustomerID; 
IF @BookingCount > 5 
BEGIN 
PRINT 'Applying reduction of ' + CAST(@ReductionAmount AS NVARCHAR(20)) + ' for customer with ID ' + CAST(@CustomerID AS NVARCHAR(10)); 
END 
ELSE 
BEGIN 
PRINT 'No reduction applied. Customer has less than 5 bookings.'; 
END 
END; 
GO
```
