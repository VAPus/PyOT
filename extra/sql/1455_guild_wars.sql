CREATE TABLE IF NOT EXISTS `guilds` (
  `guild_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `world_id` tinyint(8) unsigned NOT NULL,
  `name` varchar(64) NOT NULL,
  `created` int(11) unsigned NOT NULL,
  `motd` varchar(255) NOT NULL,
  `balance` int(11) unsigned NOT NULL,
  PRIMARY KEY (`guild_id`),
  KEY `world_id` (`world_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

INSERT INTO `guilds` (`guild_id`, `world_id`, `name`, `created`, `motd`, `balance`) VALUES ('1', '0', 'Test guild', 0, 'Hello world', '123123123123'), ('2', '0', 'Test guild 2', 0, 'Hello universe', '213123123123');

CREATE TABLE IF NOT EXISTS `guild_wars` (
  `war_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `guild_id` int(11) unsigned NOT NULL,
  `guild_id2` int(11) unsigned NOT NULL,
  `started` int(11) unsigned NOT NULL,
  `duration` int(11) unsigned NOT NULL,
  `frags` int(11) unsigned NOT NULL,
  `stakes` int(11) unsigned NOT NULL,
  `status` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '0 = invitation, 1 = rejected, 2 = accepted, 3 = cancelled, 4 = active, 5 = over',
  PRIMARY KEY (`war_id`),
  KEY `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `guild_ranks` (
  `guild_id` int(11) unsigned NOT NULL,
  `rank_id` int(6) unsigned NOT NULL,
  `title` varchar(64) NOT NULL,
  `permissions` int(11) unsigned NOT NULL,
  KEY `guild_id` (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;