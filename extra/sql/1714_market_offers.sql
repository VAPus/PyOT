CREATE TABLE IF NOT EXISTS `market_offers` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `world_id` tinyint(8) unsigned NOT NULL,
  `market_id` int(11) unsigned NOT NULL,
  `player_id` int(11) unsigned NOT NULL,
  `item_id` smallint(11) unsigned NOT NULL,
  `amount` smallint(11) unsigned NOT NULL,
  `created` int(11) unsigned NOT NULL,
  `price` int(11) NOT NULL,
  `anonymous` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `type` tinyint(4) unsigned NOT NULL COMMENT '0 = over, 1 = sale, 2 = 
buy',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
