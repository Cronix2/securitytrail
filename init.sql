DROP DATABASE IF EXISTS subdomains;
CREATE DATABASE IF NOT EXISTS subdomains;
USE subdomains;

CREATE TABLE IF NOT EXISTS `subdomains-link-to-IP` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subdomains VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45) NOT NULL
);
