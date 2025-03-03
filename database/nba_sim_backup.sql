/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.6.2-MariaDB, for osx10.19 (arm64)
--
-- Host: localhost    Database: NBA_sim
-- ------------------------------------------------------
-- Server version	11.6.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `Brukere`
--

DROP TABLE IF EXISTS `Brukere`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Brukere` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `brukernavn` varchar(50) DEFAULT NULL,
  `passord` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Brukere`
--

LOCK TABLES `Brukere` WRITE;
/*!40000 ALTER TABLE `Brukere` DISABLE KEYS */;
INSERT INTO `Brukere` VALUES
(1,'Jojo','$2b$12$Wd0vmog3it6IRLMLK8omeebiAwaLg5IjMI.bdWjDMD6v6H8i7qVO.'),
(2,'Henr1k','$2b$12$cykLouyq2AENA5OadPmZSegZ3GUlidMNc3rjjpH6cslFfFJaytAkO');
/*!40000 ALTER TABLE `Brukere` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Lederbord`
--

DROP TABLE IF EXISTS `Lederbord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Lederbord` (
  `user_id` int(11) NOT NULL,
  `antall_seire` int(11) DEFAULT 0,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Lederbord`
--

LOCK TABLES `Lederbord` WRITE;
/*!40000 ALTER TABLE `Lederbord` DISABLE KEYS */;
INSERT INTO `Lederbord` VALUES
(1,0),
(2,0);
/*!40000 ALTER TABLE `Lederbord` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-03-03 11:03:31
