CREATE TABLE IF NOT EXISTS `pvp_deaths` (
  `death_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `killer_id` int(11) unsigned NOT NULL,
  `victim_id` int(11) unsigned NOT NULL,
  `unjust` tinyint(1) NOT NULL,
  `time` int(11) unsigned NOT NULL,
  `revenged` tinyint(1) NOT NULL DEFAULT '0',
  `war_id` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`death_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;