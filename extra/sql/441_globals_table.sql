CREATE TABLE IF NOT EXISTS `globals` (
  `key` varchar(16) NOT NULL,
  `data` mediumblob NOT NULL,
  `type` varchar(16) NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
