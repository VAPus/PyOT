CREATE TABLE IF NOT EXISTS `market_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `offer_id` int(11) unsigned NOT NULL,
  `player_id` int(11) unsigned NOT NULL,
  `amount` int(11) unsigned NOT NULL,
  `time` int(11) unsigned NOT NULL,
  `type` tinyint(2) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
