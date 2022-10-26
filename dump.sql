TRUNCATE dealer RESTART IDENTITY CASCADE;

INSERT INTO dealer(dealer_name, address, phone)
VALUES
('VROOM', '357 Philip Heights Apt. 877 New Stephanie, SD 66159', '14155552671'),
('Carvana', '13245 Sullivan Mount Suite 489 Bryanborough, ME 94533', '14187581856'),
('Absolute Auto Sales', '6280 April Burgs Suite 257 Alexandermouth, CO 20438', '14137838475'),
('Texas Direct Auto', '664 Anderson Rapid Cooperview, OK 91311', '14124753875'),
('AAA Auto Buying Service', '5090 Green Plain Dianamouth, OH 21773', '14118461957'),
('Impex Auto Sales', 'PSC 0486, Box 6020 APO AP 80027', '14105861058'),
('Auto Direct Cars & Corvettes', '86237 Martin Brooks Apt. 898 Mccarthyfurt, SC 34100', '14098479687'),
('Autoland', '564 Stephanie Crossroad West Amanda, OH 69413', '14128569374'),
('Net Direct Auto Sales', 'PSC 6244, Box 0030 APO AA 90457', '14098560283'),
('AMG Auto', '21637 Green Valleys Garystad, ND 67556', '14189580486');

INSERT INTO car(model, year, color, mileage, price, dealer_id)
VALUES
('Focus S', 2011, 'Blue Flame Metallic', 85000, 7995, 1),
('Focus S', 2015, 'Blue Flame Metallic', 45000, 18000, 2),
('Nissan Frontier SV', 2020, 'Steel', 41209, 26391, 2),
('Dodge Durango R/T', 2019, 'Black', 63947, 29987, 1),
('Dodge Durango R/T', 2019, 'Black', 33947, 49987, 7),
('Kia Telluride SX', 2018, 'Black', 15768, 47300, 1),
('Kia K900 Luxury', 2021, 'Aurora Black Pearl', 41494, 39189, 3),
('Kia K900 Luxury', 2019, 'Aurora Black Pearl', 51494, 29189, 4),
('Kia Seltos S', 2021, 'Gravity Gray', 15624, 27250, 3),
('Kia Seltos S', 2019, 'Gravity Gray', 25624, 37250, 5),
('Chevrolet Corvette Stingray', 2018, 'Blade Silver', 5938, 63990, 4),
('Chevrolet Corvette Stingray', 2019, 'Blade Silver', 15938, 73990, 6),
('Chevrolet Suburban LT', 2020,  'Silver Ice', 69358, 42932, 5),
('Chevrolet Suburban LT', 2018, 'Black', 47139, 54881, 6),
('Lexus ES 300h Base', 2020, 'Silver', 27751 , 44998, 7),
('Lexus ES 300h Base', 2021, 'Silver', 17751 , 54998, 10),
('Lexus GS 350 F Sport', 2018, 'Ultra White', 26117 , 39689, 8),
('Lexus GS 350 F Sport', 2019, 'Ultra White', 16117 , 59689, 9),
('Mazda CX-9 Touring', 2010, 'Liquid Silver Metallic', 212757 , 5950, 9),
('Mazda CX-9 Touring', 2015, 'Liquid Silver Metallic', 112757 , 15950, 7),
('Mazda CX-5 Grand Touring', 2020, 'Deep Crystal Blue Mica', 12546 , 32102, 10),
('Mazda CX-9 Grand Touring', 2016, 'Titanium Flash Mica', 83968 , 25888, 10);
