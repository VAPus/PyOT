CREATE TABLE IF NOT EXISTS `accounts` (
`id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL DEFAULT '',
  `password` varchar(255) NOT NULL,
  `salt` varchar(40) NOT NULL DEFAULT '',
  `premdays` int(11) NOT NULL DEFAULT '0',
  `language` char(5) NOT NULL DEFAULT 'en_EN',
  `blocked` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'internal usage',
  `group_id` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

CREATE TABLE IF NOT EXISTS `bans` (
`ban_id` bigint(20) unsigned NOT NULL,
  `ban_type` tinyint(4) unsigned NOT NULL COMMENT '0 means ban_data = account_id, 1 means ban_data is playerId, 2 means ban_data = ip.',
  `ban_by` int(11) unsigned DEFAULT NULL,
  `ban_data` varchar(64) NOT NULL,
  `ban_reason` varchar(255) NOT NULL,
  `ban_expire` int(11) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `globals` (
  `world_id` tinyint(8) NOT NULL DEFAULT '0',
  `key` varchar(16) NOT NULL,
  `data` mediumblob NOT NULL,
  `type` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `groups` (
  `group_id` int(11) unsigned NOT NULL,
  `group_name` varchar(48) NOT NULL,
  `group_flags` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `groups` VALUES
(1, 'Player', '["SAVESELF", "HOUSE", "PREMIUM", "SPELLS", "SPEAK", "MOVE_ITEMS", "LOOT", "ATTACK"]'),
(2, 'Tutor', '["SAVESELF", "HOUSE", "PREMIUM", "SPELLS", "SPEAK", "MOVE_ITEMS", "LOOT", "ATTACK"]'),
(3, 'Community Manager', '["MUTE", "TELEPORT", "IMMUNE", "NO_EXHAUST", "IGNORED_BY_CREATURES", "TALK_ORANGE", "SPEED", "SAVESELF", "SPEAK", "MOVE_ITEMS"]'),
(4, 'Gamemaster', '["CREATEITEM", "TELEPORT", "SETHOUSEOWNER", "SAVEALL", "SAVESELF", "SPAWN", "RAID", "HOUSE", "KICK", "BAN", "MUTE", "PREMIUM", "SPELLS", "SPEAK", "SPEED", "MOVE_ITEMS", "LOOT", "INVISIBLE", "INFINATE_SOUL", "INFINATE_MANA", "INFINATE_HEALTH", "INFINATE_STAMINA", "ATTACK", "IGNORED_BY_CREATURES", "TALK_ORANGE", "TALK_RED", "IMMUNE", "NO_EXHAUST"]'),
(5, 'God', '["CREATEITEM", "TELEPORT", "SETHOUSEOWNER", "SAVEALL", "SAVESELF", "SPAWN", "RAID", "HOUSE", "MANAGESERVER", "MODIFYMAP", "KICK", "RELOAD", "BAN", "MUTE", "DEVELOPER", "PREMIUM", "SPELLS", "SPEAK", "SPEED", "MOVE_ITEMS", "LOOT", "INVISIBLE", "INFINATE_SOUL", "INFINATE_MANA", "INFINATE_HEALTH", "INFINATE_STAMINA", "ATTACK", "IGNORED_BY_CREATURES", "TALK_ORANGE", "TALK_RED", "IMMUNE", "NO_EXHAUST"]'),
(6, 'Admin', '["CREATEITEM", "TELEPORT", "SETHOUSEOWNER", "SAVEALL", "SAVESELF", "SPAWN", "RAID", "HOUSE", "MANAGESERVER", "MODIFYMAP", "KICK", "RELOAD", "BAN", "MUTE", "DEVELOPER", "PREMIUM", "SPELLS", "SPEAK", "SPEED", "MOVE_ITEMS", "LOOT", "INVISIBLE", "INFINATE_SOUL", "INFINATE_MANA", "INFINATE_HEALTH", "INFINATE_STAMINA", "ATTACK", "IGNORED_BY_CREATURES", "TALK_ORANGE", "TALK_RED", "IMMUNE", "NO_EXHAUST"]');

CREATE TABLE IF NOT EXISTS `guilds` (
`guild_id` int(11) unsigned NOT NULL,
  `world_id` tinyint(8) unsigned NOT NULL,
  `name` varchar(64) NOT NULL,
  `created` int(11) unsigned NOT NULL,
  `motd` varchar(255) NOT NULL,
  `balance` int(11) unsigned NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

INSERT INTO `guilds` VALUES
(1, 0, 'Test guild', 0, 'Hello world', 4294967295),
(2, 0, 'Test guild 2', 0, 'Hello universe', 4294967295);

CREATE TABLE IF NOT EXISTS `guild_invites` (
  `player_id` int(10) unsigned NOT NULL DEFAULT '0',
  `guild_id` int(10) unsigned NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `guild_ranks` (
  `guild_id` int(11) unsigned NOT NULL,
  `rank_id` int(6) unsigned NOT NULL,
  `title` varchar(64) NOT NULL,
  `permissions` int(11) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `guild_wars` (
`war_id` int(11) unsigned NOT NULL,
  `guild_id` int(11) unsigned NOT NULL,
  `guild_id2` int(11) unsigned NOT NULL,
  `started` int(11) unsigned NOT NULL,
  `duration` int(11) unsigned NOT NULL,
  `frags` int(11) unsigned NOT NULL,
  `stakes` int(11) unsigned NOT NULL,
  `status` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '0 = invitation, 1 = rejected, 2 = accepted, 3 = cancelled, 4 = active, 5 = over'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `houses` (
`id` int(11) unsigned NOT NULL,
  `world_id` tinyint(8) NOT NULL,
  `owner` int(11) unsigned NOT NULL DEFAULT '0',
  `guild` int(8) unsigned NOT NULL DEFAULT '0',
  `paid` int(11) unsigned NOT NULL DEFAULT '0',
  `name` varchar(64) NOT NULL,
  `town` int(8) unsigned NOT NULL DEFAULT '0',
  `size` int(8) unsigned NOT NULL,
  `rent` int(11) unsigned NOT NULL,
  `data` mediumblob,
  `price` int(11) unsigned NOT NULL DEFAULT '0',
  `for_sale` tinyint(1) unsigned NOT NULL DEFAULT '0'
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=30 ;


CREATE TABLE IF NOT EXISTS `market_history` (
`id` int(11) unsigned NOT NULL,
  `offer_id` int(11) unsigned NOT NULL,
  `player_id` int(11) unsigned NOT NULL,
  `amount` int(11) unsigned NOT NULL,
  `time` int(11) unsigned NOT NULL,
  `type` tinyint(2) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `market_offers` (
`id` int(11) unsigned NOT NULL,
  `world_id` tinyint(8) unsigned NOT NULL,
  `market_id` int(11) unsigned NOT NULL,
  `player_id` int(11) unsigned NOT NULL,
  `item_id` smallint(11) unsigned NOT NULL,
  `amount` smallint(11) unsigned NOT NULL,
  `created` int(11) unsigned NOT NULL,
  `price` int(11) NOT NULL,
  `anonymous` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `type` tinyint(4) unsigned NOT NULL COMMENT '0 = over, 1 = sale, 2 =\nbuy'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `players` (
`id` int(11) unsigned NOT NULL,
  `name` varchar(255) NOT NULL,
  `world_id` tinyint(8) unsigned NOT NULL DEFAULT '0',
  `group_id` int(11) NOT NULL DEFAULT '1',
  `account_id` int(11) NOT NULL DEFAULT '0',
  `vocation` tinyint(8) unsigned NOT NULL DEFAULT '0',
  `health` decimal(65,0) unsigned NOT NULL DEFAULT '150',
  `experience` decimal(65,0) unsigned NOT NULL DEFAULT '0',
  `lookbody` tinyint(11) unsigned NOT NULL DEFAULT '0',
  `lookfeet` tinyint(11) unsigned NOT NULL DEFAULT '0',
  `lookhead` tinyint(11) unsigned NOT NULL DEFAULT '0',
  `looklegs` tinyint(11) unsigned NOT NULL DEFAULT '0',
  `looktype` smallint(11) unsigned NOT NULL DEFAULT '136',
  `lookaddons` tinyint(11) unsigned NOT NULL DEFAULT '0',
  `lookmount` smallint(11) unsigned NOT NULL DEFAULT '0',
  `mana` decimal(65,0) unsigned NOT NULL DEFAULT '0',
  `manaspent` decimal(65,0) unsigned NOT NULL DEFAULT '0',
  `soul` int(10) unsigned NOT NULL DEFAULT '0',
  `town_id` int(11) NOT NULL DEFAULT '0',
  `posx` int(11) NOT NULL DEFAULT '0',
  `posy` int(11) NOT NULL DEFAULT '0',
  `posz` int(11) NOT NULL DEFAULT '0',
  `instanceId` mediumint(5) DEFAULT NULL,
  `sex` int(11) NOT NULL DEFAULT '0',
  `skull` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `stamina` decimal(65,0) unsigned NOT NULL DEFAULT '151200000' COMMENT 'stored in miliseconds',
  `marriage` int(10) unsigned NOT NULL DEFAULT '0',
  `lastlogin` int(11) unsigned NOT NULL DEFAULT '0',
  `online` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `conditions` blob,
  `balance` decimal(65,0) unsigned NOT NULL DEFAULT '0',
  `storage` mediumblob,
  `depot` mediumblob,
  `inventory` mediumblob
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

INSERT INTO `players` VALUES
(2, 'Test', 0, 6, 1, 1, 610, 13215603, 68, 76, 78, 39, 302, 0, 0, 2615, 42315, 100, 1, 1031, 1022, 7, 0, 1, 0, 114120000, 0, 1413678571, 0, NULL, 0, NULL, NULL, NULL);

CREATE TABLE IF NOT EXISTS `player_guild` (
  `player_id` int(11) unsigned NOT NULL,
  `guild_id` int(11) unsigned NOT NULL,
  `guild_rank` int(6) unsigned NOT NULL DEFAULT '0',
  `guild_title` varchar(255) NOT NULL DEFAULT '',
  `joined` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `player_skills` (
  `player_id` int(11) unsigned NOT NULL,
  `fist` int(11) unsigned NOT NULL DEFAULT '10',
  `fist_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `sword` int(11) unsigned NOT NULL DEFAULT '10',
  `sword_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `club` int(11) unsigned NOT NULL DEFAULT '10',
  `club_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `axe` int(11) unsigned NOT NULL DEFAULT '10',
  `axe_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `distance` int(11) unsigned NOT NULL DEFAULT '10',
  `distance_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `shield` int(11) unsigned NOT NULL DEFAULT '10',
  `shield_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `fishing` int(11) unsigned NOT NULL DEFAULT '0',
  `fishing_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `custom` tinytext COMMENT 'Might be NULL, JSON dict ID -> skilltries'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `player_skills` VALUES
(2, 12, 59, 11, 0, 11, 0, 11, 0, 11, 0, 11, 0, 10, 0, NULL);

CREATE TABLE IF NOT EXISTS `pvp_deaths` (
`death_id` int(11) unsigned NOT NULL,
  `killer_id` int(11) unsigned NOT NULL,
  `victim_id` int(11) unsigned NOT NULL,
  `unjust` tinyint(1) NOT NULL,
  `time` int(11) unsigned NOT NULL,
  `revenged` tinyint(1) NOT NULL DEFAULT '0',
  `war_id` int(11) unsigned NOT NULL DEFAULT '0'
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=9 ;

INSERT INTO `pvp_deaths` VALUES
(1, 219319406, 1375687025, 1, 1413075720, 0, 0),
(2, 219319406, 669146212, 1, 1413075720, 0, 0),
(3, 219319406, 1074462969, 1, 1413075720, 0, 0),
(4, 219319406, 1803251276, 1, 1413075720, 0, 0),
(5, 219319406, 2056656480, 1, 1413075720, 0, 0),
(6, 219319406, 194319162, 1, 1413075720, 0, 0),
(7, 219319406, 191404223, 1, 1413075720, 0, 0),
(8, 219319406, 2050224719, 1, 1413075720, 0, 0);


ALTER TABLE `accounts`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name` (`name`);

ALTER TABLE `bans`
 ADD PRIMARY KEY (`ban_id`), ADD KEY `ban_by` (`ban_by`);

ALTER TABLE `globals`
 ADD PRIMARY KEY (`key`);

ALTER TABLE `groups`
 ADD PRIMARY KEY (`group_id`), ADD KEY `group_name` (`group_name`);

ALTER TABLE `guilds`
 ADD PRIMARY KEY (`guild_id`), ADD KEY `world_id` (`world_id`);

ALTER TABLE `guild_ranks`
 ADD KEY `guild_id` (`guild_id`);

ALTER TABLE `guild_wars`
 ADD PRIMARY KEY (`war_id`), ADD KEY `status` (`status`);

ALTER TABLE `houses`
 ADD PRIMARY KEY (`id`), ADD KEY `world_id` (`world_id`);

ALTER TABLE `market_history`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `market_offers`
 ADD PRIMARY KEY (`id`);

ALTER TABLE `players`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name` (`name`), ADD KEY `account_id` (`account_id`), ADD KEY `group_id` (`group_id`);

ALTER TABLE `player_guild`
 ADD KEY `guild_id` (`guild_id`);

ALTER TABLE `player_skills`
 ADD PRIMARY KEY (`player_id`);

ALTER TABLE `pvp_deaths`
 ADD PRIMARY KEY (`death_id`);


ALTER TABLE `accounts`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
ALTER TABLE `bans`
MODIFY `ban_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE `guilds`
MODIFY `guild_id` int(11) unsigned NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
ALTER TABLE `guild_wars`
MODIFY `war_id` int(11) unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE `houses`
MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=30;
ALTER TABLE `market_history`
MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE `market_offers`
MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE `players`
MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
ALTER TABLE `pvp_deaths`
MODIFY `death_id` int(11) unsigned NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=9;
