
CREATE TABLE IF NOT EXISTS `player_skills` (
  `player_id` int(11) unsigned NOT NULL,
  `fist` int(11) unsigned NOT NULL DEFAULT '10',
  `fist_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `sword` int(11) unsigned NOT NULL DEFAULT '10',
  `sword_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `axe` int(11) unsigned NOT NULL DEFAULT '10',
  `axe_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `distance` int(11) unsigned NOT NULL DEFAULT '10',
  `distance_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `shield` int(11) unsigned NOT NULL DEFAULT '10',
  `shield_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `fishing` int(11) unsigned NOT NULL DEFAULT '0',
  `fishing_tries` int(11) unsigned NOT NULL DEFAULT '0',
  `custom` tinytext COMMENT 'Might be NULL, JSON dict ID -> skilltries',
  PRIMARY KEY (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dataark for tabell `player_skills`
--

INSERT INTO `player_skills` (`player_id`, `fist`, `fist_tries`, `sword`, `sword_tries`, `axe`, `axe_tries`, `distance`, `distance_tries`, `shield`, `shield_tries`, `fishing`, `fishing_tries`, `custom`) VALUES
(2, 10, 0, 10, 0, 10, 0, 10, 0, 10, 0, 0, 0, NULL);

ALTER TABLE `players` DROP `skills` ;

ALTER TABLE `player_skills` ADD `club` INT( 11 ) UNSIGNED NOT NULL DEFAULT '10' AFTER `sword_tries` ,
ADD `club_tries` INT( 11 ) UNSIGNED NOT NULL DEFAULT '0' AFTER `club` ;