CREATE DATABASE IF NOT EXISTS bnx;
USE bnx;

CREATE TABLE IF NOT EXISTS `users` (
	`id`        INT unsigned NOT NULL AUTO_INCREMENT,
	`login`     VARCHAR(32) NOT NULL,
	`password`  VARCHAR(32) NOT NULL,
    `email`     VARCHAR(32),
    `rights`    INT unsigned NOT NULL DEFAULT 1, 
	`reg_time`  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	`rec_time`  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`id`)
) ENGINE=InnoDB, DEFAULT CHARSET=utf8;


