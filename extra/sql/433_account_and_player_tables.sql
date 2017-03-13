CREATE TABLE IF NOT EXISTS `accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL DEFAULT '',
  `password` varchar(255) NOT NULL,
  `salt` varchar(40) NOT NULL DEFAULT '',
  `premdays` int(11) NOT NULL DEFAULT '0',
  `blocked` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'internal usage',
  `group_id` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `name`, `password`, `salt`, `premdays`, `blocked`, `group_id`) VALUES
(1, '111', '6216f8a75fd5bb3d5f22b6f9958cdede3fc086c2', '', 65535, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `players`
--

CREATE TABLE IF NOT EXISTS `players` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
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
  `sex` int(11) NOT NULL DEFAULT '0',
  `skull` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `stamina` decimal(65,0) unsigned NOT NULL DEFAULT '151200000' COMMENT 'stored in miliseconds',
  `direction` tinyint(2) unsigned NOT NULL DEFAULT '2',
  `marriage` int(10) unsigned NOT NULL DEFAULT '0',
  `skills` blob,
  `conditions` blob,
  `storage` mediumblob,
  `depot` mediumblob,
  `inventory` mediumblob,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `account_id` (`account_id`),
  KEY `group_id` (`group_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `players`
--

INSERT INTO `players` (`id`, `name`, `world_id`, `group_id`, `account_id`, `vocation`, `health`, `experience`, `lookbody`, `lookfeet`, `lookhead`, `looklegs`, `looktype`, `lookaddons`, `lookmount`, `mana`, `manaspent`, `soul`, `town_id`, `posx`, `posy`, `posz`, `sex`, `skull`, `stamina`, `direction`, `marriage`, `skills`, `conditions`, `storage`) VALUES
(2, 'Test', 0, 6, 1, 1, 15000, 717601, 68, 76, 78, 39, 302, 0, 0, 60000, 60000, 100, 1, 1000, 1000, 7, 1, 0, 151200000, 2, 0, NULL, NULL, NULL);

