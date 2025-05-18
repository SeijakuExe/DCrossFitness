CREATE DATABASE  IF NOT EXISTS `gymdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `gymdb`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: gymdb
-- ------------------------------------------------------
-- Server version	8.4.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `idAccount` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Phone` varchar(45) NOT NULL,
  `Username` varchar(45) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Gender` enum('Male','Female') DEFAULT NULL,
  `Birth` date DEFAULT NULL,
  `Access` enum('Customer','Receptionist','Trainer','Warranty','Manager') NOT NULL DEFAULT 'Customer',
  `idClass` int DEFAULT NULL,
  PRIMARY KEY (`idAccount`),
  UNIQUE KEY `Phone_UNIQUE` (`Phone`),
  UNIQUE KEY `Username_UNIQUE` (`Username`),
  KEY `idClasses_idx` (`idClass`),
  CONSTRAINT `ClassMember` FOREIGN KEY (`idClass`) REFERENCES `classes` (`idClass`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,'Admin','2188412312','Admin','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Male','1999-01-01','Manager',NULL),(3,'Jake','1323524563','Receptionist1','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Male','1990-01-22','Receptionist',NULL),(6,'Jane Doe','0123456789','Jane','scrypt:32768:8:1$rxbkKE4H3RrTeyok$dbe17989aa2a7afba5bcb3c8cf4179322778d0cb42f3118f91d05a9d8933062ab054438e683c90a03dce92afa4d0d81111d2cb3d86bdf4195bdfab7b52a95da8','Female','1990-01-22','Customer',NULL),(8,'Miya','0125443789','Miya','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Female','1999-01-01','Customer',1),(9,'Ben','0143456532','Ben','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Male','1976-01-01','Customer',1),(10,'Belle','0987654321','Phaethon','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Female','1995-05-15','Customer',1),(12,'test2','12455134235',NULL,'','Female','2025-01-09','Customer',1),(13,'Sana','123','pwtest','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Female','2025-02-26','Customer',1),(17,'San','754236923',NULL,'','Male','2025-04-07','Customer',1),(18,'Hugo','24562413','Trainer1','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Male','1999-01-01','Trainer',NULL),(19,'Andrew','24562412','Trainer2','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Male','1999-01-01','Trainer',NULL),(20,'Unchain','765439','UC','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Male','2025-04-01','Customer',NULL),(21,'Chain','5134574','CN','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Male','2025-04-03','Customer',1),(22,'Tama','84538321','Tamaaaa','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Female','2012-05-15','Customer',1),(23,'Jaykki','111111110000',NULL,NULL,'Male','2025-04-01','Customer',1),(26,'Siwoo','854272','Siwoo25','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Male','2002-02-13','Trainer',NULL),(27,'senti','12527432','senti','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Male','2021-01-08','Customer',NULL),(28,'un123','10000002','HashTest','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Male','2025-05-06','Customer',NULL),(29,'Micheal','031099197','Receptionist2','scrypt:32768:8:1$yM7VotiAEAdzOJnn$7df334a533c7493fc47f9827f2052d858437a490fe3a289c1b4aa0a1f7e7ee58df3ca00ccb9ce20f38afe969779bf7cbb90a8e882b2a2df995406ba3a29e61ec','Male','1999-11-11','Receptionist',NULL),(30,'aed','9765438765',NULL,NULL,'Male','2025-04-27','Customer',NULL);
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `areas`
--

DROP TABLE IF EXISTS `areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `areas` (
  `idArea` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Description` varchar(255) NOT NULL,
  `Note` varchar(255) NOT NULL,
  PRIMARY KEY (`idArea`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `areas`
--

LOCK TABLES `areas` WRITE;
/*!40000 ALTER TABLE `areas` DISABLE KEYS */;
INSERT INTO `areas` VALUES (1,'Chest','Focus on chest muscle workouts.','Increase weight or repetitions for intensity.'),(2,'Legs','Strengthen lower body with leg exercises.','Adjust seat height or stance for proper form.'),(3,'Back','Develop back muscles and improve posture.','Keep your back straight and avoid overextending.'),(4,'Shoulders','Improve shoulder mobility and strength.','Use lighter weights if experiencing shoulder pain.'),(5,'Arms','Enhance biceps and triceps strength.','Lower weight if struggling to maintain form.'),(6,'Core','Strengthen abdominal and core stability.','Reduce repetitions if new to core exercises.');
/*!40000 ALTER TABLE `areas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classes` (
  `idClass` int NOT NULL AUTO_INCREMENT,
  `idTrainer` int NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `idArea` int DEFAULT NULL,
  PRIMARY KEY (`idClass`),
  UNIQUE KEY `idTrainer_UNIQUE` (`idTrainer`),
  KEY `idTrainer_idx` (`idTrainer`),
  KEY `idArea_idx` (`idArea`),
  CONSTRAINT `idArea` FOREIGN KEY (`idArea`) REFERENCES `areas` (`idArea`),
  CONSTRAINT `idTrainer` FOREIGN KEY (`idTrainer`) REFERENCES `accounts` (`idAccount`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES (1,18,'Class 1',NULL),(2,19,'Class 2',NULL);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment` (
  `idEquipment` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(156) NOT NULL,
  `Category` varchar(45) NOT NULL,
  `Brand` varchar(45) NOT NULL,
  `PurchaseDate` date NOT NULL,
  `Quantity` int NOT NULL DEFAULT '1',
  `QuantityAvailable` int NOT NULL DEFAULT '1',
  `Image` varchar(255) DEFAULT NULL,
  `Size` varchar(45) NOT NULL,
  `Weight` varchar(45) NOT NULL,
  PRIMARY KEY (`idEquipment`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment`
--

LOCK TABLES `equipment` WRITE;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
INSERT INTO `equipment` VALUES (1,'TZ-4009 5 Multi-Station','Cable Machine','TZ FITNESS','2025-01-01',2,1,'https://tzfit.com/wp-content/uploads/2025/04/TZ-4009-Gym-Equipment-Multi-Station-Commercial-Multi-Station-Gym-5-Multi-Station.jpg','4900x3450x2400mm','894kg'),(2,'GC-5066 Hack Squat','Rack','TZ FITNESS','2025-01-01',4,4,'https://product.hstatic.net/200000273125/product/3c94d8c8473b8dd8.jpg_20231206100007_690x390_5ea51edf361c4de39e78fa651dd80a49.jpeg','2235*1500*1705 mm','220 kg'),(3,'Gc-5017 Smith Machine Multi Functional Machine Squat Rack','Smith Machine','TZ FITNESS','2025-01-01',1,1,'https://product.hstatic.net/200000273125/product/z6077554629031_df225eb05c50c9421546ff87af0e935f_bb9e72d17f0a4113820c8401360ec331_1024x1024.jpg','2000*1420*2175 mm','265 kg'),(4,'FM-1009 Smith Machine','Smith Machine','REALLEADER USA','2025-01-01',2,2,'https://product.hstatic.net/200000273125/product/0xaf_82ab8d9aa3b14d3ea83e3ace00ace437_71ec0d4b0c6949b3a47b5a5afdbc4ca2_cafa7f99087448d6bdf6384c9e782124_1024x1024.jpg','2310x1300x2400 mm','239 kg'),(5,'LD-2001 Leg Extenxion','Rack','REALLEADER USA','2025-01-01',2,2,'https://product.hstatic.net/200000273125/product/ed64_aa1b695ff2634197b40d84ce316909a1_dfb51d549b2f4f3798871d7a59ded4b8_92191573897d48f195b2fe43476a23fe_1024x1024.jpg','1550*1900*1200 mm','210 kg'),(6,'FW-1004 Seated Arm Curl','Rack','REALLEADER USA','2025-01-01',3,2,'https://product.hstatic.net/200000273125/product/0xaf_83393b92c1bc402e8e45c28fb0ca8c22_717ce472e5a04c38ab5d0042f9ece322_58cee3c5d0be4b3e80bd906e823efa1d_1024x1024.jpg','1440x800x1100 mm','98 kg'),(7,'FW-1009 Flat Bench','Bench','REALLEADER USA','2025-01-01',6,6,'https://product.hstatic.net/200000273125/product/0xaf_a966af1e5559427292519718f323e148_ecf18718ba9e487fb08028f6563cae4c_2d2e314ef73a482f98f429ad0c88470d_1024x1024.jpg','1550x570x450 mm','46 kg'),(8,'TT-X2commercial treadmill','Treadmill','BRIGHTWAY FITNESS','2025-01-01',2,2,'https://product.hstatic.net/200000273125/product/604f22f06745c_d190b62046214565ac8d66542518c596.jpg','1440x800x1100 mm','310 kg'),(9,' PU MDBuddy MD1039A','Weight Plate','MD BUDDY','2025-01-01',20,20,'https://product.hstatic.net/200000273125/product/ta-dia-boc-pu-mdbuddy-md1039a-1-510x510_5d8c47aabdc64a31a524360102c92ab5.jpg','~','1,25kg, 2,5kg, 5kg, 10kg, 15kg, 20kg, 25kg');
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`Admin`@`%`*/ /*!50003 TRIGGER `equipment_BEFORE_INSERT` BEFORE INSERT ON `equipment` FOR EACH ROW BEGIN
	SET NEW.QuantityAvailable = NEW.Quantity;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `exercises`
--

DROP TABLE IF EXISTS `exercises`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exercises` (
  `idExercise` int NOT NULL AUTO_INCREMENT,
  `idArea` int NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Repetition` varchar(45) NOT NULL,
  PRIMARY KEY (`idExercise`),
  KEY `list_idx` (`idArea`),
  CONSTRAINT `area_fk` FOREIGN KEY (`idArea`) REFERENCES `areas` (`idArea`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercises`
--

LOCK TABLES `exercises` WRITE;
/*!40000 ALTER TABLE `exercises` DISABLE KEYS */;
INSERT INTO `exercises` VALUES (1,1,'Bench Press','4 sets x 10 reps'),(2,1,'Incline Dumbbell Press','3 sets x 12 reps'),(3,1,'Chest Fly','3 sets x 15 reps'),(4,1,'Push-ups','4 sets x 15 reps'),(5,2,'Squats','5 sets x 12 reps'),(6,2,'Lunges','4 sets x 10 reps per leg'),(7,2,'Leg Press','3 sets x 12 reps'),(8,2,'Calf Raises','4 sets x 15 reps'),(9,3,'Deadlift','5 sets x 8 reps'),(10,3,'Pull-ups','4 sets x 10 reps'),(11,3,'Bent-over Rows','3 sets x 12 reps'),(12,3,'Lat Pulldown','3 sets x 15 reps'),(13,4,'Overhead Press','4 sets x 10 reps'),(14,4,'Lateral Raises','3 sets x 12 reps'),(15,4,'Front Raises','3 sets x 12 reps'),(16,5,'Bicep Curls','4 sets x 12 reps'),(17,5,'Tricep Dips','3 sets x 10 reps'),(18,5,'Hammer Curls','3 sets x 12 reps'),(19,5,'Skull Crushers','3 sets x 12 reps'),(20,6,'Plank','3 sets x 60 seconds'),(21,6,'Sit-ups','4 sets x 20 reps'),(22,6,'Russian Twists','3 sets x 15 reps per side'),(23,6,'Leg Raises','3 sets x 12 reps');
/*!40000 ALTER TABLE `exercises` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membership`
--

DROP TABLE IF EXISTS `membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `membership` (
  `idMembership` int NOT NULL AUTO_INCREMENT,
  `idAccount` int NOT NULL,
  `MembershipType` enum('Basic','Premium') NOT NULL,
  `StartDate` date NOT NULL,
  `EndDate` date DEFAULT NULL,
  `Status` enum('Active','Expired') NOT NULL,
  PRIMARY KEY (`idMembership`),
  KEY `membership_ibfk_1` (`idAccount`),
  CONSTRAINT `membership_ibfk_1` FOREIGN KEY (`idAccount`) REFERENCES `accounts` (`idAccount`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membership`
--

LOCK TABLES `membership` WRITE;
/*!40000 ALTER TABLE `membership` DISABLE KEYS */;
INSERT INTO `membership` VALUES (3,12,'Basic','2025-01-11','2025-04-11','Expired'),(5,9,'Premium','2025-01-11','2026-01-11','Active'),(9,10,'Basic','2024-01-01','2024-06-01','Expired'),(10,10,'Premium','2025-01-13','2025-04-13','Expired'),(19,17,'Basic','2025-04-09','2025-05-09','Expired'),(23,8,'Basic','2025-04-13','2025-05-13','Expired'),(24,8,'Basic','2025-05-13','2025-06-12','Active'),(27,22,'Basic','2025-04-17','2025-05-04','Expired'),(31,6,'Premium','2026-06-02','2026-07-02','Active'),(32,22,'Premium','2025-05-17','2026-05-12','Active'),(33,10,'Premium','2025-04-19','2025-10-16','Active'),(34,12,'Basic','2025-04-19','2026-04-14','Active'),(35,27,'Basic','2025-04-19','2025-05-04','Expired'),(36,6,'Basic','2026-07-02','2026-08-01','Active'),(37,6,'Premium','2026-08-01','2026-08-31','Active'),(38,6,'Premium','2025-02-01','2025-08-31','Active'),(39,6,'Basic','2026-08-31','2026-09-30','Active'),(40,6,'Basic','2026-09-30','2026-10-30','Active');
/*!40000 ALTER TABLE `membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `idNotification` int NOT NULL AUTO_INCREMENT,
  `Time` datetime NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `Status` enum('Uncheck','Checked') NOT NULL DEFAULT 'Uncheck',
  `idAccount` int NOT NULL,
  PRIMARY KEY (`idNotification`),
  KEY `idAccount_idx` (`idAccount`),
  CONSTRAINT `idAccount` FOREIGN KEY (`idAccount`) REFERENCES `accounts` (`idAccount`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,'2025-01-01 00:00:00','Test','Checked',6),(2,'2025-02-02 00:00:00','test2','Checked',6),(3,'2025-04-15 02:17:29','Customer Jane Doe requested membership card print.','Checked',3),(4,'2025-04-15 02:21:19','Customer Jane Doe with ID 6 requested membership card print.','Checked',3),(5,'2025-04-15 02:28:59','Customer Jane Doe, ID: 6 requested membership card print.','Checked',3),(6,'2025-04-16 01:20:51','You were marked absent today','Checked',6),(7,'2025-04-16 01:20:51','You were marked absent today','Uncheck',8),(8,'2025-04-16 01:20:51','You were marked absent today','Uncheck',9),(9,'2025-04-16 01:20:51','You were marked absent today','Uncheck',10),(10,'2025-05-02 21:53:57','Your membership will expire in 2 day(s). Please renew soon to avoid interruption.','Checked',27),(11,'2025-05-07 14:34:27','Your membership will expire in 1 day(s). Please renew soon to avoid interruption.','Checked',6),(12,'2025-05-08 14:27:27','Your membership will expire in 0 day(s). Please renew soon to avoid interruption.','Checked',6),(13,'2025-05-11 01:05:30','Customer Jane Doe, ID: 6 requested membership card print.','Checked',3),(14,'2025-05-13 23:18:20','Customer un123, ID: 28 requested membership card print.','Checked',3);
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule` (
  `idSchedule` int NOT NULL AUTO_INCREMENT,
  `Day` enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') NOT NULL,
  `Start` time NOT NULL,
  `End` time NOT NULL,
  `idStaff` int DEFAULT NULL,
  PRIMARY KEY (`idSchedule`),
  KEY `idStaff_idx` (`idStaff`),
  CONSTRAINT `idStaff` FOREIGN KEY (`idStaff`) REFERENCES `accounts` (`idAccount`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule`
--

LOCK TABLES `schedule` WRITE;
/*!40000 ALTER TABLE `schedule` DISABLE KEYS */;
INSERT INTO `schedule` VALUES (2,'Wednesday','07:00:00','11:00:00',3),(3,'Saturday','07:00:00','11:00:00',3),(4,'Tuesday','08:00:00','11:00:00',18),(5,'Friday','14:00:00','17:00:00',18),(7,'Friday','13:00:00','16:00:00',3),(8,'Sunday','13:00:00','16:00:00',3),(9,'Thursday','14:00:00','18:00:00',3),(10,'Tuesday','10:00:00','14:00:00',19),(12,'Saturday','16:00:00','19:00:00',29),(13,'Sunday','08:00:00','00:00:00',29),(14,'Monday','00:00:00','16:00:00',29),(15,'Tuesday','00:00:00','16:00:00',29);
/*!40000 ALTER TABLE `schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `idTransaction` int NOT NULL AUTO_INCREMENT,
  `idAccount` int NOT NULL,
  `TransactionDate` datetime NOT NULL,
  `Amount` decimal(10,2) NOT NULL,
  `PaymentMethod` enum('PayPal','Mobile Banking','Cash') NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `idReceiver` int DEFAULT NULL,
  PRIMARY KEY (`idTransaction`),
  KEY `transactions_ibfk_1` (`idAccount`) /*!80000 INVISIBLE */,
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`idAccount`) REFERENCES `accounts` (`idAccount`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,12,'2025-01-11 14:04:31',540000.00,'Mobile Banking','',1),(3,9,'2025-01-11 16:59:13',2520000.00,'Mobile Banking','',1),(5,10,'2025-01-13 16:15:18',810000.00,'Cash','',1),(9,6,'2025-04-08 18:45:14',200000.00,'Cash','Basic Membership for 1 months',1),(11,6,'2025-04-08 19:41:49',200000.00,'Cash','Basic Membership for 1 months',1),(12,17,'2025-04-09 14:38:57',200000.00,'Cash','Basic Membership for 1 months',1),(13,6,'2025-04-12 15:24:24',300000.00,'Cash','Premium Membership for 1 months',1),(14,8,'2025-04-13 02:02:07',200000.00,'Cash','Basic Membership for 1 months',1),(15,8,'2025-04-13 02:02:17',200000.00,'Cash','Basic Membership for 1 months',1),(16,6,'2025-04-15 00:59:27',200000.00,'Cash','Basic Membership for 1 months',1),(18,22,'2025-04-17 22:56:25',200000.00,'Cash','Basic Membership for 1 months',1),(19,6,'2025-04-17 23:18:49',200000.00,'Cash','Basic Membership for 1 months',1),(20,6,'2025-04-18 15:20:24',300000.00,'Cash','Premium Membership for 1 months',NULL),(21,6,'2025-04-18 15:24:51',300000.00,'Cash','Premium Membership for 1 months',1),(22,1,'2025-04-19 22:17:50',4000000.00,'Cash','Facility Purchase',NULL),(23,1,'2025-04-19 22:17:50',4000000.00,'Cash','Facility Purchase',NULL),(24,1,'2025-04-19 22:19:19',1000000.00,'Cash','Refund for Customer: Belle',10),(25,1,'2025-04-19 22:19:48',8000000.00,'Cash','2025/4 Salary Payment for Receptionist: Jake',3),(26,1,'2025-04-19 22:20:20',2000000.00,'Cash','Facility Purchase',NULL),(27,1,'2025-04-19 22:25:36',6000000.00,'Cash','2025/4 Salary Payment for Trainer: Hugo',18),(28,22,'2025-04-19 22:26:00',2520000.00,'Mobile Banking','Premium Membership for 12 months',1),(29,10,'2025-04-19 22:26:18',1440000.00,'Cash','Premium Membership for 6 months',1),(30,12,'2025-04-19 22:26:33',1680000.00,'Cash','Basic Membership for 12 months',1),(31,6,'2025-05-07 14:44:20',200000.00,'Cash','Basic Membership for 1 months',1),(32,6,'2025-05-08 14:48:51',300000.00,'Cash','Premium Membership for 1 months',1),(33,1,'2025-05-12 13:17:57',6000000.00,'Cash','Facility Purchase',NULL),(34,1,'2025-05-12 13:18:20',6000000.00,'Cash','2025/5 Salary Payment for Receptionist: Jake',3),(35,6,'2025-05-13 21:12:45',200000.00,'Cash','Basic Membership for 1 months',1),(36,6,'2025-05-13 23:58:36',200000.00,'Cash','Basic Membership for 1 months',1),(37,1,'2025-05-14 02:51:56',300000.00,'Cash','Refund for Customer: Ben',9);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'gymdb'
--
/*!50106 SET @save_time_zone= @@TIME_ZONE */ ;
/*!50106 DROP EVENT IF EXISTS `AutoExpireMemberships` */;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8mb4 */ ;;
/*!50003 SET character_set_results = utf8mb4 */ ;;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'SYSTEM' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`Admin`@`%`*/ /*!50106 EVENT `AutoExpireMemberships` ON SCHEDULE EVERY 1 DAY STARTS '2025-01-06 00:00:00' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
    UPDATE membership
    SET Status = 'Expired'
    WHERE EndDate < CURDATE() AND Status != 'Expired';
END */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
DELIMITER ;
/*!50106 SET TIME_ZONE= @save_time_zone */ ;

--
-- Dumping routines for database 'gymdb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-18 15:13:55
