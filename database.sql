--
-- Database: `telecom_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `crm_user`
--

CREATE TABLE `crm_user` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(20) default NULL,
  `network_type` varchar(50) default NULL,
  `username` varchar(100) default NULL,
  `password` varchar(100) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `crm_user`
--

INSERT INTO `crm_user` (`id`, `name`, `email`, `mobile`, `network_type`, `username`, `password`) VALUES
(1, 'Raj', 'akil@gmail.com', '8148956634', 'Jio', 'raj', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` varchar(20) default NULL,
  `gender` varchar(10) default NULL,
  `senior_citizen` int(11) default NULL,
  `partner` int(11) default NULL,
  `dependents` int(11) default NULL,
  `tenure` int(11) default NULL,
  `contract_type` varchar(50) default NULL,
  `paperless_billing` int(11) default NULL,
  `payment_method` varchar(50) default NULL,
  `monthly_call_minutes` float default NULL,
  `monthly_data_usage_gb` float default NULL,
  `number_of_calls` int(11) default NULL,
  `international_calls` int(11) default NULL,
  `roaming_usage` float default NULL,
  `monthly_charges` float default NULL,
  `total_charges` float default NULL,
  `avg_revenue_per_user` float default NULL,
  `internet_service` varchar(50) default NULL,
  `online_security` int(11) default NULL,
  `tech_support` int(11) default NULL,
  `streaming_tv` int(11) default NULL,
  `streaming_movies` int(11) default NULL,
  `network_type` varchar(50) default NULL,
  `churn_risk` varchar(20) default NULL,
  `churn` varchar(10) default NULL,
  `segment` int(11) default NULL,
  `churn_prediction` varchar(10) default NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customers`
--


-- --------------------------------------------------------

--
-- Table structure for table `marketing_manager`
--

CREATE TABLE `marketing_manager` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(20) default NULL,
  `network_type` varchar(50) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `marketing_manager`
--

INSERT INTO `marketing_manager` (`id`, `name`, `email`, `mobile`, `network_type`, `username`, `password`) VALUES
(1, 'Raj', 'akil@gmail.com', '8148956634', 'Jio', 'raj', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `telecom_analyst`
--

CREATE TABLE `telecom_analyst` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(20) default NULL,
  `network_type` varchar(50) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `telecom_analyst`
--

INSERT INTO `telecom_analyst` (`id`, `name`, `email`, `mobile`, `network_type`, `username`, `password`) VALUES
(1, 'Raj', 'akil@gmail.com', '8148956634', 'Jio', 'raj', '1234');
