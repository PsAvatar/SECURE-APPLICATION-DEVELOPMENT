-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Εξυπηρετητής: 127.0.0.1
-- Χρόνος δημιουργίας: 29 Μαρ 2024 στις 14:54:21
-- Έκδοση διακομιστή: 10.4.28-MariaDB
-- Έκδοση PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Βάση δεδομένων: `signup`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `login`
--

CREATE TABLE `login` (
                         `id` int(11) NOT NULL,
                         `name` varchar(30) NOT NULL,
                         `email` varchar(50) NOT NULL,
                         `password` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `login`
--

INSERT INTO `login` (`id`, `name`, `email`, `password`) VALUES
                                                            (50, '1', '1@gmail.com', '$2b$12$qgEf34N7hnc8az9HNhy9JuV0vAGmIGqSX1t0pyT9dFEd.MYDiHLlC'),
                                                            (51, '2', '2@gmail.com', '$2b$12$dtJ3dyHmtUTXlKEo2F8tPOSVobmsiNbu2mVX64GTZqnETdcTlpubK'),
                                                            (52, '3', '3@gmail.com', '$2b$12$frBGDld0yNQAK39Rf9Orq.YLAOTKBzJeGZ7LrZuFx5ED/gmb3ixpO'),
                                                            (54, '5', '5@gmai.com', '$2b$12$hW/gzbPzpvbSe9Lj4mGLCOxy3ntwjjal3bbhRwUGls2ICPplWCBra');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `ratings`
--

CREATE TABLE `ratings` (
                           `id` int(11) NOT NULL,
                           `user_id` int(11) DEFAULT NULL,
                           `restaurant_id` int(11) DEFAULT NULL,
                           `rating` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `ratings`
--

INSERT INTO `ratings` (`id`, `user_id`, `restaurant_id`, `rating`) VALUES
                                                                       (12, 51, 5, 5),
                                                                       (13, 50, 5, 2),
                                                                       (14, 50, 6, 5),
                                                                       (15, 51, 6, 1),
                                                                       (16, 50, 4, 5),
                                                                       (22, 52, 5, 1),
                                                                       (23, 52, 4, 5),
                                                                       (24, 54, 4, 1),
                                                                       (25, 54, 5, 5);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `restaurants`
--

CREATE TABLE `restaurants` (
                               `id` int(11) NOT NULL,
                               `name` varchar(255) NOT NULL,
                               `description` text DEFAULT NULL,
                               `location` varchar(255) DEFAULT NULL,
                               `address` varchar(255) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL,
                               `total_ratings` int(11) DEFAULT 0,
                               `total_rating_sum` int(11) DEFAULT 0,
                               `average_rating` float DEFAULT 0,
                               `latitude` varchar(255) NOT NULL,
                               `longitude` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `restaurants`
--

INSERT INTO `restaurants` (`id`, `name`, `description`, `location`, `address`, `total_ratings`, `total_rating_sum`, `average_rating`, `latitude`, `longitude`) VALUES
                                                                                                                                                                   (4, 'Mira Me Athens', 'A great place to eat!', 'Athens', '', 3, 11, 3.66667, '37.977370', '23.721870'),
                                                                                                                                                                   (5, 'Jonah\'s Restaurant', 'Delicious food and cozy atmosphere.', 'Athens', '', 4, 13, 3.25, '37.985480', '23.755850'),
(6, 'Aleria', 'Specializing in international cuisine.', 'Athens', '', 2, 6, 3, '37.983150', '23.717930'),
(7, 'Loupino', 'In a disarmingly intimate and warm place with unobtrusive aesthetic and luxury.', 'Thessaloniki', '', 0, 0, 0, '40.634260', '22.936840'),
(8, 'Akratos Oinos', 'Pivoting back to the traditional Greek cooking but with a constant eye on the future, the menu celebrates authentic Greek recipes interpreted into refined, fine-dining dishes.', 'Thessaloniki', '', 0, 0, 0, '40.634770', '22.937460');

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`id`);

--
-- Ευρετήρια για πίνακα `ratings`
--
ALTER TABLE `ratings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `restaurant_id` (`restaurant_id`);

--
-- Ευρετήρια για πίνακα `restaurants`
--
ALTER TABLE `restaurants`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT για άχρηστους πίνακες
--

--
-- AUTO_INCREMENT για πίνακα `login`
--
ALTER TABLE `login`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT για πίνακα `ratings`
--
ALTER TABLE `ratings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT για πίνακα `restaurants`
--
ALTER TABLE `restaurants`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Περιορισμοί για άχρηστους πίνακες
--

--
-- Περιορισμοί για πίνακα `ratings`
--
ALTER TABLE `ratings`
  ADD CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `login` (`id`),
  ADD CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
