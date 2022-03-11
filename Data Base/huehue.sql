-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`customer` (
  `customer_id` INT NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `email` VARCHAR(64) NOT NULL,
  `password` CHAR(60) NOT NULL,
  `password_encoder` ENUM('bcrypt', 'scrypt') NOT NULL,
  `created_at` TIMESTAMP NULL,
  `updated_at` TIMESTAMP NULL,
  `active` TINYINT NOT NULL,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  PRIMARY KEY (`customer_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`manager`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`manager` (
  `manager_id` INT NOT NULL,
  `email` VARCHAR(64) NOT NULL,
  `active` TINYINT NOT NULL,
  `password` CHAR(60) NOT NULL,
  `password_encoder` ENUM('bcrypt', 'scrypt') NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `created_at` TIMESTAMP NULL,
  `updated_at` TIMESTAMP NULL,
  PRIMARY KEY (`manager_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`roles` (
  `role_id` INT NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`role_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`manager_roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`manager_roles` (
  `manager_id` INT NOT NULL,
  `role_id` INT NOT NULL,
  INDEX `fk_manager_roles_roles1_idx` (`role_id` ASC) VISIBLE,
  CONSTRAINT `fk_manager_roles_manager1`
    FOREIGN KEY (`manager_id`)
    REFERENCES `mydb`.`manager` (`manager_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_manager_roles_roles1`
    FOREIGN KEY (`role_id`)
    REFERENCES `mydb`.`roles` (`role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`company` (
  `comany_id` INT NOT NULL,
  `manager_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`comany_id`),
  INDEX `fk_company_manager1_idx` (`manager_id` ASC) VISIBLE,
  CONSTRAINT `fk_company_manager1`
    FOREIGN KEY (`manager_id`)
    REFERENCES `mydb`.`manager` (`manager_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`service`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`service` (
  `sevice_id` INT NOT NULL,
  `manager_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `rating` DECIMAL(3,2) NULL,
  `price` DECIMAL(4,2) NULL,
  `created_at` TIMESTAMP NULL,
  `updated_at` TIMESTAMP NULL,
  `category` TINYINT NULL,
  `status` TINYINT NOT NULL,
  PRIMARY KEY (`sevice_id`),
  INDEX `fk_service_manager1_idx` (`manager_id` ASC) VISIBLE,
  INDEX `fk_service_customer1_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_service_manager1`
    FOREIGN KEY (`manager_id`)
    REFERENCES `mydb`.`manager` (`manager_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_service_customer1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `mydb`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`payment` (
  `payment_id` INT NOT NULL,
  `sevice_id` INT NOT NULL,
  `amount` DECIMAL(5,2) NOT NULL,
  `payment_date` DATETIME NULL,
  `created_at` TIMESTAMP NULL,
  `status` TINYINT NULL,
  `updated_at` TIMESTAMP NULL,
  PRIMARY KEY (`payment_id`),
  INDEX `fk_payment_service_idx` (`sevice_id` ASC) VISIBLE,
  CONSTRAINT `fk_payment_service`
    FOREIGN KEY (`sevice_id`)
    REFERENCES `mydb`.`service` (`sevice_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`city`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`city` (
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`address` (
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`training_plan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`training_plan` (
  `id_training` INT NOT NULL,
  `id_service` INT NULL,
  `expiration_date` DATE NULL,
  `updated_at` VARCHAR(45) NULL,
  `created_at` TIMESTAMP NULL,
  PRIMARY KEY (`id_training`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`session` (
  `session_id` INT NOT NULL,
  `training_plan_id` INT NULL,
  `duration` TIME NULL,
  `description` VARCHAR(45) NULL,
  PRIMARY KEY (`session_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`employee` (
  `company_id` INT NOT NULL,
  `status` INT NOT NULL,
  `created_at` TIMESTAMP NULL,
  `updated_at` VARCHAR(45) NULL,
  `employee_id` INT NULL)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`category` (
  `category_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `updated_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`service_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`service_category` (
  `category_id` INT NOT NULL,
  `sevice_id` INT NOT NULL,
  `updated_at` TIMESTAMP NULL,
  PRIMARY KEY (`sevice_id`, `category_id`),
  INDEX `fk_service_category_service1_idx` (`sevice_id` ASC) VISIBLE,
  CONSTRAINT `fk_service_category_category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `mydb`.`category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_service_category_service1`
    FOREIGN KEY (`sevice_id`)
    REFERENCES `mydb`.`service` (`sevice_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
