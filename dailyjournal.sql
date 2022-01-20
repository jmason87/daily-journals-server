CREATE TABLE `Entries` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`	TEXT NOT NULL,
	`entry`	TEXT NOT NULL,
    `date` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL,
	FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`)

);
CREATE TABLE `Moods` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label`	TEXT NOT NULL
);

INSERT INTO `Entries` VALUES (null, "Python", "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake", "Wed Sep 15 2021 10:11:33", 1);
INSERT INTO `Entries` VALUES (null, "JavaScript", "I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.", "Wed Sep 15 2021 10:10:47 ", 2);
INSERT INTO `Entries` VALUES (null, "SQL", "Today I learned SQL", "Wed Sep 15 2021 10:10:47 ", 3);


INSERT INTO `Moods` VALUES (null, "Happy");
INSERT INTO `Moods` VALUES (null, "Sad");
INSERT INTO `Moods` VALUES (null, "Angry");
INSERT INTO `Moods` VALUES (null, "Ok");

SELECT
    e.id,
    e.concept,
    e.entry,
    e.date,
    e.mood_id
FROM Entries e

