-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: std-mysql    Database: std_1846_exam
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('4d4f8acea97b');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_genre`
--

DROP TABLE IF EXISTS `book_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_genre` (
  `book_id` int(11) DEFAULT NULL,
  `genre_id` int(11) DEFAULT NULL,
  KEY `fk_book_genre_book_id_books` (`book_id`),
  KEY `fk_book_genre_genre_id_genres` (`genre_id`),
  CONSTRAINT `fk_book_genre_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_book_genre_genre_id_genres` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_genre`
--

LOCK TABLES `book_genre` WRITE;
/*!40000 ALTER TABLE `book_genre` DISABLE KEYS */;
INSERT INTO `book_genre` VALUES (3,7),(3,4),(3,8),(4,6),(4,2),(4,12),(6,7),(6,2),(2,5),(2,7),(2,6),(7,7),(7,5),(7,8),(8,10),(8,5),(13,4),(13,13),(5,7),(5,4);
/*!40000 ALTER TABLE `book_genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `short_desc` text NOT NULL,
  `year` year(4) NOT NULL,
  `publisher` varchar(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  `pages` int(11) NOT NULL,
  `rating_sum` int(11) NOT NULL,
  `rating_num` int(11) NOT NULL,
  `background_image_id` varchar(100) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_books_background_image_id_images` (`background_image_id`),
  CONSTRAINT `fk_books_background_image_id_images` FOREIGN KEY (`background_image_id`) REFERENCES `images` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (2,'Режьте, братцы, режьте. Сборник рассказов','В нашей стране великий американский писатель Марк Твен (1835-1910) известен прежде всего как автор бессмертных \"Приключений Тома Сойера\" и \"Приключений Гекльберри Финна\", но его блестящий талант юмориста и сатирика в первую очередь воплотился в многочисленных рассказах, которые в последние годы почти не издавались в России. Предлагаемый сборник, в котором представлены образцы лучших рассказов, написанных Твеном за сорок с лишним лет, призван заполнить этот пробел.\r\nМарк Твен был первым по-настоящему американским писателем, и все мы с тех пор - его наследники.\r\nУильям Фолкнер',2022,'Текст','Марк Твен',448,4,1,'39448296-1721-4f85-a74e-21d1b7992ce5','2023-06-12 16:25:44'),(3,'Преступление и наказание','Роман Федора Михайловича Достоевского «Преступление и наказание» был вдохновлен жизнью самого писателя: идея произведения зародилась, когда он отбывал наказание на каторге в Омске. Текст, начинавшийся как исповедь, превратился, по словам автора, в «психологический отчет одного преступления».\r\nИстория студента Раскольникова, посвященная преступлению и раскаянию, трудному моральному выбору и поиску света даже в самые темные времена, стала одной из важнейших книг в мировой литературе и остается актуальной и по сей день.',2023,'Манн, Иванов и Фербер','Федор Достоевский',640,0,0,'7bfc9e97-2b41-4974-9a1d-245f729620e7','2023-06-12 17:51:28'),(4,'Собачье сердце','\"Собачье сердце\", гениальная повесть Михаила Булгакова, написанная еще в 1925 году, едва не стоившая автору свободы и до 1987 года издававшаяся лишь за рубежом и ходившая по рукам в самиздате, в представлениях не нуждается.\r\nЧуть ли не до последней буквы разобранная на цитаты история милого пса Шарика, превращенного, благодаря эксперименту профессора Преображенского, в типичного \"красного хама\" Полиграфа Шарикова, среди русскоязычных читателей вот уже нескольких поколений носит поистине культовый статус.\r\nТакже в состав сборника входит \"Жизнь господина де Мольера\", - печальная и блестяще-остроумная романизированная биография великого французского драматурга.',2019,'ACT','Михаил Булгаков',352,0,0,'6a17f7e8-33d6-4f2d-97c9-5ac6cc5dd050','2023-06-12 17:56:50'),(5,'Повелитель мух','\"Повелитель мух\".\r\nСтранная, страшная и бесконечно притягательная книга.\r\nИстория благовоспитанных мальчиков, внезапно оказавшихся на необитаемом острове.\r\nФилософская притча о том, что может произойти с людьми, забывшими о любви и милосердии.\r\nГротескная антиутопия, роман-предупреждение и, конечно, напоминание о хрупкости мира, в котором живем мы все.Роман Уильяма Голдинга \"Повелитель мух\" (1954) – антиутопия с символическим подтекстом, исследующая особенности взаимоотношений детей на необитаемом острове, куда они попали в военное время. Способны ли они к разумной самоорганизации или подчинятся природным импульсам? Между собой спорят дикарь и цивилизованный человек.',2021,'АСТ','Уильям Голдинг',320,0,0,'bdf24413-0f99-4f80-af3a-a6d521261d0d','2023-06-12 18:00:26'),(6,'Тарас Бульба','\"Тарас Бульба\" - историческая повесть, в которой описана история казацкого восстания 1637-1638 годов, подавленного польскими войсками. Центральными темами повести являются патриотизм и героизм запорожских казаков. Торжество духовности показано, прежде всего, в главном герое - Тарасе Бульбе, судьба которого полна драматизма. Белинский так отзывался об этом произведении: \"Тарас Бульба\" есть отрывок, эпизод из великой эпопеи жизни целого народа. Если в наше время возможна гомерическая эпопея, то вот вам её высочайший образец, идеал и прототип!..\"',2018,'АСТ','Николай Гоголь',320,0,0,'e8c4f9d3-2a17-421a-9d7d-e4bc9f23fe67','2023-06-13 00:34:10'),(7,'Бойцовский клуб','\"Бойцовский клуб\" - самый знаменитый роман Чака Паланика. Все помнят фильм режиссера Дэвида Финчера с Брэдом Питтом в главной роли? Он именно по этой книге. Это роман-вызов, роман, созданный всем назло и вопреки всему, в нем описывается поколение озлобившихся людей, потерявших представление о том, что можно и чего нельзя, где добро и зло, кто они сами и кто их окружает. Сам Паланик называет свой \"Бойцовский клуб\" новым \"Великим Гэтсби\". Какие же они - эти Гэтсби конца XX века?',2022,'АСТ','Чак Паланик',256,0,0,'70c6ed92-2fc6-4ed2-adbb-1d3a9ca4bc20','2023-06-13 16:35:07'),(8,'Басни','Молодому Крылову покровительствовал сам Гаврила Романович Державин. Начинавший тогда как драматург Крылов разочаровался увидеть свои пьесы на сцене и стал издавать сатирический журнал «Почта духов». Высмеивал абсурдность устоявшихся правил жизни и негодовал на безнравственность сильных мира сего.\nНо за радикализм журнал был закрыт.\nan &lt;script&gt;evil()&lt;/script&gt; example\nПервые Басни Крылова появились намного позже, но уже первая книга басен сделала его имя очень известным.\nИван Крылов — герой многочисленных анекдотов и легенд, прозванный «дедушкой Крыловым», слился в сознании современников со своими баснями. Василий Жуковский считал его басни «поэтическими уроками мудрости». И правда, строки Крылова буквально на глазах стали пословицами, крылатыми словами. Александр Пушкин называл Ивана Крылова «истинно народным поэтом».',2022,'Эксмо','Иван Крылов',352,0,0,'6a8e794b-eff0-4e74-925f-4cc4d456b5ab','2023-06-13 16:43:19'),(13,'Змеиные тропы','**Рожденная в яркой славе своего создателя империя** Мирэй трещит по швам. Жадные до власти сановники растаскивают все, до чего могут дотянуться. Знать праздно предается развлечениям, в армии моральное разложение, а император слаб. Что может быть хуже? Только война. Наследный принц Маэль ар Вариар пытается вновь сшить имперское полотно. Но враги не дремлют. А они есть как снаружи, так и внутри. Прогулка по змеиным тропам никогда не бывает легкой.',2023,'Т8','Айрин Бран',680,5,1,'ced23f64-c268-4af1-9dbd-8addda8515bf','2023-06-14 13:53:55');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_genres_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (10,'Басня'),(7,'Драма'),(14,'Классицизм'),(6,'Комедия'),(1,'Новелла'),(2,'Повесть'),(3,'Пьеса'),(5,'Рассказ'),(4,'Роман'),(11,'Сказка'),(8,'Трагедия'),(9,'Ужасы'),(12,'Фантастика'),(13,'Фэнтези');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `histories`
--

DROP TABLE IF EXISTS `histories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `histories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_histories_book_id_books` (`book_id`),
  KEY `fk_histories_user_id_users` (`user_id`),
  CONSTRAINT `fk_histories_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_histories_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `histories`
--

LOCK TABLES `histories` WRITE;
/*!40000 ALTER TABLE `histories` DISABLE KEYS */;
INSERT INTO `histories` VALUES (1,7,1,'2023-06-14 18:07:22'),(2,7,NULL,'2023-06-14 18:13:16'),(3,4,NULL,'2023-06-15 14:03:44'),(4,4,NULL,'2023-06-15 14:05:22'),(5,3,NULL,'2023-06-15 14:05:33'),(6,13,NULL,'2023-06-15 14:05:37'),(7,5,4,'2023-06-15 14:06:48'),(8,6,4,'2023-06-15 14:06:51'),(9,8,4,'2023-06-15 14:06:58'),(10,2,4,'2023-06-15 14:07:03'),(11,6,5,'2023-06-15 14:07:26'),(12,13,5,'2023-06-15 14:07:29'),(13,4,5,'2023-06-15 14:07:32'),(14,3,5,'2023-06-15 14:07:36'),(15,13,5,'2023-06-15 14:07:39'),(16,5,2,'2023-06-15 14:08:02'),(17,7,NULL,'2023-06-15 14:08:08'),(18,5,1,'2023-06-15 18:07:56'),(19,5,1,'2023-06-15 18:08:00'),(20,6,1,'2023-06-16 14:33:43'),(21,4,1,'2023-06-16 14:33:48'),(22,6,1,'2023-06-16 14:33:51'),(23,6,1,'2023-06-16 14:33:53'),(24,8,1,'2023-06-16 14:45:25'),(25,2,1,'2023-06-16 15:01:16'),(26,13,1,'2023-06-16 15:07:45'),(27,5,1,'2023-06-16 15:11:22'),(28,5,1,'2023-06-16 15:11:35'),(29,3,1,'2023-06-16 15:11:43'),(30,5,5,'2023-06-16 15:35:37'),(31,13,5,'2023-06-16 15:35:44'),(32,8,5,'2023-06-16 15:35:54');
/*!40000 ALTER TABLE `histories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `images` (
  `id` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `md5_hash` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_images_md5_hash` (`md5_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES ('39448296-1721-4f85-a74e-21d1b7992ce5','2023-06-12_162546886.png','image/png','a6205a85234ea6adb37c4acb51505a19','2023-06-12 16:25:44'),('6a17f7e8-33d6-4f2d-97c9-5ac6cc5dd050','2023-06-12_175646302.png','image/png','48897af3e1a07d48b0564b3e6ee2f2b8','2023-06-12 17:56:50'),('6a8e794b-eff0-4e74-925f-4cc4d456b5ab','2023-06-13_164320643.png','image/png','c5b2d6c90ab3a94043410ec41436873d','2023-06-13 16:43:19'),('70c6ed92-2fc6-4ed2-adbb-1d3a9ca4bc20','2023-06-13_163218768.png','image/png','a14b0846bc6bf1c092f42b91916ed4d1','2023-06-13 16:35:07'),('7bfc9e97-2b41-4974-9a1d-245f729620e7','2023-06-12_175127864.png','image/png','0edd703dbe91b884cba127e67bb6c73f','2023-06-12 17:51:28'),('bdf24413-0f99-4f80-af3a-a6d521261d0d','2023-06-12_180029723.png','image/png','26f29f7b72d461fbaebf445de111e461','2023-06-12 18:00:26'),('ced23f64-c268-4af1-9dbd-8addda8515bf','2023-06-14_135236727.png','image/png','ad4a29b0c01f52c669285bbb6b2b1200','2023-06-14 13:53:55'),('e8c4f9d3-2a17-421a-9d7d-e4bc9f23fe67','2023-06-13_003255889.png','image/png','fd276292eb0ef805d0e1474636e82075','2023-06-13 00:34:10');
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rating` int(11) NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_reviews_book_id_books` (`book_id`),
  KEY `fk_reviews_user_id_users` (`user_id`),
  CONSTRAINT `fk_reviews_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_reviews_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,4,'Хорошие приятные рассказы','2023-06-12 21:44:02',2,5),(8,5,'#### Вау\r\nВсе очень круто, мне ***Понравилось***!!!','2023-06-14 15:40:50',13,1);
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `desc` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_roles_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Администратор','Суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),(2,'Модератор','Повышенные права, может редактировать данные книг'),(3,'Пользователь','Обычный пользователь, может оставлять рецензии');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_name` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `login` varchar(100) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_login` (`login`),
  KEY `fk_users_role_id_roles` (`role_id`),
  CONSTRAINT `fk_users_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Иванов','Иван','Иванович','user','pbkdf2:sha256:260000$cg3NlI5zNMQn6HUm$a9dbe03f2eb6f56abe628adc789fdf30b19bc1dfcbbfffdf5ec3bb2cacbb80bf',1,'2023-06-12 21:28:02'),(2,'Петров','Петр','Петрович','petrov','pbkdf2:sha256:260000$tgm77b6Gt7vVV4ut$28781c11038d9ebf63651949d16563313371152767340b0866599ab9ecd929ab',2,'2023-06-12 21:28:02'),(3,'Фёдоров','Фёдор','Фёдорович','fedorov','pbkdf2:sha256:260000$zGej5JncghAVmQly$5e393fd02e73b61258f5efa16eaa16459506a53699a4789d2bc0c5e682760d7e',3,'2023-06-12 21:28:02'),(4,'Степанов','Степан','Степанович','stepanov','pbkdf2:sha256:260000$a66jlqEuHYMNUqI6$ea7cbb5226b8425d8388f7d49ee5dde569abe0d5fad8f4c7c29118909f4d224c',3,'2023-06-12 21:28:02'),(5,'Максимов','Максим','Максимович','maximov','pbkdf2:sha256:260000$qEiqXAIWhWvzFIMy$b6430dc0e291cd176b704c238d235252f6301868037615f6fc0bb9e22ca11059',3,'2023-06-12 21:28:02'),(7,'Павлов','Павел','Павлович','pavlov','pbkdf2:sha256:260000$3QRvkLhSp8mYqInA$8efcfb9a4c002f46fa2526e46ed435eeebf394419fcad612a5aba90ad62e99ea',1,'2023-06-15 17:33:55'),(8,'Алексеев','Алексей','Алексеевич','alexeev','pbkdf2:sha256:260000$E8qIy6xUizG4OvBU$49f5a79a3764a806842a199697034766b6bf174ca6ec19c77e8c001b43b1b20c',2,'2023-06-15 17:33:55'),(9,'Тарасов','Тарас','Тарасович','tarasov','pbkdf2:sha256:260000$qEqFW2M4wHRggFg7$67c157105e8bc67fc2a6504f85a35536832ebb62f2926a61905246a9c4ea58a6',3,'2023-06-15 17:33:55'),(10,'Данилов','Даниил','Данилович','danilov','pbkdf2:sha256:260000$zpGoaJhtgYYov2jV$0b3c7f368762763ae1532e294d021c5391782ccf45ac2830bc8fcc3e9bc9eba9',3,'2023-06-15 17:33:56');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-16 16:34:05
