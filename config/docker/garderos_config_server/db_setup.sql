USE mysql;
DROP USER 'garderos'@'%';
FLUSH PRIVILEGES;
CREATE USER 'garderos'@'%' IDENTIFIED BY 'garderos';
GRANT ALL PRIVILEGES ON config.* TO 'garderos'@'%';
GRANT ALL PRIVILEGES ON logdata.* TO 'garderos'@'%';
FLUSH PRIVILEGES;
QUIT;