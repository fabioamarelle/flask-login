CREATE DATABASE IF NOT EXISTS flasklogin;

USE flasklogin;

CREATE TABLE IF NOT EXISTS cuentas (
    id INT NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(255),
    email VARCHAR(255),
    contraseña VARCHAR(255),
    PRIMARY KEY (id)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4;