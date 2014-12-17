CREATE TABLE IF NOT EXISTS `permissions` (
  `ID`  INTEGER PRIMARY KEY,
  `Level` int(10) NOT NULL,
  `Name` varchar(25) NOT NULL,
  `Values` text NOT NULL,
  `PermittedForums` varchar(150) NOT NULL DEFAULT '',
  `Secondary` tinyint(4) NOT NULL DEFAULT '0'
);

CREATE TABLE IF NOT EXISTS `users_main` (
  `ID`  INTEGER PRIMARY KEY,
  `Username` varchar(20) NOT NULL,
  `IRCKey` char(32) DEFAULT NULL,
  `IP` varchar(15) NOT NULL DEFAULT '0.0.0.0',
  `Class` tinyint(2) NOT NULL DEFAULT '5',
  `Enabled` tinyint(2) NOT NULL DEFAULT '0',
  `Paranoia` text,
  `Visible` tinyint(2) NOT NULL DEFAULT '1',
  `PermissionID` int(10) NOT NULL,
  FOREIGN KEY(`PermissionID`) REFERENCES `permissions`(`ID`)
)