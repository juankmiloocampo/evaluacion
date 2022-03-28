CREATE SCHEMA evaluacion2236347;
USE evaluacion2236347;

CREATE TABLE `evaluacion2236347`.`usuarios` (
  `email` VARCHAR(100) NOT NULL,
  `nombres` VARCHAR(200) NOT NULL,
  `apellidos` VARCHAR(200) NOT NULL,
  `password` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`email`));
  
CREATE TABLE `evaluacion2236347`.`productos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `precio` INT NOT NULL,
  PRIMARY KEY (`id`));