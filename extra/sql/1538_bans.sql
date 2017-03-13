CREATE TABLE IF NOT EXISTS `bans` (
  `ban_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `ban_type` tinyint(4) unsigned NOT NULL COMMENT '0 means ban_data = account_id, 1 means ban_data is playerId, 2 means ban_data = ip.',
  `ban_data` varchar(64) NOT NULL,
  `ban_reason` varchar(255) NOT NULL,
  `ban_expire` int(11) unsigned NOT NULL,
  PRIMARY KEY (`ban_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

ALTER TABLE `bans` ADD `ban_by` INT( 11 ) unsigned NULL DEFAULT NULL AFTER `ban_type` ,
ADD INDEX ( `ban_by` ) 