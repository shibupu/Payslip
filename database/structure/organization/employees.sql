CREATE TABLE `employees` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `emp_no` varchar(20) NOT NULL,
  `department` tinyint(4) NOT NULL default '1' COMMENT '1 - Programming, 2 - Support, 3 - Management',
  `designation` varchar(30) NOT NULL,
  `grade` char(1) NOT NULL,
  `address` text NOT NULL,
  `phone` varchar(20) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `date_of_birth` date NOT NULL,
  `date_of_joining` date NOT NULL,
  `date_of_adding` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
