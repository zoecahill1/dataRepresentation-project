create database project;

use project;

create table movies(
id int NOT NULL AUTO_INCREMENT,
name varchar(250),
genre varchar(250),
description varchar(1000),
totalVotes int,
PRIMARY KEY(id)
);

INSERT INTO `movies` (`id`, `name`, `genre`, `description`, `totalVotes`) VALUES ('1', 'Avengers: Endgame', 'Action & Adventure', 'The grave course of events set in motion by Thanos that wiped out half the universe and fractured the Avengers ranks compels the remaining Avengers to take one final stand in Marvel Studios\' grand conclusion to twenty-two films, Avengers: Endgame.', '20');

INSERT INTO `movies` (`id`, `name`, `genre`, `description`, `totalVotes`) VALUES (NULL, 'The Wizard of Oz', 'Classics', 'L. Frank Baums classic tale comes to magisterial Technicolor life! The Wizard of Oz stars legendary Judy Garland as Dorothy, an innocent farm girl whisked out of her mundane earthbound existence into a land of pure imagination. Dorothys journey in Oz will take her through emerald forests, yellow brick roads, and creepy castles, all with the help of some unusual but earnest song-happy friends', '9');

INSERT INTO `movies` (`id`, `name`, `genre`, `description`, `totalVotes`) VALUES (NULL, 'The Lord of the Rings: The Return of the King', 'Fantasy', 'Gandalf and Aragorn lead the World of Men against Sauron\'s army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.', '13');

INSERT INTO `movies` (`id`, `name`, `genre`, `description`, `totalVotes`) VALUES (NULL, 'Toy Story 4', 'Comedy', 'When a new toy called \"Forky\" joins Woody and the gang, a road trip alongside old and new friends reveals how big the world can be for a toy.', '10');

create table topmovies(
id int NOT NULL AUTO_INCREMENT,
Title varchar(250),
Year int,
PRIMARY KEY(id)
);