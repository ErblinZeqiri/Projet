-- OM 2020.02.12
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: NOM_PRENOM_SUJET_BD_104_2020

-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS erblin_zeqiri_conf-serveur_1c_2020;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS erblin_zeqiri_conf-serveur_1c_2020;

-- Utilisation de cette base de donnée

USE erblin_zeqiri_conf-serveur_1c_2020;
-- --------------------------------------------------------
-- phpMyAdmin SQL Dump
-- version 4.5.4.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Dim 29 Mars 2020 à 13:53
-- Version du serveur :  5.7.11
-- Version de PHP :  5.6.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `erblin_zeqiri_conf-serveur_1c_2020`
--

-- --------------------------------------------------------

--
-- Structure de la table `t_location`
--

CREATE TABLE `t_location` (
  `ID_Location` int(11) NOT NULL,
  `Location` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_location`
--

INSERT INTO `t_location` (`ID_Location`, `Location`) VALUES
(1, 'Bureau1'),
(2, 'Bureau2');

-- --------------------------------------------------------

--
-- Structure de la table `t_mail`
--

CREATE TABLE `t_mail` (
  `ID_Mail` int(11) NOT NULL,
  `Adresse_Mail` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_mail`
--

INSERT INTO `t_mail` (`ID_Mail`, `Adresse_Mail`) VALUES
(1, 'fedsad@dsds.cj'),
(2, 'sadada@dsfsdf.dsfds');

-- --------------------------------------------------------

--
-- Structure de la table `t_personne`
--

CREATE TABLE `t_personne` (
  `ID_Personne` int(11) NOT NULL,
  `Nom_Pers` varchar(40) NOT NULL,
  `Prenom_Pers` varchar(40) NOT NULL,
  `Date_Naissance_Pers` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_personne`
--

INSERT INTO `t_personne` (`ID_Personne`, `Nom_Pers`, `Prenom_Pers`, `Date_Naissance_Pers`) VALUES
(1, 'Zeqiri', 'Erblin', '1998-10-17'),
(2, 'erer', 'reererwre', '2018-11-22');

-- --------------------------------------------------------

--
-- Structure de la table `t_pers_a_mail`
--

CREATE TABLE `t_pers_a_mail` (
  `ID_Pers_A_Mail` int(11) NOT NULL,
  `FK_Personne` int(11) NOT NULL,
  `FK_Mail` int(11) NOT NULL,
  `Date_Mail` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_pers_a_mail`
--

INSERT INTO `t_pers_a_mail` (`ID_Pers_A_Mail`, `FK_Personne`, `FK_Mail`, `Date_Mail`) VALUES
(1, 1, 1, '2020-03-10 17:05:59'),
(2, 2, 2, '2020-03-10 17:05:59');

-- --------------------------------------------------------

--
-- Structure de la table `t_pers_a_serveur`
--

CREATE TABLE `t_pers_a_serveur` (
  `ID_Pers_A_Serveur` int(11) NOT NULL,
  `FK_Personne` int(11) NOT NULL,
  `FK_Serveur` int(11) NOT NULL,
  `Date_Pers_Ask_Serveur` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_pers_a_serveur`
--

INSERT INTO `t_pers_a_serveur` (`ID_Pers_A_Serveur`, `FK_Personne`, `FK_Serveur`, `Date_Pers_Ask_Serveur`) VALUES
(1, 2, 2, '2020-03-10 17:06:27'),
(2, 1, 1, '2020-03-10 17:06:27');

-- --------------------------------------------------------

--
-- Structure de la table `t_serveur`
--

CREATE TABLE `t_serveur` (
  `ID_Serveur` int(11) NOT NULL,
  `Nombre_Port` int(24) NOT NULL,
  `Nombre_U` int(42) NOT NULL,
  `Date_Conf_Serv` date NOT NULL,
  `Description` text NOT NULL,
  `Puissance` int(11) NOT NULL,
  `Date_Serveur` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_serveur`
--

INSERT INTO `t_serveur` (`ID_Serveur`, `Nombre_Port`, `Nombre_U`, `Date_Conf_Serv`, `Description`, `Puissance`, `Date_Serveur`) VALUES
(1, 2, 4, '2020-03-18', 'voila voila', 51, '2020-03-10 15:13:24'),
(2, 31121231, 2111, '2020-03-25', 'qweweqewq', 21321321, '2020-03-10 17:05:29'),
(3, 0, 0, '0000-00-00', 'voilà c\'est tellement rose', 0, '2020-03-24 19:42:46');

-- --------------------------------------------------------

--
-- Structure de la table `t_serv_a_location`
--

CREATE TABLE `t_serv_a_location` (
  `ID_Serv_A_Location` int(11) NOT NULL,
  `FK_Serveur` int(11) NOT NULL,
  `FK_Location` int(11) NOT NULL,
  `Date_Serv_A_Location` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_serv_a_location`
--

INSERT INTO `t_serv_a_location` (`ID_Serv_A_Location`, `FK_Serveur`, `FK_Location`, `Date_Serv_A_Location`) VALUES
(1, 2, 1, '2020-03-10 17:06:40'),
(2, 1, 2, '2020-03-10 17:06:40');

-- --------------------------------------------------------

--
-- Structure de la table `t_serv_a_status`
--

CREATE TABLE `t_serv_a_status` (
  `ID_Serv_A_Status` int(11) NOT NULL,
  `FK_Serveur` int(11) NOT NULL,
  `FK_Status` int(11) NOT NULL,
  `Date_Serv_A_Status` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_serv_a_status`
--

INSERT INTO `t_serv_a_status` (`ID_Serv_A_Status`, `FK_Serveur`, `FK_Status`, `Date_Serv_A_Status`) VALUES
(1, 2, 1, '2020-03-10 17:07:07'),
(2, 2, 2, '2020-03-10 17:07:07');

-- --------------------------------------------------------

--
-- Structure de la table `t_serv_a_type_equipement`
--

CREATE TABLE `t_serv_a_type_equipement` (
  `ID_Serv_A_Type_Equipement` int(11) NOT NULL,
  `Fk_Serveur` int(11) NOT NULL,
  `FK_Type_Equipement` int(11) NOT NULL,
  `Date_Serv_A_Type_Equipement` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_serv_a_type_equipement`
--

INSERT INTO `t_serv_a_type_equipement` (`ID_Serv_A_Type_Equipement`, `Fk_Serveur`, `FK_Type_Equipement`, `Date_Serv_A_Type_Equipement`) VALUES
(1, 1, 2, '2020-03-10 17:07:40'),
(2, 2, 2, '2020-03-10 17:07:40');

-- --------------------------------------------------------

--
-- Structure de la table `t_status`
--

CREATE TABLE `t_status` (
  `ID_Status` int(11) NOT NULL,
  `Status` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_status`
--

INSERT INTO `t_status` (`ID_Status`, `Status`) VALUES
(1, 'Traité'),
(2, 'A traité'),
(3, 'voilà c\'es');

-- --------------------------------------------------------

--
-- Structure de la table `t_type_equipement`
--

CREATE TABLE `t_type_equipement` (
  `ID_Type_Equipement` int(11) NOT NULL,
  `Type_Equipement` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_type_equipement`
--

INSERT INTO `t_type_equipement` (`ID_Type_Equipement`, `Type_Equipement`) VALUES
(1, 'cxvxvxcv'),
(2, 'xcvcxvx'),
(3, 'voilà c\'est tellement rose');

--
-- Index pour les tables exportées
--

--
-- Index pour la table `t_location`
--
ALTER TABLE `t_location`
  ADD PRIMARY KEY (`ID_Location`);

--
-- Index pour la table `t_mail`
--
ALTER TABLE `t_mail`
  ADD PRIMARY KEY (`ID_Mail`);

--
-- Index pour la table `t_personne`
--
ALTER TABLE `t_personne`
  ADD PRIMARY KEY (`ID_Personne`);

--
-- Index pour la table `t_pers_a_mail`
--
ALTER TABLE `t_pers_a_mail`
  ADD PRIMARY KEY (`ID_Pers_A_Mail`),
  ADD KEY `FK_Mail` (`FK_Mail`),
  ADD KEY `FK_Personne` (`FK_Personne`);

--
-- Index pour la table `t_pers_a_serveur`
--
ALTER TABLE `t_pers_a_serveur`
  ADD PRIMARY KEY (`ID_Pers_A_Serveur`),
  ADD KEY `FK_Personne` (`FK_Personne`),
  ADD KEY `FK_Serveur` (`FK_Serveur`);

--
-- Index pour la table `t_serveur`
--
ALTER TABLE `t_serveur`
  ADD PRIMARY KEY (`ID_Serveur`);

--
-- Index pour la table `t_serv_a_location`
--
ALTER TABLE `t_serv_a_location`
  ADD PRIMARY KEY (`ID_Serv_A_Location`),
  ADD KEY `FK_Serveur` (`FK_Serveur`),
  ADD KEY `FK_Location` (`FK_Location`);

--
-- Index pour la table `t_serv_a_status`
--
ALTER TABLE `t_serv_a_status`
  ADD PRIMARY KEY (`ID_Serv_A_Status`),
  ADD KEY `FK_Serveur` (`FK_Serveur`),
  ADD KEY `FK_Status` (`FK_Status`);

--
-- Index pour la table `t_serv_a_type_equipement`
--
ALTER TABLE `t_serv_a_type_equipement`
  ADD PRIMARY KEY (`ID_Serv_A_Type_Equipement`),
  ADD KEY `Fk_Serveur` (`Fk_Serveur`),
  ADD KEY `FK_Type_Equipement` (`FK_Type_Equipement`);

--
-- Index pour la table `t_status`
--
ALTER TABLE `t_status`
  ADD PRIMARY KEY (`ID_Status`);

--
-- Index pour la table `t_type_equipement`
--
ALTER TABLE `t_type_equipement`
  ADD PRIMARY KEY (`ID_Type_Equipement`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `t_location`
--
ALTER TABLE `t_location`
  MODIFY `ID_Location` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_mail`
--
ALTER TABLE `t_mail`
  MODIFY `ID_Mail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_personne`
--
ALTER TABLE `t_personne`
  MODIFY `ID_Personne` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_pers_a_mail`
--
ALTER TABLE `t_pers_a_mail`
  MODIFY `ID_Pers_A_Mail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_pers_a_serveur`
--
ALTER TABLE `t_pers_a_serveur`
  MODIFY `ID_Pers_A_Serveur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_serveur`
--
ALTER TABLE `t_serveur`
  MODIFY `ID_Serveur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `t_serv_a_location`
--
ALTER TABLE `t_serv_a_location`
  MODIFY `ID_Serv_A_Location` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_serv_a_status`
--
ALTER TABLE `t_serv_a_status`
  MODIFY `ID_Serv_A_Status` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_serv_a_type_equipement`
--
ALTER TABLE `t_serv_a_type_equipement`
  MODIFY `ID_Serv_A_Type_Equipement` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_status`
--
ALTER TABLE `t_status`
  MODIFY `ID_Status` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `t_type_equipement`
--
ALTER TABLE `t_type_equipement`
  MODIFY `ID_Type_Equipement` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `t_pers_a_mail`
--
ALTER TABLE `t_pers_a_mail`
  ADD CONSTRAINT `t_pers_a_mail_ibfk_1` FOREIGN KEY (`FK_Personne`) REFERENCES `t_personne` (`ID_Personne`),
  ADD CONSTRAINT `t_pers_a_mail_ibfk_2` FOREIGN KEY (`FK_Mail`) REFERENCES `t_mail` (`ID_Mail`);

--
-- Contraintes pour la table `t_pers_a_serveur`
--
ALTER TABLE `t_pers_a_serveur`
  ADD CONSTRAINT `t_pers_a_serveur_ibfk_1` FOREIGN KEY (`FK_Personne`) REFERENCES `t_personne` (`ID_Personne`),
  ADD CONSTRAINT `t_pers_a_serveur_ibfk_2` FOREIGN KEY (`FK_Serveur`) REFERENCES `t_serveur` (`ID_Serveur`);

--
-- Contraintes pour la table `t_serv_a_location`
--
ALTER TABLE `t_serv_a_location`
  ADD CONSTRAINT `t_serv_a_location_ibfk_1` FOREIGN KEY (`FK_Serveur`) REFERENCES `t_serveur` (`ID_Serveur`),
  ADD CONSTRAINT `t_serv_a_location_ibfk_2` FOREIGN KEY (`FK_Location`) REFERENCES `t_location` (`ID_Location`);

--
-- Contraintes pour la table `t_serv_a_status`
--
ALTER TABLE `t_serv_a_status`
  ADD CONSTRAINT `t_serv_a_status_ibfk_1` FOREIGN KEY (`FK_Serveur`) REFERENCES `t_serveur` (`ID_Serveur`),
  ADD CONSTRAINT `t_serv_a_status_ibfk_2` FOREIGN KEY (`FK_Status`) REFERENCES `t_status` (`ID_Status`);

--
-- Contraintes pour la table `t_serv_a_type_equipement`
--
ALTER TABLE `t_serv_a_type_equipement`
  ADD CONSTRAINT `t_serv_a_type_equipement_ibfk_1` FOREIGN KEY (`Fk_Serveur`) REFERENCES `t_serveur` (`ID_Serveur`),
  ADD CONSTRAINT `t_serv_a_type_equipement_ibfk_2` FOREIGN KEY (`FK_Type_Equipement`) REFERENCES `t_type_equipement` (`ID_Type_Equipement`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
