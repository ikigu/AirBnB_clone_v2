-- Sets up the db for hbnb
-- Creates the development database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Create the dev user
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grant all privileges to the dev user
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
-- Grant SELECT to the deve user in performace schema
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;