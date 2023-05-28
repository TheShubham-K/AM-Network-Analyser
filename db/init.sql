CREATE DATABASE network_data;
USE network_data;
CREATE TABLE traffic(
    id INT AUTO_INCREMENT,
    time_recorded DATETIME NOT NULL,
    ip_address VARCHAR(30) NOT NULL,
    port INT NOT NULL,
    primary key(id)
);